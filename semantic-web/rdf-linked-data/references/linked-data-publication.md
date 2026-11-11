# Publishing and consuming Linked Data

## Design durable identifiers

Choose an IRI policy before publishing substantial data. Separate a resource identifier from an editable label and from an internal database location. A stable path such as `https://data.example.org/id/site/17` can survive changes to the site's name, storage engine, and web presentation.

Decide what each identifier denotes: a physical object, organization, observation, conceptual work, downloadable dataset, or document describing one of those things. Avoid letting one IRI alternately mean an object and a particular web-page response when their metadata differs. A description can have an author and modification time that the described object does not.

Use fragment identifiers or appropriately configured redirects/content negotiation where suitable. These are publication design options, not requirements for every RDF dataset. Keep the design explainable to consumers and test it with actual HTTP requests.

## Return useful descriptions

Offer a human-readable page and one or more RDF representations when the audience benefits. Negotiate using the HTTP `Accept` header, return an accurate `Content-Type`, and set `Vary: Accept` when representations differ by that header. Use cache controls and validators that reflect the publication update policy.

A dereferenced description should contain enough context to identify the resource and follow meaningful relationships. Include labels, types, relevant links, vocabulary documentation, and licensing where appropriate. Do not assume the consumer will fetch every linked IRI; provide essential context in the intended retrieval unit.

Publish dataset metadata that distinguishes dataset identity, distributions, release versions, and access endpoints. A dataset landing page, a SPARQL endpoint, and a downloadable N-Quads file are different resources. Describe provenance, temporal coverage, update cadence, and known limitations explicitly rather than embedding these meanings only in a graph name.

## Link carefully

Prefer links with a known semantic strength. A related webpage, a concept mapping, a matching identifier, and individual identity are not interchangeable. `rdfs:seeAlso` suggests another information resource; it does not entail identity. `owl:sameAs` is a strong identity assertion and can propagate all properties under an equality-aware reasoner.

For uncertain matches, publish the matching claim, evidence, method, and confidence using a suitable model instead of silently merging resources. Keep original identifiers available so consumers can reverse or revise the resolution decision.

Use explicit source and release metadata when importing data from several publishers. Two graphs agreeing on an IRI does not establish that either source is accurate, current, or authorized to make the claim. RDF provides a representation framework; trust is an additional application policy.

## Plan change and retirement

Distinguish mutable “current” URLs from immutable release URLs. Preserve historical identifiers and document replacements. If an entity splits, merges, or changes classification, decide whether the resource identity remains the same; do not derive that answer from a changed label alone.

Keep old vocabulary terms dereferenceable with deprecation guidance when possible. Test linked-data publication after deployment: the resource IRI, redirect chain, negotiated RDF document, base IRI resolution, and external links should agree. A valid Turtle file on disk does not prove a functional publication.

## Consume within an explicit retrieval policy

Treat RDF documents as data. Limit remote fetch size, redirects, recursion, and timeouts where dereferencing is part of the workflow. Do not let arbitrary data terms become unrestricted network requests. Check XML external-entity behavior for RDF/XML and remote-context loading for JSON-LD. Cache versioned dependencies when reproducibility matters.

Use the W3C [Linked Data Platform](https://www.w3.org/TR/ldp/) only when its HTTP interaction model is actually required; publishing RDF does not automatically make a service LDP-conformant. Read [Cool URIs for the Semantic Web](https://www.w3.org/TR/cooluris/) as a publication design Note, and [Data on the Web Best Practices](https://www.w3.org/TR/dwbp/) for wider lifecycle guidance.
