# Shared record contract

## Integrate specialist outputs explicitly

Specialist templates retain domain-specific fields because a processing record, subscription review, incident record and accessibility journey are different objects. Do not pass them directly to an evidence checker that expects another schema. Preserve the source record and map its findings into the shared obligation/control register.

For each finding retain `finding_id`, originating skill/record, feature, entity, countries, profile revision, release/environment, observed facts, unknowns, source/version/provision, normative type, applicability, temporal state, implementation status, evidence, owner, due-date basis and reopening event.

Use these canonical states at the integration boundary:

| Dimension | Values | Meaning |
| --- | --- | --- |
| Applicability | `applicable`, `not_applicable`, `conditional`, `unknown` | Whether this duty attaches to the defined facts; a conditional decision still needs its conditions resolved before reliance |
| Temporal state | `applicable_now`, `future`, `transitional`, `unresolved` | The operative provision/cohort schedule, separate from applicability |
| Implementation | `planned`, `implemented`, `verified`, `failed`, `expired` | Current engineering/evidence state |
| Normative type | `binding_law`, `contract`, `guidance`, `standard`, `internal_policy` | Why a requirement exists and what legal effect it has |
| Review outcome | `ready_for_authorised_review`, `ready_with_nonblocking_followups`, `blocked`, `insufficient_evidence` | Scoped assessment, not the actor's release authority |

## Map without fabricating certainty

A specialist `needs-evidence`, `needs-review` or `unknown` remains unresolved; it never becomes `not_applicable`. A `gap` maps to the particular missing implementation/evidence requirement. A `satisfied` statement needs its actual basis inspected: a document review can satisfy one documentary control without proving runtime behaviour. Do not automatically convert it into `verified` for every linked control.

Map a documented `not-applicable` spelling to `not_applicable`, retaining its reason, source, reviewer, evidence and reopening event. When a specialist uses `future`, map the underlying scope decision separately from the future application date. A provision can apply to a product category in future while parallel present duties still attach now.

Do not alter a source record's meaning to make schemas align. Preserve raw findings and the normalisation decision so a reviewer can reconstruct it. A named owner in an unadopted template is not a real assignment, and a generated report is not a signed review.

## Build an assurance package

Select controls for the actual change in the reviewed scope. Create the evidence-report fields required by `eu-platform-agent-assurance`, binding them to the exact profile, release and environment. Supply real files/references and their observation dates. The checker can reject inconsistent packages but cannot decide whether this selection covers the law or whether the evidence proves the control.

Do not reuse this file's state taxonomy as a legal interpretation or a statutory report format. Regulatory forms and contractually agreed reports may need different fields; use their actual current requirements and preserve the common internal linkage.
