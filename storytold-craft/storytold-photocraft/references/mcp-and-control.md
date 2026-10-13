# MCP, control authentication and file authority

**Read when:** starting an agent server, attaching to a live editor, or diagnosing an authorization failure.

## Deterministic startup

Headless MCP is `photocraft-cli mcp`. Grant read and write authority independently with `--automation-read-root` and `--automation-write-root`. Without a corresponding root that authority is absent. Under this policy a relative file path is interpreted against its respective root; do not borrow VectorCraft's working-directory-relative rule.

The desktop control server is loopback-only. Prefer a private token file rather than a token exposed in process arguments:

```sh
photocraft --control 7878 --control-token-file /private/photocraft.token \
  --automation-read-root /work/in --automation-write-root /work/out
photocraft-cli mcp --bridge 127.0.0.1:7878 \
  --control-token-file /private/photocraft.token
```

Create the authorized directories and protect the token directory first. A missing token file is created; an existing one is reused. Newly created Unix token files are mode 0600; Windows requires an appropriate user-only ACL. Never include credentials in transcripts or sample assets.

A raw TCP connection must first send an `auth` request with the token. Authentication is per connection. Later messages use `{id,method,params}` and receive `{id,ok,result}` or `{id,ok,error}`. This is not JSON-RPC 2.0 despite its superficially similar envelope. The MCP bridge handles that translation.

## Tool selection

Prefer `command_list` → `doc_inspect` → `command_run` → `render_preview`. `command_run` uses `{id,params,wait?}`. Registry IDs such as `image.adjustments.invert` are not MCP tool names. `command_batch` uses ordered `steps` and defaults to stopping at an error, without rollback. Query both the enabled state and the command's parameter documentation.

`render_preview` is bounded: default maximum side 1024, upper bound 2048 in the reviewed guide. UI inspection and window screenshots require a bridged desktop. Use a rendered document image to judge exported content, and a window screenshot only when UI state matters.

## UI distinctions and uncertain outcomes

`engine.execute` executes command defaults directly; `ui.menu.invoke` can open the corresponding dialog. They are not semantically identical clicks. A dialog preview may be uncommitted, whereas another UI control may apply immediately. Read UI state before deciding that Escape will undo something.

A desktop control timeout can occur after work has started, or when an occluded/sleeping Wayland window stops processing frame callbacks. Timeout is not cancellation. Reconnect, authenticate and inspect document/history/jobs before retrying a non-idempotent operation.

## Evidence

- [photo-mcp](https://github.com/storytold/photocraft/blob/184c226a76c9ca6234d473912d438feaa48c1cb0/docs/mcp.md)
- [photo-control](https://github.com/storytold/photocraft/blob/184c226a76c9ca6234d473912d438feaa48c1cb0/docs/control-protocol.md)
- [photo-cli](https://github.com/storytold/photocraft/blob/184c226a76c9ca6234d473912d438feaa48c1cb0/apps/photocraft-cli/src/lib.rs)
