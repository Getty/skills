# NewsCodes, Media Topics, and rights metadata

## Preserve code identity independently of labels

NewsCodes is a family of controlled vocabularies for subjects, editorial and production roles, statuses, technical formats, and other concerns. Media Topics is the subject taxonomy within that family. Select the vocabulary appropriate to the property rather than using a subject code as a generic metadata label.

Keep the full concept URI, source vocabulary, retrieved vocabulary version or timestamp, and original source code. Labels are multilingual display values, not stable identifiers. A label can change or be translated while the concept URI remains the same. Avoid constructing URIs from labels or assuming every scheme uses the same code shape.

Resolve QCodes through the actual catalog. For example, a publisher can choose a scheme alias other than a commonly recommended alias. The resolved concept is determined by the catalog's scheme URI and code, not by the alias text alone. Retain unresolved codes with their context so they can be repaired when the missing catalog arrives.

Follow the [NewsCodes guidelines](https://www.iptc.org/std/NewsCodes/guidelines/) and [CV server](https://cv.iptc.org/newscodes/) for definitions, retirement notes, multilingual labels, and machine-readable representations. Preserve retired concepts for historical interpretation. A replacement suggestion does not necessarily express logical equivalence.

## Use subject classification as classification

Keep publisher-assigned topics separate from automatically predicted ones, recording assignment source, model or rule version, time, and any supplied confidence/relevance. Use confidence only within the provider's documented scoring meaning. Do not merge human assignment and model suggestion into one indistinguishable list.

When aligning Media Topics with another vocabulary, retain the supplied relation. A “related concept” mapping to Wikidata or a legacy Subject Code does not justify `owl:sameAs` or formal class equivalence. Review broader/narrower scope and intended retrieval use. An article classified under a topic does not make every mentioned organization an instance of a corresponding OWL class.

For multilingual display, use supported language tags and an explicit fallback policy. Preserve the original language and avoid translating a label into an unverified concept match. Snapshot vocabulary data when reproducing historical classification or search behavior matters.

## Keep rights scopes and claims intact

Preserve copyright holder, notice, usage terms, source attribution, credit lines, embargoes, and structured rights expressions as distinct metadata. The party distributing an item is not automatically its creator or rights holder. A notice naming a rights holder is a source assertion; it does not independently prove ownership or grant a license.

Track the target of each restriction or permission: the whole item, its content, a particular rendition, a component, or an associated asset. A package containing several images does not necessarily provide one common usage policy for all of them. Carry scope through conversions and downstream exports rather than attaching all restrictions to an undifferentiated text record.

The license of NewsCodes, a schema, or documentation is separate from the rights of news content described using those resources. Publication status and embargo timing are likewise separate from contractual permission to reuse material. A `usable` editorial state does not create an unrestricted content license.

## Understand RightsML's role

RightsML 2.0 is an IPTC profile of ODRL for media rights. It expresses actions, permissions, prohibitions, duties, constraints, assets, and relevant parties through an explicit policy model. Inspect the selected policy type, target, assigner/assignee, action, constraints, duties, and conflict/interpretation rules before evaluating it.

Retain linked or encoded rights expressions with their language/profile identifier and acquisition metadata. If a processor does not support an expression, report that limitation and preserve the expression rather than declaring permission. Do not reduce a structured policy to a boolean that loses recipient, territory, purpose, time, or rendition scope.

Consult the [RightsML 2.0 specification](https://www.iptc.org/std/RightsML/2.0/RightsML_2.0-specification.html) and [ODRL 2.2 information model](https://www.w3.org/TR/odrl-model/). This guidance concerns faithful data handling; it does not decide the legal validity of a particular contract or whether a publisher's rights claims are correct.
