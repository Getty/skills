# Interoperability and neighboring formalisms

## Choose by the required question

| Question | Suitable role |
| --- | --- |
| Which actions can reach a goal from this abstract state? | PDDL planning |
| May this principal perform this operation now? | Cedar, Rego/OPA, XACML, or an authorization layer |
| Which business outcome follows from facts? | DMN/FEEL or another decision model |
| Is this object/request valid? | Schema validation, CEL, or validation rules |
| Which predefined steps follow an event? | Workflow/state-machine orchestration |
| When should known jobs use limited resources? | Scheduling/constraint programming |
| How should a high-level task decompose by domain methods? | HTN planning |
| What should be done under uncertain observations/outcomes? | A suitable contingent/probabilistic/epistemic model |

PDDL is useful for choosing a sequence rather than merely checking a single condition.
It does not automatically supply authentication, policy combining, user approval,
workflow durability, compensation, or world observations. Keep those contracts in
the host application and expose their results as clearly sourced facts where useful.

## Integrate with a typed world model

Map application objects to PDDL symbols using a stable registry. If upstream data is
RDF or a knowledge graph, choose the finite subset and translate open-world knowledge
into the planning model deliberately. Missing RDF assertions are not automatically
false; classical PDDL's closed-world initial state makes a stronger assumption.

Represent resources and capabilities at the level needed for the goal. A planner
does not need an entire corporate ontology to route one parcel. Retain provenance
from each planning fact to the observation or record that supplied it so a plan can
be invalidated when that source changes.

## Avoid misleading translations

A Cedar permit is not an unconditional PDDL action effect. It is a decision under a
policy/data snapshot. A DMN eligibility result is not a guarantee that an execution
step succeeds. A workflow rollback is not always the inverse of its forward action.
Keep each translation's assumptions explicit and test counterexamples.

If publishing a planner service, define request and result envelopes separately from
PDDL syntax: input hashes, profile, engine configuration, status, plan, metric,
validation report, and errors. Preserve statuses such as timeout and unsupported
feature instead of collapsing them into an empty plan.

Use the [IPC source catalogue](https://ipc08.icaps-conference.org/deterministic/PddlResources.html)
for the boundaries of PDDL variants. Consult the optional sibling skills by name
when needed; this skill remains standalone and has no filesystem dependency on them.
