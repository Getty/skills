# Taxonomies, DTS discovery, and dimensions

## Resolve concepts through the DTS

A discoverable taxonomy set (DTS) includes the schemas and linkbases reached through the defined discovery mechanisms. Identify the report's entry points and follow imports, references, and extension relationships. A taxonomy name without an entry point and version is not enough for reproducible interpretation. See [XBRL 2.1](https://specifications.xbrl.org/work-product-index-group-base-spec-base-spec.html).

Use expanded concept names, not prefixes or display labels. Two reports can use different prefixes for the same namespace. Conversely, identical local names in different namespaces can denote different concepts. Retain definitions, references, datatype, period type, balance where applicable, and abstraction status when assessing a mapping.

Inspect effective relationships within their link roles and arcroles. Presentation relationships organize views; they do not automatically define arithmetic. Label relationships supply human-readable names, including different roles and languages. Reference relationships link concepts to supporting authoritative material. Calculation relationships express selected numerical relationships under specific rules. Definition networks support other semantics, including dimensional structures.

## Understand dimensions

XBRL Dimensions adds qualified reporting aspects. Explicit dimensions select taxonomy-defined members; typed dimensions supply values that conform to a declared typed domain. Hypercube relationships describe permitted combinations for relevant primary items. Defaults, inheritance, target roles, and usable members affect validation. Consult the [Dimensions Recommendation](https://www.xbrl.org/specification/dimensions/rec-2012-01-25/dimensions-rec-2006-09-18+corrected-errata-2012-01-25-clean.html).

Do not interpret every dimension as a simple spreadsheet column with an unconstrained list of labels. A member valid for one primary item or relationship network may be invalid elsewhere. A dimension can appear in different networks with different constraints. Closed-hypercube rules do not mean every dataset in the system is globally closed.

When a default member is defined for an explicit dimension, its omission from the instance can carry that default meaning; the default is not normally encoded by explicitly placing that member in the context. Do not replace omission with an “unknown” member without checking the DTS. For typed members, preserve the typed value and compare according to the applicable rules rather than raw XML whitespace alone.

## Keep reporting scope visible

For a fictional revenue table, a total for all operating segments is not automatically comparable to a fact for one named segment. A fact reported without a particular dimension can have a defined default interpretation. Another fact can use a different consolidation axis or typed identifier. Compare the complete dimensional meaning before combining them.

Avoid summing members unless the taxonomy and business semantics justify aggregation. Members may overlap, represent alternatives, or include an already consolidated total. “All dimension values shown in this table” is not proof of an exhaustive disjoint partition.

## Decide whether to extend

Search the accepted base taxonomy before creating a new concept. Compare definitions, references, data type, period type, balance, and dimensional usage. A different preferred label alone may not justify an extension. Conversely, a similar label is insufficient to justify using a materially different standard concept.

Where the filing profile permits or requires extensions, place new concepts in a controlled namespace and document their meaning. Add necessary relationships and labels. Apply required anchoring rules only within the relevant profile; anchoring is not a universal property of all XBRL taxonomies. Keep broader/narrower relationships distinct from exact equivalence.

## Package reproducibly

[Taxonomy Packages](https://specifications.xbrl.org/spec-group-index-taxonomy-packages.html) provide package metadata, entry points, and URL remapping. Preserve logical references while resolving local copies through the package mechanism. Do not rewrite namespaces merely to point to local files.

Pin package versions and checksums, record extension dependencies, and test offline resolution when reproducibility matters. A successful download of the main schema does not establish that every linkbase and imported taxonomy is present. Report unresolved dependencies before interpreting missing concepts or empty networks as actual absence.
