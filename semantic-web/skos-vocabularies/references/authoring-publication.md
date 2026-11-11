# Authoring, migration, and publication

## Design a conversion contract

Begin with a representative sample that includes a polyhierarchy, ambiguous label, multilingual term, retired concept, and external mapping. Document how source columns or fields become RDF statements. Keep source row identifiers even when concepts receive new IRIs. If several rows represent labels for one concept, explain the grouping rule and retain enough information to reverse an incorrect merge.

Record the source's implicit conventions. An indented heading may mean a broader subject, an array grouping, or a formatting artifact. A code prefix may reflect hierarchy, but do not infer parent links from prefixes without confirmation. “See” and “see also” may represent preferred-term redirects, associative links, or instructions for compound indexing. Preserve unresolved cases for editorial review.

Map names, codes, definitions, status, relations, and ordering separately. Treat a one-column keyword list as a starting vocabulary, not proof that every entry has a clear concept definition. For legacy classification schedules, check ranges, synthesized codes, and instructions that cannot be represented by a simple concept tree. State what the SKOS export captures and what remains in accompanying documentation.

## Establish sustainable identity

Choose a controlled namespace and avoid changing IRIs with labels, spelling, or parent placement. Define how new identifiers are allocated, who can retire terms, and how collisions are resolved. Retain persistent old identifiers after merges or splits; a vanished URI prevents consumers from interpreting historical records.

For a split, record the successor candidates and the circumstances under which each should be selected. A split does not warrant several exact-match links from the old concept to narrower new concepts. For a merge, preserve previous meanings and avoid assuming that the merged concept is interchangeable with each predecessor in all contexts. Use explicit local change metadata where SKOS lacks the necessary relationship.

Separate replacement guidance from logical identity. An HTTP redirect helps access a resource but is not by itself an adequate conceptual migration record. If a concept's meaning changes materially, prefer a new identity and document the transition rather than silently rewriting historical semantics.

## Govern labels and alignment

Define editorial ownership, supported languages, review states, and acceptance criteria. A small workflow can be sufficient: proposed, reviewed, published, retired. Keep workflow state out of language tags and source labels. Ensure that translation approval does not accidentally authorize a new concept or mapping.

Review external alignment as its own artifact. For each accepted link, record the source releases and an example retrieval task. Ask whether replacing one concept with the other loses or adds relevant documents. Include a negative example to reveal excessive exact matching. When the external vocabulary changes, recheck affected mappings rather than regenerating them solely from similar labels.

## Publish and preserve releases

Provide at least a documented RDF serialization, a human-readable view, a release identifier or date, vocabulary provenance, and explicit licensing information. Keep the vocabulary's license distinct from the rights of documents classified with it. Choose stable concept landing pages and, where feasible, content negotiation or clearly linked machine-readable representations. Follow the [W3C vocabulary-publication guidance](https://www.w3.org/TR/swbp-vocab-pub/) while adapting deployment details to the actual hosting platform.

Pin each downloadable release with a checksum and state its scope. A manifest can enumerate concepts, files, imported schemes, and validation-profile versions. Do not imply that RDF graph membership and scheme membership mean the same thing. Preserve older releases when reproducibility or historical indexing matters.

Test a release with a real consumer: load a concept by identifier, display a requested language, traverse direct parents, expand ancestors, and resolve a mapping. Compare results before and after a change. Report deliberate compatibility changes and migration steps, especially when codes or mappings change. These release practices are recommended operational choices; SKOS does not prescribe a package format or update protocol.
