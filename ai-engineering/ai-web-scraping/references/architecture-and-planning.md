# Architecture and planning

## Choose what AI should do

| Role | Suitable work | Main failure | Required control |
| --- | --- | --- | --- |
| Development assistant | Propose selectors, code, schemas | Overfits one template | Review code and test held-out snapshots |
| Extraction model | Interpret prose into a schema | Unsupported value or wrong entity | Source regions, validation, labeled evaluation |
| Browser planner | Navigate unfamiliar interactive UI | Loops, side effects, wrong terminal state | Bounded actions and verified postconditions |
| Classifier/router | Classify templates, propose paths, select fallback | Discards useful pages | Routing recall, rejected samples, confirmation against actual responses |
| Repair assistant | Propose fixes when monitored invariants fail | Plausible wrong field | Quarantine affected output until regression fixtures pass |

Combine roles only when the workload benefits. A model that proposes a selector once, with a parser executing it repeatedly, is an AI-assisted pipeline even when production records need no model call.

## Define the contract

Infer defaults from the task; ask only when a missing choice changes deliverable, access, cost, or meaning. Record output format, URL/path/locale scope, entity and variant identity, field semantics, evidence, freshness, resource limits, and acceptance thresholds.

Distinguish a known URL list, a known inventory, listing totals, and an unknown site universe. One page can hold many entities and one entity can appear in several views, so define page identity and business identity separately. A model's confidence score establishes neither inventory nor completeness.

Sample ordinary records, missing fields, alternate templates, and pagination edges. Preserve source variants instead of flattening them into an assumed universal record.

## Separate stages

1. **Discovery:** emit candidate URL, parent, and discovery source.
2. **Scope:** admit or reject under a versioned policy.
3. **Acquisition:** fetch/render; emit status and immutable snapshot metadata.
4. **Preparation:** derive text, DOM regions, tables, or images with transform identity.
5. **Extraction:** propose records and field evidence against that representation.
6. **Validation:** accept, reject, or quarantine with machine-readable reasons.
7. **Persistence:** write observations/entities idempotently and retain lineage.
8. **Delivery:** export agreed data plus coverage and error information.

Keep model work replaceable at a clean boundary. After a schema change, re-extract retained snapshots instead of refetching when retention and freshness permit. Separate fetch failures from interpretation failures so retries target the right stage.

## Explore then repeat

For repetitive sites:

1. Sample multiple templates and unusual records.
2. Inspect response JSON, JSON-LD, and DOM; identify stable source IDs.
3. Optionally ask a model for a declarative plan with base/field selectors.
4. Restrict selector and transform features; never execute generated code with production credentials.
5. Replay on training and held-out fixtures, comparing values and counts.
6. Version the approved plan by site/template and data contract.
7. Run deterministic extraction; fall back only on named failures such as an unknown template.
8. Retain fallback cases; promote repaired plans only after replay.

Automatic repair must never change field meaning silently: a neighboring price can satisfy a selector while violating the contract, and a browser agent can reach a plausible page without completing the task.

## Build a vertical slice

Produce the final output format from a small, varied source set. Confirm required fields survive filtering before optimizing tokens. Measure requests and usable snapshots, browser actions/time, model calls/tokens/truncation, unique entities and required-field coverage, rejected records, and cost per accepted entity ([evaluation](evaluation.md)).

Scale only after the slice passes, raising one capacity limit at a time while watching site responses and downstream queue age. For production crawling use an established frontier and scheduler, not a recursive loop; [Scrapy's architecture](https://docs.scrapy.org/en/latest/topics/architecture.html) is a mature model. Record the outcome as in [tool selection](tool-selection.md#record-the-decision).
