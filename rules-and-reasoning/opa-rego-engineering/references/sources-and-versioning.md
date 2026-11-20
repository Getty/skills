# Sources and versioning

Prefer OPA primary documentation/source for language claims,
Gatekeeper docs for controller behavior, and Terraform docs for plan JSON. Bundled
examples and workflow text are original; no upstream policy corpus is redistributed.

## Baseline

Use Rego v1 for bundled examples. Official releases inspected list v1.22.4 from
November 12. Current docs also expose Rego v2 and opt-in newer negation/Boolean
syntax. Gatekeeper documentation inspected labels itself v3.23.x. These observations
do not dictate the user's deployment versions. Re-check supported features against
actual release notes, capabilities, and runtime before adoption.

## Primary source map

| Topic | Source |
| --- | --- |
| Language | https://www.openpolicyagent.org/docs/policy-language |
| Keywords | https://www.openpolicyagent.org/docs/policy-reference/keywords/import ; https://www.openpolicyagent.org/docs/policy-reference/keywords/not ; https://www.openpolicyagent.org/docs/policy-reference/keywords/every ; https://www.openpolicyagent.org/docs/policy-reference/keywords/default ; https://www.openpolicyagent.org/docs/policy-reference/keywords/some ; https://www.openpolicyagent.org/docs/policy-reference/keywords/contains |
| Migration | https://www.openpolicyagent.org/docs/v0-upgrade ; https://www.openpolicyagent.org/docs/v0-compatibility |
| CLI/tests/errors | https://www.openpolicyagent.org/docs/cli ; https://www.openpolicyagent.org/docs/policy-testing ; https://www.openpolicyagent.org/docs/errors |
| Capabilities/security | https://www.openpolicyagent.org/docs/operations ; https://www.openpolicyagent.org/docs/security |
| API/facts | https://www.openpolicyagent.org/docs/rest-api ; https://www.openpolicyagent.org/docs/external-data |
| Management | https://www.openpolicyagent.org/docs/management-bundles ; https://www.openpolicyagent.org/docs/management-decision-logs ; https://www.openpolicyagent.org/docs/management-status ; https://www.openpolicyagent.org/docs/management-discovery |
| Performance/Wasm | https://www.openpolicyagent.org/docs/policy-performance ; https://www.openpolicyagent.org/docs/wasm |
| Gatekeeper | https://open-policy-agent.github.io/gatekeeper/website/docs/constrainttemplates/ ; https://open-policy-agent.github.io/gatekeeper/website/docs/input/ |
| Terraform | https://www.openpolicyagent.org/docs/terraform ; https://developer.hashicorp.com/terraform/internals/json-format |
| Releases | https://github.com/open-policy-agent/opa/releases |

## Refresh

Review releases, capability changes, dialect changes, and integration field updates.
Replay bundled cases and real decision cases. Update the verification date only
after checking those surfaces, not by replacing a version string. Retain an old
corpus where compatibility comparisons are needed.

## Verification scope

The Python tool is a saved-response classifier, not an evaluator or conformance
suite. Native example results are recorded after execution. No live Gatekeeper,
Terraform apply, bundle rollout, or Wasm deployment is performed by this skill's
preparation checks. Re-run against the actual deployment runtime before claiming
integration validation.

## Observed preparation checks

The official Linux amd64 OPA **1.22.4** binary passed strict compiler
checks and **10/10** bundled policy tests. The saved-response helper passed **11**
positive and negative envelope cases, including duplicate keys and wrong types.
Skill frontmatter, local reference links, and JSON fixtures were also checked.
No Kubernetes/Gatekeeper cluster, Terraform apply, or Wasm host was exercised.
