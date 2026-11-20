<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Interoperability

RUML baseline: release 1.0.0, specification commit `d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4`. External standards below are identified editions used for comparison; this reference does not assert that they are the latest editions.

## Contents

- [The boundary to preserve](#the-boundary-to-preserve)
- [Directional integration map](#directional-integration-map)
- [Akoma Ntoso and RUML Text](#akoma-ntoso-and-ruml-text)
- [LegalRuleML and DMN](#legalruleml-and-dmn)
- [RDF and OWL](#rdf-and-owl)
- [SHACL](#shacl)
- [PROV-O](#prov-o)
- [A conversion contract](#a-conversion-contract)
- [Sources](#sources)

## The boundary to preserve

RUML §1.5 does not define general formal mappings to adjacent legal-data standards. Do not claim that a RUML rulemap is automatically LegalRuleML, DMN, RDF, OWL, SHACL, or a PROV record. Its JSON syntax does not make it JSON-LD. [§1.5][relationship]

There is a specific, important qualification: §4.12 defines **RUML Text**, a JSON representation of Akoma Ntoso XML with conversion rules, namespaces, element identity and dialect validation. This is standardized text representation, not an automatic conversion of legal prose or arbitrary rule semantics into an executable rulemap. [§4.12][text-reference]

Keep four concerns distinguishable in any integration:

1. The source document and the exact version interpreted.
2. The rule definition and the interpretation choices used to construct it.
3. The case facts or other inputs to an evaluation.
4. The evaluation activity, results and effects.

The same subject can appear in more than one representation, but the representations need not have identical identity, semantics, or completeness. Links should state their purpose rather than imply equality by default.

## Directional integration map

The “integration” column is architectural advice unless explicitly labeled as RUML-defined.

| Standard and primary source | Its relevant concern | Directional integration | Main boundary |
| --- | --- | --- | --- |
| [LegalRuleML Core 1.0, OASIS Standard][legalruleml] | RuleML-based representation of legal norms, including defeasibility | Select and document a supported subset for translation into or out of RUML decisions | A Boolean node does not automatically preserve normative modality, priority or exceptions |
| [DMN 1.5, OMG][dmn] | Decision models, decision tables and FEEL expressions | Translate a defined decision fragment or call a separately implemented decision service | FEEL and JSONata semantics require an explicit translation contract |
| [Akoma Ntoso 1.0, OASIS][akn] | Structured legal documents in XML | RUML-defined text conversion and source anchors; interpreted rules are a separate artifact | Text conversion is not rule extraction |
| [RDF 1.1 Concepts, W3C][rdf] | Graphs of subject–predicate–object statements and datasets | Export rule metadata, ordered structure and results into an application vocabulary; import selected facts through adapters | RDF representation alone does not execute RUML |
| [OWL 2 Primer, second edition, W3C][owl] | Ontologies and logical entailment under open-world semantics | Define domain terms or enrich facts before a scoped RUML evaluation | Non-entailment does not mean the RUML condition is false |
| [SHACL Recommendation, W3C][shacl] | RDF graph validation against shapes | Validate a projected graph or inputs; retain native RUML validation | A conforming graph does not prove the source JSON or evaluator conforms |
| [PROV-O Recommendation, W3C][prov] | Provenance of entities, activities and agents | Describe source interpretation, conversion and evaluation outside or alongside RUML | Provenance records neither certify truth nor replace the result file |

These are complementary integration directions, not a ranking of expressiveness or suitability.

## Akoma Ntoso and RUML Text

**RUML-defined behavior:** an XML element becomes a JSON object with `type`, optional `attrs`, and optional `content`; character data is represented by strings, and children retain document order. Root `content` has `type`, `attrs`, and `content`, with the dialect as default `attrs.xmlns`. Adjacent strings merge. Preserve whitespace and elements/attributes from unfamiliar namespaces. [§4.12][text-reference]

The conversion omits the XML declaration, document type declaration, comments, processing instructions, and `xsi:schemaLocation`. It normalizes the dialect's element prefix to the default namespace. The specified roundtrip guarantee is qualified canonical equivalence with these exceptions, not byte-for-byte restoration of the original XML. Archive the original source separately when those original bytes matter. [§4.12 conversion][text-reference]

Converted content must validate against the named dialect when rendered as XML (`TXT-18`); a fragment must be valid in its original complete-document position. Passing `ruml.schema.json` does not perform that dialect validation. The RUML table identifies OASIS AKN 3.0 and LegalDocML.de 1.8.2 examples; do not silently use the schema of one dialect for another. [§4.12 dialects][text-reference]

RUML's element `GUID` and the dialect's `eId` serve different purposes. Every element with `eId` must have a lowercase UUID `GUID`; anchors use that GUID. Preserve matched element GUIDs across imported versions even when numbering and `eId` change (`TXT-03`, `TXT-16`). A new copied element gets a new identity. [§4.12 identity][text-reference]

Example anchor payload on a rule node, assuming the text and element already exist:

```json
{
  "id": "ruml:text-reference",
  "payload": {
    "refs": [{
      "id": "text_example_act",
      "element": "38abfd95-96c3-4dc6-98a8-a04a98206357",
      "type": "represents"
    }]
  }
}
```

`represents` asserts which norm the node implements; `refers-to` provides a reference without that assertion. At most one `represents` anchor is allowed on a node. An `element` must exist in that entry's structured `content`; anchors are not free-form character offsets or arbitrary XML IDs (`TXT-01`, `TXT-19`, `TXT-20`). [§4.12 anchors][text-reference]

**Integration advice:** version the extraction/interpretation step independently from the XML-to-JSON conversion. Tests should show that anchors still resolve after an amendment and that a changed legal condition triggers review of affected rules, not just successful text reimport.

## LegalRuleML and DMN

LegalRuleML extends RuleML with legal-norm features; its specification addresses defeasible rules and priority mechanisms. A general conversion must account for those semantics, not merely translate element names into `AND` and `OR`. [LegalRuleML §§4.1–4.2][legalruleml]

For a proposed LegalRuleML → RUML conversion, enumerate the accepted source constructs and the target interpretation. Reject or surface unsupported constructs explicitly. If a third-party capability supplies missing reasoning, declare its role and requiredness according to RUML and disclose the added runtime dependency. This is a custom integration, not an official mapping.

DMN provides business decision modeling and a standardized FEEL expression language. [OMG DMN overview][dmn-overview] [DMN 1.5 specification][dmn-pdf] For DMN ↔ RUML, define input/output types, missing-value behavior, ordering, decision-table match policy, numeric behavior, and how non-Boolean outputs become a Boolean condition or remain separate data.

Do not translate DMN `null`, multiple matching rows, or FEEL expressions by lexical substitution. Likewise, RUML `XOR` is not an “exactly one rule matched” test. Preserve the original DMN artifact and decision identifier, and use paired examples to demonstrate equivalence only for the claimed subset. [RUML §3.6][operators]

A remote DMN service can be wrapped by application adapters or a declared custom capability. That arrangement is architecturally possible, but RUML does not standardize a DMN endpoint, protocol, mapping, or service-capability ID.

## RDF and OWL

RDF represents information as graphs and datasets. [RDF 1.1 Concepts][rdf] A projection can make rule definitions, sources, and runs queryable together, but its vocabulary and reconstruction rules are application work. Do not add `@context` to a RUML root: the root is closed to fields outside the specification (`FMT-07`). Export a separate graph/document or use an allowed extension location. [Chapter 8][rules]

Recommended identity separation for a projection:

| RUML identity | Projection responsibility |
| --- | --- |
| `metadata.id` plus immutable artifact version | Identify the exact rulemap artifact; retain its digest |
| Node UUID `rulemap.nodes[lexId].id` | Identify the stable rule definition in the stated artifact context |
| LexID key | Retain the local key without treating it as a global entity identifier |
| Evaluation ID plus result path | Identify one evaluated node occurrence; preserve its LexID backlink |
| Text entry key plus element GUID | Identify the anchored source element in the applicable text version |

Preserve child and capability-entry order with explicit positions or another reversible ordered representation. Two incoming references to one modular definition are different occurrences during evaluation; collapsing their results onto one RDF subject can destroy evidence.

OWL's open-world assumption permits missing facts to remain unknown rather than false. [OWL 2 Primer §3][owl] Therefore an ontology entailment check must define which outcome supplies a RUML input: positive entailment, explicit negative evidence, inconsistency, and no conclusion are different cases. Never infer `false` merely because a reasoner did not entail a fact.

Use domain class/property IRIs to define what DataPoints mean if useful, while retaining explicit data extraction and validation. Neither an OWL restriction nor a node labeled with an ontology term automatically executes the legal test represented by that node.

## SHACL

SHACL validates an RDF data graph against a shapes graph and produces a validation report. Its `sh:conforms` is a statement about that validation, not a RUML node status. [SHACL §§3.4–3.6][shacl]

Suggested use: define graph shapes for the exported model, verify the projection, and keep findings traceable to original JSON Pointers. A missing graph edge may be a projection defect even if the source contains the correct `children` entry. Check the source artifact before “repairing” it.

If native chapter-8 constraints are reproduced as SHACL shapes, maintain a rule-to-shape coverage table and tests for both directions. Label checks requiring external files, expression parsing, or execution separately. Do not replace JSON syntax/order evidence with a graph that has already discarded it.

## PROV-O

PROV-O supplies `prov:Entity`, `prov:Activity`, and `prov:Agent`, together with relations for use, generation and derivation. [PROV-O §3.1][prov] A useful **application mapping proposal** is: source/version and RUML/result artifacts are entities; interpretation, conversion and evaluation are activities; accountable software or people are agents.

Illustrative external Turtle, not a RUML-defined serialization:

```turtle
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix ex: <https://example.invalid/audit/> .
ex:rulemap-v1 a prov:Entity .
ex:evaluation-42 a prov:Activity ;
  prov:used ex:rulemap-v1, ex:input-snapshot-42 ;
  prov:wasAssociatedWith ex:engine-build-7 .
ex:result-42 a prov:Entity ;
  prov:wasGeneratedBy ex:evaluation-42 .
```

Add evidence for source interpretation and provider observations when those distinctions matter. Keep the actual `.ruml-result`, its schema validation and artifact reference; the provenance graph links the records without replacing them. A relation such as `prov:wasDerivedFrom` records derivation, not legal endorsement.

## A conversion contract

For any requested integration, write the following before claiming interoperability:

1. **Direction and versions:** exact source/target editions, dialects, artifact and converter versions.
2. **Supported subset:** accepted constructs and semantics; explicit failure behavior for unsupported constructs.
3. **Identity policy:** document version, rule UUID, occurrence path, text GUID, and external identifiers kept distinct.
4. **Value policy:** datatypes, units, precision, time zones, missing/null/undefined handling, and ordering.
5. **Semantic obligations:** conditions under which outputs are equivalent; effects, recursion and unknown values included.
6. **Validation evidence:** native source validation, conversion checks, native target validation, and representative semantic comparisons.
7. **Loss and provenance:** omitted material, preserved originals, interpretation assumptions, and conversion findings.

A one-way metadata projection can be useful without being reversible. Say so. A reversible structure conversion still needs separate evidence for semantic preservation, and an executable result still needs separate review of the underlying legal interpretation.

## Sources

[relationship]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/01-introduction/1-5-relationship-to-other-standards.md
[text-reference]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-12-ruml-text-reference.md
[operators]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-6-operators.md
[rules]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/08-validation/index.md
[legalruleml]: https://docs.oasis-open.org/legalruleml/legalruleml-core-spec/v1.0/os/legalruleml-core-spec-v1.0-os.html
[dmn]: https://www.omg.org/spec/DMN/1.5/About-DMN
[dmn-overview]: https://www.omg.org/dmn/index.htm
[dmn-pdf]: https://www.omg.org/spec/DMN/1.5/PDF
[akn]: https://docs.oasis-open.org/legaldocml/akn-core/v1.0/akn-core-v1.0-part1-vocabulary.html
[rdf]: https://www.w3.org/TR/rdf11-concepts/
[owl]: https://www.w3.org/TR/owl2-primer/
[shacl]: https://www.w3.org/TR/shacl/
[prov]: https://www.w3.org/TR/prov-o/
