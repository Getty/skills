# Missing data, errors, and unknowns

## Keep four categories distinct

A present null is a value. An absent field has no binding at that path. A runtime
error reports failed evaluation. An unknown represents deliberately incomplete
knowledge in a host-supported partial-evaluation mode. Do not flatten these into
false inside a generic conversion helper.

For maps, compare these original fixtures:

| Map | `has(request.owner)` | Direct owner access |
| --- | --- | --- |
| `{}` | false | Missing-key error |
| `{"owner":null}` | true | Null value |
| `{"owner":""}` | true | Empty string |
| `{"owner":"alice"}` | true | String value |

This table assumes `request` is present and map-like. An absent parent binding or
incorrect parent type is a different case. Typed protobuf presence/default behavior
also needs its own adapter tests.

## Use presence checks intentionally

`has(request.owner) && request.owner == 'alice'` can produce false when the owner
key is absent. `has` does not establish that the owner is meaningful or authoritative.
For arbitrary dynamic map keys, use an appropriate membership check rather than
inventing `has(map[key])` syntax. Guard parent paths where necessary.

Treat checking as an early error detector, not a guarantee against missing dynamic
fields. Record parse/type failures separately from runtime failures.

## Understand Boolean error absorption

CEL's Boolean operators allow a decisive false for AND or true for OR to determine
the outcome despite another operand's error. Do not depend on textual operand
execution order. Custom functions should remain pure and bounded. Use conditional
expressions where branch selection is the intended value computation.
[Language semantics](https://github.com/cel-expr/cel-spec/blob/master/doc/langdef.md).

Test both a decisive Boolean plus an error and an unresolved Boolean plus an error.
An error-absorbing expression is not a general try/catch mechanism. Keep diagnostics
appropriate to the engine rather than assuming one fixed error must be reported
when multiple subexpressions can fail.

## Use partial knowledge explicitly

Configure partial activations/unknown attributes through the chosen implementation.
A missing ordinary binding is not automatically an unknown. Decide how to consume
an unknown result: request more facts, preserve a residual expression, or refuse
an operation until a definitive answer exists.

Support for unknown values and residual AST generation differs between stacks.
The [CEL API reference](https://cel.dev/reference/api-reference) documents that
these are distinct capabilities. Do not promise residual expressions merely because
an evaluator can return an unknown set.

The bundled Python corpus exercises errors and absence, not host-specific unknown
activation APIs. Add runtime-specific tests before relying on partial evaluation
in an integration.
