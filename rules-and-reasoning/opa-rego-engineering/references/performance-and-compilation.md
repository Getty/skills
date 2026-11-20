# Performance and compilation

## Measure the workload

Set an end-to-end latency/throughput budget. Separate serialization, network,
lookup, evaluation, and response consumption. Use representative data cardinality;
a small benchmark does not predict a policy scanning thousands of memberships.

Prefer keyed objects for unique-identifier lookups and avoid accidental iteration
cross-products. Use profiling, metrics, and `opa bench` supported by the installed
release. Compare distributions, not a single fastest sample.
[Performance guidance](https://www.openpolicyagent.org/docs/policy-performance).

Replay semantic cases after optimization. A clever comprehension can change
undefined behavior or duplicate handling. Preserve a readable baseline and compare
real input distributions before accepting complexity.

## Partially evaluate intentionally

Identify known facts and unknown request fields. Partial evaluation specializes a
policy and produces residual conditions for a later stage; remaining unknowns are
not automatically false. It does not translate arbitrary Rego into portable SQL.

For data filtering, verify backend operations and agreement with direct decisions.
Consider joins, counts, pagination, and error paths that could reveal excluded data.
Treat the residual format as a versioned integration contract.
[Compile API](https://www.openpolicyagent.org/docs/rest-api#compile-api).

## Target Wasm deliberately

Build with a named entrypoint and inspect the artifact. OPA's Wasm output is an
evaluation program, not the whole OPA management service. Verify ABI and required
host built-ins. Some functions need host implementations, and strict built-in-error
behavior differs from native OPA. [Wasm](https://www.openpolicyagent.org/docs/wasm).

Run identical policy/input/data cases on native OPA and the actual Wasm host.
Compare errors and missing results as well as values. Confirm data refresh,
concurrency, memory ownership, and evaluation limits for the host.

## Cache at the correct layer

Distinguish prepared-query, compiled-artifact, reference-data, and decision caches.
A true-answer cache needs all relevant identity/resource/policy/data versions or
explicit invalidation. Compilation may remain valid while a permission becomes
stale immediately after revocation. Do not conflate those validity periods.

Document performance with the real runtime and hardware. Keep baseline evidence
before an upgrade to distinguish parsing, activation, and evaluation regressions.
When external lookups dominate, changing rule syntax may have negligible effect;
address measured costs rather than optimizing the most visible source expression.
