# Identity, versions, collections, and bundles

## Describe fixed aspects and versions

Define what an entity identifier fixes: exact bytes, a logical record revision, a particular observed state, or some other bounded view. Keep the observed revision identifier separate from a local content hash and retrieval timestamp. A content hash identifies content under a chosen algorithm; it does not establish when or by whom the content was produced.

Mint a new entity for a materially different version within the chosen identity contract. Record a known revision relationship with `prov:wasRevisionOf`. Re-fetching identical bytes can create a new retrieval activity without creating a new source content version. A new provenance observation can likewise be a new description of an existing entity.

Use `prov:specializationOf` when one entity gives more specific aspects of the same thing described by another. A dated document state can specialize a more general document entity if the shared-aspects interpretation is defensible. A revision relationship describes derivation between versions; specialization describes their relationship to a more general entity. They can be useful together but are not interchangeable.

## Use alternate descriptions carefully

`prov:alternateOf` relates entities presenting aspects of the same thing. Neither alternate nor specialization means unrestricted OWL identity. A PDF rendition and a text rendition may be modeled as alternate views if their intended “same thing” is defined, while their distinct byte-level identities and generation histories remain intact.

Under PROV Constraints, alternate is reflexive, symmetric, and transitive, while specialization is transitive and irreflexive; specialization implies alternate. Do not assume every generic OWL processor implements all PROV Constraints inferences. Declare the inference regime before expecting these results from queries or validation.

Do not use alternate as a weak record-linkage candidate relation. Once accepted as part of a model, it has stronger consequences than “possibly related.” Keep uncertain identity assessments separately, including evidence, method, and review state. A document discussing a person is not an alternate of that person.

## Represent collections without assuming completeness

Use `prov:Collection` and `prov:hadMember` for an entity containing other entities. Give a versioned collection its own identity when membership changes under a fixed membership interpretation. Ordinary membership assertions do not prove that all members have been listed. Declare completeness in an application profile or manifest when required.

Use PROV-Dictionary for keyed collections when keys, insertion, and removal histories matter. Do not describe a general map implementation as standardized PROV-Dictionary merely because it has key/value fields; verify the extension's terms and mapping. Distinguish a member's production history from the history of assembling the collection.

## Capture provenance of provenance

A `prov:Bundle` is a named set of provenance descriptions and is itself an entity. It can have a generation activity, attribution, and derivation from other bundles. Distinguish the time of the described activity from the later time when an observer produced a provenance record.

An RDF named graph is a possible representation convention, not an automatic PROV bundle interpretation. Declare that convention and how bundle identity relates to graph content. Adding or removing a statement changes the described bundle. Avoid merging providers' graphs into one unqualified union if disagreement or attribution must remain visible.

Synthetic TriG illustrating an explicitly chosen graph-to-bundle convention:

```trig
@prefix ex: <https://example.org/prov/> .
@prefix prov: <http://www.w3.org/ns/prov#> .

ex:record1 {
    ex:result a prov:Entity ; prov:wasGeneratedBy ex:run .
    ex:run a prov:Activity .
}
ex:record1 a prov:Bundle ; prov:wasAttributedTo ex:observer .
ex:observer a prov:Agent .
```

The observer is responsible for the provenance description. That attribution does not automatically assign the observer responsibility for producing the result.

Consult [PROV-DM bundles and alternates](https://www.w3.org/TR/prov-dm/), [PROV-Constraints](https://www.w3.org/TR/prov-constraints/), [PROV-Dictionary](https://www.w3.org/TR/prov-dictionary/), and [PROV-Links](https://www.w3.org/TR/prov-links/) for their different scopes. PROV-Links is a Working Group Note, not a requirement for ordinary bundle use.
