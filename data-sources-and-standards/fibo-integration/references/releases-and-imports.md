# Releases, imports, and maintenance

## Establish the baseline

Distinguish an EDM publication, an OMG adopted specification, a repository tag or commit, and a moving branch. They can contain related content with different histories. The [OMG Business Entities 1.1 page](https://www.omg.org/spec/EDMC-FIBO/BE/1.1/About-BE) identifies a particular specification and machine-readable documents; it should not be labeled the complete current EDM distribution.

Record these fields before an executable integration:

- Publisher, distribution, release identifier, retrieval date, and license location.
- Entry-point ontology IRIs and physical document locations.
- Version IRIs, repository commit or artifact checksum where available.
- Required external ontologies and their resolved versions.
- Reasoner, parser, and validation profile used for acceptance.

FIBO `master` is a moving development branch, not a baseline to track automatically. Prefer an appropriate published release for reproducible use and recheck the official distribution.

## Resolve the whole import closure

An ontology IRI identifies the ontology; a retrieval URL locates a serialization. A class IRI identifies a term. These need not be interchangeable strings. `owl:imports` brings imported ontology semantics into consideration; merely including a prefix declaration does not load definitions. See the [OWL 2 structural specification](https://www.w3.org/TR/owl2-syntax/).

Follow imports recursively and report every failure. Use the supplied [XML catalog](https://github.com/edmcouncil/fibo/blob/master/catalog-v001.xml) or equivalent controlled resolution mechanism to map logical ontology IRIs to local documents. Preserve canonical IRIs even when files are mirrored. Resolve external dependencies, including OMG Commons, as part of the same manifest.

Do not combine a new module with an arbitrary old dependency because filenames match. Do not assume a browser's successful HTML response is an RDF serialization. Check content type, parser success, ontology identity, and expected term counts. A friendly ontology viewer is useful for exploration but can hide missing imports in an executable toolchain.

## Build a stable local working set

Choose the needed entry points, fetch their closure, and retain an immutable copy or reproducible retrieval manifest. Run a load with network resolution disabled to establish that the selected package is complete. Report intentional exclusions. If a dependency cannot be obtained, describe the semantic limitation rather than silently continuing as though the ontology were complete.

Keep upstream files unchanged. Put extensions, mapping axioms, and data in separate artifacts. Preserve upstream notices when redistributing ontology material and inspect licenses for external dependencies separately. The checked FIBO source carries an MIT license notice; that does not determine the license of every referenced dataset.

## Assess an upgrade semantically

Compare more than filenames and labels. Inspect added or removed terms, deprecations, changed definitions, subclass changes, property domains and ranges, restrictions, and imports. A stable term IRI can acquire changed axioms; a changed IRI can represent a deliberate replacement.

Run existing competency queries and examine changed entailments. Revalidate instance data and local extensions. Update generated documentation and mappings only after reviewing these effects. Keep a migration table with old term, new term, reason, compatibility assessment, and required data change. A replacement annotation is useful evidence, not an automatic guarantee of exact equivalence.

## Troubleshoot by layer

A missing class can be a retrieval problem, an omitted import, a changed namespace, a deprecated term, or a mistaken expectation. A reasoning failure can be caused by incompatible versions, an unsupported construct, or inconsistent data. Identify the failing layer before editing the vocabulary. Preserve a small reproducer and the exact dependency manifest so that a correction can be checked against the same baseline.
