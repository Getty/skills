# Troubleshooting

| Symptom | Inspect first | Useful correction |
| --- | --- | --- |
| Everything permits | Empty/broad target, catch-all Permit, permit-overrides | Restore reviewed scope and combination |
| Everything is NotApplicable | Root selection, category/ID mismatch, target logic | Fix identity and applicability |
| Missing attribute causes Indeterminate | MustBePresent and subsequent bag extraction | Repair trusted fact source/cardinality |
| MustBePresent=false still errors | one-and-only over empty/multiple bag | Use correct bag function or explicit scalar contract |
| Two “equivalent” engines disagree | Algorithm URI/version, issuer mode, provider configuration | Compare exact feature profiles |
| XML passes XSD but PDP rejects | Function/algorithm support and policy references | Validate runtime capabilities |
| JSON endpoint rejects a policy | JSON Profile vs product administration format | Use the correct API/representation |
| Permit but access blocked | PEP obligations, correlation, local enforcement | Diagnose enforcement separately |
| First-applicable skips expected rule | Earlier applicable result, including error | Review rule order and target |
| Policy reload has no effect | Loaded root/version and cache | Verify active effective policy graph |
| Only-one-applicable errors | Multiple matching policy targets | Model scope uniqueness explicitly |

## Minimize without changing semantics

Capture the request, selected root policy, references, engine version/configuration,
attribute-provider outputs, and response status. Redact values without changing type,
cardinality, category, or applicability. Preserve issuer labels and whether attributes
were absent, empty, or multi-valued.

Inspect the first layer that can explain the result: transport/parse, root loading,
target matching, attribute resolution, function evaluation, combining, obligation
expression, then PEP execution. Do not blame policy logic for a request adapter that
placed an attribute in the wrong category.

Keep extended Indeterminate information when engine diagnostics expose it. A potential
Deny error combined with Permit differs from a potential Permit error combined with
Permit under deny-overrides. A generic Boolean trace loses this distinction.

For an implementation disagreement, produce the smallest policy/request pair that
still differs and identify the normative clause/profile. Do not alter expected
semantics merely to accommodate the first engine tested.

The bundled inspector is an inventory/schema tool, not a semantic debugger.
Its output can identify identifiers and namespaces but cannot explain a decision
without actual evaluator evidence.

Authority: [core specification](https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-en.html)
and [AuthzForce troubleshooting/configuration](https://github.com/authzforce/core).
