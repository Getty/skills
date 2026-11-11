# Reports, inference, and execution

## Read a report as structured evidence

A validation report has a `sh:ValidationReport` node and a boolean `sh:conforms`. Results identify the focus node and severity, and usually expose the source shape, constraint component, path, offending value, and an explanation. Some fields are absent when they do not apply; for example, a missing-value count violation has no offending value to display.

```turtle
@prefix ex: <https://example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .

[] a sh:ValidationReport ;
    sh:conforms false ;
    sh:result [ a sh:ValidationResult ;
        sh:focusNode ex:sample8 ;
        sh:resultPath ex:site ;
        sh:sourceShape ex:RequiredSiteShape ;
        sh:sourceConstraintComponent sh:MinCountConstraintComponent ;
        sh:resultSeverity sh:Violation ;
        sh:resultMessage "A site value is required." ] .
```

Under the 2017 Recommendation, `sh:conforms` is true only when validation produces no results. Severity labels do not alter that normative rule. A validator option or application gate may allow warnings, but explain that acceptance policy separately from the report's standards meaning. The default severity is `sh:Violation`; `sh:Warning`, `sh:Info`, and other severity IRIs classify results.

Do not assert exact engine-authored message wording or report ordering. Compare meaningful RDF fields and preserve nested details when logical/nested constraints produce them.

## Distinguish violations from failures

A completed run can report ordinary nonconformance. It can also encounter a parser error, an ill-formed shapes graph, an unsupported feature, a SPARQL evaluation failure, recursion handling failure, or a timeout. These are not interchangeable outcomes.

Do not turn a validation failure into an empty “conforms” report. Capture the process/API outcome and machine-readable report separately. If an engine stops after a limit or first violation, describe the report as incomplete enumeration rather than asserting that only those violations exist.

## Define entailment and graph context

Class constraints and class targets use SHACL's specified instance/subclass behavior over available data. A validator may additionally offer RDFS or OWL materialization. Record that setting and any imported ontology graph; it can change target coverage, value counts, classes, and closed-shape results.

A domain axiom can infer a type that satisfies a class check. If the contract requires a producer to supply that type explicitly, validating only a materialized graph does not prove the asserted input met the contract. Preserve and select the appropriate graph for each check.

A shapes graph can declare an entailment requirement through supported mechanisms, but engine support is not universal. Unsupported required entailment should be treated according to the specification and engine's failure reporting, not silently ignored.

## Handle deactivation and coverage

`sh:deactivated true` disables validation by the shape under the standard's rules. A deactivated referenced shape can therefore change nested conformance outcomes; it is more than hiding a message. SHACL-SPARQL constraints also have defined deactivation support. Record intentional deactivation in the contract and inspect inherited/reused shapes before relying on a result.

Validate shapes themselves when generation or complex edits introduce a risk of malformed parameters. Metavalidation does not prove that the shapes express the correct domain requirement. Check target counts or independent record IDs separately, especially when class targets depend on a type field that may be missing.

For reproducibility, record data/shape versions, graph selection, imports, validator version, feature flags, inference settings, target coverage, result limits, and report. The [SHACL Recommendation](https://www.w3.org/TR/shacl/) defines reports and failures; implementation documentation defines concrete CLI/API behavior.
