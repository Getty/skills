# Testing and conformance

## Separate evidence layers

| Check | What it establishes |
| --- | --- |
| Bounded secure XML parsing | Well-formed accepted input under parser policy |
| Official XSD | Structural validity against that schema |
| Engine loading | Supported identifiers, configuration, and references |
| Policy fixtures | Actual decision/status/obligations for named requests |
| Relevant conformance suite | Behavior on that suite and feature subset |
| PEP integration | Enforcement and obligation handling in the application |
| Requirement review | Modeled policy matches reviewed organizational intent |

Do not claim full XACML conformance from a few examples or schema validation.
Preserve exact versions and enabled options for each result. Conformance of a PDP
does not authenticate facts or implement a correct PEP automatically.

## Build a revealing corpus

Include all four external outcomes. Exercise missing required attributes, explicit
empty bags, duplicate/multiple values where scalar cardinality is assumed, datatype
mismatch, issuer differences, and outside-target requests. For combining, test
conflicting Permit/Deny and error states with different potential effects.

Test obligations and advice separately from the decision. Include unsupported
obligation IDs and failures in assignment expressions. For policy references,
test unavailable IDs, version selection, and cycles. For selectors/providers, test
their failures in addition to ordinary successful data retrieval.

For batch profiles, verify expansion/correlation and partial errors. For the PEP,
simulate unavailable PDP, malformed response, stale decision, and failed obligation
handler. These are not ordinary negative business decisions.

## Use independent expectations

Derive expected decisions from the reviewed policy requirement and normative
semantics, not by copying the output of the engine under test. Keep reason notes
with cases. A result change on an engine upgrade should trigger investigation,
not automatic rewriting of expected values.

For migration, run old/new engines against identical facts and compare Decision,
Status class, obligations/assignments, advice where relevant, and included-policy
identifiers. The application may deliberately ignore optional fields, but that
normalization must be explicit.

## Bundled verification

The example covers Permit, Deny, NotApplicable, and Indeterminate on a named local
PDP. The parser/schema helper has negative probes for DTD, wrong namespace, broken
XML, and wrong root. The runner asserts returned obligation IDs without performing
their effects. It does not test every datatype, profile, or implementation.

Authority: [normative core](https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-en.html)
and [AuthzForce conformance fixtures](https://github.com/authzforce/core/tree/develop/pdp-testutils/src/test/resources/conformance).
