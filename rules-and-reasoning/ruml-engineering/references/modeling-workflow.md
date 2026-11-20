<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# From source material to a reviewable RUML rulemap

Baseline: RUML **1.0.0**, wire version **`"1.0"`** at commit
`d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4`.
The workflow is **Engineering advice**, grounded in the cited format requirements; its worksheets
and review stages are not new RUML fields or mandatory standard processes.
Reference material adapts specification text © 2026 Rulemapping Group GmbH, **CC BY-SA-4.0**;
upstream schemas/tests/examples are **Apache-2.0**. See [licence](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/LICENSE.md).

## Contents

- [Define the decision and freeze the source](#define-the-decision-and-freeze-the-source)
- [Extract propositions before building nodes](#extract-propositions-before-building-nodes)
- [Normalize facts and preserve evidence](#normalize-facts-and-preserve-evidence)
- [Choose the smallest faithful construct](#choose-the-smallest-faithful-construct)
- [Worked fictional model and decision table](#worked-fictional-model-and-decision-table)
- [Review interpretation and test execution separately](#review-interpretation-and-test-execution-separately)
- [Release and change review](#release-and-change-review)

## Define the decision and freeze the source

Start with one sentence describing what the root's true and false results mean. Specify the subject,
decision date, relevant source version and intended use. A rulemap for eligibility is a different
artifact from a procedure for requesting evidence, even if both concern the same application.
Use `metadata.documentType` for the document's classification; it does not replace this analysis.

Collect source text plus referenced definitions, exceptions, tables, amendments and effective-date
rules before extracting operators. Record a stable source identifier, version and precise location
for every proposition. Preserve the distinction between text that **creates the rule**, explanatory
material, and documents being examined in a particular evaluation.

The standard supports this separation through:

- `ruml:text-reference`: foundational normative text; a node may have one `represents` anchor and
  additional `refers-to` anchors for definitions or cross-references.
- `ruml:context`: supporting materials and documents under examination; `subject: true` marks the
  latter, while query-specific context roles state how that material is used.
- `ruml:tree-reference`: links to nodes of another versioned RUML document, whose own nodes carry
  their local text anchors. Do not create a local text anchor into another RUML file's registry.

Text and context registries belong in the relevant root capability's **`payload.data`**, with node
references inside its node-level payload. Some older prose abbreviates this as a root `data` field;
the schema has no such root property. Use the current capability structure.

Sources: [§3.3](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-3-metadata-object.md), [§4.12 texts and anchors](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-12-ruml-text-reference.md), [§4.11 context](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-11-ruml-context.md), [§4.15 external references](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-15-ruml-tree-reference.md).

## Extract propositions before building nodes

Build a separate modeling worksheet with source span, proposed proposition, subject, time, evidence
needed, exception relationship and unresolved interpretation. These are worksheet columns, not
additional `.ruml` root/node fields. Preserve the original wording alongside its proposed executable
meaning so reviewers can inspect what was inferred.

Break a compound sentence into propositions whose outcomes can be explained independently. Keep
negation scope explicit: “not both A and B” differs from “neither A nor B”; “unless E” may override
one prerequisite, the whole rule, or only a consequence. Do not choose the scope merely from the
nearest noun or punctuation. Definitions may change multiple branches at once.

For each numerical rule, settle the comparator, unit, reference period, rounding point, boundary
inclusion and aggregation population. “At least 3” and “more than 3” are distinct. A majority needs
a denominator and a tie rule; abstentions or unavailable evidence need an explicit interpretation.
RUML's combiner guard propagates any undefined child before executing a count, regardless of the
threshold's mathematical bounds.

Keep alternative interpretations as review alternatives until resolved. A draft may use the
`undefined` operator where structural aggregation is undecided, but a completed branch should not
be assigned AND simply to make the file executable. A format validator cannot decide whether the
source's exception, burden of proof or temporal scope was interpreted correctly.

Sources for the available constructs: [§3.5 nodes](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-5-node-object.md), [§3.6 operators](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-6-operators.md), [§4.14 expressions](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-14-ruml-expression.md).

## Normalize facts and preserve evidence

Separate three artifacts: the rule definition, the evidence, and the normalized case input consumed
by the evaluator. An extracted claim is not automatically an established fact. Record source
location and review state in the evidence workflow, then bind only the adopted value into the
case's datapoint input document. Preserve conflicting evidence rather than silently selecting the
first value or converting missing evidence to false.

| Modeling concern | Portable RUML mechanism | What remains an implementation responsibility |
| --- | --- | --- |
| Named, typed fact | `ruml:datapoints` entry with `name`, `type`, `binding` | Evidence-to-value resolution and domain meaning |
| Repeated structured entities | Datapoint `type: "object"`, named `set`, optional `cardinality` | Choosing which entity a runtime occurrence evaluates |
| Derived amount or date | `binding.type: "computed"` and JSONata expression | Review units, rounding and dependency meaning |
| Human/external input | `input` or `external` binding; symbolic external `ref` | Concrete service mapping and acquisition procedure |
| Source document under examination | `ruml:context` with subject role | Case-specific retrieval and evidence review |
| Why a predicate exists | Local text anchors or versioned tree references | Interpretation approval |

For each input, document whether absence means unknown, inapplicable or false under the actual
rule. RUML query input omits datapoints without a value. `undefined` is an evaluation status, not
a magic input literal; a string `"undefined"` is still a string. `null`, zero and empty string are
also not interchangeable with absence. Check the JSONata expression's result for the exact missing
input case instead of assuming every comparison propagates missingness.

Prefer boolean-valued facts for already established yes/no findings and typed values for measurements.
For a declared boolean datapoint, the query expression `dp_registered` directly returns its boolean
value and yields no result when the entry is absent. By contrast, an arbitrary comparison may have
different missing-value behavior. A query's nonboolean/no-result outcome maps to node undefined.

Normalize units and relevant times before comparison, while retaining the original evidence.
Computed datapoint dependencies must be acyclic; reusable set definitions must not recurse either.
Those are different constraints from the permitted self-recursion of modular rule nodes.
Do not store extraction confidence as a node truth value. If AI participates in deciding a leaf,
declare `ruml:ai-query`, its inputs and policy explicitly; keep judgments traceable to evidence.

Sources: [§4.7 datapoints and sets](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-7-data-points.md), [§4.8 query result contract](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-8-ruml-query.md), [§4.9 AI queries](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-9-ruml-ai-query.md).

## Choose the smallest faithful construct

| Interpreted relationship | Candidate construct | Review question |
| --- | --- | --- |
| Every prerequisite applies | `AND` | Is early undefined allowed to stop optimized evaluation before a later false? |
| Any alternative suffices; inspect all alternatives | `OR` | Are all branches meant to be visited even after a true? |
| Ordered alternatives with early exit | `XOR` | Is its legal exclusivity premise appropriate? It does not enforce exactly one. |
| Negation of a complete aggregate | `NOT_AND`, `NOT_OR`, `NOT_XOR` | Which entire proposition is negated? |
| Threshold, quorum, exactly-one count or selected-child combination | `DELEGATED` + `ruml:expression` | Is there a prose rule, declared required support, and understood undefined behavior? |
| One predicate over case facts | Leaf + `ruml:query` | Does it return a boolean and use declared datapoints? |
| A value consumed elsewhere | Computed datapoint | Is this a value calculation rather than a node's truth decision? |
| Repeated check under the same rule definition | Modular node | Are normative anchors shared and occurrence input binding defined? |
| External descriptive dependency | `ruml:tree-reference` | Is a link sufficient, or must the other subtree actually execute? |
| External executable dependency | `ruml:tree-include` | Are version resolution, leaf restriction and inclusion-cycle rules satisfied? |
| Effect following a decision | `ruml:actions` | Is it a reaction to status rather than part of logical aggregation? |

Do not encode an ordinary conjunction in opaque JSONata without a reason. The specification
recommends warning when a delegated expression is equivalent to a logical operator.
Keep an exception as an independently reviewable branch where its scope permits; a single-child
negated parent can express absence of one exception without negating unrelated prerequisites.

Sources: [§3.6](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-6-operators.md), [§4.10 actions](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-10-ruml-actions.md), [§4.16 inclusion](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-16-ruml-tree-include.md).

## Worked fictional model and decision table

**Original example, not a real regulation or an upstream fixture:** a program accepts a registered
applicant who meets at least two of three criteria, unless an exclusion applies. Interpret the
exclusion as applying to the whole eligibility decision, and treat unresolved input as unknown.

| LexID | Label | Structure / expression |
| --- | --- | --- |
| `"1"` | Eligible | `AND`, children `["2", "3", "7"]` |
| `"2"` | Registered | Query `dp_registered` |
| `"3"` | At least two criteria | `DELEGATED`, children `["4", "5", "6"]`; expression `$count($children[status = "true"]) >= 2` |
| `"4"`, `"5"`, `"6"` | Criterion A / B / C | Queries `dp_criterion_a`, `dp_criterion_b`, `dp_criterion_c` |
| `"7"` | No exclusion | `NOT_OR`, children `["8"]` |
| `"8"` | Exclusion applies | Query `dp_excluded` |

For a full file, give every node a unique UUID and label; declare the five boolean datapoints and
`ruml:query`; declare `ruml:expression` with `required: true`; put the threshold's prose description
inside the expression payload. Add metadata and source references as appropriate. This table is a
modeling worksheet, not a substitute file format.

`T`, `F`, `U` below mean true, false, undefined after leaf evaluation; unknown boolean input is
omitted from the input object. Outcomes follow the specified operators, not an invented policy.

| Registered | Criteria A/B/C | Exclusion applies | Optimized root | Complete root |
| --- | --- | --- | --- | --- |
| T | T/T/F | F | T | T |
| T | T/F/F | F | F | F |
| T | T/T/F | T | F | F |
| T | T/T/U | F | U | U |
| U | T/F/F | F | U | F |
| T | T/T/F | U | U | U |

The fourth row is deliberately strict: a mathematically sufficient count does not bypass RUML's
undefined-child guard. In the fifth, optimized AND stops at registration and skips the threshold
and exclusion branches; complete mode discovers the false threshold. In the second, optimized
mode skips node `"7"` after the threshold fails and therefore omits its descendant `"8"` from the
result map. These trace differences belong in review because they affect which evidence is sought.

Semantic basis: [§3.6](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-6-operators.md), [threshold conformance cases](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/03-data-model/3-6-operators--delegated-evaluation.test.yaml), [§5.1 skipped descendants](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format/5-1-result-model.md).

## Review interpretation and test execution separately

Use three distinct review outputs. **Interpretation review** traces each predicate and exception
to its source and lists unresolved choices. **Format validation** checks JSON/schema plus semantic
constraints. **Execution verification** checks scenario outcomes and traces in the actual engine.
Passing one does not establish the other two.

For interpretation, ask whether every source prerequisite is represented, every inferred rule is
identified, exceptions attach at the correct level, and source versions/effective dates agree.
Read the map from labels and delegated descriptions before reading code; then verify expressions
actually implement that prose. Test at threshold boundaries and with each exception activated.

For execution, cover a positive case, each decisive negative branch, missing input before and after
a decisive sibling, combiner unknown propagation, conflicting leaf decisions, and both modes.
When modules or recursion appear, add occurrence-specific inputs, an exit case and the depth bound.
Use pinned upstream fixtures to check the engine; use domain scenarios to check this rulemap.
Do not mistake fixture acceptance for independent validation of the source interpretation.

Run schema validation with asserted formats, then reference, identity, lifecycle and capability
checks. Preserve duplicate-key evidence during JSON parsing. Report which layers actually ran.
Keep undocumented evaluator policies, such as some mixed undefined majority cases, visible instead
of describing them as guaranteed by the standard.

Sources: [§8 validation layers](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/08-validation/index.md), [spec-test contract](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/appendix/A-spec-tests/runner-contract.md), [§5.0–5.1 results](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format/5-1-result-model.md).

## Release and change review

Before review or release, replace draft parent operators, remove leaf operators and resolve the
source-to-node map. Record content version and times, capability/runtime requirements, evaluation
mode, external mappings, interpretation decisions and verified scenarios in the release record.
The latter is project documentation, not a request to add arbitrary fields to `.ruml` metadata.

For a changed rulemap, compare more than text diffs: child order, fallback capability order,
threshold populations, negation scope, source version, datapoint normalization, module contexts and
external subtree versions can all alter behavior. Re-run affected boundary and missing-data cases.
Changes to child order also change result paths; preserve enough identity information to interpret
older results against their original document.

Use a new document UUID, draft status and `derivedFrom` when making a working copy of an in-force
document. Keep document lifecycle status distinct from node evaluation status. A structural draft
is not automatically ready for publication; conversely `published` is not a legal metadata enum.
When packaging is required, verify the container's hashes and signatures separately from JSON
validity. A hash detects changes but does not establish who approved an interpretation.

Sources: [§3.3 lifecycle](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-3-metadata-object.md), [§3.8 change validation](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-8-integrity-validation.md), [§2.4 integrity](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/02-file-format-basics/2-4-integrity.md).
