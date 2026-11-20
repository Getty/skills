# Validation and the DMN TCK

## Validate layers independently

| Layer | What it can establish | What remains |
| --- | --- | --- |
| XML parser | Well-formed document | Correct schema and semantics |
| XSD | Allowed elements, attributes, ordering, basic types | FEEL and business correctness |
| Model checks | References, types, supported constructs | Runtime result for concrete inputs |
| Table analysis | Selected gaps, overlaps, or shadowing | Completeness outside analyzed domain |
| Engine execution | Observed outcome on a pinned runtime | Unexecuted cases and source interpretation |
| Host integration | Input/output conversion and error handling | Behavior of unrelated downstream actions |

Name the layer and its limitations in every validation result. A green modeler icon
may describe only one of these layers.

## Use independent expectations

Write cases from the business contract, including outcomes at boundaries and
errors for malformed facts. Keep expected results independent of the implementation.
Compare types and diagnostics, not only stringified values. A list with one context
is not the same result shape as that context; absent/null/false are not equivalent.

For Unique, include overlap and gap probes; for Any, differing-output overlap; for
Collect, duplicate outputs and no hits; for Priority, an output-priority reorder;
for First, a row-order regression. For every imported BKM/service, test at least one
successful binding and a missing/wrong-type parameter.

## Use the TCK as evidence, not a blanket guarantee

The [DMN TCK](https://github.com/dmn-tck/tck) is a community test corpus with
serialized models, inputs, and expected results. It does not define a new language.
Pin a revision and the vendor runner configuration. Follow that runner's own build
instructions instead of assuming one Maven profile works unchanged for every
revision. Inspect skipped, unsupported, missing, and failed cases separately.

The [results site](https://dmn-tck.github.io/tck/index.html) presents submissions
against versions and test sets. A submission may become incomplete when the corpus
grows. Avoid comparing percentages from different totals or treating a historical
submission as evidence for the binary in the user's deployment.

Run relevant labels first to answer a concrete portability question. A full suite
is appropriate for broad engine qualification, not for every local text edit.
Preserve model and runner licenses if redistributing upstream fixtures. The bundled
examples in this skill are original and are not a copied TCK.

## Handle disagreements honestly

When engines disagree, reduce the case to one construct, retain all runtime/profile
versions, read the normative clause, and check known OMG/TCK issues. Distinguish a
specification ambiguity from an implementation defect or adapter conversion bug.
Do not modify an expected result solely to make one runtime pass. Report the
observed difference and select an explicitly documented deployment profile.
