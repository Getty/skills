---
name: fibo-integration
description: "Use when applying FIBO, the Financial Industry Business Ontology — financial concept definitions, modules and IRIs, OWL imports and releases, legal entities, instruments, listings, mappings, extensions."
---

# FIBO Integration

## Establish the purpose

Treat FIBO as a formal vocabulary of financial business concepts and relationships. Use it to clarify meaning, compare definitions, align data models, or express knowledge with shared semantics. Distinguish the ontology from operational records: knowing the definition of an issuer does not establish who issued a particular bond. FIBO is developed in OWL and published by the EDM Council; particular domain specifications also have OMG publication histories. Check which distribution the task names before treating them as interchangeable. See [the FIBO overview](https://spec.edmcouncil.org/fibo) and [sources](references/sources.md).

Keep the skill independent of implementation language, storage engine, institution, and other personal skills. A glossary exercise may need only definitions; an executable ontology integration needs an import closure, instance model, validation policy, and reproducible version selection.

## Navigate the references

- Read [foundations and scope](references/foundations.md) to explain what FIBO provides, select domains, and distinguish its semantic role from data exchange and reporting standards.
- Read [terms and modeling patterns](references/terms-and-modeling.md) before modeling entities, parties, issuer roles, instruments, identifiers, or listings. Use its IRIs as examples, then inspect the chosen release.
- Read [releases and imports](references/releases-and-imports.md) when downloading, loading, pinning, upgrading, or troubleshooting FIBO and external dependencies.
- Read [mapping and extensions](references/mapping-and-extensions.md) to translate a source model, assess equivalence, or design an application vocabulary.
- Read [validation and examples](references/validation-and-examples.md) for an original Turtle fragment, competency questions, reasoning boundaries, and acceptance criteria.
- Read [primary sources](references/sources.md) for authority, version caveats, and last-checked information.

## Follow the working sequence

1. **State the question.** Establish whether the user wants an explanation, concept lookup, mapping, executable ontology, or migration. Write two or three concrete questions the result must answer. Identify relevant jurisdictions, dates, instrument categories, and granularity only where they change meaning.
2. **Choose an evidence baseline.** Identify the EDM release or OMG specification and its date. Inspect the ontology documents and their imports. Record whether each needed module is released, provisional, or otherwise marked. Use a moving development branch for investigation only when that is appropriate; disclose its status.
3. **Resolve concepts by meaning.** Search labels, synonyms, definitions, annotations, and class restrictions. Record the full term IRI and defining ontology. Read inherited axioms and referenced properties. Do not construct a plausible IRI from an English noun or assume a familiar term still lives in an older FIBO module.
4. **Separate the modeled objects.** Distinguish a legal entity from a role it plays, a security from its identifier, a listing from a trading venue, and a contract from a document describing it. Express time-dependent claims with their context instead of overwriting durable identity.
5. **Choose the degree of adoption.** Use a documented semantic crosswalk for terminology alignment, an application ontology for formal integration, or direct instance typing where the source evidence supports it. Preserve the original data and the mapping rationale.
6. **Validate the intended meaning.** Check RDF syntax, imports, logical consistency, and sample query results. Apply explicit data completeness rules separately. Test ambiguous and negative cases, not merely one example that works.
7. **Explain the outcome.** Provide definitions, exact identifiers, evidence, assumptions, mapping strength, and unresolved distinctions. For implementation work, include the version manifest and a small example. For a conceptual question, avoid unnecessary deployment instructions.

## Apply decision rules

Prefer the smallest coherent set of imported ontologies that supports the task, with its required dependencies. Do not cut out selected axioms and call the result an unchanged FIBO module. Preserve upstream namespaces and place local additions in a separate namespace.

Treat `owl:equivalentClass`, `owl:equivalentProperty`, and `owl:sameAs` as strong logical commitments. Use weaker documented mappings when definitions overlap without matching. Resolve contradictions by revisiting evidence and meaning; do not silently remove inconvenient axioms.

Check version-sensitive claims against current primary sources. Stable concept explanations may reuse this material, but exact term locations, deprecations, import paths, and release status require verification for the selected baseline. Report a missing or ambiguous concept honestly and propose an explicitly local extension if needed.
