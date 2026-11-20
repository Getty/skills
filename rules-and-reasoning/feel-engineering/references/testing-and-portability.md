# Testing and portability

## Build discriminating cases

Test the result value, result type, warnings/errors, and parser mode. Include the
smallest case that distinguishes the intended semantics from a plausible mistake.
For example, `false and null` distinguishes ternary logic from blanket-null
propagation; an empty `every` distinguishes universal quantification from a
nonempty-approval requirement.

| Feature | Distinguishing case |
| --- | --- |
| Number precision | `0.1 + 0.2 = 0.3` and a large integer boundary |
| Mixed kinds | `1 = "1"` |
| Branching | `if null then "a" else "b"` |
| Indexing | First, last, zero, and out-of-range index |
| Filtering | A null predicate and a missing context field |
| Quantifiers | Empty list and an unknown predicate |
| Functions | Wrong arity/type and unknown function |
| Unary tests | Endpoint input and wrong parser mode |
| Temporal values | Leap day, offsets, month end, and invalid date |
| Host binding | Missing field versus explicit null and string versus number |

## Separate normative expectations from engine observations

Keep the expected standard result fixed when an implementation disagrees. Record
the actual version and diagnostic behavior. The bundled `portability-probes.json`
expects true for the decimal identity; feelin 8.2.0 returned false without warnings
in the observed run. That probe intentionally fails on that version and identifies
a numeric portability limit. Do not weaken equality to a tolerance in a test about
exact FEEL decimal semantics.

The same runtime also returned true without warnings for `amount <= 100` with
`amount: "100"`, for the unary tests `<= 100` and `>= 100` on the string `"100"`,
and for `every a in approvals satisfies a.approved` with
`approvals: [{approved: "false"}]`. Standard FEEL expects null in these cases:
mixed string/number ordering does not perform host coercion, and the quantifier
combines its non-Boolean predicate using ternary conjunction. The probe file retains
these four expectations separately from the 36 passing core cases. See
[DMN 1.6 tables 50, 51, 53, 55, and 56](https://www.omg.org/spec/DMN/1.6/PDF).

Treat this as observed behavior of feelin 8.2.0, not as permission to use strings as
Booleans or numbers. Enforce the input contract before evaluation and retain the
result diagnostics; warning absence alone cannot detect these observed coercions.
Do not claim that switching an expression from full mode to unary-test mode repairs
the type issue.

A tolerance can be an application decision for approximate measurements, but must
be stated as a separate rule. It does not repair conformance of an interpreter's
underlying numeric representation.

## Use shared suites with the right scope

Use the [DMN TCK](https://github.com/dmn-tck/tck) to select language cases relevant
to the requested profile. Pin corpus and runner revisions. A FEEL-only runner does
not thereby validate decision services, imports, all hit policies, or DMNDI.
Distinguish unsupported and missing tests from passing tests.

Compare engines with identical typed inputs and equivalent parser entry points.
Normalize output only where the contract explicitly permits it; do not reorder
lists, discard nulls, or coerce strings to hide differences. Preserve raw results
alongside normalized comparisons when debugging an adapter.

## Validate fixes proportionately

After an expression fix, run the reproducer and adjacent boundaries. For an engine
or dialect migration, run a broader profile suite and real business fixtures because
many unrelated expressions can change. State untested features. A green set of
educational examples is useful evidence for those examples, not certification of
the entire FEEL language or the underlying business policy.
