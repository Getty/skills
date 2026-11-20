# XML and interchange

## Pin namespaces instead of guessing

For DMN 1.6, the official [DMN16.xsd](https://www.omg.org/spec/DMN/20240513/DMN16.xsd)
uses `https://www.omg.org/spec/DMN/20240513/MODEL/`. Its default expression/type
language URI is `https://www.omg.org/spec/DMN/20240513/FEEL/`. The date in a
namespace is not the publication month and must not be synthesized from `1.6`.

Keep the XML model namespace distinct from `definitions/@namespace`, which identifies
the business model, and from the namespace URI used for FEEL. The `exporter` and
`exporterVersion` attributes describe tooling, not the business model revision.

## Preserve identity and references

Assign stable IDs to decisions, inputs, requirements, table components, and rules
where tooling benefits from identity. An ID identifies an XML element; a name is
used in business/expression contexts. Renaming a decision can affect expressions
and host lookups even if its ID is unchanged.

Resolve local `href="#id"` references against the same definitions document.
Resolve imported elements using the proper namespace and import contract. Do not
replace every namespace URI or fragment with a global search-and-replace. An
unresolved import is not permission to fabricate an empty dependency.

XML element ordering is part of XSD validity. Generate XML with a proper serializer;
escape `<` and `&` in text and preserve FEEL quotes. Avoid copying diagram-oriented
XML fragments into an unrelated version profile.

## Treat diagram interchange separately

DMN 1.6 reuses the [DMNDI15 schema](https://www.omg.org/spec/DMN/20230324/DMNDI15.xsd)
and associated DI/DC schemas. Diagram coordinates and labels help presentation but
do not define decision logic. A model without layout can still have valid executable
logic; an attractive diagram can contain an invalid decision expression.

Round-trip through the actual editor and compare identifiers, namespaces, imports,
expressions, hit policies, annotations, and vendor extension elements. Loss of
unrecognized extensions can change execution if the deployment depended on them.
Preserve unsupported content or disclose its removal.

## Validate with a complete local schema set

Download normative schemas from the selected release's links and keep imports
resolvable locally. Disable network/entity resolution when processing arbitrary
models. The bundled helper accepts an explicit XSD path and uses local imports;
it does not download schemas or claim FEEL validity.

Separate these outcomes in a report: well-formed XML; XSD-valid document; resolved
model references; supported runtime profile; successful evaluation; correct business
meaning. Migrating only the namespace satisfies none of the later checks. Retain
before/after artifacts and rerun distinguishing cases after editor conversion.
