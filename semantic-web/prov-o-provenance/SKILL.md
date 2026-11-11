---
name: prov-o-provenance
description: "Use when modeling, recording or querying provenance with W3C PROV and PROV-O — entities, activities, agents, wasDerivedFrom, wasAttributedTo, qualified relations, revisions, bundles, provenance of provenance."
---

# PROV and PROV-O

## Frame the provenance question

Use PROV to describe how something came about: which inputs were used, which process produced an output, who was responsible, and how different versions or descriptions relate. Begin with a concrete question, such as “Which source revision produced this chart?” or “Which organization was responsible for this processing step?” Choose the granularity needed to answer it.

Distinguish the PROV conceptual model from its encodings. PROV-DM defines the model; PROV-O expresses it in RDF/OWL; PROV-N provides a compact notation; PROV-XML supports XML interchange. The PROV Constraints Recommendation defines consistency conditions beyond ordinary RDF syntax or the assertions an OWL reasoner happens to check. Use the selected representation without requiring any particular store, framework, or sibling skill.

Treat provenance as recorded assertions about a history. A valid graph does not prove that the history happened, that a source is reliable, or that an extracted claim is true. Explain who supplied the provenance and what evidence supports it.

## Navigate directly

| Need | Read |
| --- | --- |
| Understand the core concepts and select relation direction | [Model and relations](references/model-and-relations.md) |
| Add role, time, plan, or derivation details correctly | [Qualified influence](references/qualified-influence.md) |
| Model revisions, alternate descriptions, collections, or bundles | [Identity, versions, and bundles](references/identity-versions-and-bundles.md) |
| Capture, serialize, publish, or query provenance | [Capture and exchange](references/capture-exchange-and-query.md) |
| Check constraints and separate trust from consistency | [Validation and trust](references/validation-and-trust.md) |
| Verify authority, normative status, or extensions | [Sources and limits](references/sources.md) |

## Build a model in six steps

1. **Identify the things and their scope.** Assign entity identifiers to relevant inputs and outputs, including the specific versions or states required for replay. Explain which aspects of each entity are fixed. Separate an artifact from a process execution and from the software or person responsible for that execution.
2. **Identify observed activities and agents.** Record actual processing runs, their inputs, outputs, times when known, and responsible agents. Avoid inventing a named activity merely because a derivation must have involved some process. Keep unknown information unknown.
3. **Add the simplest accurate relations.** Use activity-to-input `prov:used`, output-to-activity `prov:wasGeneratedBy`, and derived-entity-to-source `prov:wasDerivedFrom`. Use entity attribution and activity association for the corresponding responsibility claims. Assert derivation only when supported; sharing an activity does not establish that every output depends on every input.
4. **Qualify only when details matter.** Give a usage, association, generation, or other influence its own node when it needs a role, time, plan, or other metadata. Keep the qualified relation's direction and influencer property correct. Emit compatible simple relations where consumers need them.
5. **Record versioning and provenance provenance.** Distinguish a new entity version from a new description of the same entity. Use specialization for a more specific view of the same thing, revision for a derived revised version, and bundles for named sets of provenance descriptions. Document the graph-to-bundle convention used in an RDF dataset.
6. **Validate at the requested level.** Parse the serialization, check the application profile, inspect PROV constraints and supported inferences, then review whether the recorded relationships match the evidence. Report these outcomes separately.

## Apply the important boundaries

Do not interpret `prov:wasAttributedTo` as a license grant or legal ownership determination. Do not convert association into authorship of every output. Use qualified delegation to record acting on behalf of another agent in a particular activity; do not infer delegation from employment alone.

Keep generation, usage, invalidation, activity start/end, retrieval time, publication time, and the date a provenance record was written distinct. Invalidation describes the end of an entity's availability in the modeled history; retiring a search result or correcting an annotation is not automatically the invalidation of the underlying artifact.

Do not treat `prov:specializationOf` or `prov:alternateOf` as `owl:sameAs`. Do not assume derivation is transitive merely because a path exists. State whether a query returns directly asserted derivation, reachability, or results from a declared inference regime.

Check property domains before adding qualifiers. For example, `prov:hadRole` is intended for associations and instantaneous events, not as a universal role property on every qualified influence. Use a documented extension where necessary instead of accidentally inferring the wrong PROV type.

## Deliver evidence with the model

For explanations, provide a small synthetic example and translate each important edge into plain language. For implementation, deliver the model decisions, sample serialization, capture points, query assumptions, and observed validation results. Preserve original source evidence and distinguish captured observations from inferred relations and later assessments. State any unavailable source versions, incomplete instrumentation, unsupported constraints, and limits on replay without claiming that completeness or trust follows from standards conformance.
