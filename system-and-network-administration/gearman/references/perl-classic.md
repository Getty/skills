# Classic Perl: Gearman::Client and Gearman::Worker

Use for the pure-Perl binding, not `Gearman::XS`. Evidence: [P1, P2, P9](sources.md). Runnable adapters are under [examples/perl](../examples/README.md). Pin the installed distribution and dependencies before attributing current repository behavior to an older CPAN release.

## Client API and identity

`Gearman::Client->new` constructs a client; `job_servers` supplies endpoints. `do_task($function, $bytes, { uniq => $id })` returns a **scalar reference** on success, including a reference to an empty string. Test `defined`, then dereference; do not compare the result with a PHP string or the XS return tuple. `dispatch_background` returns a handle or failure, not a result. Store the request ID separately from that handle and retain the server origin where available.

Use JSON bytes from an explicitly configured UTF-8 serializer. Avoid relying on convenience serialization of Perl references: it makes a cross-language contract ambiguous and can introduce unsafe object decoding. Classic documentation explicitly recommends supplying a unique value for background work with persistent queues. This unique is not a durable exactly-once key.

For parallel submissions inspect the binding's task/task-set APIs, callback lifetime, limits and error reporting. Define a maximum number of outstanding tasks and bounded result buffering before adding asynchronous submission. A synchronous API wrapped in unlimited child processes is not controlled concurrency.

## Worker lifecycle and callback contract

Register a named function with a code reference. The callback receives a `Gearman::Job`; `arg` supplies workload bytes. A defined callback return value means a completed result; an undefined return means failure. `work` is already a long-running loop. Do not wrap it in a tight retry loop without understanding when it returns. Its `stop_if` hook supports stopping between work cycles; a signal flag does not interrupt an already blocked business dependency.

In the inspected upstream `Worker.pm`, an uncaught callback exception sends a serialized `WORK_EXCEPTION`, and the surrounding path can subsequently send `WORK_FAIL`. The inspected Gearmand 2.1 implementation treats the first exception packet as terminal. Therefore the bundled adapter catches expected contract errors inside the callback and returns `undef`, producing one failure path rather than depending on this cross-version exception interaction. Reproduce it against the exact installed distribution before changing library internals. Never include raw secret-bearing exceptions in job results.

Keep database and Gearman connections process-local. Fork worker children first and establish their connections afterward. Use a supervisor for process restart; distinguish an invalid job from a systemic database outage before choosing whether to keep consuming.

## Names, timeouts, and interoperability

The classic prefix helper uses a tab-separated prefix/function encoding. An explicit dotted name such as `gearman_skill.sum.v1` is easier to share with other bindings. A function prefix is not access control.

The optional registration timeout is a server-side assignment timeout, not a Perl execution sandbox. The old callback can continue running after the server gives up on its connection or assignment. Protect effects using application identity and independently bounded operations. Inventory all timeout units rather than assuming the worker registration timeout matches a client socket timeout.

## Acceptance checklist

Exercise empty result, callback failure, UTF-8 JSON, numeric strings versus integers, duplicate unique while active, completed-job resubmission, worker termination after an effect, graceful stop while idle, reconnect registration, and a server restart. The included standalone contract CLI is testable without installing the Gearman module; syntax checks alone do not establish native binding compatibility.
