# Types, numbers, and operators

## Preserve types at the boundary

Use numbers, strings, Booleans, null, lists, contexts, functions, ranges, dates,
times, date-times, and the two duration kinds according to the selected profile.
A JSON string `"42"` is not the number `42`; a date-looking string is not a date.
Use explicit conversion and inspect diagnostics for invalid input.

Standard FEEL numbers follow Decimal128-based decimal semantics with 34 digits
and half-even rounding. Host libraries may use BigDecimal, binary floats, or other
representations. Verify both conversion and arithmetic where money, large IDs, or
exact thresholds matter. Do not route a 20-digit identifier through a JavaScript
number merely because FEEL has a numeric type; identifiers can remain strings.
See [DMN 1.6 §10.3.2.3](https://www.omg.org/spec/DMN/1.6/PDF).

## Use the actual operator semantics

| Expression | Purpose | Caution |
| --- | --- | --- |
| `a = b`, `a != b` | Equality/inequality | Mixed kinds do not imply coercion |
| `a < b`, `a <= b` | Ordering | Only supported comparable kinds |
| `x between a and b` | Inclusive bounds | Type and missing-value behavior matter |
| `x in [a..b)` | Interval membership | Open upper bound excludes `b` |
| `x ** 2` | Exponentiation | Parenthesize unary minus explicitly |
| `a and b`, `a or b`, `not(a)` | Boolean operations | Three-valued behavior in FEEL |

Use `=` rather than `==`. Write `-(4 ** 2)` or `(-4) ** 2` explicitly when the
intended sign matters; FEEL's precedence should not be guessed from another
language. Standard FEEL does not represent NaN or infinity as ordinary number
values. Define handling of division by zero and other invalid arithmetic through
the engine's result plus diagnostics.

## Distinguish equality from serialization

Numeric scale differences do not automatically imply different FEEL numeric values.
Context key order in JSON is not the same concept as ordered evaluation of context
entries. A list's order is meaningful. Test structured equality using the engine
rather than comparing arbitrary pretty-printed output.

`null = null` is true. `1 = "1"` is null under FEEL's mixed-kind semantics;
B-FEEL deliberately differs. Do not convert unknown comparison results into false
before the business rule has specified that treatment.

## Round and convert deliberately

Specify when rounding happens, its scale, and the selected function's behavior.
Rounding each line item and rounding the total can produce different outcomes.
Use explicit `number(...)` conversion parameters for locale-specific text and
validate that grouping/decimal conventions match the input source. Separate
formatting for display from the value used to make a decision.

The [Camunda type guide](https://docs.camunda.io/docs/components/modeler/feel/language-guide/feel-data-types/)
illustrates one host mapping; it is not a universal representation contract.
