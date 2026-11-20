# Worked examples

## Synthetic training-record access

The example policy permits active subjects with an analyst role to read training
records. It explicitly denies suspended subjects. It uses 3.0 deny-overrides and
returns an audit obligation on Permit. This is a synthetic authorization example,
not a statement about organizational or legal requirements.

Files in `assets/examples`:

- `training-policy.xml`: two rules and an explicit action/resource target.
- `authzforce-pdp.xml`: product configuration selecting that root policy.
- `request-*.xml`: seven original contexts.
- `request-permit.json`: equivalent single-request JSON-profile context.
- `cases.json`: expected decisions and obligation IDs.

| Case | Expected decision | Purpose |
| --- | --- | --- |
| Active analyst, read | Permit | Normal access plus audit obligation |
| Suspended analyst | Deny | Explicit prohibition |
| Write instead of read | NotApplicable | Outside target |
| Active viewer | NotApplicable | No matching permit |
| Missing status | Indeterminate | Required fact unavailable |
| Two status values | Indeterminate | Scalar extraction fails |
| Analyst plus viewer roles | Permit | Legitimately multi-valued role bag |
| Active analyst via JSON | Permit | Request/response adapter subset |

The policy requires exactly one status but permits multiple roles. Its obligation
handler is deliberately outside the evaluator. No helper performs audit writes.

## Parse and validate offline

Requires Python 3 and `lxml`. Supply the official XACML core XSD and its W3C
`xml.xsd` dependency locally:

```bash
python3 scripts/inspect_xacml.py assets/examples/training-policy.xml
python3 scripts/inspect_xacml.py assets/examples/training-policy.xml --xsd /local/xacml-core-v3-schema-wd-17.xsd --xml-xsd /local/xml.xsd
```

The resolver maps the core schema's explicit W3C import to the provided local file
and rejects unmapped dependencies. The helper does not fetch schemas or evaluate
policies. It inventories IDs, functions, algorithms, and designators. Successful
schema validation does not establish supported algorithms or correct business intent.

## Execute the pinned local PDP profile

Use a trusted AuthzForce Core CLI jar and a compatible Java runtime:

```bash
python3 scripts/run_cases.py --jar /trusted/authzforce-ce-core-pdp-cli-21.0.1.jar
```

The runner launches the CLI against each original context, requires a single result,
and compares Decision and obligation IDs. It supports both included request formats.
With the bundled configuration it performs no obligation effects or external PIP
requests. Review any alternate configuration for network access and side effects.
The supplied jar is trusted executable code, not sandboxed data.

The JSON response uses `Id` for obligation identity, while XML uses `ObligationId`.
The runner deliberately reads each format according to its representation.

## Observed verification

- Policy plus seven XML requests: **8/8** accepted by the official core XSD.
- Pinned AuthzForce Core CLI 21.0.1: **8/8** decision/obligation cases passed.
- Parser rejection probes: DTD, wrong namespace, malformed XML, wrong root.
- Helper rejection controls: a deliberately incorrect expected decision fails.
- Basic skill metadata, local links, JSON parsing, and helper syntax checked.

The runtime observation covers the common single-request JSON subset used here;
it does not establish complete JSON Profile 1.1 conformance. No live PEP, actual
obligation handler, external PIP, XPath, delegation, or multi-decision profile was
tested. The binary is a reproducible test profile, not a “latest production” recommendation.
