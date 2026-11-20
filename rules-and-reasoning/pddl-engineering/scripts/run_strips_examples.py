#!/usr/bin/env python3
"""Exercise only the bundled typed STRIPS fixtures with pyperplan 2.1."""
from pathlib import Path
from importlib.metadata import version
import json


def main():
    if not __debug__:
        raise SystemExit("Run without Python -O: this fixture helper requires assertions")
    try:
        from pyperplan.pddl.parser import Parser
        from pyperplan.grounding import ground
        from pyperplan.search import breadth_first_search
    except ImportError as exc:
        raise SystemExit("Install pyperplan==2.1 in your selected Python environment first") from exc
    installed = version("pyperplan")
    if installed != "2.1":
        raise SystemExit(f"This fixture helper is pinned to pyperplan 2.1; found {installed}")
    base = Path(__file__).resolve().parents[1] / "assets" / "examples"
    def load(problem):
        parser = Parser(str(base / "domain.pddl"), str(base / problem))
        domain = parser.parse_domain()
        return ground(parser.parse_problem(domain))
    task = load("problem.pddl")
    found = breadth_first_search(task)
    assert found is not None, "expected a plan for the connected fixture"
    assert len(found) == 3, f"expected a shortest three-action plan; got {len(found)}"
    state = task.initial_state
    for operator in found:
        assert operator.applicable(state), f"inapplicable planner operator: {operator.name}"
        state = operator.apply(state)
    assert task.goal_reached(state), "planner sequence did not achieve goal"
    # Use library transition semantics, not a separate handwritten PDDL evaluator.
    # Retain irrelevant operators so supplied candidate plans can also be inspected.
    parser = Parser(str(base / "domain.pddl"), str(base / "problem.pddl"))
    full_task = ground(parser.parse_problem(parser.parse_domain()), remove_irrelevant_operators=False)
    by_name = {op.name: op for op in full_task.operators}
    def replay(file):
        state = full_task.initial_state
        steps = []
        for raw in (base / file).read_text().splitlines():
            line = raw.split(";", 1)[0].strip().lower()
            if line:
                steps.append(" ".join(line.split()))
        for index, name in enumerate(steps, 1):
            operator = by_name.get(name)
            if operator is None or not operator.applicable(state):
                return False, index
            state = operator.apply(state)
        return full_task.goal_reached(state), None
    valid, bad_step = replay("valid.plan")
    assert valid and bad_step is None, "expected the original witness to pass library replay"
    valid, bad_step = replay("invalid.plan")
    assert not valid and bad_step == 2, "expected the moved-first counterexample to fail at step 2"
    blocked = breadth_first_search(load("blocked-problem.pddl"))
    assert blocked is None, "expected exhaustive finite BFS to find no plan for the blocked instance"
    empty = breadth_first_search(load("already-done-problem.pddl"))
    assert empty is not None and len(empty) == 0, "expected a valid empty plan"
    print(json.dumps({
        "runtime": f"pyperplan {installed}",
        "profile": "bundled typed STRIPS fixtures only; no action costs",
        "generated_plan": [op.name for op in found],
        "checks": {
            "shortest_plan_length": len(found),
            "original_plan_replay": "passed",
            "invalid_plan_rejected_at_step": bad_step,
            "blocked_instance_exhaustive_bfs": "no plan",
            "already_satisfied_goal": "empty plan",
        },
        "independent_VAL_validation": "not performed by this helper",
        "real_world_actions_executed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
