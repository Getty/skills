---
name: cel-engineering
description: "Use when writing, embedding, testing or debugging Common Expression Language (CEL) expressions — declarations and type environments, parse/check/eval, macros and comprehensions, missing fields, null, errors and unknowns, host functions, cost limits, Kubernetes x-kubernetes-validations and ValidatingAdmissionPolicy, Envoy conditions, Google Cloud IAM Conditions, or porting CEL between runtimes."
---

# CEL Engineering

Treat CEL as an expression language embedded in a host-defined environment. Keep
language semantics, declarations, extensions, input adaptation, and the host's
interpretation of results separate. A CEL Boolean does not enforce an action by itself.

Use primary documentation and pin the actual runtime
and host versions. The bundled runnable examples target **cel-expr-python 0.1.3**,
the CEL C++ Python wrapper, with no host extensions. They do not simulate Kubernetes,
Envoy, IAM, or every CEL implementation. See [sources](references/sources-and-versioning.md).

## Route the task

| Need | Read |
| --- | --- |
| Types, syntax, conversion, or expression design | [Language and types](references/language-and-types.md) |
| Missing fields, null, errors, unknowns, or Boolean behavior | [Missing data and errors](references/missing-data-and-errors.md) |
| `has`, list/map macros, quantification, or iteration | [Collections and macros](references/collections-and-macros.md) |
| Time, strings, regular expressions, or numeric edge cases | [Time, strings, and numbers](references/time-strings-and-numbers.md) |
| Implement a CEL host or cache checked programs | [Embedding and runtime](references/embedding-and-runtime.md) |
| Add CRD validation or transition constraints | [Kubernetes CRDs](references/kubernetes-crds.md) |
| Author admission policies, bindings, and parameters | [Validating Admission Policy](references/validating-admission-policy.md) |
| Use Envoy/IAM or translate between environments | [Host profiles and portability](references/host-profiles-and-portability.md) |
| Bound work or optimize evaluation | [Cost and performance](references/cost-and-performance.md) |
| Validate, debug, and compare implementations | [Testing and troubleshooting](references/testing-and-troubleshooting.md) |
| Run the original fixtures with a real evaluator | [Worked examples](references/worked-examples.md) |
| Verify current support and source authority | [Sources and versioning](references/sources-and-versioning.md) |

Load only the relevant references. Use the skill independently of any other skill
or application stack. Do not treat a host-specific variable as a CEL language global.

## Establish the evaluation contract

Inspect the expression, declared variables/types, runtime version, extensions,
representative bindings, expected output type, and actual error. For an illustrative
task use explicit assumptions; ask only when missing host semantics change the answer.

Record:

1. Expression source and revision; retain useful source positions for diagnostics.
2. Names, types, namespaces, protobuf descriptors, and field-presence semantics.
3. Standard macros and extension libraries enabled by the host.
4. Parse/check configuration and required result type.
5. Runtime values, unknown/partial-activation policy, custom functions, and limits.
6. Consumer behavior for true, false, null, error, unknown, and wrong-type outputs.

Choose the smallest environment that answers the task. Prefer typed declarations
when the shape is known; use `dyn` intentionally rather than to hide type errors.
For permission, admit only an explicitly valid Boolean true under the host contract.

## Author or repair expressions

1. Define required facts and a small expected-result table before compressing logic.
2. Write readable conditions with explicit numeric and time conventions.
3. Guard optional map/message fields using the host's presence model. Distinguish
   absence, explicit null, empty value, and a protobuf default.
4. Use `all` for universal checks and `exists` for existential checks. Add nonempty
   constraints separately; an empty collection can satisfy `all`.
5. Keep custom functions deterministic and bounded. Fetch external facts before
   evaluation unless a documented host API deliberately provides another model.
6. Parse and type-check at configuration time, retaining checked artifacts only
   with the matching environment/profile metadata.
7. Evaluate with the real runtime. Compare value type as well as value; host-language
   equality or truthiness may merge outcomes that CEL keeps distinct.
8. Test missing fields, wrong types, empty collections, boundary values, and errors.
9. Test the actual host binding and enforcement scope where integration is requested.
10. Deliver source, declarations/profile, observed results, and explicit untested layers.

## Preserve non-obvious behavior

- CEL is not JavaScript, SQL, Python, Rego, or FEEL with different punctuation.
  Do not import another language's truthiness, coercion, or missing-value semantics.
- `int`, `uint`, and `double` are distinct. Numeric adaptation from JSON belongs
  to the host; do not assume every number reaches CEL as the intended type.
- Field presence does not imply a non-null, nonempty, or authorized value.
  `has` is a macro with specific syntax, not a general exception-catching function.
- Runtime errors and unknowns are distinct, and neither is the literal null.
  Missing bindings do not automatically become partial-evaluation unknowns.
- Boolean `&&`/`||` have commutative error-absorbing semantics. Do not depend on
  left-to-right function execution or side effects. A decisive false/true can
  determine the result even when another operand errors.
- `exists_one` is not ordinary short-circuit `exists`: check error behavior and
  cardinality rather than stopping after the first successful member.
- Non-Turing-completeness does not make every input cheap. Nested bounded
  comprehensions and large data can exceed a production budget.
- Core CEL does not give every host identical extensions. Version optional values,
  string/list libraries, custom functions, and serialized AST formats explicitly.
- A checked expression is checked for an environment. Do not reuse it under
  different declarations, descriptors, functions, or host assumptions silently.
- A true IAM condition, CRD rule, or Envoy condition participates in a larger host
  decision. It does not independently prove an overall permission was granted.

## Run the examples

Create an isolated environment if the dependency is unavailable:

```bash
python3 -m venv /path/to/cel-example-env
/path/to/cel-example-env/bin/python -m pip install 'cel-expr-python==0.1.3'
/path/to/cel-example-env/bin/python scripts/run_cases.py assets/examples/cases.json
```

On Windows use that environment's `Scripts/python.exe`. The runner executes local
fixtures through the real CEL wrapper. It checks exact result categories and types;
it is not a replacement evaluator. Use it for trusted, bounded test fixtures,
not as an exposed untrusted-expression service. Read the worked-examples reference.

The supplied CRD and admission YAML are original integration examples. They require
validation on the intended Kubernetes release and a disposable test scope before
claiming cluster behavior. The local CEL corpus does not emulate those APIs.

## Deliver evidence at the correct layer

For expressions, provide declarations, source, input cases, and actual outcomes.
For embedding, include profile/cache keys, limits, and result handling. For Kubernetes,
include applicability, schema/binding/parameter behavior, and actual server results.
For portability, list the shared subset and observed disagreements.

Use `opa-rego-engineering`, `dmn-engineering`, or `feel-engineering` when comparison
requires those systems. Map semantics explicitly before claiming equivalent rules.
