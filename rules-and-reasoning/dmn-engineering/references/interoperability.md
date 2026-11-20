# Interoperability and neighboring languages

## Compare the question each language answers

| Technology | Typical responsibility | What a DMN bridge must preserve |
| --- | --- | --- |
| RUML | Explicit rulemaps with its own operators, statuses, and result traces | Evaluation order, unknown states, evidence, and capabilities |
| Rego/OPA | General policy evaluation integrated with operational enforcement | Input/data documents, undefined results, and decision envelope |
| CEL | Embedded typed expressions in a host-defined environment | Declared variables, type conversions, errors, and host restrictions |
| Cedar | Authorization over principal/action/resource/context | Permit/forbid composition and entity/schema semantics |
| XACML | Attribute-based authorization requests and decisions | NotApplicable/Indeterminate, combining algorithms, obligations |
| PDDL | Plans using modeled actions and goals | State transitions and execution assumptions beyond one decision |
| JSON Logic | JSON-encoded expression trees | Truthiness, coercion, missing values, and operator profile |
| RDF/OWL/SHACL | Graph semantics and constraint validation | Open/closed-world assumptions and explicit mapping of values |

This is an architectural comparison, not a claim of automatic translation. Use the
respective primary specification and runtime when implementing a bridge. Other
skills in the collection are optional aids; no other installed skill is required.

## Design mappings as explicit contracts

Map input and output domains before translating syntax. Identify values that have
no direct counterpart: null, missing data, undefined evaluation, technical errors,
multiple hits, obligations, or pending human interpretation. Preserve these in a
wrapper rather than flattening all non-success states to `false`.

For RUML, do not infer Boolean XOR semantics from an operator name or map an ordered
operator directly to DMN Any. For XACML/Cedar, a business decision table that outputs
`allow` does not automatically reproduce authorization composition or enforcement.
For PDDL, a decision can choose parameters or classify a state; it cannot replace
a planner's state-transition search merely by returning an action label.

## Test translation boundaries

Retain source identifiers and source revisions in the transformed artifact. For
semantic graphs, store a projection of decisions/rules and their provenance without
claiming that OWL entailment executes a DMN table. For JSON inputs, define units and
types before binding to FEEL.

Build paired cases that reveal differences: absent fields, mixed numeric/string
values, overlapping matches, order changes, empty collections, and exceptions.
Document any unsupported feature instead of silently dropping it. If translation
is intentionally partial, mark the supported subset and reject out-of-profile
models with a useful diagnostic.

Start from [OMG DMN](https://www.omg.org/spec/DMN/1.6) for DMN semantics and use
a language-neutral decision envelope only as an application convention. No standard
in this table establishes universal equivalence with the others.
