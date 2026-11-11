# Capture, exchange, and query

## Instrument meaningful boundaries

Choose a capture point where inputs, outputs, and responsible actors are known: a processing-job boundary, publication step, measurement session, or data import. Record a stable run identifier before execution, then attach observed inputs, outputs, and outcomes as they become available. Preserve failure and retry distinctions instead of making each successful retry overwrite the earlier execution history.

Keep required provenance small enough to collect reliably. For a reproducible transformation, useful fields include source revision or checksum, process identity, software/configuration version, parameters, output identity, and capture time. These are application requirements rather than universal PROV mandatory properties. Add environment information only when it affects interpretation or replay; do not claim that a full machine inventory guarantees reproducibility.

Distinguish directly observed facts from inferred dependencies and operator-supplied explanations. If a scheduler knows a job started but cannot see which files the job actually read, record the observed boundary and describe the limitation. Avoid turning intended inputs into asserted usages without evidence. Preserve original source artifacts or durable references whenever the task requires audit or reconstruction.

## Serialize with an explicit contract

Choose RDF/PROV-O when consumers need graph integration or SPARQL. Use PROV-N for concise human-oriented exchange and debugging, or PROV-XML for an XML contract. A generic JSON object called “provenance” is not automatically a standardized PROV serialization. Identify the chosen JSON mapping and its limits if JSON is required.

Pin namespace IRIs, serialization, schema or profile version, identifier policy, and handling of unknown extensions. Use absolute identifiers in published exports where local context would otherwise be lost. Keep blank nodes when their local identity is sufficient, but use stable relation identifiers when updates or external references need to address the same qualified influence again.

Preserve datatypes and timezone information on timestamps. A missing timestamp is not the same as an arbitrary epoch value. Record partial or approximate observations with a documented extension when `xsd:dateTime` would invent precision. Distinguish source clocks from the receiver's clock.

## Query direct relations and paths differently

Synthetic SPARQL for direct inputs to the generating activity:

```sparql
PREFIX prov: <http://www.w3.org/ns/prov#>
SELECT DISTINCT ?output ?run ?input
WHERE {
  ?output prov:wasGeneratedBy ?run .
  ?run prov:used ?input .
}
```

This finds inputs used by the output's generating activity. It does not prove each returned input directly determined that output. A different query for `prov:wasDerivedFrom+` returns reachability across available derivation edges, not newly asserted standard transitive derivation statements. State that distinction in explanations and exported fields.

For qualified-only graphs, either query the qualification structure or use an agreed entailment/materialization step. Include named-graph selection when provider provenance or bundle boundaries matter. A default-union graph can conceal disagreement, so inspect the dataset configuration before interpreting results.

## Publish and reconcile descriptions

PROV-AQ describes mechanisms for discovering provenance and relating a resource to provenance services. Use it when an interoperability requirement calls for discovery; it is not required for storing a small local PROV graph. Check current HTTP tooling and security requirements separately from the older Note's examples.

Treat corrections to provenance as versioned descriptions. Retain the source of each correction, what it supersedes, and the affected entities or activities. A corrected observation does not necessarily change the underlying artifact. When exporting a subset, retain identifiers for referenced dependencies or document that the export is incomplete rather than fabricating full descriptions.

Use [PROV-N](https://www.w3.org/TR/prov-n/), [PROV-XML](https://www.w3.org/TR/prov-xml/), [PROV-AQ](https://www.w3.org/TR/prov-aq/), and [SPARQL 1.1](https://www.w3.org/TR/sparql11-query/) for format and query contracts. The instrumentation and reconciliation process described here is adaptable implementation guidance.
