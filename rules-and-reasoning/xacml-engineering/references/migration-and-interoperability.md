# Migration and interoperability

## Migrate XACML 2.0 deliberately

The 3.0 model changes request categories, target structure, functions, advice, and
combining semantics. A syntactic converter helps with XML transformation but does
not establish semantic equivalence. Preserve the original engine/profile and run
representative requests before and after conversion.

Do not replace every legacy identifier with a 3.0 prefix. Some valid identifiers
retain their original version. Pay special attention to legacy override algorithms
versus the extended-Indeterminate behavior of 3.0 algorithms.

AuthzForce documents migration tooling, but pin the tool and verify its supported
subset. Treat product-specific variable/designator shortcuts, selectors, providers,
and administration APIs as additional migration work.

## Map responsibilities before languages

| Target | What may map | What needs explicit design |
| --- | --- | --- |
| Cedar | Subject/action/resource checks, attributes, relationships | Forbid semantics, schema/entities, error handling, obligations |
| Rego/OPA | Attribute predicates and structured decisions | Undefined/errors, composition, deployment, enforcement |
| CEL | Individual typed conditions | Full policy hierarchy, combining, four decisions |
| DMN/FEEL | Decision tables or business conditions | Access enforcement, bags, status, obligations |
| JSON Logic | Small serialized predicates | Types, coercion, missing values, richer outcomes |
| RUML | Rule descriptions and traceable source checks | Result algebra, ordered operators, capabilities, actions |

These are application-level mappings, not promised standard converters. Use the
corresponding skill when implementing a target.

## Preserve observable semantics

Define equivalence at the PEP boundary: access outcome, obligation handling, failure
classification, and relevant diagnostics. Internal representations can differ, but
do not collapse Indeterminate into NotApplicable or false before combining unless
that loss is explicitly accepted.

Build counterexamples involving conflicting rules, missing attributes, multi-valued
roles, ambiguous issuers, and failed mandatory obligations. A passing Permit/Deny
happy-path corpus cannot demonstrate preservation of authorization behavior.

For staged migration, compare old and candidate decisions on identical trusted
snapshots without executing effects twice. Keep one authoritative enforcement path
until the reviewed cutover. Attribute semantics and freshness must match, not merely
the visible policy expression.

Avoid judging XACML by unsupported claims that no new deployments use it. Decide
from the existing estate, interoperable profiles, required semantics, operational
cost, and the actual target implementation.

Authority: [OASIS 2.0/3.0 differences](https://wiki-static.oasis-open.org/xacml/DifferencesBetweenXACML2.0AndXACML3.0),
[AuthzForce migration guidance](https://github.com/authzforce/core#xacml-20-support-and-migrating-to-xacml-30),
and [core combining algorithms](https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-en.html).
