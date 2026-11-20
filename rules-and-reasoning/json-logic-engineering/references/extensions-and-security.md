# Extensions and security

## Keep extensions explicit

Use a small, versioned operation registry. Specify argument types, return types,
error behavior, resource cost, and whether an operation depends on external state.
Avoid importing a broad host library whose methods exceed the intended capability.

A custom function receives evaluated arguments. It cannot create a new lazy branch
construct through ordinary registration. It may read the current data through host
binding in the JavaScript implementation, so audit its use of context. Register
operations at process startup, then keep the registry stable.

The project documents that arbitrary object-method invocation was removed in
json-logic-js 2.0.0 following a prototype-pollution advisory. Treat this as version
history, not a blanket claim that later versions sandbox all inputs or extensions.
Review the actual installed package and relevant advisories.

## Bound untrusted rules

Define maximum bytes, AST nodes/depth, collection sizes, string sizes, permitted
paths, permitted operators, and execution time. Reject unknown operations before
evaluation. Exclude debugging/effectful operations from a pure profile. Reject
duplicate keys before JSON parsing loses evidence of ambiguity.

The bundled inspector enforces a deliberately narrow structural profile. It does
not prove runtime cost, detect all risky paths, constrain a custom function, or
make an evaluator safe. Combine static checks with a trusted execution boundary,
bounded inputs, and a genuinely interruptible worker/process when needed.

A rule shaped as JSON is still code in the policy domain. Separate who can edit a
rule, who can publish it, and who can submit facts. Never let an untrusted caller
choose an unrestricted operation registry or a local module path.

## Keep effects outside expressions

Prefer preparing facts before evaluation and executing an authorized effect after
a typed decision. If an extension calls a service, document credentials, timeout,
retry, replay, and idempotency separately. A deterministic-looking AST with a clock,
random generator, network request, or database lookup is not reproducible by itself.

For browser use, remove secrets from input rather than trying to hide them through
rules. A user controls their browser and can inspect data and alter evaluation.
Server enforcement must stand independently.

Authority: [adding operations and historical advisory](https://jsonlogic.com/add_operation.html)
and [reference evaluator source](https://github.com/jwadhams/json-logic-js/blob/2.0.5/logic.js).
