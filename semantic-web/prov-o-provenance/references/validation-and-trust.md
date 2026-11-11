# Validation, temporal reasoning, and trust

## Separate four questions

1. Can the serialization be parsed?
2. Does the graph meet the application's completeness and type requirements?
3. Does the represented history satisfy the selected PROV constraints and inferences?
4. Is there evidence that the recorded history and its substantive claims are authentic or reliable?

A positive answer to an earlier question does not establish a later one. PROV-O is an OWL ontology; a generic RDF parser or OWL consistency check is not a complete implementation of PROV Constraints. Conversely, a local shape requiring timestamps on every activity may be useful without being a universal PROV requirement.

## Check temporal structure without inventing clocks

PROV Constraints reasons about ordering between instantaneous events, including generation, usage, invalidation, start, and end. Some relations impose precedence and others strict precedence. Full checking involves relevant inferences, normalization/unification, typing, uniqueness, and ordering rules, not just comparing timestamp strings.

The specification explicitly separates event order from observed time values: timestamps do not determine the formal event-order constraints, and event order does not automatically infer timestamp order. An application may flag apparently inconsistent timestamps as additional diagnostics. Normalize offsets and document clock assumptions for those diagnostics. Do not describe a simple `start <= use <= end` timestamp test as the entire normative PROV validity algorithm.

Inspect likely capture errors: input usage preceding its availability, a generated entity associated with contradictory generation descriptions, an activity confused with its artifact, and cycles involving strict ordering. Distinguish an incomplete record from a demonstrably inconsistent one. Missing time does not necessarily invalidate a history.

## Validate structure and identity

Check that simple and qualified relations identify the same endpoints; usage nodes cite entities, generation nodes cite activities, and associations cite agents. Check that derivation references point to the intended usage and generation. Keep identifiers for objects distinct from identifiers for relations when applying PROV Constraints.

Avoid a blanket “every node has exactly one PROV class” rule. Some type combinations are allowed, including an agent also being an entity. Check actual disjointness and the application's stated profile. Watch for implicit typing caused by misplaced properties, especially role and time predicates on the wrong influence class.

Test a replay, two observations of one run, a retry producing a distinct output, a revision, and a bundle supplied by a different observer. Verify that a provenance correction does not silently rewrite the artifact identity or erase the original observer's account.

## Model assessments explicitly

Separate at least three notions: source reliability, extraction or measurement quality, and confidence in a downstream interpretation. PROV has no general built-in probability-of-truth or trust-score predicate. If an assessment is needed, define an assessment entity with a target, scale, method, assessor, version, and supporting evidence. Record its production provenance independently.

Do not interpret `prov:hadPrimarySource` as “verified source,” attribution as proof of authorship, or a complete-looking history as authentication. A source can issue incorrect provenance. Cryptographic signatures, attestations, and access-control evidence address different questions and need their own mechanisms and threat model.

When representing a claim extracted from a report, identify the claim record and source span as entities. Provenance can show that an extractor produced the record from that report. It cannot turn the report's assertion into an accepted world fact. Preserve modality, attribution, negation, and competing accounts in the claim model rather than squeezing them into provenance predicates.

## Report verification honestly

State the parser, data profile, inference regime, and constraint checker actually used. A useful result says which examples passed, which constraints were not exercised, and whether the source history was independently corroborated. Keep operational completeness requirements and evidence assessments labeled as application choices.

Use [PROV Constraints](https://www.w3.org/TR/prov-constraints/) for normative consistency rules and [PROV Overview](https://www.w3.org/TR/prov-overview/) to distinguish the family members. This guide does not claim that ordinary RDF validation proves authenticity, authorization, accuracy, or legal responsibility.
