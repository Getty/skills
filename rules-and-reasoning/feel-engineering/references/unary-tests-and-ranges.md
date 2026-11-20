# Unary tests and ranges

## Choose the correct mode

A unary test evaluates an implicit input. A DMN table's input entry commonly uses
this mode, while a formula or output entry uses full expression mode. The same
source text can mean different things depending on the entry point; record the
mode in fixtures and integration code.

| Unary-test source | Meaning for the implicit value |
| --- | --- |
| `"urgent"` | Equals this string |
| `< 10` | Is less than ten |
| `[10..20]` | Is between ten and twenty, including endpoints |
| `(10..20]` | Excludes ten and includes twenty |
| `"normal", "urgent"` | Matches one alternative |
| `not("blocked")` | Negates the corresponding test |
| `-` | Unrestricted test |

For full expressions write an explicit operand, such as `weight < 10` or
`weight in [10..20]`. Do not prepend a dummy variable by string concatenation
and assume every unary-test construct translates that way.

## Model intervals precisely

Track lower/upper endpoints and inclusivity independently. Distinguish the interval
`[2..5]` from the two-element list `[2,5]`. `[2..5]` is a range value/test, not an
instruction to materialize all numbers between its endpoints. Use explicit iteration
syntax for numeric sequences where supported.

Adjacent partitions such as `< 10` and `>= 10` cover the boundary without overlap.
`< 10` and `> 10` leave a gap; `<= 10` and `>= 10` overlap. Repeat the same
reasoning for dates and ordered strings, including valid input domain restrictions.
A syntactically valid interval is not proof of a complete decision table.

## Bind the implicit value explicitly

Interpreters expose different unary-test APIs. In the bundled feelin adapter the
implicit input is bound as `?` in the context. Other engines may take a separate
argument. Use the engine's documented contract and avoid leaking a test-only binding
convention into a DMN file.

Advanced unary tests can use `?` explicitly or involve lists/Boolean expressions;
confirm the exact profile rather than treating S-FEEL and full FEEL as identical.
The [Camunda unary-test guide](https://docs.camunda.io/docs/components/modeler/feel/language-guide/feel-unary-tests/)
shows one concrete implementation; [DMN 1.6](https://www.omg.org/spec/DMN/1.6/PDF)
is normative.

## Test absence and negation

Include null, a wrong-kind input, each endpoint, one interior value, and values
outside the interval. Negation does not necessarily make an unknown result true.
Distinguish `not("blocked")` from a business requirement that the value must be a
known member of an allowed enum. The latter needs an explicit allowed domain.
