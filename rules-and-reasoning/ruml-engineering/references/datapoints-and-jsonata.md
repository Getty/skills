<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# DataPoints and JSONata

Evidence: official RUML 1.0.0 (2026-11-15), commit `d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4`. The file version remains `$specVersion: "1.0"`.
**Normative** describes the pinned contract. **Implementation recommendation** and **Snapshot gap** mark local engineering choices or missing standardization.

## Contents

- [Definitions and runtime values](#definitions-and-runtime-values)
- [Complete type inventory](#complete-type-inventory)
- [Validation rules](#validation-rules)
- [Sets, cardinality, and dataSets](#sets-cardinality-and-datasets)
- [Bindings and dependency resolution](#bindings-and-dependency-resolution)
- [Leaf queries](#leaf-queries)
- [Parent expressions](#parent-expressions)
- [Missing values and type strictness](#missing-values-and-type-strictness)
- [Numbers, dates, and execution controls](#numbers-dates-and-execution-controls)
- [Evidence and tests](#evidence-and-tests)

## Definitions and runtime values

`ruml:datapoints` has role `data`. Its root `payload.data` maps identifiers to definitions; actual case values are supplied by the runtime and do not belong in those definitions. The map key is the identifier, so an extra `id` member is not part of a DataPoint definition. [D1]

Each definition requires `name`, `type`, and `binding`. Optional fields are `description`, `unit`, `format`, `options`, `validation`, `sensitive`, `set`, and `cardinality`, with type-specific restrictions. DataPoint IDs, set IDs, and set field IDs match `^[a-z_][a-z0-9_]*$`; a `dp_` or `set_` prefix is conventional, not required. [D1][D4]

The schema describes definitions, not a complete universal instance-data document schema. A successful RUML document validation does not prove that a later API response, user input, or computed value has the declared type.

For JSONata, the runtime supplies a JSON object whose keys are top-level DataPoint IDs. A missing value has no entry. For example, a resolved integer named `age` appears as `{"age": 24}`, rather than `{"data":{"age":24}}` or `{"age":{"value":24}}`. [D2]

## Complete type inventory

RUML defines twenty DataPoint types in this snapshot. There are no standard `decimal`, `array`, or `null` type names. [D1][D4]

| Type | Runtime meaning / representation | Important restriction |
| --- | --- | --- |
| `string` | JSON string | Text constraints may apply |
| `number` | JSON number | Integer or fractional value |
| `boolean` | JSON boolean | Distinct from strings and numeric flags |
| `date` | `YYYY-MM-DD` string | Calendar date, without time |
| `datetime` | ISO 8601 date and time string | Timezone recommended, not mandatory |
| `time` | `HH:MM` or `HH:MM:SS` string | Seconds may be omitted |
| `integer` | Integral numeric value | Negative values allowed |
| `currency` | Numeric monetary amount | `unit` is required |
| `percentage` | Numeric percentage | Range 0 through 100 |
| `duration` | ISO 8601 duration string | Calendar components may matter |
| `email` | Email-address string | RFC 5322 is the referenced format |
| `phone` | Telephone-number string | E.164 |
| `location` | Geographic identifier/value | Optional granularity in `format` |
| `identifier` | Official-identifier string | Optional identifier-kind hint in `format` |
| `iban` | Bank-account string | ISO 13616 |
| `count` | Nonnegative integer | Use for quantities without negative values |
| `url` | URI string | RFC 3986; reachability need not be tested during validation |
| `address` | Structured postal-address object | Fields described include street, postalCode, city, region, country |
| `enum` | A selected option value | Nonempty `options`; each option requires string `value`, optional `label` |
| `object` | An instance of a named set, possibly repeated | Requires `set`; cardinality is available only here |

`unit` is permitted only for `currency`, `number`, and `percentage`; it is compulsory for currency, with an ISO 4217 code recommended. `format` is permitted only for `location`, `identifier`, and `address`. `options` is exclusive to `enum`; `set` and `cardinality` are exclusive to `object`. [D1]

Location formats are `country`, `region`, `union`, `postal`, `municipality`, and `coordinates`. Identifier formats are `taxId`, `vatId`, `socialSecurity`, `passport`, `nationalId`, `commercial`, and `custom`; the schema constrains these vocabularies. Do not assume a generic free-form `format` for these two types. [D4]

## Validation rules

The `validation` object may express `required`, `min`, `max`, `minLength`, `maxLength`, `pattern`, `enum`, and `message`. The following table groups the exact applicability rules; `required` and `message` are allowed for every type. [D1]

| Types | Additional permitted validation fields |
| --- | --- |
| `string` | `minLength`, `maxLength`, `pattern`, `enum` |
| `number`, `integer` | `min`, `max`, `enum` |
| `date`, `datetime`, `time`, `currency`, `percentage`, `duration`, `count` | `min`, `max` |
| `email`, `phone`, `iban`, `url` | `pattern` |
| `location` | `enum` |
| `identifier` | `minLength`, `maxLength`, `pattern` |
| `boolean`, `address`, `enum`, `object` | None |

Inapplicable fields are invalid; do not quietly ignore a currency `pattern` or boolean `min`. Numeric bounds are numbers for `number`, `integer`, `currency`, and `percentage`; `count` bounds are nonnegative integers. Date/time/duration bounds are strings in their corresponding formats. [D1][D4]

`minLength` and `maxLength` are integers in `[0, 9007199254740991]`. Patterns must be valid ECMAScript-compatible regular expressions and apply to the whole value, with implicit beginning/end anchoring. An `enum` constraint is cumulative with other applicable constraints. [D1]

Tools are instructed to **SHOULD** apply these checks before decision logic. A `required: true` constraint means a value must be present, and a computed result **must** satisfy its declared type and validation. Do not inflate the general SHOULD into a new document-level rejection rule. [D1]

**Implementation recommendation:** represent acquisition failure, absent optional input, invalid obtained input, and a valid false/zero/empty value separately. Produce diagnostics at the DataPoint ID and nested instance path, rather than silently substituting defaults after any failure.

## Sets, cardinality, and dataSets

The standardized field is `payload.sets`, alongside `payload.data`. There is **no `dataSets` field** in the published RUML or RUML-EXT schema. A runtime may use that word in its own API, but must map it explicitly rather than serialize it as a RUML field. [D1][D4]

Each set definition has `name`, a `fields` map of DataPoint definitions, and optional `description`. The schema requires a nonempty name and at least one field. A field may itself be an object referencing another set. Every set reference must resolve, and direct or transitive set recursion is forbidden. [D1][D4]

An object definition uses `"type": "object", "set": "person"`. With no cardinality it denotes one object. When `cardinality.max > 1`, its runtime value is a list of objects. `min` must be an integer at least zero and `max` an integer at least one. [D1]

Nested members are accessed from the top-level ID: `applicant.birth_date`; repeated instances use array access, such as `guarantors[0].family_name`. Do not promote each nested field into a separate global ID merely because it has a name in `fields`. [D1]

**Snapshot gap:** the schema permits a cardinality object without one or both bounds, and does not itself require `min <= max`. Detailed defaults for such partial bounds are not specified. For portable authoring, emit both bounds and a coherent interval; label stricter acceptance checks as a local profile unless the standard is clarified.

Set-definition recursion is different from computed-value dependency cycles and from modular rule-node recursion. Validate these graphs independently; permitting rule recursion does not authorize recursive set types. [D1]

## Bindings and dependency resolution

| `binding.type` | Required fields beyond `type` | Permitted additional fields | Contract |
| --- | --- | --- | --- |
| `input` | None | `hint`, `placeholder`, `defaultValue` | Obtain user input; appropriate input controls recommended |
| `external` | `ref` | `description`, `sourceType`, `fallback` | Resolve a symbolic source using tool configuration |
| `computed` | `expression` | `description` | Compute a typed value from other DataPoints using JSONata |

For external bindings, `sourceType` is `api`, `database`, `file`, or `rulemap`. The tool must let the user configure the source; endpoint, authentication, and source implementation belong in tool configuration. The published schema restricts `fallback` to an `input` binding with its input hints/default, not an arbitrarily nested external/computed binding. [D1][D4]

Computed bindings may depend on other computed DataPoints. Cycles, including transitive cycles, are forbidden; computed values must not be solicited as user input. Resolve dependencies before consumers and check the resulting value against its definition. [D1]

**Implementation recommendation:** use a parsed expression representation to identify statically visible DataPoint dependencies. A text search is not a reliable parser for identifiers, strings, nested scopes, or dynamic access. Document any restrictions needed to validate dynamic dependency discovery.

An external binding is a sourcing hint, not an executable URL. A `defaultValue` is not evidence that the user supplied that value. Record whether a value came from a default, direct input, external resolution, or computation in runtime provenance where that distinction matters.

## Leaf queries

`ruml:query` is a leaf-only `decision` capability. Its payload requires nonempty `expression` and permits `description`. Expressions must be valid **JSONata 2.2.0**; syntax validation belongs to semantic validation, beyond the schema's string check. [D2][D4]

DataPoint names are properties of the input document. `age >= 18` reads the `age` property; a name such as `$age` is a JSONata variable and is not the standard DataPoint addressing convention. Every referenced DataPoint ID must be defined. [D2]

The result must be the actual boolean `true` or `false` to decide the node. Any other value, including no result, yields `undefined`; strings `"true"` and `"false"`, numbers, objects, arrays, and `null` must not be accepted by host-language truthiness. [D2]

The serialized node result uses status strings. Thus JSONata boolean `true` becomes RUML result `"true"`; the expression does not need to return that string. Query result payloads record `expression`, `inputs`, and string-valued `result`. [D5]

A computed binding and a query have different outputs: a computed currency value can legitimately be a number, whereas the same number returned by a query is undecidable. Do not route all JSONata uses through a boolean-only wrapper. [D1][D2]

## Parent expressions

`ruml:expression` is the official `combiner`. Its root declaration must explicitly set `required: true`; its node requires `operator: "DELEGATED"`, nonempty `children`, and exactly one combiner. The payload requires both `expression` and explanatory `description`. It is forbidden in RUML-EXT. [D3]

It receives the query DataPoint input document plus the **bound variable** `$children`, ordered like the node's `children` array. Each direct-child item has `lexId`, `label`, and `status`; the status is the string `"true"` or `"false"`. `$children` is not an invented DataPoint or an ordinary root key. [D3]

All children must be evaluated; `DELEGATED` does not short-circuit. If any child is `undefined`, the parent is `undefined` and the expression must not run. The child array therefore does not present an undecidable child for the expression to override. [D3]

Examples of the specified style:

| Intent | JSONata expression |
| --- | --- |
| At least two fulfilled direct children | `$count($children[status = "true"]) >= 2` |
| More fulfilled than unfulfilled children | `$count($children[status = "true"]) * 2 > $count($children)` |
| Select a particular child's decision | `$children[lexId = "4"].status = "true"` |

Prefer identity-based child selection to positional indexing when a particular child is intended. JSONata indices are zero-based; result paths use one-based child positions. These two coordinate systems must not be mixed. [D3][D5]

The recorded expression payload has `expression`, `inputs`, ordered `children` objects containing only `lexId` and `status`, and `result`. `inputs` is `{}` when no DataPoints were read. Write no expression payload when evaluation was prevented by an undefined child. [D3][D5]

The planned addition of per-child numeric DataPoint values is explicitly outside this release. Do not invent `$children[].value`, scores, or node-local computed DataPoints to claim standard support for weighted child totals. [D3]

## Missing values and type strictness

Omit unavailable DataPoints from the input document. JSON `null`, an absent property, an empty sequence, `0`, `false`, and an empty string have different meanings; collapsing them changes JSONata behavior. A missing input does not justify replacing every resulting expression value with a guessed boolean. [D2]

Check the actual final result type after JSONata execution. An expression may explicitly handle missing values and still return a boolean. Conversely, a successful computation that returns a string is still `undefined` for the decision contract. Separate engine errors from legitimate no-result outcomes in diagnostics.

**Implementation recommendation:** define and test expression authors' missing-data policy. A guard can deliberately produce no result when a prerequisite is absent; a default can deliberately decide otherwise. Such authoring policy belongs in the expression or runtime profile, not an undocumented coercion layer.

Nested object validation, enum membership, default-value checking, and external-source coercion need runtime validation. Keep original inputs available for explanation; if a user interface normalizes a value, record the normalized value actually supplied to the query.

## Numbers, dates, and execution controls

RUML currency values are JSON numbers. The format does not define a decimal arithmetic package, scale, rounding mode, currency conversion, or tax rounding policy. **Implementation recommendation:** specify these explicitly for money calculations and preserve exact source amounts separately when required. Do not silently change a currency value into a string while claiming the same type contract.

JCS canonicalization uses IEEE 754-compatible number serialization. A decimal library's internal representation and a document's canonical numeric bytes are different concerns. Do not hash arbitrary pretty-printer output or assume decimal precision survives a binary-number conversion. [D6]

`date` and `datetime` are different; metadata timestamps additionally use RFC 3339, while DataPoint `datetime`/`time` bounds may omit seconds and timezone offsets. The upstream tests explicitly accept `08:00` and `2024-01-01T08:00` bounds. [D1][D7]

Dates, times, and durations must be compared by value, not lexicographically. **Snapshot gap:** timezone-free values, mixed offsets, and calendar durations need a specified comparison context; the document does not settle every ambiguity. Record timezone/calendar assumptions instead of inventing UTC or treating months as fixed day counts.

`ruml:expression` should be deterministic, but `$random`, `$now`, `$millis`, and `$eval` are permitted; OP-05 requires parser acceptance. A result file alone cannot replay the unrecorded nondeterministic values. [D3]

**Implementation recommendation:** bound expression time, memory, recursion, regex work, and external function exposure. Execution restrictions are deployment controls, not grounds to relabel a spec-permitted expression syntactically invalid. Capture actual engine/version and relevant environmental inputs for reproducible runs.

## Evidence and tests

The §4.7 suite tests identifier syntax, type-specific bounds, timezone-free time/datetime bounds, length bounds, and cardinality minimum values. Operator fixtures also accept nondeterministic combiners and reject missing/false `required` for `ruml:expression`. These are evidence of specific requirements, not comprehensive runtime JSONata coverage. [D7][D8]

[D1]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-7-data-points.md
[D2]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-8-ruml-query.md
[D3]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-14-ruml-expression.md
[D4]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/schemas/ruml.schema.json
[D5]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format/5-1-result-model.md
[D6]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/07-container/7-3-hashing.md
[D7]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/04-capabilities/4-7-data-points.test.yaml
[D8]: https://github.com/Law-as-Code-Institute/ruml/tree/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/03-data-model
