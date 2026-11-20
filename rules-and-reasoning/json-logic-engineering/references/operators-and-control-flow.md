# Operators and control flow

## Predict the actual value

Use `if` for conditional selection. Supply condition/result pairs with an explicit
fallback. Built-in `if` evaluates only the selected branch. An ordered condition
chain expresses priority; changing its order may change the decision.

`and` and `or` return operands. `{"and":[true,"ready",7]}` returns `7`;
`{"or":[0,"review",false]}` returns `"review"`. Use `!!` only when deliberately
requesting JSON Logic truthiness, not as validation of a Boolean result.

Retain cases for empty/nonempty arrays, empty string, string zero, numeric zero,
null, false, and true. A host-language cast may differ from the project's
[truthiness contract](https://jsonlogic.com/truthy.html).

## Make comparisons intentional

Prefer strict scalar equality for typed input. Coercing equality may equate values
whose types differ. Neither equality operator should be advertised as portable
deep equality for records or lists. In JavaScript those values are compared as
objects; use selected scalar fields or a documented structural-equality extension.

Use chained `<` or `<=` only with supported arity. A three-operand range is useful,
but `>` and `>=` are not automatically symmetric multi-operand forms. Exercise both
endpoints. Preserve operand order through builders and translators.

Arithmetic is not input validation. Check numeric strings, null, zero denominators,
overflow, and non-finite values. Set units, precision, and rounding explicitly.
Formatting a number for display is separate from deciding its business value.

## Distinguish lazy and eager operations

Built-in `if`, `and`, and `or` implement special lazy control paths. Collection
operations implement scoped control paths. Ordinary custom functions receive already
evaluated operands. A custom `unless` therefore cannot prevent evaluation of a
side-effecting argument.

The JavaScript `log` operation writes to the host log. Exclude it from production
profiles intended to have no effects, and emit redacted diagnostics from the wrapper.
Do not replace a lazy built-in with an ordinary function without retesting behavior.

Authority: [operations](https://jsonlogic.com/operations.html),
[extension limitations](https://jsonlogic.com/add_operation.html), and
[pinned source](https://github.com/jwadhams/json-logic-js/blob/2.0.5/logic.js).
