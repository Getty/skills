# Obligations and advice

## Model enforcement requirements explicitly

An obligation carries required work associated with an effect. Examples include
audit recording, applying a mask, or attaching a handling label. Define each
ObligationId's semantics in the PEP contract, including assignment types, timing,
failure behavior, and idempotency. The PDP returns instructions; it does not perform
the external work merely by evaluating an ObligationExpression.

Advice communicates optional information. Do not move mandatory work into advice
to avoid integration effort. Conversely, do not make informational hints mandatory
unless denying access when they cannot be processed is intended.

## Preserve evaluation and combination

Obligation/advice expressions can occur at supported levels of the policy hierarchy.
Their applicability depends on effect and contribution under the selected combining
algorithm. Do not collect every obligation appearing in every policy file.
An error computing a relevant expression can affect evaluation, so test the resulting
decision as well as the returned assignment.

For a Permit response, execute or guarantee required obligations at the correct
enforcement point. If an obligation is unknown, invalid, or cannot be fulfilled,
do not grant unconditional access. Preserve a distinct enforcement failure reason;
this is different from a PDP deciding Deny.

A masking obligation is particularly sensitive: filtering fields after an unrestricted
response has already been sent is too late. Define which component applies the
restriction and verify that downstream code cannot bypass it.

## Test the PEP separately

Policy tests should check the returned obligation IDs and assignments. Integration
tests should check actual execution: recognized/unknown ID, malformed assignment,
unavailable handler, retries, duplicate delivery, and partial completion. For an
audit requirement, determine whether recording must succeed before access or can
be durably guaranteed as part of the transaction.

Do not perform real effects while merely displaying stored responses or running
a policy fixture. The bundled runner verifies returned IDs only. It does not
demonstrate that an audit record was written or that a mask was applied.

Log policy decision and enforcement result separately. A Permit followed by failed
obligation handling should be diagnosable without pretending the PDP emitted Deny.

Authority: [core obligations, advice, and PEP behavior](https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-en.html).
