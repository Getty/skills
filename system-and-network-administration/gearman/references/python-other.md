# Python and other language integrations

Evidence: [Y1, G13, G3](sources.md). Product listings are discovery aids, not a certification of maintenance or compatibility.

## Python choices

OpenDev's `gear` has documented client/worker abstractions, event handling and reconnection behavior. Its included server is described as a testing facility rather than a production server under load. Do not substitute it for gearmand simply because an import exposes a class named `Server`. Other distributions with names such as `gearman` or `python-gearman` have different APIs, release histories and supported Python versions; inspect the exact installed package before writing code.

The bundled stdlib Python protocol lab exists to make framing, terminal handling, failure classification and contract tests inspectable without external dependencies. It is **not** a new recommended production Gearman library. It intentionally lacks concurrent task multiplexing, automatic failover, full protocol coverage and production reconnection policy. Use it for isolated examples and compatibility probes within its declared limits.

The client maintains an end-to-end monotonic submission deadline and never silently resends. Its worker uses one execution slot, bounded payload parsing and an idle-stop signal. Unexpected execution failures close the connection; a supervisor can restart the process, while server retry policy and application idempotency govern the job.

## Selecting any language binding

Create a capability matrix for the exact version: foreground/background, unique keys, priority, progress/data/exception events, binary payloads, timeouts and their units, multi-server selection, TLS client and worker support, certificate verification, graceful stop, reconnect/re-registration, cancellation and scheduling. Mark unknown fields as unverified rather than filling them from another language's API.

Review source and tests for partial writes, truncated frames, job-handle correlation, duplicate registration, callback exceptions, return buffer lifetime and result-size limits. Inspect packaging on the target OS/architecture. A fast benchmark on one happy-path function does not validate any of these failure behaviors.

## Cross-language contract testing

Run every producer against every supported worker version using shared fixtures. Include ASCII, Unicode, NUL-containing opaque bytes where applicable, integer boundaries, empty results, malformed JSON, duplicate fields, unexpected schema versions and domain errors. Compare parsed semantics, not incidental JSON key order. Explicitly document any parser acceptance differences.

Choose a transport-neutral domain service so unit tests need no Gearman server. Keep retry policy outside a serializer, and keep business idempotency outside a connection object. For Go, Java, Ruby, Node.js, Rust or another runtime, apply this same matrix and inspect the selected upstream implementation before supplying exact method names. This skill deliberately does not fabricate a comprehensive binding catalog.
