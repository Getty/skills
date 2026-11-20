# Governance and provenance

## Keep model identity separate from execution evidence

Assign a stable identity to the business decision and immutable revisions to
released models. Store the exact source artifact or hash, runtime/profile version,
entry point, input snapshot identity, result, relevant diagnostics, and evaluation
time. If an external reference dataset influences the result, record its version.
A timestamp without the input/model versions is insufficient for replay.

Attach source references to the narrowest useful decision or rule. Preserve source
edition, relevant section, applicability period, and the interpretation decision.
A link to a policy document establishes traceability, not that the executable rule
is a correct or legally sufficient interpretation.

## Review changes by effect

Explain which input partitions change outcome and why. Run a before/after case set
and inspect changed results, new diagnostics, and lost coverage. Keep business
approval, technical validation, and deployment authority as distinct responsibilities
appropriate to the user's existing workflow; do not invent extra approval gates.

Use effective dates as explicit inputs or model-selection rules. Do not replace the
historical model and then claim to reproduce a past decision using today's rules.
When correcting an error, retain both the original observed result and the corrected
re-evaluation if the application requires that distinction.

## Explain results without inventing a trace

Report the actual selected decision, relevant bound facts, and matching rule IDs
when available. Explain intermediate calculations only if they were observed or
recomputed with a clearly stated method. A language model can produce a readable
explanation from a trace, but that explanation is not additional execution evidence.
Keep sensitive values out of routine logs and retain protected replay evidence only
where required by the application.

Annotations can carry useful business comments, but DMN does not standardize a
universal runtime API for retrieving all matched annotations. Do not promise a
portable explanation interface based only on a modeler's UI.

## Establish operational ownership

Record who maintains data contracts, model logic, engine upgrades, and action
integration. Specify rollback by model revision and test it through the same entry
point used by callers. Replaying a decision should remain separate from replaying
action effects.

DMN's model and annotation constructs are defined in the
[OMG specification](https://www.omg.org/spec/DMN/1.6/PDF). The logging, release,
and replay arrangements above are application design recommendations rather than
additional requirements imposed by the standard.
