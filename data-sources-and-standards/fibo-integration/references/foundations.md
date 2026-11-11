# Foundations and scope

## Understand the layers

Use FIBO to make the meaning of financial terms explicit. Its concepts are OWL classes, properties, restrictions, and individuals, supplemented by human-readable annotations. It can support a business glossary, semantic interoperability, and machine reasoning. The [EDM overview](https://spec.edmcouncil.org/fibo) describes the ontology as a shared model of finance-related things and relationships; it does not promise a complete database of real companies, market prices, or transactions.

Separate four layers in an explanation:

| Layer | What to identify | Typical mistake |
|---|---|---|
| Business meaning | The conditions that make something a concept | Matching a label while ignoring its definition |
| Logical representation | Classes, properties, restrictions, and identity | Treating annotations as executable constraints |
| Instance assertions | Particular entities, instruments, agreements, events | Assuming the vocabulary supplies current reference data |
| Application policy | Required fields, permissions, workflow, quality rules | Assuming OWL defines every operational requirement |

A dictionary definition and an OWL restriction have different jobs. Read both. A note may explain a jurisdictional nuance that cannot be mechanically inferred from a short class hierarchy. Conversely, a formal axiom may imply classifications not visible in the label.

## Select domains deliberately

The [official repository](https://github.com/edmcouncil/fibo) organizes content into domains and modules. Common starting points include Foundations (FND) for general concepts; Business Entities (BE) for organizations and legal structures; Financial Business and Commerce (FBC) for shared financial concepts; Securities (SEC) for securities, equity, and debt detail; Derivatives (DER); Loans (LOAN); Corporate Actions and Events (CAE); and Indices and Indicators (IND). Use the current tree for the complete inventory.

Choose by competency question rather than by filename alone. “Which instruments did this entity issue?” needs roles and instruments. “What venue terms apply to this share?” may require listing and market concepts. “Who controls a subsidiary?” requires a precise account of ownership, control, legal rights, and time. These questions can share concepts without having identical dependency sets.

Treat broad FIBO coverage as a starting hypothesis, not proof that every niche product, local legal form, or business process is fully modeled. Check maturity annotations and actual content. A large import tree is not evidence that every domain is equally mature.

## Explain the boundaries

Use a cross-standard comparison to prevent category errors:

| Artifact or standard | Principal role | Relation to FIBO |
|---|---|---|
| LEI or ISIN | Identify a particular entity or instrument | Supply identity evidence for instances |
| XBRL taxonomy | Define reporting concepts and reporting relationships | May be mapped with accounting context retained |
| ISO 20022 message model | Structure financial messages and business exchanges | May share business meaning without equivalent fields |
| Market data feed | Publish observations and reference records | Supply assertions that need source and time |
| RDF/OWL | Represent and give semantics to linked statements | Provide the formal language in which FIBO is expressed |
| SHACL or application rules | Validate a chosen data contract | Enforce operational completeness beyond ontology reasoning |

A mapping between these artifacts is a design decision. A reporting fact called “assets” may have consolidation, period, currency, and accounting-policy aspects absent from a bare asset concept. Preserve those distinctions rather than replacing a precise fact with a broad category.

## Choose an adoption level

Start with terminology alignment when the goal is shared understanding. Record source definitions, FIBO candidates, and differences without introducing logical axioms. Move to a local application ontology when reusable classes and relationships are needed. Use instance-level reasoning only when evidence, performance, and entailment requirements justify it.

For any level, make success measurable: agreed definitions, fewer ambiguous mappings, reproducible queries, or explicit exception handling. Do not equate success with the number of FIBO classes imported.
