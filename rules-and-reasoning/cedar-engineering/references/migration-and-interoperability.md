# Migration and interoperability

## Compare semantics before translating syntax

Create a migration table with source result, source error behavior, Cedar equivalent,
and enforcement behavior. Explicitly preserve defaults, precedence, hierarchy,
missing facts, and whether multiple matching rules contribute to the result.

| Source | Main migration question |
| --- | --- |
| Handwritten RBAC/ACL | Are denial precedence and ownership exceptions explicit? |
| Rego/OPA | What query result and undefined/error mapping form the API contract? |
| XACML | How are NotApplicable, Indeterminate, obligations, and combining algorithms preserved? |
| JSON Logic/CEL | Which surrounding policy-combining and trust rules must be supplied? |
| DMN/FEEL | Is the result an authorization decision or a business classification used as a fact? |
| SQL access filters | Do join absence, nulls, and row filtering match Cedar entity semantics? |

Do not translate first-match ACLs by merely preserving their order. Cedar policy
order does not implement precedence. Do not translate every XACML Permit into a
Cedar permit while discarding obligations. An obligation may be a necessary condition
of valid enforcement, and Cedar's decision model does not reproduce an obligation
handler automatically.

## Migrate with a dual-evaluation corpus

Record policy and input versions, evaluate both systems without changing effects,
and classify differences. Include deny-heavy and adversarial requests; production
traffic alone may contain few boundary cases. Require deliberate resolution of each
permission expansion. Preserve historical behavior only when it is intended; a
migration can expose an existing bug, but changing it is a separate reviewed decision.

Use an adapter to normalize source facts into a typed Cedar entity/context contract.
Keep the adapter deterministic and test it separately. Do not let the language
migration silently change identifier reuse, tenant routing, or trusted claim sources.

## Retain each system's proper role

Use Cedar for authorization decisions. Use DMN for business decision models, PDDL
for planning, and a workflow/orchestrator for effects and obligations. An agent can
propose a plan, then request authorization for each protected operation with current
facts. A precomputed Allow for one action is not blanket permission for the rest
of a workflow.

Consult the source engine's primary specification and [Cedar authorization semantics](https://docs.cedarpolicy.com/auth/authorization.html)
when constructing a mapping. Optional sibling skills can provide domain details;
this skill does not depend on their installation or file layout.
