---
name: shacl-standards
description: "Use when writing, running or debugging SHACL validation — shapes, targets, property paths, Core constraints, sh:closed, qualified value shapes, SHACL-SPARQL, validation reports, SHACL 1.2."
---

# SHACL Validation

Use SHACL to check selected RDF nodes against explicit conditions expressed as an RDF shapes graph. Explain three things first: which data graph is checked, which nodes are selected, and which conditions determine conformance. A clean report can mean the intended records passed, or that no intended record was targeted; establish coverage separately.

Use the SHACL Recommendation of 20 July 2017 as the baseline for Core and SHACL-SPARQL. SHACL 1.2 is a later revision whose specifications each carry their own publication status; read it from the document. Keep advanced Notes, newer drafts, and vendor extensions separate from the implemented baseline.

## Navigate the references

- [Shapes, targets, and paths](references/shapes-targets-paths.md): graph roles, focus/value nodes, target selection, reusable shapes, and path semantics.
- [Core constraint design](references/core-constraints.md): cardinalities, node kinds, classes, datatypes, values, logical/nested constraints, qualified counts, and closed shapes.
- [Reports, inference, and execution](references/reports-execution.md): conformance, severities, validation failures, entailment, coverage, deactivation, and reproducible runs.
- [SPARQL and advanced features](references/sparql-advanced.md): custom constraints, pre-bound variables, portability restrictions, recursion, rules, and feature boundaries.
- [Worked examples and diagnosis](references/examples-diagnosis.md): complete original shapes/data, expected outcomes, failure analysis, and meaningful verification.
- [Sources and versions](references/sources.md): primary specifications, implementation documentation, and dated status distinctions.

Read the relevant reference directly. This material does not depend on another skill or assume any programming language, graph store, or application architecture.

## Define the validation contract

Identify the data graph, shapes graph, available class/subclass information, and selected graph policy. A dataset may contain many named graphs, while a particular validation run checks a chosen graph or a deliberately constructed union. Do not silently merge unrelated releases or sources.

List the records that should be checked independently of the shape's target expression. Decide whether validation uses asserted data, subclass information already present, or a specified inference/materialization step. Preserve the original asserted graph when derived statements will be added for validation.

Separate shape syntax errors, malformed data syntax, unsupported features, engine failures, and actual data violations. Choose SHACL Core where it expresses the requirement clearly; use SPARQL constraints for conditions that need its additional expressiveness.

## Translate requirements deliberately

1. Choose explicit targets and verify that they select the intended nodes.
2. Use property shapes to inspect values reached through a path and node shapes to constrain the node itself.
3. Express requiredness with minimum counts and optionality by omitting a positive minimum. Datatype or class constraints alone generally do not require a missing property to exist.
4. Combine IRI/node-kind checks with class checks when references must meet both conditions.
5. Use nested shapes for structural requirements and qualified counts when only values matching another shape should count.
6. Scope closed shapes narrowly and identify permitted metadata explicitly.
7. Provide useful messages, stable shape identifiers where reuse matters, and an explicit severity policy.

Do not translate OWL existential restrictions into required input fields without a declared application rule. SHACL checks the available graph; OWL describes possible interpretations and can infer facts. Neither automatically replaces the other.

## Run and inspect

Parse data and shapes separately. Record validator version and enabled feature set. Check shape well-formedness when generating or substantially changing shapes, using available metavalidation support. Set inference options explicitly rather than relying on defaults.

Capture the machine-readable report and execution outcome. Verify focus-node coverage separately; use independently known input identifiers when a missing type could exclude a record. Treat restricted-node reruns as restricted coverage, especially for cross-record constraints.

Compare report meaning through focus node, result path, source shape, constraint component, severity, and value as relevant. Do not depend on arbitrary result ordering, generated blank-node labels, or exact engine-authored message wording.

## Deliver an explained result

Return the shapes or explanation, the graph/target/inference assumptions, observed conformance results, and any material unsupported features. Distinguish normative conformance from an application's acceptance threshold for warnings. For a repair, explain the actual violated condition and whether changing data, shape, target, or graph context is appropriate. Avoid automatically weakening a constraint merely to produce a green report.
