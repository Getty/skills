# Worked examples and helper limits

## Original shipping-lane model

`assets/examples/shipping-lane.dmn` is an original educational DMN 1.6 model.
It contains two inputs, one decision, two information requirements, and a three-row
Unique table. It deliberately omits diagram layout and vendor extensions.

The synthetic contract accepts a nonnegative numeric weight in kilograms and an
urgency enum of `normal` or `urgent`. Urgent shipments select `express`; normal
shipments at or below 10 kg select `economy`; heavier normal shipments select
`freight`. The case file records five valid outcomes and four host-level invalid
input outcomes. Those invalid-input outcomes belong to the application contract;
they are not claims about one engine's response when bypassing validation.

Do not use the policy as a real shipping recommendation. It exists to illustrate
domain coverage, an exact threshold, explicit input binding, and separation of
input validation from decision evaluation.

## Inspect the artifact

Run from the skill directory:

```bash
python3 scripts/inspect_dmn.py assets/examples/shipping-lane.dmn
```

The helper supports UTF-8 XML up to 10 MiB, rejects DTD/entity declarations, and
inventories decisions/tables. It checks duplicate IDs, unresolved local references,
selected reference endpoint kinds, cycles in local decision information requirements,
row cell counts, hit-policy spelling, and basic aggregate/output compatibility.
External references are listed but not resolved.

A successful result means these selected checks passed. It does not prove complete
model semantics, valid FEEL, table coverage, correct imports, or correct business
interpretation. A DMN-looking namespace is inventoried; its full grammar requires
the chosen official XSD.

## Add actual schema validation

Provide `lxml` in the Python environment and a locally complete schema set:

```bash
python3 scripts/inspect_dmn.py assets/examples/shipping-lane.dmn \
  --schema /path/to/DMN16.xsd
```

Obtain DMN16, DMNDI15, DI, and DC from the
[official DMN 1.6 artifact links](https://www.omg.org/spec/DMN/1.6).
The helper disables network/entity resolution and does not download schemas.
Exit 0 means selected checks passed; exit 1 means a detected model/parsing/schema
problem; exit 2 is used for command-line usage or a missing `lxml` dependency.
Schema configuration errors may also be reported as exit 1 with their actual message.

## Recorded verification and remaining layers

The example passed the bundled inspection and validation against the
official DMN16 XSD with its imported schema set. A broken local reference, duplicate
ID, and DTD-bearing file were each rejected by the helper. The case JSON parsed,
and the model is well-formed XML.

**No complete DMN runtime was executed for this bundled model.** Therefore the
case file contains expected business outcomes, not claimed engine observations.
To complete runtime verification, load the exact model into a chosen DMN 1.6-capable
engine or deliberately migrate to its supported profile, invoke `shipping-lane`,
and compare all cases through the documented host input adapter. Record the
engine/version and distinguish model execution from host validation failures.
