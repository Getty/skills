# Worked examples and real-engine checks

## Contents and scope

`assets/examples/core-cases.json` contains 36 original examples covering arithmetic,
null/equality, ternary logic, conditional behavior, binding, missing variables,
list indexing/filtering/projection, contexts/functions, Cartesian iteration,
quantifiers, empty aggregates, temporal comparisons, and unary tests.

`assets/examples/portability-probes.json` contains six normative expectations for
numeric precision and type handling that reveal limits of the tested JavaScript
runtime. The expected values are kept independent of that runtime's observed behavior.

The fixtures use JSON-compatible contexts and expected results. Temporal cases
compare values inside FEEL and return Booleans; this avoids pretending that a
plain JSON string faithfully represents an engine's date/duration object.
These fixtures are an application example format, not the official DMN TCK format.

## Supply a real interpreter

The helper requires Node.js and an existing absolute module file that exports
`evaluate(source, context)` and `unaryTest(source, context)`, returning a
`{value, warnings}` result. This is the documented
[feelin API](https://github.com/nikku/feelin). It is not a generic adapter for every
FEEL package. Unary-test contexts bind the implicit input as `?`.

Use a project-local, exact runtime dependency. For the recorded run, feelin 8.2.0
was installed in a temporary test project with lifecycle scripts disabled:

```bash
npm install --ignore-scripts --no-audit --no-fund --save-exact feelin@8.2.0
```

Do not install into the skill directory. Retain the application project's lockfile
when repeatable dependency resolution matters. Substitute the package's actual
absolute `dist/index.js` path in these commands, run from the skill directory:

```bash
node scripts/run_cases.mjs --engine /path/to/node_modules/feelin/dist/index.js \
  --cases assets/examples/core-cases.json
node scripts/run_cases.mjs --engine /path/to/node_modules/feelin/dist/index.js \
  --cases assets/examples/portability-probes.json
```

The helper validates case shape/unique IDs, runs the real interpreter, compares
values with strict structural equality, checks optional minimum warning counts,
and preserves all returned warnings. Unexpected warnings are reported but do not
independently fail a case unless a specified assertion fails. Exit 0 means all case
assertions passed; exit 1 means a result/error mismatch; exit 2 means setup/fixture
failure. The helper performs no network requests and has no built-in evaluator.

## Recorded results

With **feelin 8.2.0**, all **36 core cases passed**. The missing-variable case
returned null and an explicit missing-variable warning. The separate portability
run failed all six normative probes, retaining the standard expectations:

| Expression | Normative FEEL expectation | Observed feelin 8.2.0 |
| --- | --- | --- |
| `0.1 + 0.2 = 0.3` | true | false, no warning |
| `9007199254740993 > 9007199254740992` | true | false, no warning |
| `amount <= 100`, with `amount: "100"` | null | true, no warning |
| Unary test `<= 100`, input `"100"` | null | true, no warning |
| Unary test `>= 100`, input `"100"` | null | true, no warning |
| `every a in approvals satisfies a.approved`, with `[{approved: "false"}]` | null | true, no warning |

The [DMN 1.6 number model](https://www.omg.org/spec/DMN/1.6/PDF) defines decimal
precision that distinguishes the numeric values. Its comparison and ternary-logic
rules (tables 50, 51, 53, 55, and 56) do not coerce the string inputs in the other
four cases: mixed-kind ordering yields null, and a non-Boolean quantifier predicate
combines through ternary conjunction. Validate numeric and Boolean input types at
the host boundary; changing parser mode does not fix the observed coercions.
Keep the failed probes as compatibility evidence. Do not edit expected results to
make the selected implementation appear conformant. These observations neither certify the whole interpreter nor establish
the behavior of another release or of an entire DMN engine. B-FEEL execution was
not tested in this run.
