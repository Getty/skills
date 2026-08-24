---
name: docker-engine-api
description: "Use when talking to the Docker Engine HTTP API directly — writing or debugging a client, hitting /containers, /images, /build, /exec, /events over the socket, curl --unix-socket probes, garbled log output, a 400 on push, filters that match nothing, or making a client work against Podman."
---

# Docker Engine HTTP API

For code that speaks the API over a socket rather than shelling out to `docker`.
The CLI hides everything below; a client has to handle it. Endpoint lists live
in the daemon's own reference — what follows is what the reference states once
and clients get wrong repeatedly.

## Versioning

Every path is prefixed `/v1.NN` (`/v1.47/containers/json`). Unversioned paths
work and mean "whatever the daemon defaults to" — fine for `/version` and
`/_ping`, wrong for anything a client should pin.

`GET /version` answers `ApiVersion` (newest supported) and `MinAPIVersion`
(oldest). Negotiate by requesting `/version` unprefixed, then using
`ApiVersion` for everything else. Asking for a version above `ApiVersion` fails
with 400 `client version 1.99 is too new`; below `MinAPIVersion` fails the same
way. A feature added in a later version is simply absent — the daemon returns
404 or silently ignores the query parameter, so a client that assumes a
parameter took effect can be wrong without any error.

## Response shapes

- **204 No Content** is the success case for `start`, `stop`, `kill`, `pause`,
  `remove` and friends. There is no body to decode.
- **304 Not Modified** means the container was already in the requested state —
  starting a running container, stopping a stopped one. It is *not* an error,
  and a client that only special-cases `>= 400` will hand back an empty result
  here. Decide explicitly whether that is success.
- **Errors** carry `{"message": "..."}` as JSON with a 4xx/5xx status. The
  message is human text; do not parse it for control flow.
- **`/build`, `/images/create` (pull) and `/images/{name}/push` stream
  newline-delimited JSON** — one object per line: `{"stream":…}`,
  `{"status":…,"progress":…}`, `{"aux":{"ID":…}}`, `{"errorDetail":{…}}`.

**A failed build, pull or push is still HTTP 200.** The failure arrives as an
`errorDetail` object inside the stream, after the daemon has already committed
to a successful status line. Any client that treats HTTP status as the verdict
reports a broken build as a success. Scan the events.

## The multiplexed stream — the one that looks like it works

`GET /containers/{id}/logs`, `/containers/{id}/attach` and
`POST /exec/{id}/start` return **frames, not text**, whenever the container was
created **without** a TTY:

```
[STREAM_TYPE, 0, 0, 0, SIZE1, SIZE2, SIZE3, SIZE4][payload of SIZE bytes]
```

`STREAM_TYPE` is 0 stdin, 1 stdout, 2 stderr. `SIZE` is a big-endian uint32.
Frames repeat until the stream ends. Measured against a container running
`echo OUT; echo ERR 1>&2`:

```
Tty=0:  01 00 00 00 00 00 00 04  "OUT\n"   02 00 00 00 00 00 00 04  "ERR\n"
Tty=1:  "OUT\r\n"  "ERR\r\n"
```

**With `Tty: true` the stream is raw** — no headers, and newlines arrive as
`\r\n` because a PTY is involved. That is the trap: a developer testing by hand
reaches for an interactive container, sees clean text, and ships a client that
emits header bytes into the caller's log output for every non-TTY container —
which is every container a program actually runs. Demultiplex by reading eight
bytes, taking the length, reading that many payload bytes, repeating. Go clients
get this from `stdcopy.StdCopy`; everyone else writes it.

`attach` and `exec/start` additionally accept `Upgrade: tcp` +
`Connection: Upgrade`, to which the daemon answers **101 Switching Protocols**
and hands over a bidirectional connection. Without those headers it answers 200
and streams the same frames one-way.

## Filters are JSON, and the shape is specific

`filters` is a query parameter holding a JSON-encoded **map of string to array
of string** — the values are arrays of *strings*, even for booleans:

```
?filters={"dangling":["true"],"label":["stage=build"]}     correct
?filters={"dangling":true}                                 matches nothing
```

Wrong-shaped filters do not error. The daemon accepts them and returns an
unfiltered or empty list, so the bug surfaces as "my prune deleted too much" or
"my list is empty", never as a 400.

Query-string booleans elsewhere are strings: `?all=1` / `?all=true`. Booleans
in a **JSON request body** must be real JSON booleans — a language that encodes
`1` where the daemon expects `true` gets a type error from the API.

## Registry auth

`X-Registry-Auth` carries **base64url of a JSON object**, and the padding is
required — the daemon decodes with Go's `base64.URLEncoding`, not
`RawURLEncoding`. Stripping `=` produces
`failed to parse "X-Registry-Auth" header ... unexpected EOF`.

The header is mandatory on **every** push, anonymous included; the anonymous
form is the encoding of `{}`, which is `e30=` — three characters and one pad,
the shortest case and the one that proves padding matters. Payload keys:
`username`, `password`, `serveraddress`, or `identitytoken`.

`/build` uses a different header for the same job: `X-Registry-Config`,
base64url of a map from registry hostname to auth object, because a build may
pull from several registries.

## Bodies and paths

`POST /build` is the odd one: the request body is the **tar build context**
(`Content-Type: application/x-tar`), and every option — `t`, `dockerfile`,
`buildargs`, `target`, `platform` — rides in the query string. `buildargs` and
`labels` are themselves JSON-encoded strings inside that query.

Container endpoints accept a name or any unambiguous ID prefix. Image
references keep their slashes and tags inside the path
(`/images/myrepo/app:v1/push`) — percent-encoding them breaks the reference.
Names from `GET /containers/json` arrive with a leading `/`.

`exec` is two calls: `POST /containers/{id}/exec` creates the instance and
returns an `Id`, `POST /exec/{id}/start` runs it. The exit status comes from
`GET /exec/{id}/json` afterwards (`ExitCode`), never from the start call.

## Other engines

Podman serves this API on a compat socket — enable with
`systemctl --user enable --now podman.socket`, reach it at
`unix://$XDG_RUNTIME_DIR/podman/podman.sock`, and it announces API 1.41.
Multi-stage builds including `target` pass through unchanged, and the frame
format above is byte-identical. It is a reimplementation, not Docker: treat
anything beyond the documented surface — event payload details, healthcheck
fields, error message text — as unverified until measured against the engine
you actually target.

Clients differ in how they *find* the daemon: `DOCKER_HOST` is the one
mechanism all of them honour. Docker contexts
(`~/.docker/config.json` `currentContext` plus
`~/.docker/contexts/meta/*/meta.json`) are resolved by the `docker` CLI and
docker-java but not by most library clients, so "works in the terminal, fails
in my program" usually means a context the program never read.

## Probing by hand

```bash
curl --unix-socket /var/run/docker.sock http://localhost/v1.47/containers/json
curl --unix-socket /var/run/docker.sock -X POST \
  'http://localhost/v1.47/images/create?fromImage=alpine&tag=3'
```

`curl` writes the raw stream, frame headers included — that is the fastest way
to confirm what a client should be seeing before blaming the client.
