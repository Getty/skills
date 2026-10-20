# Developing server extensions and persistence backends

Evidence: [S3, S4, S1, S2](sources.md). This is an implementation method, not a claim of a stable loadable-plugin ABI. Inspect matching backend and build-registration code before writing exact extension scaffolding.

## Choose the right extension boundary

Most business functions belong in external workers. Do not add document rendering, privileged shell execution or an application-specific API call inside gearmand's event-processing path. Use a server change when the requirement genuinely concerns queue storage, protocol transport, admission, scheduling or daemon behavior.

Prefer an authenticated application gateway or producer policy when a requirement can be implemented without modifying the native daemon. A new packet or backend increases the compatibility and crash-recovery surface for every deployment using it.

## Persistence callback contract

The inspected public server queue interface contains add, flush and done operations, including explicit byte sizes, function, unique ID, priority and scheduling time. Replay reconstructs pending jobs through the server's startup path. Find the corresponding registration/interface implementation in the selected tag and use an existing backend as a structural guide—not as proof of durability correctness.

For a new backend define:

| Boundary | Required decision |
|---|---|
| Add acknowledged | Exactly which backend commit/flush has completed? |
| Done acknowledged | Which stored entry is removed and is removal idempotent? |
| Replay | How are bytes, identity, priority and scheduling time reconstructed? |
| Duplicate/storage key | Is identity scoped by function and unique, and how are empty keys treated? |
| Failure/reconnect | Are errors bounded, visible and classified without blocking indefinitely? |
| Upgrade | How are old rows/records read or migrated, and can rollback still read them? |

Use parameter binding or binary-safe backend APIs; never construct SQL or storage keys from uncontrolled text with ad-hoc separators. Preserve zero bytes and lengths. Treat function/key encoding changes as a stored-data migration. Define what happens after an uncertain backend commit and repeated add/done calls.

## Protocol extensions

Inspect command-number allocation and packet metadata in the matching protocol definitions. Define direction, exact field boundaries, empty-field behavior, length/numeric limits, negotiation and backward failure behavior. Do not silently overload a standard command with incompatible semantics. Update parsers, state machines, tests and diagnostic output together.

For scheduling extensions define clock source, integer ranges, worker wakeup, persistence replay and shutdown behavior. For cancellation define queued versus already assigned jobs; removing a server record cannot retract an external effect already executing on a worker.

## Required engineering tests

Run normal add/complete/replay and then fail each boundary: before backend commit, after commit before reply, before/after deletion, during reconnect, during timer callback and during shutdown. Inject duplicate operations, oversized/binary payloads, backend permission denial and backend unavailability. Check bounded latency, memory ownership and clean final counters.

Build with the matching project's test system, relevant real backends, sanitizers and deterministic stress seeds. No custom backend implementation is bundled here: claiming a working backend without compiling against the internal API would be misleading. The included tests focus on the independently executable protocol and application boundaries.
