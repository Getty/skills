# Standards, scope, and version selection

## Select the standard for the information exchanged

| Standard or vocabulary | Main role | Boundary |
| --- | --- | --- |
| NewsML-G2 | XML news items, packages, concepts, planning, and management | Does not establish the truth of reported content |
| ninjs | JSON representation of news objects, renditions, associations, events, and planning where supported | Field structures vary by version family |
| NewsCodes | Controlled values for many editorial, administrative, and technical properties | Each scheme has its own meaning and maintenance |
| Media Topics | Subject taxonomy within NewsCodes | Subject classification is not entity identity |
| RightsML | Machine-readable media rights expressions based on ODRL | Requires applicable policies, targets, and interpretation |

Choose the simplest representation that preserves the required information and matches the receiving system. Do not convert an established feed solely to obtain a preferred serialization if conversion loses lifecycle, package, or rights details. For a new integration, inspect both systems' supported versions and profiles before selecting a contract.

## Separate approval, publication, and deployed support

An approval announcement can run ahead of the published files. The IPTC [Autumn Meeting 2026 report](https://iptc.org/news/autumn-meeting-2026-report/) announced NewsML-G2 2.36 and ninjs 3.3, 2.4 and 1.8 while the distribution index, release redirect and user guide still exposed 2.35 and 3.2, 2.3 and 1.7, and the expected new directory and schema URL returned 404.

Treat such a gap as a publication mismatch, not proof that the approved versions do not exist elsewhere. Open the official release resources and inspect the actual downloaded schema before using a newer version. The examples in this skill target NewsML-G2 2.35 and ninjs 3.2; they do not claim these are the newest approved standards.

Record standard version, schema file revision/checksum, provider profile, and item revision separately. A specification document can receive editorial revisions without changing the standard version. A provider can update an item without changing its format. A JSON Schema `$schema` identifies the schema language dialect, while the schema's `$id` identifies that particular schema resource.

## Define a conversion contract

Create a mapping table with source path, target path, meaning, multiplicity, language handling, and loss/extension policy. Resolve actual semantics rather than matching spelling. A title may be administrative metadata while a headline is intended for publication. A content URL is not necessarily the managed item identifier. A package relationship is not necessarily a textual reference.

Check representation-specific features: inline content, remote media, part-level metadata, composite items, repeated subjects, source roles, item links, catalog resolution, rights scope, and event/planning structures. If the target cannot represent a feature, keep a documented extension or a source sidecar and clearly mark the lossy projection. Do not claim arbitrary round-trip conversion from a successful example.

## Validate with the right tools

Pin schemas and their dependencies locally for repeatable validation. Configure an XML parser's entity/network behavior deliberately and follow XSD imports/includes. For ninjs, select a JSON Schema validator supporting the declared dialect; enable format assertions when required because many validators do not enforce URI/date formats by default.

Validate the concrete output after conversion, then apply semantic checks: identity/version preservation, rights and status propagation, subject resolution, package relationships, and body-language handling. A structurally valid minimal item may still be unsuitable for a provider's business workflow. Document those additional profile requirements rather than attributing them to the general standard.

Use the [NewsML-G2 overview](https://iptc.org/standards/newsml-g2/), [ninjs user guide](https://www.iptc.org/std/ninjs/userguide/), and [NewsCodes guidelines](https://www.iptc.org/std/NewsCodes/guidelines/) for orientation, then the exact versioned schemas and specification for implementation.
