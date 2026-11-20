---
name: xacml-engineering
description: "Use when writing, validating or integrating OASIS XACML 3.0 access control — XML policies and requests, PDP/PEP/PIP, targets and conditions, attribute bags, combining algorithms, Indeterminate and NotApplicable, obligations and advice, the JSON Profile, AuthzForce."
---

# XACML Engineering

Treat XACML as a versioned authorization language and decision protocol. Keep
policy evaluation, attribute trust, and access enforcement separate. A PDP returning
Permit does not perform the protected action or discharge its obligations.

Use **XACML 3.0 Plus Errata 01 (2017-07-12)** and **JSON Profile of XACML 3.0
Version 1.1 (2019-06-20)** as the core baselines.
Select additional profiles and implementation support explicitly. Do not infer
obsolescence, adoption rates, or deployment suitability solely from publication age.

## Route to the needed reference

| Task | Read |
| --- | --- |
| Design PDP/PEP/PAP/PIP boundaries and trusted facts | [Architecture and enforcement](references/architecture-and-enforcement.md) |
| Author PolicySet, Policy, Rule, Target, and Condition | [Policy model and authoring](references/policy-model-and-authoring.md) |
| Resolve attributes, bags, cardinality, issuers, and functions | [Attributes and functions](references/attributes-and-functions.md) |
| Predict outcomes and combine policies correctly | [Decisions and combining](references/decisions-and-combining.md) |
| Enforce required effects and interpret advice | [Obligations and advice](references/obligations-and-advice.md) |
| Build XML/JSON request and response adapters | [Request and response profiles](references/request-and-response-profiles.md) |
| Choose RBAC, multiple-decision, delegation, or other profiles | [Profiles and capability selection](references/profiles-and-capability-selection.md) |
| Configure a real PDP or embed one | [Runtime integration](references/runtime-integration.md) |
| Validate schemas, behavior, and enforcement | [Testing and conformance](references/testing-and-conformance.md) |
| Publish policy, manage fact freshness, or improve performance | [Operations and lifecycle](references/operations-and-lifecycle.md) |
| Translate legacy or other authorization systems | [Migration and interoperability](references/migration-and-interoperability.md) |
| Diagnose mismatches or Indeterminate results | [Troubleshooting](references/troubleshooting.md) |
| Run original fixtures and helpers | [Worked examples](references/worked-examples.md) |
| Verify normative documents and implementation versions | [Sources and versioning](references/sources-and-versioning.md) |

Load references selectively. Use this skill independently of any application,
language, identity provider, or sibling skill. Refer to `cedar-engineering`,
`opa-rego-engineering`, `cel-engineering`, or `dmn-engineering` only for tasks
that also need those technologies.

## Establish the authorization contract

Inspect policies, requests, response handling, PDP configuration, and attribute
providers before proposing changes. Identify the protected action/resource, trusted
subject identity, relevant attributes and issuers, root policy/version, algorithm,
required profiles, and enforcement obligations.

For a synthetic example, choose explicit assumptions and proceed. For a repair,
capture a minimized request and all decision-relevant policy/configuration versions.
Do not infer that the business requirement is “allow” merely because a caller
expected a successful HTTP response.

## Build or repair the system

1. **Define the access question.** Distinguish subject identity, action, resource,
   and environmental facts. Document where trusted facts come from and their freshness.
2. **Choose the supported profile.** Pin core/errata, optional profiles, PDP/version,
   algorithms, datatypes/functions, request format, and extension configuration.
3. **Model scope and conditions.** Use targets for applicability and conditions
   for Boolean tests. Keep IDs stable. Make missing and multi-valued attribute behavior
   explicit; do not assume every attribute bag has exactly one value.
4. **Select combination semantics deliberately.** Name exact algorithm URIs, including
   rule versus policy variants and legacy versus 3.0 versions.
5. **Connect enforcement.** Grant only on an acceptable Permit result after required
   obligations can be satisfied. Preserve Deny, NotApplicable, Indeterminate, and
   transport failures as distinct diagnostic outcomes.
6. **Validate in layers.** Parse safely, validate pinned XSD/profile structure, load
   into the chosen PDP, exercise behavior, and verify PEP obligations/failure handling.
7. **Exercise meaningful cases.** Include Permit, Deny, no matching policy, missing
   required attributes, multi-valued scalar assumptions, overlapping rules, and
   unavailable attribute providers. Test actual result correlation for batch requests.
8. **Publish and report.** Preserve root-policy and attribute-source revisions,
   observed checks, limitations, and rollback. Do not equate schema validity with
   full conformance, trusted facts, or correct organizational policy.

## Preserve the critical semantics

- Preserve four external decisions: Permit, Deny, NotApplicable, and Indeterminate.
  The extended Indeterminate{P}/{D}/{DP} states affect internal combining; do not
  invent these as additional standard wire Decision values.
- An empty Target matches all. Within a Target, AnyOf elements combine conjunctively;
  each AnyOf contains alternative AllOf elements, whose Match elements are conjunctive.
- AttributeDesignator returns a bag. Missing with MustBePresent=false produces an
  empty bag; a subsequent one-and-only can still fail. MustBePresent is not a default.
- Match category, ID, datatype, and applicable issuer rules precisely. An issuer
  label alone is not proof of authenticity.
- Treat NotApplicable as absence of applicable policy, not as an explicit permit or
  an infrastructure failure. Keep the PEP's final enforcement rule separate.
- Deny-overrides is not the same as deny-unless-permit. Permit-overrides is not a
  general “secure default.” Algorithm names cannot replace their actual truth tables.
- Only-one-applicable concerns policy applicability, not “exactly one Permit rule.”
- Obligations are mandatory under their enforcement contract; advice is optional.
  A Permit with an unsupported obligation must not become unconditional access.
- The JSON Profile standardizes request/response interchange. It is not a generic
  JSON encoding for XACML policies or every product's administration API.
- Preserve exact identifiers. The normative 3.0 XML namespace ends in `schema:wd-17`;
  the historical suffix does not make it the wrong final namespace.

## Use the bundled examples and tools

```bash
python3 scripts/inspect_xacml.py assets/examples/training-policy.xml
python3 scripts/inspect_xacml.py assets/examples/training-policy.xml --xsd /local/xacml-core-v3-schema-wd-17.xsd --xml-xsd /local/xml.xsd
python3 scripts/run_cases.py --jar /trusted/authzforce-ce-core-pdp-cli-21.0.1.jar
```

The inspector safely parses bounded XML, inventories identifiers and algorithms,
and optionally validates with caller-supplied local official schemas. It disables
network/entity resolution and rejects DTD declarations. It does not evaluate policies
or validate an arbitrary PDP configuration.

The case runner executes a supplied trusted AuthzForce CLI against original local
fixtures. It checks decisions and obligation IDs. With the bundled local configuration it
performs no obligation effects or external provider calls. A supplied jar or alternate
configuration is trusted executable input and may enable such effects. The tested
engine profile is separate from normative XACML and newer engine releases.

## Return a useful diagnosis

Name the relevant request attribute, policy/rule, algorithm, and status when evidence
supports it. Distinguish policy outcome from attribute lookup, parser, transport, and
PEP execution failures. Provide corrected files and a regression case for repairs.
State any unsupported profile or untested enforcement path plainly.
