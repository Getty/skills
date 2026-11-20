# Modeling patterns

## Choose the simplest faithful permission model

Use role-based access for stable groups of permissions, attributes for conditions
that vary by principal or resource, and relationships for ownership, membership, or
sharing. Combine them when the business rule actually requires the combination.
Do not generate a single policy per user when group membership would make revocation
and review clearer; equally, do not hide object-specific shares inside enormous
role names. See [Cedar design patterns](https://docs.cedarpolicy.com/overview/patterns.html)
and [role-based access](https://docs.cedarpolicy.com/bestpractices/bp-implementing-roles.html).

| Requirement | Candidate model | Review question |
| --- | --- | --- |
| Editors may update project documents | Principal group plus resource container | Does membership extend to subprojects? |
| Owners may update their own item | Entity-valued owner attribute | Is ownership transfer atomic with policy data? |
| Confidential items require MFA | Resource flag and trusted request context | What happens if the flag or MFA fact is absent? |
| Suspended users cannot act | Explicit forbid over trusted state | Can missing entity data disable the forbid? |
| One-off sharing | Template-linked policy or reviewed ACL relation | Who may create and revoke a share? |
| Same-tenant access | Explicit typed tenant equality/membership | Can data hydration cross tenants? |

For hierarchical access, specify whether ancestors confer permissions on descendants,
whether direct membership differs from indirect membership, and whether the container
itself should match. Cedar `in` is reflexive; if the container must be excluded, add
the appropriate identity restriction. Avoid importing a general graph path query
that Cedar cannot express.

## Isolate tenants deliberately

Put a trusted tenant reference on principals and resources, constrain data loaders
to the request's tenant, and enforce the relevant relation in policy. Test an otherwise
identical request with only the resource tenant changed. Test duplicated display names,
stale shared resources, and a user with legitimate membership in multiple tenants.

Choose a policy-store boundary separately from a schema namespace. A shared schema
can describe isolated tenants, while a separate store can still be unsafe if request
routing selects the wrong one. For cross-tenant sharing, model an explicit grant and
its permitted scope; do not remove the general tenant check globally.

## Authorize permission management

Sharing, role assignment, policy editing, and ownership transfer are protected actions.
Authorize the ability to grant a permission separately from the permission itself.
An editor may be allowed to modify content without being allowed to grant everyone
edit access. Review amplification: can a user obtain a broader permission by editing
a relationship that the authorizer trusts? See [meta-permissions](https://docs.cedarpolicy.com/bestpractices/bp-meta-permissions.html).

Use separate actions for read, write, delete, export, and administer when they have
different consequences. Map a multi-object operation into explicit checks, and
specify whether all checks must pass. Authorizing a container must not silently
imply permission to act on every child.

## Keep business logic bounded

Return a permission decision from Cedar. Calculate tax, pricing, eligibility scores,
or action plans in the appropriate domain layer. If a business decision is an input
to authorization, carry its source and freshness with the fact. The optional sibling
skills `dmn-engineering`, `opa-rego-engineering`, and `pddl-engineering` cover different
jobs; no installation of those skills is required to use this one.
