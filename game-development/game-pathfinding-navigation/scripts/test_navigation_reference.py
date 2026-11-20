#!/usr/bin/env python3
"""Analytical and invariant checks for the small navigation reference module."""

import json
import math
from pathlib import Path
import random
import unittest

from navigation_reference import (
    Edge, Graph, astar, dijkstra, discrete_conflicts, follow_policy,
    graph_from_record, grid_graph, grid_heuristic, heuristic_audit,
    reverse_cost_field, run_demo,
)


ASSETS = Path(__file__).resolve().parents[1] / "assets"
FIXTURES = json.loads((ASSETS / "search-fixtures.json").read_text())
GRID_FIXTURES = json.loads((ASSETS / "grid-fixtures.json").read_text())


def graph(nodes, edges):
    return Graph(nodes, [Edge(*edge) for edge in edges])


def fixture(name):
    return next(case for case in FIXTURES["search_cases"] if case["name"] == name)


def bellman_ford_to_goal(model, goal):
    """Independent finite-graph oracle: repeated relaxation, no priority queue."""
    distance = {node: math.inf for node in model.nodes}
    distance[goal] = 0.0
    for _ in range(max(0, len(model.nodes) - 1)):
        changed = False
        for edge in model.edges.values():
            candidate = edge.cost + distance[edge.target]
            if candidate < distance[edge.source]:
                distance[edge.source] = candidate
                changed = True
        if not changed:
            break
    return distance


class SearchTests(unittest.TestCase):
    def test_analytical_fixture_results(self):
        for case in FIXTURES["search_cases"]:
            with self.subTest(case=case["name"]):
                model = graph_from_record(case["graph"])
                result = astar(model, case["start"], case["goal"], case.get("heuristic"))
                expected = case["expected"]
                self.assertEqual(result.status, expected["status"])
                self.assertEqual(result.cost, expected["cost"])
                self.assertEqual(result.nodes, expected["nodes"])

    def test_goal_is_not_returned_when_discovered(self):
        case = fixture("goal_discovery_trap")
        result = dijkstra(graph_from_record(case["graph"]), "S", "G")
        self.assertEqual(result.cost, 2)
        self.assertNotEqual(result.edges, ["SG"])

    def test_inconsistent_admissible_heuristic_reopens(self):
        case = fixture("admissible_inconsistent")
        result = astar(graph_from_record(case["graph"]), "S", "G", case["heuristic"])
        self.assertEqual(result.cost, 5)
        self.assertEqual(result.reopenings, 1)

    def test_stale_expensive_queue_entries_do_not_expand(self):
        model = graph(["S", "A", "B", "G"], [
            ("SA", "S", "A", 10), ("SB", "S", "B", 1),
            ("BA", "B", "A", 1), ("AG", "A", "G", 20),
        ])
        result = dijkstra(model, "S", "G")
        self.assertEqual(result.cost, 22)
        self.assertEqual(result.expansions, 3)
        self.assertEqual(result.reopenings, 0)

    def test_parallel_edges_keep_actual_edge_identity(self):
        model = graph(["S", "G"], [
            ("expensive", "S", "G", 5), ("cheap", "S", "G", 2),
        ])
        result = dijkstra(model, "S", "G")
        self.assertEqual(result.edges, ["cheap"])
        self.assertEqual(result.cost, 2)

    def test_start_is_goal_costs_zero_even_with_zero_budget(self):
        model = graph(["A"], [])
        result = astar(model, "A", "A", max_expansions=0)
        self.assertEqual(result.status, "found")
        self.assertEqual(result.cost, 0)
        self.assertEqual(result.nodes, ["A"])

    def test_budget_exhausted_is_not_unreachable(self):
        model = graph(["S", "G"], [("SG", "S", "G", 1)])
        stopped = astar(model, "S", "G", max_expansions=0)
        self.assertEqual(stopped.status, "budget_exhausted")
        self.assertIsNone(stopped.cost)
        self.assertEqual(stopped.nodes, [])
        self.assertEqual(astar(model, "S", "G", max_expansions=1).status, "found")

    def test_unreachable_has_no_cost_or_partial_route(self):
        case = fixture("unreachable")
        result = dijkstra(graph_from_record(case["graph"]), "S", "G")
        self.assertEqual((result.status, result.nodes, result.cost),
                         ("unreachable", [], None))

    def test_zero_self_loop_does_not_change_path(self):
        model = graph(["S", "G"], [
            ("loop", "S", "S", 0), ("SG", "S", "G", 0),
        ])
        result = dijkstra(model, "S", "G")
        self.assertEqual(result.cost, 0)
        self.assertEqual(result.edges, ["SG"])

    def test_deterministic_order_independent_of_input_edge_order(self):
        edges = [("SA", "S", "A", 1), ("SB", "S", "B", 1),
                 ("AG", "A", "G", 1), ("BG", "B", "G", 1)]
        first = graph(["S", "A", "B", "G"], edges)
        second = graph(["G", "B", "A", "S"], list(reversed(edges)))
        self.assertEqual(first.fingerprint, second.fingerprint)
        self.assertEqual(dijkstra(first, "S", "G"), dijkstra(second, "S", "G"))

    def test_results_agree_with_independent_oracle_on_small_graphs(self):
        rng = random.Random(71623)
        for trial in range(60):
            nodes = [str(index) for index in range(7)]
            edges = []
            for source in nodes:
                for target in nodes:
                    if source != target and rng.random() < 0.24:
                        edges.append((f"{source}>{target}", source, target, rng.randrange(0, 8)))
            model = graph(nodes, edges)
            truth = bellman_ford_to_goal(model, "6")
            heuristic = {node: (0 if math.isinf(cost) else cost * rng.choice([0, .25, .5, 1]))
                         for node, cost in truth.items()}
            for start in nodes:
                with self.subTest(trial=trial, start=start):
                    result = astar(model, start, "6", heuristic)
                    uniform = dijkstra(model, start, "6")
                    if math.isinf(truth[start]):
                        self.assertEqual(result.status, "unreachable")
                        self.assertEqual(uniform.status, "unreachable")
                    else:
                        self.assertEqual(result.cost, truth[start])
                        self.assertEqual(uniform.cost, truth[start])
                        self.assertEqual(result.nodes[0], start)
                        self.assertEqual(result.nodes[-1], "6")
                        self.assertEqual(len(result.edges), len(result.nodes) - 1)
                        for source, target, edge_id in zip(result.nodes, result.nodes[1:], result.edges):
                            self.assertEqual((model.edges[edge_id].source, model.edges[edge_id].target),
                                             (source, target))


class ReverseFieldTests(unittest.TestCase):
    def test_directed_multigoal_distances(self):
        case = FIXTURES["reverse_field"]
        field = reverse_cost_field(graph_from_record(case["graph"]), case["goals"])
        self.assertEqual(field.distance, case["expected_distances"])

    def test_goal_fields_follow_original_edge_direction(self):
        case = FIXTURES["reverse_field"]
        model = graph_from_record(case["graph"])
        field = reverse_cost_field(model, case["goals"])
        result = follow_policy(model, field, "A")
        self.assertEqual(result.nodes, ["A", "B", "G"])
        self.assertEqual(result.cost, 5)

    def test_zero_cycle_policy_terminates(self):
        case = FIXTURES["zero_cycle_field"]
        model = graph_from_record(case["graph"])
        field = reverse_cost_field(model, case["goals"])
        result = follow_policy(model, field, case["start"])
        self.assertEqual(result.cost, case["expected"]["cost"])
        self.assertEqual(result.nodes, case["expected"]["nodes"])
        for source, target in zip(result.nodes, result.nodes[1:]):
            self.assertGreater(field.settlement_rank[source], field.settlement_rank[target])

    def test_unreachable_is_distinct_from_a_goal(self):
        model = graph(["S", "G", "U"], [("SG", "S", "G", 1)])
        field = reverse_cost_field(model, ["G"])
        self.assertEqual(follow_policy(model, field, "G").status, "found")
        self.assertEqual(follow_policy(model, field, "U").status, "unreachable")
        self.assertIsNone(field.next_edge["G"])
        self.assertIsNone(field.next_edge["U"])
        self.assertEqual(field.distance["G"], 0)
        self.assertIsNone(field.distance["U"])

    def test_field_is_rejected_on_changed_snapshot(self):
        original = graph(["S", "G"], [("SG", "S", "G", 1)])
        changed = graph(["S", "G"], [("SG", "S", "G", 2)])
        field = reverse_cost_field(original, ["G"])
        with self.assertRaisesRegex(ValueError, "snapshot"):
            follow_policy(changed, field, "S")

    def test_policy_rejects_non_descending_corrupted_successor(self):
        model = graph(["A", "B", "G"], [
            ("AB", "A", "B", 0), ("BA", "B", "A", 0), ("BG", "B", "G", 1),
        ])
        field = reverse_cost_field(model, ["G"])
        field.next_edge["B"] = "BA"
        with self.assertRaisesRegex(ValueError, "rank"):
            follow_policy(model, field, "A")


class HeuristicTests(unittest.TestCase):
    def test_audit_distinguishes_admissibility_and_consistency(self):
        case = fixture("admissible_inconsistent")
        audit = heuristic_audit(graph_from_record(case["graph"]), ["G"], case["heuristic"])
        self.assertTrue(audit["admissible_within_tolerance"])
        self.assertFalse(audit["consistent_within_tolerance"])
        self.assertTrue(audit["zero_at_goals"])
        self.assertIn("BA", [entry["edge_id"] for entry in audit["inconsistent_edges"]])

    def test_overestimate_is_reported(self):
        model = graph(["S", "G"], [("SG", "S", "G", 1)])
        audit = heuristic_audit(model, ["G"], {"S": 2, "G": 0})
        self.assertFalse(audit["admissible_within_tolerance"])
        self.assertEqual(audit["overestimates"][0]["node"], "S")

    def test_goal_zero_is_checked_separately(self):
        model = graph(["S", "G"], [("SG", "S", "G", 1)])
        audit = heuristic_audit(model, ["G"], {"S": 1, "G": 1})
        self.assertFalse(audit["zero_at_goals"])
        with self.assertRaisesRegex(ValueError, "goal"):
            astar(model, "S", "G", {"S": 1, "G": 1})

    def test_cheap_portal_invalidates_geometric_lower_bound(self):
        grid = grid_graph(3, 1)
        heuristic = grid_heuristic(grid, "2,0")
        changed = Graph(grid.graph.nodes, [*grid.graph.edges.values(),
                                         Edge("portal", "0,0", "2,0", .1)])
        audit = heuristic_audit(changed, ["2,0"], heuristic)
        self.assertFalse(audit["admissible_within_tolerance"])
        self.assertEqual(dijkstra(changed, "0,0", "2,0").cost, .1)

    def test_nonadmissible_h_is_not_claimed_to_find_optimum(self):
        model = graph(["S", "A", "G"], [
            ("SG", "S", "G", 5), ("SA", "S", "A", 1), ("AG", "A", "G", 1),
        ])
        result = astar(model, "S", "G", {"S": 0, "A": 100, "G": 0})
        self.assertEqual(result.status, "found")
        self.assertEqual(result.cost, 5)
        self.assertEqual(dijkstra(model, "S", "G").cost, 2)


class GridTests(unittest.TestCase):
    def test_analytical_grid_fixtures_and_heuristic_bounds(self):
        for case in GRID_FIXTURES["cases"]:
            with self.subTest(case=case["name"]):
                model = grid_graph(
                    case["width"], case["height"], blocked=case["blocked"],
                    multipliers={tuple(row["cell"]): row["value"] for row in case["multipliers"]},
                    diagonals=case["diagonals"])
                heuristic = grid_heuristic(model, case["goal"])
                result = astar(model.graph, case["start"], case["goal"], heuristic)
                if case["expected_cost_s"] is None:
                    self.assertEqual(result.status, "unreachable")
                else:
                    self.assertAlmostEqual(result.cost, case["expected_cost_s"])
                audit = heuristic_audit(model.graph, [case["goal"]], heuristic)
                self.assertTrue(audit["admissible_within_tolerance"])
                self.assertTrue(audit["consistent_within_tolerance"])

    def test_diagonal_is_blocked_when_one_side_cell_is_blocked(self):
        model = grid_graph(2, 2, blocked=[(1, 0)], diagonals=True)
        self.assertNotIn("0,0>1,1", model.graph.edges)
        self.assertEqual(dijkstra(model.graph, "0,0", "1,1").cost, 2)

    def test_both_blocked_side_cells_do_not_create_a_diagonal_escape(self):
        model = grid_graph(2, 2, blocked=[(1, 0), (0, 1)], diagonals=True)
        self.assertEqual(dijkstra(model.graph, "0,0", "1,1").status, "unreachable")

    def test_destination_costs_are_directed(self):
        model = grid_graph(2, 1, multipliers={(1, 0): 4})
        self.assertEqual(dijkstra(model.graph, "0,0", "1,0").cost, 4)
        self.assertEqual(dijkstra(model.graph, "1,0", "0,0").cost, 1)

    def test_scale_and_speed_produce_time_cost(self):
        model = grid_graph(3, 1, cell_size_m=2, base_speed_m_s=4)
        self.assertEqual(dijkstra(model.graph, "0,0", "2,0").cost, 1)
        self.assertEqual(grid_heuristic(model, "2,0")["0,0"], 1)

    def test_subunit_multiplier_is_included_in_heuristic_scale(self):
        model = grid_graph(3, 1, multipliers={(1, 0): .2, (2, 0): .2})
        h = grid_heuristic(model, "2,0")
        self.assertAlmostEqual(h["0,0"], .4)
        self.assertAlmostEqual(astar(model.graph, "0,0", "2,0", h).cost, .4)


class ConflictTests(unittest.TestCase):
    def test_swap_is_detected(self):
        result = discrete_conflicts({"a": ["X", "Y"], "b": ["Y", "X"]})
        self.assertEqual([entry["type"] for entry in result], ["edge_swap"])

    def test_vertex_conflict_is_detected(self):
        result = discrete_conflicts({"a": ["A", "X"], "b": ["B", "X"]})
        self.assertEqual([entry["type"] for entry in result], ["vertex"])
        self.assertEqual(result[0]["time"], 1)

    def test_goal_occupancy_policy_changes_conflicts(self):
        paths = {"a": ["X"], "b": ["B", "X"]}
        self.assertEqual(len(discrete_conflicts(paths)), 1)
        self.assertEqual(discrete_conflicts(paths, stay_at_goal=False), [])

    def test_following_vacated_vertex_is_allowed(self):
        self.assertEqual(discrete_conflicts({"a": ["A", "B"], "b": ["B", "C"]}), [])

    def test_empty_schedule_set_has_no_conflicts(self):
        self.assertEqual(discrete_conflicts({}), [])


class InvalidInputTests(unittest.TestCase):
    def test_invalid_graph_numbers_are_rejected(self):
        for cost in [-1, math.nan, math.inf, -math.inf, True, "2"]:
            with self.subTest(cost=cost), self.assertRaises(ValueError):
                graph(["S", "G"], [("SG", "S", "G", cost)])

    def test_duplicate_and_unknown_graph_identities_are_rejected(self):
        with self.assertRaises(ValueError):
            graph(["S", "S"], [])
        with self.assertRaises(ValueError):
            graph(["S"], [("edge", "S", "missing", 1)])
        with self.assertRaises(ValueError):
            graph(["S"], [("edge", "S", "S", 1), ("edge", "S", "S", 2)])

    def test_bad_heuristic_inputs_are_rejected(self):
        model = graph(["S", "G"], [("SG", "S", "G", 1)])
        for h in [{"S": -1, "G": 0}, {"S": math.nan, "G": 0},
                  {"S": math.inf, "G": 0}, {"S": 0}, {"S": False, "G": 0}]:
            with self.subTest(h=h), self.assertRaises(ValueError):
                astar(model, "S", "G", h)

    def test_bad_budget_inputs_are_rejected(self):
        model = graph(["S", "G"], [("SG", "S", "G", 1)])
        for budget in [-1, 1.5, True]:
            with self.subTest(budget=budget), self.assertRaises(ValueError):
                astar(model, "S", "G", max_expansions=budget)

    def test_bad_endpoints_and_goals_are_rejected(self):
        model = graph(["S", "G"], [])
        with self.assertRaises(ValueError):
            astar(model, "unknown", "G")
        for goals in [[], ["unknown"], "G"]:
            with self.subTest(goals=goals), self.assertRaises(ValueError):
                reverse_cost_field(model, goals)

    def test_bad_grid_inputs_are_rejected(self):
        for kwargs in [{"width": 0, "height": 2}, {"width": True, "height": 2},
                       {"width": 2, "height": 2, "blocked": [(2, 0)]},
                       {"width": 2, "height": 2, "multipliers": {(0, 0): 0}},
                       {"width": 2, "height": 2, "base_speed_m_s": 0},
                       {"width": 1, "height": 1, "blocked": [(0, 0)]}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                grid_graph(**kwargs)

    def test_invalid_schedule_is_rejected(self):
        for paths in [{"a": []}, {"a": "XY"}, {"": ["X"]}, {"a": [""]}]:
            with self.subTest(paths=paths), self.assertRaises(ValueError):
                discrete_conflicts(paths)

    def test_demo_is_finite_json_and_matches_expected_examples(self):
        result = run_demo()
        json.dumps(result, allow_nan=False)
        self.assertEqual(result["search"]["weighted_detour"]["cost"], 6)
        self.assertEqual(result["search"]["admissible_inconsistent"]["reopenings"], 1)
        self.assertEqual(result["zero_cycle_policy"]["cost"], 2)


if __name__ == "__main__":
    unittest.main()
