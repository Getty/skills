# Worked examples

## Understand the synthetic fixture

The example models two tenants, a blue team, three users, and two documents. Team
members may read documents in their own tenant; confidential documents require MFA.
Owners may write their own same-tenant documents with MFA. A suspended user is denied
by an explicit forbid. The short IDs are educational; use immutable production IDs.

Files under `assets/examples/` contain the schema, policies, entity snapshot, and a
compact case manifest. `unsafe-forbid.cedar` deliberately accesses missing context
and demonstrates skip-on-error. Do not deploy it.

Run the official CLI and local helpers from the skill directory:

```bash
cedar --version
cedar language-version
cedar validate --policies assets/examples/policies.cedar --schema assets/examples/schema.cedarschema
python3 scripts/audit_entities.py assets/examples/entities.json --require-parents
python3 scripts/run_example_cases.py --cedar /path/to/cedar
```

`run_example_cases.py` translates the compact manifest into temporary files in the
CLI's documented `run-tests` format. It validates the normal policy set, runs six
schema-conforming cases with the schema, and runs two intentional error cases without
schema-aware request rejection so the evaluator behavior is visible. It never makes
network requests or executes a protected application operation.

## Expected behavior

| Case | Decision | Evaluation errors |
| --- | --- | --- |
| Blue-team read, confidential document, MFA true | Allow | 0 |
| Same read with MFA false | Deny | 0 |
| Suspended team member with MFA | Deny | 0 |
| Read a different tenant's document | Deny | 0 |
| Owner writes own document with MFA | Allow | 0 |
| Different owner/tenant attempts write | Deny | 0 |
| Required MFA omitted, evaluated without schema validation | Deny | 1 |
| Broad permit plus forbid using absent `blocked` context | Allow | 1 |

The last two cases intentionally bypass schema-aware request checking only to inspect
language behavior. In a normal integration reject malformed requests at the input
boundary. Confirm the unsafe forbid fails validation against the example schema.

## Verification evidence and limits

The authoring check used the official **cedar-policy-cli 4.15.0**, reporting language
**4.7**, downloaded from the upstream release with its published SHA-256 checked.
The archive digest was `befc810b9527bfd97813bf061c45958dccf2ce6c8496ad725eab14a472c30a3c`.
The normal policy set passed strict validation and the eight decision/error assertions
were exercised with the CLI. The graph audit was checked against valid, duplicate,
cyclic, and missing-parent inputs. Re-run these checks on the chosen runtime.

These fixtures do not establish completeness of a real application's permission
model, managed-service compatibility, partial-evaluation correctness, or revocation
behavior. Those require the application's actual policies, data loaders, and deployment.
