# Remote loading, reproducibility, and integrity

## Treat context retrieval as part of interpretation

A remote context can change a compact property's IRI, datatype, or link interpretation without changing the surrounding JSON. Record which context bytes were used. For durable contracts, prefer versioned context URLs or an application-controlled loader with a verified local copy.

A document loader may retrieve both JSON-LD documents and contexts, follow redirects, interpret content types and HTTP link headers, and cache results. Its behavior is part of the processing environment. A context URL reachable in a browser is not evidence that every production processor will resolve it identically.

Set a loader policy appropriate to the task: permitted schemes and hosts, redirects, private-network access, response sizes, nesting depth, number of remote contexts, timeouts, and cache lifetime. These controls matter when inputs are untrusted or processing must be reproducible. They need not obstruct a simple offline educational example.

## Pin dependencies without changing meaning

For an offline or reproducible pipeline, map approved context URLs to exact local bytes while retaining the intended document URL and base-resolution behavior. Do not replace every remote URL with a file URL if that changes relative references. Record context digests and processor options with the resulting dataset.

Context caching is a correctness choice as well as a performance choice. A mutable context can cause the same business JSON to expand differently at different times. Conversely, a stale cache can miss an intended contract update. Use explicit versioning and deployment rules rather than relying on incidental cache expiration.

`@protected` protects selected term definitions within context-processing rules. It does not authenticate the remote publisher, pin retrieved bytes, block all malicious context behavior, or replace an authorization policy. Handle processor errors as errors; do not silently fall back to interpreting rejected JSON-LD as ordinary JSON with guessed semantics.

## Distinguish canonicalization from formatting

Pretty-printing JSON, sorting object keys, expansion, compaction, flattening, and framing are not RDF dataset canonicalization. Blank-node identifiers and alternative graph layouts are central reasons raw serialization hashes are unstable.

RDFC-1.0, defined by the RDF Dataset Canonicalization Recommendation, provides a specific canonicalization procedure for supported RDF datasets. It does not validate the truth of statements or infer that different IRIs denote the same entity. A canonicalization algorithm also has resource-consumption considerations for difficult blank-node structures.

Specify the algorithm/version, RDF conversion options, selected graph set, and digest/signature suite together. If a deployed protocol names another normalization algorithm or fixed legacy identifier, follow that protocol and check compatibility; do not silently substitute RDFC-1.0 because both procedures sound like normalization.

## Keep signatures in their protocol

A valid signature establishes a cryptographic relationship to the signed material under a particular verification procedure. It does not by itself establish that a signer was authorized to make a claim or that remote dependencies were interpreted as intended. Inspect the protocol's treatment of contexts, proof fields, canonicalization, identifiers, and key resolution.

Do not offer a hand-rolled “sort JSON and sign” recipe as interchangeable with a standardized linked-data security suite. For a requested implementation, use the specified suite and verified library behavior, then exercise a context-change and a data-change case to confirm what is covered.

Primary references: [JSON-LD 1.1 API](https://www.w3.org/TR/json-ld11-api/), including remote document loading and security considerations; [RDF Dataset Canonicalization](https://www.w3.org/TR/rdf-canon/), Recommendation of 21 May 2024. Consult the applicable cryptographic protocol separately rather than treating JSON-LD as a signature specification.
