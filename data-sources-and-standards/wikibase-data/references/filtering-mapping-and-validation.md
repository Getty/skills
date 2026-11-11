# Filtering, mapping, and verification

## Define what a subset means

Specify entity-type scope, repository, properties, languages, rank policy, time conditions, and whether reference/qualifier context is retained. Distinguish selecting entities from pruning their statements. An entity selected by one subject criterion may still contain unrelated statements; document whether these remain.

Define dependency closure explicitly. A useful export might retain selected entities plus referenced property definitions, units, calendar/globe entities, and selected labels for linked objects. Unlimited recursive expansion can effectively recreate the whole graph, while no expansion can leave values uninterpretable. Choose a bounded policy, preserve unresolved identifiers, and report the boundary.

Pin the query and its input dataset, not merely the resulting list of IDs. Record endpoint and retrieval time for WDQS results because a current query is not a historical snapshot. For reproducible releases, record a dump or revision manifest and the filter/mapping version. Preserve enough provenance to explain why an entity entered or left the subset.

## Map meaning deliberately

Wikidata's [P31](https://www.wikidata.org/wiki/Property:P31) states instance membership; [P279](https://www.wikidata.org/wiki/Property:P279) states subclass relationships. Preserve these source assertions with rank and context. Do not mechanically translate every such statement into an accepted OWL axiom: the repository's modeling conventions, metamodeling, qualifiers, inconsistencies, and application scope require review.

Likewise, mapping an external identifier to an internal object requires checking identifier scheme, normalization, issuer, scope, and possible collisions or deprecated assignments. Matching labels, a shared URL, or an alias is candidate evidence. Keep proposed matches separate from accepted identity and record the basis of acceptance. Do not attach `owl:sameAs` merely to simplify joins.

Treat source statement references as pointers to evidence requiring interpretation. Several statements citing the same source are not necessarily independent evidence. A deprecation reason, temporal qualifier, or measurement method can change how a value should be used. Keep acceptance criteria distinct from source rank selection.

## Preserve a source view and derived views

Retain a faithful source representation alongside compact application views when auditability matters. A direct relationship without qualifiers can be a useful display projection if it links back to the complete statement. Name each projection and state losses. Do not claim a round trip when order, reference grouping, datatypes, or values cannot be reconstructed.

Version mappings independently from parsing. Re-running a new mapping over the same preserved source should produce a new derived result without pretending the upstream source revision changed. Retain exported schema versions and dependency manifests so consumers can compare releases reliably.

## Verify meaning, not only parsing

Use a small synthetic fixture plus a pinned real entity representation. Include normal, preferred, and deprecated statements for one property, and verify best-rank selection including multiple preferred values and a deprecated-only case. Include concrete, unknown, and no-value snaks. Check that unknown/no-value do not collapse into ordinary nulls.

Include repeated qualifiers, two distinct reference groups, order arrays, multilingual aliases, a property entity, and an unsupported entity type. Exercise a quantity beyond binary float's exact integer range, missing bounds, a unit URI, a year-precision date, a non-default calendar or globe, and an unfamiliar datavalue type. Compare preserved values structurally and, where required, original bytes.

For operational behavior, verify repeated application, two revisions, an older delayed event, a redirect, deletion/restoration, and an update gap requiring reconciliation. Test subset entry and exit as well as a dependency change that affects other selected entities. Assert expected semantic outcomes rather than merely mirroring implementation branches.

Report counts for entities, statements by rank, qualifiers, reference groups, and unresolved dependencies. Inspect a few records end to end. State which endpoint calls, formats, entity types, update operations, and scale were actually exercised. The [Stable Interface Policy](https://www.wikidata.org/wiki/Wikidata:Stable_Interface_Policy) supports robust clients but does not exempt an application from handling documented extensibility or its own conversion losses.
