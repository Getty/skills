# Sources and versioning

Use normative OASIS publications for standard semantics and
implementation documentation/source for a product's support and configuration.

## Normative baseline

| Source | Status and purpose |
| --- | --- |
| [XACML 3.0 Plus Errata 01](https://docs.oasis-open.org/xacml/3.0/errata01/os/xacml-3.0-core-spec-errata01-os-complete.html) | OASIS Standard incorporating approved errata, 2017-07-12 |
| [Core XSD](https://docs.oasis-open.org/xacml/3.0/errata01/os/schema/xacml-core-v3-schema-wd-17.xsd) | Normative machine-readable structure |
| [W3C XML namespace schema](https://www.w3.org/2001/xml.xsd) | Imported schema dependency |
| [JSON Profile 1.1](https://docs.oasis-open.org/xacml/xacml-json-http/v1.1/os/xacml-json-http-v1.1-os.html) | OASIS Standard, 2019-06-20; request/response interchange |
| [OASIS standards archive](https://www.oasis-open.org/standards/) | Publication/status cross-check |
| [XACML committee](https://www.oasis-open.org/committees/xacml/) | Profiles and current work |

The core publication lists its DOC as authoritative and publishes HTML/PDF
representations. Normative machine-readable artifacts prevail over displayed
definitions where the publication says so. Preserve this distinction in a dispute.

Core XSD SHA-256 inspected:
`f548f8f9ee422ea7107821c2f66822d173beccb238f53b176f8466f53367f37a`.

## Implementation evidence

- [AuthzForce Core](https://github.com/authzforce/core): embedded PDP, CLI, extensions,
  migration, provider and preprocessor behavior.
- [AuthzForce Server](https://github.com/authzforce/server): multi-tenant PAP/PDP service.
- [Maven CLI artifact 21.0.1](https://repo.maven.apache.org/maven2/org/ow2/authzforce/authzforce-ce-core-pdp-cli/21.0.1/):
  exact executed test binary and published checksum.
- [OASIS 2.0/3.0 differences](https://wiki-static.oasis-open.org/xacml/DifferencesBetweenXACML2.0AndXACML3.0):
  migration context, subordinate to normative publications.

Executed `authzforce-ce-core-pdp-cli-21.0.1.jar` SHA-256:
`44b3212f15e0bae5e3410bfe5b6fd4b9a613ce7a687413c185d98cf866691107`.
The downloaded artifact matched its published SHA-1 checksum. This records retrieval
integrity, not a comprehensive supply-chain assurance claim. No third-party binary
or normative schema is bundled with the skill.

The tested artifact, current development README, and a newer product release need
not have identical support. The README describes JSON Profile 1.0 support; the
skill's normative JSON baseline is 1.1. Only the explicitly tested common subset
is claimed for this binary. Verify required 1.1 features on the chosen deployment.

## Refresh procedure

1. Check core errata and each selected profile's publication/status.
2. Pin schemas, engine binary, modules, configuration schema, and provider behavior.
3. Compare function, datatype, algorithm, and profile support.
4. Run the relevant conformance subset and original behavioral fixtures.
5. Test the PEP and required obligations separately.
6. Update evidence and unsupported/untested layers without rewriting expectations
   solely to make a new implementation pass.

All fixtures and helper code are original educational material. Refer to upstream
licenses and notices before redistributing their schemas, documents, or binaries.
Do not infer current market adoption from document age.
