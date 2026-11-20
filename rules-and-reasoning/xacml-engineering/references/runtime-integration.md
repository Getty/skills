# Runtime integration

## Configure a real PDP

Pin a PDP build and its configuration schema. Load policies through the selected
policy provider and select the root policy explicitly. Treat provider modules,
datatypes, functions, preprocessors, and result postprocessors as runtime dependencies.
Do not mix configuration examples from different engine generations.

For the tested AuthzForce Core CLI profile, a pdp configuration names a StaticPolicyProvider,
policy location, and rootPolicyRef. This configuration is product-specific; it is not
a XACML Policy document. The included configuration is for the tested local example,
with no external attribute provider or live action.

The upstream CLI form is:

```bash
java -jar /trusted/authzforce-ce-core-pdp-cli-21.0.1.jar -p pdp.xml request.xml
java -jar /trusted/authzforce-ce-core-pdp-cli-21.0.1.jar -p -t XACML_JSON pdp.xml request.json
```

Use the exact version documented for the example, or deliberately retest an upgrade.
The skill does not recommend this older binary as the latest production release.
Inspect the installed CLI help rather than assuming flags or administration URLs.

## Isolate XML resolution

Disable DTDs, external entities, and network schema resolution in general input
processing. Pin local schemas and their imports. An example that fetches schemas
over HTTP at runtime is not necessary for a hardened deployment. Preserve the
official schema's namespace; configure a local resolver/catalog rather than editing
standard identifiers to fit a tool.

Separate XML validity from policy loading. The PDP must resolve supported algorithms,
function IDs, policy references, attribute providers, and variable dependencies.
An XSD does not check the organizational meaning of those choices.

## Bind and consume requests

Build request attributes from trusted application facts. Validate category, datatype,
issuer rules, and cardinality. Preserve the actual operation's resource/action.
Decide whether a provider may fill missing attributes or override supplied values;
test that choice explicitly.

On response, verify request correlation and an acceptable Decision. Process required
obligations through known handlers. Preserve status information without exposing
sensitive raw attributes to an untrusted client. Treat exceptions and timeout as
technical failures, not successful evaluation with an omitted result.

## Measure the whole path

Separate parse/load time, provider lookups, expression evaluation, response processing,
and enforcement work. Reuse a loaded immutable PDP instance where the engine supports
it. Avoid recreating the complete policy graph for each request. Benchmark realistic
attribute distributions and worst-case policy applicability, not only one simple Permit.

Authority: [AuthzForce Core API/CLI](https://github.com/authzforce/core),
[server API responsibilities](https://github.com/authzforce/server), and
[core schema](https://docs.oasis-open.org/xacml/3.0/errata01/os/schema/xacml-core-v3-schema-wd-17.xsd).
