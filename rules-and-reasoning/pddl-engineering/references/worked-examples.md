# Worked examples

## Use the small typed STRIPS model

`assets/examples/domain.pddl` models a robot moving along directed connections,
picking up one parcel, and dropping it. `handempty` prevents a second pickup while
carrying. The initial connected problem has the robot and parcel at `dock`; the goal
requires the parcel at `lab` and the robot's hand empty.

The original witness is:

```lisp
(pick bot parcel-a dock)
(move bot dock lab)
(drop bot parcel-a lab)
```

The invalid candidate moves first and then attempts to pick the parcel at `lab`,
where it is absent. The blocked problem has no route. The already-done problem starts
with the goal true. All files use only `:strips :typing`; none demonstrates ADL,
numeric, temporal, preference, or action-cost support.

## Run reproducibly

Use a separate Python environment if installing the optional dependency:

```bash
python3 -m venv /path/to/pddl-example-env
/path/to/pddl-example-env/bin/python -m pip install pyperplan==2.1
/path/to/pddl-example-env/bin/python scripts/run_strips_examples.py
```

On Windows, use the environment's `Scripts/python.exe` path. The helper reads only
bundled fixtures, invokes pyperplan parsing, grounding, breadth-first search, and
transition functions, and prints a JSON result. It performs no network request and
executes no real robot or application action. Use it as a reproducible illustration,
not as an arbitrary-input validation service.

For independent validation with a compatible VAL installation:

```bash
Validate -v assets/examples/domain.pddl assets/examples/problem.pddl assets/examples/valid.plan
Validate -v assets/examples/domain.pddl assets/examples/problem.pddl assets/examples/invalid.plan
```

The first should pass and the second should report the unavailable pickup precondition.
Inspect validator output rather than treating any generated console text as success.

## Observed authoring checks

The **pyperplan 2.1** run found a three-action shortest plan for the
connected finite unit-cost instance, replayed the supplied witness successfully,
rejected the invalid plan at step 2, exhausted the blocked instance without a plan,
and returned an empty plan for the already-satisfied goal. The helper used the same
library's transition semantics for replay; that is not independent validation.

No VAL, Fast Downward, temporal planner, numeric planner, or real-world execution was
run for these fixtures during authoring. The independent VAL commands are a documented
next validation layer, not claimed test results. No conclusion about all PDDL profiles
follows from the small STRIPS fixture.

## Extend with one modeled concern at a time

Add a second parcel to test carrying capacity, remove only one directional route to
test connectivity assumptions, or change the target to test problem generation.
For costs or durations, create a separate profile and select a compatible planner.
Do not silently feed unsupported extensions to this STRIPS-only helper.
