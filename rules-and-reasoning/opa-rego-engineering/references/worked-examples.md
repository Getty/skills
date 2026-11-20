# Worked examples

## Synthetic workspace authorization

The original policy permits active members to read their own resource within their
tenant and active editors to read/write within that tenant. It permits no cross-tenant
access. Malformed requests produce a defined false permission.

The identity snapshot is educational data, not authentication code. A real host
must supply verified identity and authoritative resource metadata. The `allow`
entrypoint is Boolean; `decision` is an object with that Boolean and a synthetic
revision. Choose the query deliberately.

## Native checks

From the skill directory:

```bash
opa check --strict assets/examples/policy.rego assets/examples/policy_test.rego
opa test assets/examples/policy.rego assets/examples/policy_test.rego assets/examples/data.json -v
opa eval --data assets/examples/policy.rego --data assets/examples/data.json --input assets/examples/input.json 'data.workspace.authz.decision'
opa eval --strict-builtin-errors --data assets/examples/policy.rego --data assets/examples/data.json --input assets/examples/input.json 'data.workspace.authz.allow'
```

Expect true for the supplied owner-read input. Tests cover owner read, editor write,
cross-tenant denial, inactive/unknown users, missing fields, malformed types,
unsupported action, and owner write without an editor role.

## Check the consumer

```bash
python3 scripts/check_decision.py assets/examples/response-allow.json
python3 scripts/check_decision.py assets/examples/response-deny.json
python3 scripts/check_decision.py assets/examples/response-undefined.json
```

Expect statuses 0, 1, and 2. The helper rejects duplicate keys, nonstandard numbers,
missing result, wrong result type, oversized files, and error-shaped envelopes.
It prints a small JSON classification and performs no network calls or effects.
It consumes Boolean Data API responses, not CLI JSON or structured decisions.

Status 2 includes undefined and malformed envelopes; `reason` distinguishes them.
The caller still owns transport, authentication, freshness, and resource enforcement.
Do not discard the status through a shell pipeline and accidentally continue.

## Use fixtures to extend coverage

Add a new input with an independent expected result before adding a permission.
Keep synthetic identities explicit. For a new editor override, include a same-tenant
allow and cross-tenant denial. For a new action, include unknown-action behavior.
For missing data, decide whether the host rejects the request or the policy gives a
negative decision, then test that exact boundary.

The verification record appears in sources-and-versioning. Local evaluation does
not prove that a deployed gateway supplies authentic facts or consumes the result
correctly; those require integration evidence from that actual system.
