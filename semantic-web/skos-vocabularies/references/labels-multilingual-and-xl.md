# Labels, multilingual data, and SKOS-XL

## Choose the right lexical property

Use `skos:prefLabel` for the preferred display term in a language, `skos:altLabel` for acceptable alternatives, and `skos:hiddenLabel` for lookup terms normally hidden from display, such as known misspellings. These properties label a resource; their use does not by itself force the resource to be a SKOS concept.

Keep at most one distinct preferred label per language tag for a resource. The same literal cannot occupy two of the preferred, alternative, and hidden properties on that resource: the properties are pairwise disjoint. Duplicate RDF triples are not separate values. Two different concepts can share a preferred label; deciding whether that ambiguity is acceptable belongs to the application profile.

Preserve language tags and script or region distinctions. `en`, `en-GB`, and `en-US` are distinct tags, although tag comparison is case-insensitive. Do not invent tags to encode a notation system, a translation's approval state, or a font. Follow BCP 47 for language identification and put workflow metadata elsewhere. Define a documented display fallback, such as exact requested tag, suitable broader language, then an explicitly chosen fallback language. Report fallback use instead of relabeling the source language.

## Keep normalization reversible

Retain original lexical values before Unicode normalization, whitespace cleanup, transliteration, or case folding. Choose normalization rules for search indexes separately from published labels. A useful search key does not become the authoritative label. For example, accent removal can improve some searches while destroying distinctions useful in names or other languages.

Translate concepts from their definitions and scope, not isolated strings. Ask a reviewer whether the proposed translation has a broader or narrower meaning. If the meanings diverge, create distinct concepts or a reviewed mapping instead of pretending they are translations of one concept. Record translation status and source outside SKOS's basic lexical predicates when the workflow requires them.

## Notation and documentation

Use `skos:notation` for a code, preferably with a datatype identifying the notation system where that distinction matters. Preserve leading zeros, punctuation, and alphabetic prefixes. A code can change independently from a label, and the same code may occur in different systems. Enforce uniqueness only within a documented scope.

Choose notes by purpose: `skos:definition` explains meaning; `skos:scopeNote` guides inclusion and exclusion; `skos:example` illustrates usage; `skos:editorialNote` supports editors; `skos:historyNote` describes historical context; `skos:changeNote` records a change. SKOS permits flexible note representations. A publication profile can prefer language-tagged literals or structured note resources with author and date, but should not call that preference a universal requirement.

## Give labels identity when necessary

SKOS-XL uses `skosxl:Label` resources connected through `skosxl:prefLabel`, `skosxl:altLabel`, or `skosxl:hiddenLabel`. Each label resource has exactly one `skosxl:literalForm`. Use separate label resources for different language-tagged forms. This allows attaching provenance, editorial status, or label-to-label relationships without treating a string as a concept.

Synthetic Turtle example:

```turtle
@prefix ex: <https://example.org/vocab/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix skosxl: <http://www.w3.org/2008/05/skos-xl#> .

ex:rail a skos:Concept ;
    skosxl:prefLabel ex:railLabelEn ;
    skos:prefLabel "Rail transport"@en .
ex:railLabelEn a skosxl:Label ;
    skosxl:literalForm "Rail transport"@en .
```

The simple preferred label follows from the XL relation and literal form under the SKOS-XL property-chain semantics; publishing it explicitly helps consumers without that reasoning support. Keep explicit and derived forms synchronized. Two XL resources with the same literal form are not automatically the same label resource. Conversely, adding multiple preferred XL labels with different forms in the same language can violate the simple-label integrity rule after entailment.

Consult the [SKOS lexical-label rules](https://www.w3.org/TR/skos-reference/#labels), [SKOS-XL appendix](https://www.w3.org/TR/skos-reference/#xl), and [BCP 47 specification](https://www.rfc-editor.org/rfc/rfc5646) when resolving exact language or cardinality questions.
