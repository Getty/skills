# TLS/PKI architecture decision record

## Decision context

Owner, date, environment, services, intended clients, threat model, regulatory/policy constraints and support lifetime.

## Trust graph

For each hop: connection address; expected identity; TLS initiator/terminator; server credential; trust bundle; optional client identity; authorization policy; proxy/interception boundary.

## Issuance and profiles

Public/private issuer choice; root/intermediate hierarchy; permitted names and purposes; key custody; enrollment authentication; identity derivation; bounded lifetimes; denied-request tests.

## Bootstrap and recovery

Authenticated initial trust distribution; CA/storage/registry/DNS dependencies; independent recovery path; backup custody; restore drill; RTO/RPO; compromised-key rollback exclusions.

## Lifecycle

Renewal eligibility and ARI; state ownership/locking; validation and atomic publication; reload behavior; live probes; alert thresholds; root overlap/removal; offboarding.

## Compatibility evidence

Client/backend versions; root sources; algorithm/name/purpose behavior; positive and negative results; unresolved clients; explicit exceptions with owners and deadlines.

## Alternatives and rationale

Compare at least the plausible public/private/managed/workload-identity alternatives. State rejected choices and why, without treating convenience as the only criterion.

## Approval and follow-through

Change owner; approver; staged rollout; eligible rollback; monitoring; scheduled acceptance/recovery exercises; outstanding risks.
