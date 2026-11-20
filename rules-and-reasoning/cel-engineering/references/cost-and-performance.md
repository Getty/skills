# Cost, safety, and performance

## Bound more than language expressiveness

CEL lacks arbitrary recursion and general loops, but finite comprehensions can
still perform substantial work. Nested scans, large maps, huge strings, and repeated
regex work need budgets. Define maximum source length, AST depth/size, input size,
collection cardinality, and evaluation work for an exposed service.

Choose parser/checker/evaluator limits supported by the actual library. Custom
functions require their own resource bounds; evaluator cost accounting may not
fully reflect their external work. Pure-looking syntax cannot constrain a host
callback that opens a network connection or runs arbitrary code.

## Use static and runtime controls appropriately

Kubernetes uses cost estimation and runtime budgets to protect API-server resources.
Schema bounds can improve estimates; a cheap-looking expression over unbounded
collections may be rejected. Distinguish configuration-time cost rejection from
runtime exhaustion. [Kubernetes CEL constraints](https://kubernetes.io/docs/reference/using-api/cel/).

For a custom host, measure worst relevant input sizes, not only averages. Test
malformed inputs and expensive negative paths. Document timeout/cancellation behavior
for the runtime and any functions. If a library cannot enforce required limits,
add an appropriate process/host boundary instead of claiming CEL alone is sufficient.

## Compile once, bind many times

Keep parse/check work outside the hot request path. Reuse prepared programs only
under the same environment contract. Avoid rebuilding descriptors and extension
registries for every request. Use bounded caches with eviction and a key including
the profile, not only expression source.

Measure parse, check, prepare, activation adaptation, and evaluation separately.
The [CEL Go implementation](https://github.com/cel-expr/cel-go/blob/master/README.md)
describes reusable programs; other implementations have different lifecycle APIs.

## Improve the measured expensive path

Replace repeated joins with precomputed keyed facts when meaning is preserved.
Avoid converting timestamps or normalizing strings repeatedly inside a nested
comprehension. Limit dynamically constructed patterns and data structures. Replay
the semantic corpus after every optimization.

Use realistic distributions and record runtime version, host configuration, and
input sizes with results. Do not repeat general microsecond performance claims as
a guarantee for arbitrary policies, functions, or machines. A fast predicate can
still belong to a slow service if data fetching or input conversion dominates.

## Protect diagnostics and caches

Budget trace/explanation output as well as evaluation. Logs of every intermediate
value can expose private data or consume more resources than the expression itself.
Cache compiled programs separately from decisions: a cached permission can become
stale after identity or resource changes even while the expression remains valid.
