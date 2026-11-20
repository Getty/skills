---
name: dmn-engineering
description: "Use when modeling, validating or executing OMG DMN decision models — .dmn files, decision requirements diagrams, decision tables and hit policies, boxed expressions, decision services, DMNDI, engine portability, TCK conformance, migrating rules into DMN."
---

# DMN Engineering

Treat DMN as a versioned language for describing decisions, their information
requirements, and executable decision logic. Keep business meaning, model structure,
expression semantics, engine behavior, and application enforcement separate.

Use **OMG DMN 1.6**, listed as formal in September 2026, as the normative baseline.
DMN 1.7 beta is a separate development
version. Do not equate the newest specification with the user's engine support.
Use a supported older interchange profile when the actual target requires it.
Read [sources and versioning](references/sources-and-versioning.md) before making
version claims or changing namespaces.

## Select the task references

| Task | Read |
| --- | --- |
| Draw a DRD or distinguish information, knowledge, and authority | [Decision requirements](references/decision-requirements.md) |
| Turn prose into reviewed business decisions | [Modeling workflow](references/modeling-workflow.md) |
| Select hit policies, diagnose overlap, or specify no-match behavior | [Decision tables](references/decision-tables.md) |
| Choose boxed expressions, FEEL, BKM, or decision-service boundaries | [Expressions and services](references/expressions-and-services.md) |
| Read, generate, migrate, or round-trip `.dmn` XML | [XML and interchange](references/xml-and-interchange.md) |
| Choose an engine, embed execution, or integrate with workflows | [Engines and integration](references/engines-and-integration.md) |
| Validate models, compare implementations, or use the DMN TCK | [Validation and TCK](references/validation-and-tck.md) |
| Version decisions and retain useful explanations | [Governance and provenance](references/governance-and-provenance.md) |
| Map to RUML, authorization, planning, or semantic graphs | [Interoperability](references/interoperability.md) |
| Resolve common failures without changing business meaning | [Troubleshooting](references/troubleshooting.md) |
| Run the original model and the local inspection helper | [Worked examples](references/worked-examples.md) |
| Establish source authority and refresh the baseline | [Sources and versioning](references/sources-and-versioning.md) |

Load only the references needed for the current task. Use the standalone
`feel-engineering` skill for detailed expression work if available; this skill is
usable independently and includes the DMN/FEEL boundary needed for ordinary models.

## Establish the decision contract

Identify the output question, inputs, admissible input domain, result type, and
business owner. Inspect the supplied model and target runtime before proposing a
replacement. Distinguish an explanatory diagram from an executable deliverable.

For an implementation, record:

- Specification/interchange version and expression dialect.
- Engine, modeler, adapter, and deployment versions.
- Input names, types, missing-value policy, and data-source assumptions.
- Decision or decision-service entry point and output envelope.
- Required hit policies, imports, functions, and diagnostics.
- External effect boundaries and how the caller treats errors or missing decisions.

Use explicit assumptions for educational examples. Ask only when missing business
meaning or deployment facts materially change the requested outcome.

## Build or repair a model

1. **Define the question.** Write one precise decision question and an output domain.
   Separate facts, eligibility, calculations, routing, and actions when they change
   independently. Preserve source references for disputed or regulated wording.
2. **Model information requirements.** Build the DRG from dependencies; render useful
   views as DRDs. Use information requirements for input data and decisions,
   knowledge requirements for callable knowledge, and authority requirements for
   sources of authority. An authority link does not execute source text.
3. **Select the representation.** Use a decision table for finite combinations of
   conditions, a literal expression for a compact formula, a context for named
   intermediate values, and a BKM for parameterized reusable logic. Choose a
   decision service for a published decision interface, not a workflow lifecycle.
4. **Choose semantics before rows.** Specify the input domain, completeness goal,
   hit policy, priority order where applicable, and no-match handling. Draw boundary
   partitions before writing entries. Treat row order as logic only for policies
   whose semantics use it.
5. **Type and bind the logic.** Bind input expressions to actual model variables.
   Put unary tests in input entries and value expressions in output entries.
   Quote string literals. Make host conversion of dates, numbers, and collections
   explicit. Preserve the difference between FEEL and B-FEEL.
6. **Serialize for the target.** Pin the model namespace and referenced schema set.
   Keep model namespace, model identifiers, and exporter version distinct. Preserve
   stable IDs, namespace-qualified imports, and optional diagram information.
7. **Validate in layers.** Parse XML, validate the correct XSD, resolve references,
   check expression types and table semantics, execute business cases, and test
   the actual host adapter. Schema acceptance alone is not execution evidence.
8. **Deliver the evidence.** Include model files, decision contract, cases and
   expected outcomes, runtime assumptions, actual check results, and limitations.
   For repairs, explain the smallest change that fixes the observed defect.

## Preserve the non-obvious semantics

- A DRD is a view; a DRG is the underlying requirements graph. Arrows express
  dependencies, not a BPMN control-flow schedule.
- A BKM provides parameterized knowledge; a knowledge source provides authority.
  Neither is interchangeable with an input-data node.
- `UNIQUE` requires disjoint matches but does not establish completeness. A valid
  input can still match no rule. `ANY` permits overlap only with equal outputs.
- `FIRST` uses row order. `PRIORITY` uses the declared output-value order. They are
  different policies even when a particular example produces the same result.
- `COLLECT` without aggregation returns matched outputs without a guaranteed order.
  Preserve duplicates. `RULE ORDER` provides row order; `OUTPUT ORDER` uses output
  priorities. Sum/count aggregate all matched outputs, not distinct values.
- Aggregated Collect requires a single result output. Annotations do not count as
  result outputs. Do not aggregate compound contexts without explicit post-processing.
- Test no-hit behavior separately from aggregation over an empty list. DMN 1.6
  clause 10.3.2.10 specifies a default output or `null`; adapters and engines may
  expose a different wrapper. Do not silently normalize that into a false decision.
- A dash is the unrestricted unary test. A blank output cell, an empty string,
  `null`, and a no-match decision are different situations.
- A table row combines its input conditions conjunctively. A comma-separated unary
  test within one cell offers alternatives; it does not add another table column.
- FEEL uses one-based list indexing and three-valued Boolean behavior. Boolean
  results are not interchangeable with JavaScript truthiness or SQL predicates.
- B-FEEL in DMN 1.6 shares FEEL grammar but changes error/default semantics. Selecting
  it can change a decision and must be reviewed and tested as a semantic migration.
- A conformance level is scoped to the specification and its compliance points.
  Level 3 does not require Java/PMML/ONNX functions or every vendor extension.
- Preserve specification disagreements instead of quietly inventing an answer.
  For example, 1.6 clauses 8.2.11 and 10.3.2.10 differ on compound Output Order;
  use single-output Output Order for portability until the selected profile resolves it.
- A successful evaluation does not execute a business action unless the host does
  so. Keep model evaluation repeatable and keep effects in explicit application code.

## Use the bundled helper

From the skill directory, run:

```bash
python3 scripts/inspect_dmn.py assets/examples/shipping-lane.dmn
python3 scripts/inspect_dmn.py assets/examples/shipping-lane.dmn --schema /path/to/DMN16.xsd
```

The first command inventories UTF-8 XML and selected structural defects. The second
also performs XSD validation using `lxml` and a locally complete official schema
set. Neither evaluates FEEL or proves table completeness. The helper rejects DTDs,
performs no network requests, and returns a nonzero status for detected errors.
Read [worked examples](references/worked-examples.md) for exact limits and cases.

## Report useful results

For an explanation, connect the decision to its inputs and show why the chosen
representation helps review. For execution, name the model and engine versions,
entry point, bound inputs, decision result, and diagnostics. For a migration,
state preserved semantics, changed semantics, and tests that distinguish them.

Report a missing runtime as an untested layer. Do not label a parser, diagram
renderer, or partial evaluator as a complete DMN engine. Avoid universal engine
rankings; compare the actual required features and pinned versions.
