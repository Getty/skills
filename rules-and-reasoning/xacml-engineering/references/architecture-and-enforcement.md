# Architecture and enforcement

## Assign responsibilities

Use a policy enforcement point (PEP) at the boundary where access can actually be
granted or refused. Use a policy decision point (PDP) to evaluate policy. A policy
administration point (PAP) manages policies; policy information points (PIPs) supply
attributes. A context handler translates application facts and requests into the
evaluation context. Products may combine these components, but their responsibilities
remain distinct.

Authenticate the caller before deriving subject facts. Bind action and resource
from the actual operation, not a user-controlled label unrelated to the endpoint.
Retrieve authoritative attributes from trusted stores. Pass only the necessary
facts and preserve their freshness/source information outside or alongside the
XACML context according to the application's evidence model.

## Enforce a complete decision

Define the PEP contract before writing a policy. A defensible closed-world access
adapter grants only an accepted Permit whose required obligations can be fulfilled.
It blocks access for Deny, NotApplicable, Indeterminate, malformed responses,
unmatched batch results, and transport failure, while preserving these differences
for diagnostics. This is an explicit application enforcement rule; it is not a
claim that the PDP internally maps every state to Deny.

Perform the protected action under the same relevant state assumptions as the
decision. For mutable balances, ownership, or revocation, address the time between
check and use through transactions, version checks, or a deliberately bounded
decision lifetime. A correct policy cannot repair stale or forged facts.

## Keep trust boundaries concrete

An attribute's Issuer is matching metadata, not a cryptographic signature. The
context handler/PIP must decide which incoming assertions are authoritative.
Untrusted callers must not override authoritative role, tenant, classification,
current time, or subject identity simply by providing the same attribute ID.

Choose embedded versus remote PDP based on deployment needs. Embedded evaluation
can reduce a network dependency but requires consistent policy distribution.
Remote evaluation centralizes management but adds availability, authentication,
latency, and response-correlation concerns. Measure the complete decision path.

Do not make an HTTP 200 response synonymous with Permit. Transport success and
authorization outcome are separate. Likewise, a PDP health check does not verify
that the intended root policy was loaded or that required PIPs work.

Authority: [OASIS core architecture and processing model](https://docs.oasis-open.org/xacml/3.0/errata01/os/xacml-3.0-core-spec-errata01-os-complete.html),
[AuthzForce embedded engine](https://github.com/authzforce/core), and
[AuthzForce server architecture](https://github.com/authzforce/server).
