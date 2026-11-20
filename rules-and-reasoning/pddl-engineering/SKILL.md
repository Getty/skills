---
name: pddl-engineering
description: "Use when modeling, generating, solving, validating or debugging PDDL planning domains and problems — STRIPS/ADL, typed actions and goals, numeric fluents and action costs, durative or concurrent plans, derived predicates, timed initial literals, preferences and trajectory constraints, planner choice, Fast Downward, VAL or pyperplan, execution monitoring and replanning, or agents that hand planning to a planner."
---

# PDDL Engineering

Treat PDDL as a family of planning-language profiles describing an abstract state,
available transitions, and a goal. Keep model validity, search outcome, plan validity,
and faithful execution separate. A found and validated plan is a witness that the
modeled goal is reachable under the model's assumptions; it is not a proof that
real-world execution will succeed or be safe.

Use the original PDDL/IPC publications for language semantics and each planner's
current capability documentation for execution support. Do not label a planner
simply “PDDL-compatible” without identifying its supported features. Read [sources and versioning](references/sources-and-versioning.md).

## Select the relevant reference

| Task | Read |
| --- | --- |
| Choose a PDDL family and requirement profile | [Scope and feature profiles](references/scope-and-profiles.md) |
| Design predicates, types, actions, and invariants | [Domain modeling](references/domain-modeling.md) |
| Build a problem instance, initial state, and goal | [Problems and goals](references/problems-and-goals.md) |
| Model resources, numeric effects, and cost objectives | [Numeric fluents and costs](references/numeric-and-costs.md) |
| Model durations, concurrency, and temporal validity | [Temporal planning](references/temporal-and-concurrency.md) |
| Use derived facts, timed literals, constraints, or preferences | [Derived facts and constraints](references/derived-and-constraints.md) |
| Select a planner, heuristic, and search guarantee | [Planner selection](references/planner-selection.md) |
| Validate a candidate plan or diagnose a failure | [Validation and debugging](references/validation-and-debugging.md) |
| Connect plans to tools, observations, and replanning | [Execution and replanning](references/execution-and-replanning.md) |
| Reduce grounding and search cost without changing meaning | [Performance and compilation](references/performance-and-compilation.md) |
| Compare planning with workflows, authorization, or uncertainty models | [Interoperability](references/interoperability.md) |
| Run the small executable fixtures and helper | [Worked examples](references/worked-examples.md) |
| Check primary evidence and refresh implementations | [Sources and versioning](references/sources-and-versioning.md) |

Load targeted references rather than the entire bundle. Keep the examples' synthetic
warehouse facts distinct from facts about a real environment.

## Establish the planning task

Inspect supplied domain/problem files, planner command, logs, and plan before rewriting.
Identify the state abstraction, object universe, actions, desired terminal condition,
required invariants, and optimization objective. Determine whether actions are
instantaneous or durative, deterministic or uncertain, and whether the world can
change while the plan runs.

Record the planner, version/build, search configuration, feature requirements,
time/memory limits, plan format, validator, and numeric tolerance. Use a small labeled
example when requirements are unspecified; ask only when the missing modeling choice
changes which plans should count as valid.

## Model and solve systematically

1. **Define the goal and invariants.** State what must hold at the end and what must
   remain true throughout. A final-state goal does not enforce a trajectory condition.
2. **Choose the smallest adequate profile.** Start with typed STRIPS for deterministic
   finite-state action sequencing. Add ADL, numeric, temporal, or preference features
   only when their semantics are needed and the selected planner supports them.
3. **Define objects and state facts.** Separate static facts from fluents. Declare
   types and predicate argument order. State units for every numeric quantity.
4. **Write actions as contracts.** Include enabling preconditions, consumed facts,
   established facts, resource use, and capacity restrictions. An omitted effect means
   the corresponding fact persists; it does not mean “unknown afterward.”
5. **Create a coherent problem instance.** Match the domain name, declare objects,
   initialize all relevant facts/numeric values, and express the intended goal.
   Do not treat unobserved external facts as safely false without a modeling decision.
6. **Inspect and parse before search.** Check requirements, parameter typing, arity,
   names, parentheses, and planner support. An accepted parser input is only one layer.
7. **Search with explicit guarantees.** Distinguish satisficing, bounded, and optimal
   configurations. Preserve stdout/stderr, exit status, resource limits, and the actual
   plan file; a nonempty plan file can survive from a previous run.
8. **Validate the returned plan.** Recheck it against the exact domain/problem pair
   with an appropriate validator, preferably independent of the planner. Verify goals,
   preconditions, temporal invariants, and objective value where supported.
9. **Review model adequacy.** Inspect counterexample plans and test missing resources,
   blocked routes, capacity, impossible goals, and an already-satisfied goal.
10. **Execute through controlled adapters.** Bind each action to a real tool operation,
    check current authorization and preconditions, observe actual effects, and replan
    after divergence. Never mark predicted effects as observed facts automatically.

## Preserve the non-obvious semantics

- Keep `:requirements` as a feature declaration, not a mechanism that enables features
  in an incapable planner. A planner and its chosen heuristic can have different limits.
- Keep delete effects distinct from negative preconditions. `(not (p ...))` in an
  effect is normal STRIPS deletion; a negative condition requires the relevant profile.
- Keep closed-world propositional absence separate from unknown observation. Ordinary
  classical PDDL does not represent epistemic uncertainty implicitly.
- Keep action schemas distinct from grounded actions. Objects, predicate arity, and
  types constrain legal groundings; numeric fluent values are not arbitrary objects.
- Evaluate action applicability before applying its effects. Do not interpret an action
  as a sequence of imperative assignments in the textual order of its effect list.
- Preserve frame behavior: facts not changed by an action remain as they were.
- Model exclusivity and capacity explicitly. Typing a robot or vehicle does not make
  it occupy one location or carry only one item automatically.
- Separate logical reachability from cost optimality. `:metric` describes an objective;
  a satisficing planner need not optimize it or prove an optimum.
- Separate `at start`, `over all`, and `at end` conditions. An invariant over an open
  action interval is not automatically an endpoint condition.
- Preserve the no-moving-targets restrictions for concurrent endpoints. Two effects
  that appear harmless sequentially may not be legal at the same timestamp.
- Do not mutate a derived predicate directly with action effects. Respect the derived
  rule restrictions and compute its semantics from underlying facts.
- Keep hard goals/constraints distinct from soft preferences and violation penalties.
- Treat timed initial literals as modeled exogenous events, not a prediction service.
- Treat timeout, out-of-memory, incomplete search, unsupported input, and proved
  unsolvability as different outcomes. “No plan returned” is not a proof of no plan.
- Accept an empty valid plan when the initial state already satisfies the goal.
  Do not confuse an empty plan with a missing result.
- Treat optimality claims as conditional on the objective, algorithm, heuristic,
  pruning, compilation, bounds, and completed search.

## Use the bundled examples

The examples use only typed STRIPS: one robot, one parcel, two locations, and a
single-item carrying capacity. They are suitable for pyperplan 2.1. They do not
exercise numeric, temporal, ADL, or preference support.

```bash
python3 scripts/run_strips_examples.py
Validate -v assets/examples/domain.pddl assets/examples/problem.pddl assets/examples/valid.plan
```

The Python helper requires `pyperplan==2.1`; it uses that library's parser, grounding,
search, and transition functions for these fixed fixtures. It is not a general PDDL
validator or an independent substitute for VAL. Read the worked-example reference for
installation, observed checks, and validation limits.

## Report evidence accurately

For a generated model, return domain, problem, assumptions, requirements, test cases,
and the intended action-to-world mapping. For a solve, return the actual plan and
search status, observed metric, resources, and validation evidence. For a failure,
identify the earliest unsupported construct, violated precondition, missing fact,
or exhausted search resource.

Say “a valid plan was found for this model” when that is what was established.
Reserve “unsolvable” and “optimal” for an outcome supported by the completed algorithm
and its assumptions. Do not call a symbolic action sequence an authorized execution.
