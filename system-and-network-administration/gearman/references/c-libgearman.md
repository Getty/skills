# C/C++ with libgearman

Evidence: [C1–C5, G1](sources.md). The [C examples](../examples/README.md) implement binary-safe echo under a separate function, not the JSON sum contract. They require installed matching headers/library; no native compilation was possible in the authoring environment.

## Client ownership and errors

Create a client, add the selected server, configure bounded I/O waiting, submit bytes with an explicit size, inspect `gearman_return_t`, then release all owned resources. `gearman_client_do` returns an allocated result according to the documented allocator contract. With default allocation, free the result; when supplying custom allocators, use the matching ownership rules. A zero-length result can be successful even if its pointer is null.

Never derive workload or result length from `strlen` when the protocol carries binary data. Avoid retaining pointers into a task/job object after that object is freed or reused. On failure, copy a bounded diagnostic while its owning object remains alive and sanitize it before logging.

Synchronous `do` can report intermediate work events rather than final success. A client that supports status/data/warnings must resume the same operation according to libgearman's documented state machine, not resubmit it as a new logical request. The bundled minimal client is restricted to the bundled echo worker, which produces only a final result; unexpected intermediate codes fail visibly rather than silently duplicating work.

## Worker ownership

A worker callback receives a job, context, output size pointer and return-code pointer. Inspect workload and size, validate limits, allocate the result with compatible ownership, set the output length and return status, then return the result pointer. In the normal callback API libgearman performs the terminal send from this return contract. Do not also manually send a second completion.

Use one independently owned worker/client object per execution context unless the installed API explicitly documents safe concurrent access. Sharing a struct between threads is not made safe by libgearman internally using threads elsewhere. Create connections after fork. Keep signal handlers minimal; set a `sig_atomic_t` flag and let a bounded wait return control to the main loop.

## Production additions

The sample is intentionally smaller than a production framework. Add application serialization, an admission policy, structured request identity, external-effect idempotency, dependency deadlines, reconnect backoff, metrics and secure transport. Validate availability of TLS client **and worker** APIs against headers and linked runtime. Version 2.0 added the previously missing worker SSL setter; a wrapper built against older headers may not expose it.

For asynchronous tasks define task ownership, callback reentrancy, event-loop integration and maximum outstanding work. Register data/status/complete/fail callbacks, and always release abandoned tasks. Bound result sizes independently of request sizes. The minimal C example checks the returned size after libgearman has allocated it; that check is not a pre-allocation defense against an untrusted server. Its trusted-echo scope is intentional. A failed client connection means a potentially unknown server outcome, not automatic permission to replay an effectful operation.

## Build and diagnostics

Compile with warning flags and a controlled dependency prefix; use `pkg-config` when the installed development package supplies metadata, otherwise use the documented linker flags for that package. Test debug, AddressSanitizer/UndefinedBehaviorSanitizer and representative optimized builds. Inspect the actual dynamic-library resolution of the deployed executable. A clean compile proves neither server compatibility nor crash recovery.
