#!/usr/bin/env python3
"""Analytical and invariant checks for the small terrain reference kernels."""

import itertools
import json
import math
from pathlib import Path
import random
import unittest

from reference_math import (
    EdgeProposal, balance_residual, compact_layer, crest_transfer_proposal,
    cut_fill, dry_mass_from_volume, layer_state, polygon_metrics, run_demo,
    stage_for_volume, stage_volume, transfer_volumes,
)


FIXTURES = json.loads((Path(__file__).resolve().parents[1] / "assets" / "numeric-fixtures.json")
                     .read_text(encoding="utf-8"))


class GeometryTests(unittest.TestCase):
    def test_rectangle_known_metrics(self):
        metrics = polygon_metrics(FIXTURES["polygon"]["vertices_m"])
        self.assertEqual(metrics["area_m2"], 2)
        self.assertEqual(metrics["centroid_m"], [1, 0.5])
        self.assertEqual(metrics["perimeter_m"], 6)

    def test_orientation_and_start_vertex_do_not_change_area(self):
        points = FIXTURES["polygon"]["vertices_m"]
        for offset in range(4):
            ring = points[offset:] + points[:offset]
            for direction in (ring, list(reversed(ring))):
                metrics = polygon_metrics(direction)
                self.assertEqual(metrics["area_m2"], 2)
                self.assertEqual(metrics["centroid_m"], [1, 0.5])
        self.assertEqual(polygon_metrics(points)["signed_area_m2"], 2)
        self.assertEqual(polygon_metrics(list(reversed(points)))["signed_area_m2"], -2)

    def test_closed_ring_and_large_translation(self):
        points = [[1e9, 1e9], [1e9 + 2, 1e9], [1e9 + 2, 1e9 + 1], [1e9, 1e9 + 1]]
        metrics = polygon_metrics(points + points[:1])
        self.assertEqual(metrics["area_m2"], 2)
        self.assertEqual(metrics["centroid_m"], [1e9 + 1, 1e9 + 0.5])

    def test_concave_polygon_area_and_centroid(self):
        # A 2x2 square minus its upper-right 1x1 square.
        metrics = polygon_metrics([[0, 0], [2, 0], [2, 1], [1, 1], [1, 2], [0, 2]])
        self.assertEqual(metrics["area_m2"], 3)
        self.assertAlmostEqual(metrics["centroid_m"][0], 5 / 6)
        self.assertAlmostEqual(metrics["centroid_m"][1], 5 / 6)

    def test_invalid_polygons(self):
        rings = ([], [[0, 0], [1, 0]], [[0, 0], [1, 0], [2, 0]],
                 [[0, 0], [2, 2], [0, 2], [2, 0]],
                 [[0, 0], [1, 0], [1, 1], [1, 0]], [[0, 0], [1, 0], [1, math.nan]])
        for ring in rings:
            with self.subTest(ring=ring), self.assertRaises(ValueError):
                polygon_metrics(ring)


class EarthworksTests(unittest.TestCase):
    def test_partial_area_cut_fill(self):
        self.assertEqual(cut_fill(FIXTURES["cut_fill"]["patches"]),
                         {"cut_m3": 10, "fill_m3": 2.5, "net_fill_m3": -7.5})

    def test_cut_fill_partition_does_not_change_result(self):
        whole = cut_fill([[25, 10, 12]])
        split = cut_fill([[5, 10, 12], [7, 10, 12], [13, 10, 12]])
        self.assertEqual(whole, split)
        self.assertEqual(whole["fill_m3"], 50)

    def test_empty_and_zero_height_change(self):
        self.assertEqual(cut_fill([])["net_fill_m3"], 0)
        self.assertEqual(cut_fill([[100, -3, -3]])["cut_m3"], 0)

    def test_compaction_preserves_mass_and_transfers_water(self):
        result = compact_layer(**FIXTURES["compaction"]["inputs"])
        self.assertEqual(result["dry_mass_kg"], 159000)
        self.assertAlmostEqual(result["old_thickness_m"], 1)
        self.assertAlmostEqual(result["thickness_m"], 0.8)
        self.assertAlmostEqual(result["bulk_volume_m3"], 80)
        self.assertAlmostEqual(result["pore_capacity_m3"], 20)
        self.assertAlmostEqual(result["retained_pore_water_m3"], 20)
        self.assertAlmostEqual(result["expelled_water_m3"], 10)
        self.assertAlmostEqual(result["retained_pore_water_m3"] + result["expelled_water_m3"], 30)

    def test_loose_and_compacted_volumes_differ_for_same_solids(self):
        dry_mass = dry_mass_from_volume(100, 2650, 0.4)
        self.assertEqual(dry_mass, 159000)
        self.assertAlmostEqual(layer_state(dry_mass, 2650, 0.25, 100)["bulk_volume_m3"], 80)

    def test_zero_layer_and_unsaturated_compaction(self):
        self.assertEqual(layer_state(0, 2650, 0.4, 100)["thickness_m"], 0)
        result = compact_layer(159000, 2650, 100, 0.4, 0.25, 10)
        self.assertEqual(result["retained_pore_water_m3"], 10)
        self.assertEqual(result["expelled_water_m3"], 0)

    def test_invalid_material_and_patch_inputs(self):
        bad_calls = (
            lambda: layer_state(-1, 2650, 0.4, 100),
            lambda: layer_state(1, 0, 0.4, 100),
            lambda: layer_state(1, 2650, 1, 100),
            lambda: layer_state(1, 2650, -0.1, 100),
            lambda: layer_state(1, 2650, 0.4, 0),
            lambda: compact_layer(159000, 2650, 100, 0.4, 0.25, 41),
            lambda: compact_layer(159000, 2650, 100, 0.25, 0.4, 10),
            lambda: cut_fill([[0, 1, 2]]),
            lambda: cut_fill([[1, math.nan, 2]]),
            lambda: dry_mass_from_volume(math.inf, 2650, 0.4),
        )
        for index, operation in enumerate(bad_calls):
            with self.subTest(index=index), self.assertRaises(ValueError):
                operation()


class StorageTests(unittest.TestCase):
    def test_known_stage_curve_breakpoints(self):
        patches = [[60, 0], [40, 1]]
        for volume, stage in ((0, 0), (30, 0.5), (60, 1), (110, 1.5), (210, 2.5)):
            with self.subTest(volume=volume):
                self.assertAlmostEqual(stage_for_volume(patches, volume), stage)
                self.assertAlmostEqual(stage_volume(patches, stage), volume)

    def test_dry_convention_and_negative_elevations(self):
        self.assertEqual(stage_for_volume([[4, -10], [2, -5]], 0), -10)
        self.assertEqual(stage_volume([[4, -10], [2, -5]], -11), 0)
        self.assertEqual(stage_for_volume([[4, -10], [2, -5]], 26), -4)

    def test_storage_patch_permutation_and_partition(self):
        for patches in itertools.permutations([[20, 0], [40, 0], [40, 1]]):
            self.assertAlmostEqual(stage_for_volume(patches, 110), 1.5)
            self.assertAlmostEqual(stage_volume(patches, 1.5), 110)

    def test_terrain_edit_preserves_volume_and_changes_level(self):
        sample = FIXTURES["storage_edit"]
        old_stage = stage_for_volume(sample["old_patches"], sample["volume_m3"])
        new_stage = stage_for_volume(sample["new_patches"], sample["volume_m3"])
        self.assertAlmostEqual(old_stage, 1.5)
        self.assertAlmostEqual(new_stage, 1.8)
        self.assertAlmostEqual(stage_volume(sample["new_patches"], new_stage), 110)
        # Holding stage fixed would have silently discarded 30 m3.
        self.assertAlmostEqual(stage_volume(sample["new_patches"], old_stage), 80)

    def test_many_unequal_areas_round_trip(self):
        patches = [[0.3, -8], [17, -2], [4, 2], [1.7, 2], [50, 9]]
        for volume in (0.1, 1, 20, 80, 200, 1000):
            reconstructed = stage_volume(patches, stage_for_volume(patches, volume))
            self.assertTrue(math.isclose(reconstructed, volume, rel_tol=1e-12, abs_tol=1e-12))

    def test_invalid_storage_inputs(self):
        for patches, volume in (([], 1), ([[0, 1]], 1), ([[1, math.inf]], 1),
                                ([[1, 0]], -1), ([[1, 0]], math.nan)):
            with self.subTest(patches=patches, volume=volume), self.assertRaises(ValueError):
                stage_for_volume(patches, volume)


class TransferTests(unittest.TestCase):
    def test_collective_donor_limit_and_no_instant_reuse(self):
        sample = FIXTURES["transfers"]
        result = transfer_volumes(sample["volumes_m3"], [EdgeProposal(**edge) for edge in sample["edges"]])
        self.assertEqual(result.volumes_m3, sample["expected_final_m3"])
        self.assertEqual(result.actual_transfers_m3, sample["expected_actual_m3"])
        self.assertEqual(result.donor_scales["A"], 0.5)
        self.assertEqual(result.residual_m3, 0)

    def test_reversing_edge_orientation_preserves_physical_result(self):
        original = transfer_volumes({"A": 2, "B": 7}, [EdgeProposal("AB", "A", "B", -3)])
        reverse = transfer_volumes({"A": 2, "B": 7}, [EdgeProposal("AB", "B", "A", 3)])
        self.assertEqual(original.volumes_m3, {"A": 5, "B": 4})
        self.assertEqual(original.volumes_m3, reverse.volumes_m3)
        self.assertEqual(original.actual_transfers_m3["AB"], -reverse.actual_transfers_m3["AB"])

    def test_order_independence(self):
        sample = FIXTURES["transfers"]
        edges = [EdgeProposal(**edge) for edge in sample["edges"]]
        for permutation in itertools.permutations(edges):
            result = transfer_volumes(sample["volumes_m3"], permutation)
            self.assertEqual(result.volumes_m3, sample["expected_final_m3"])

    def test_many_outlets_cannot_make_negative_water(self):
        cells = {"source": 0.1, **{str(i): 0 for i in range(100)}}
        proposals = [EdgeProposal(f"out{i:03d}", "source", str(i), 0.013) for i in range(100)]
        result = transfer_volumes(cells, proposals)
        self.assertTrue(all(value >= 0 for value in result.volumes_m3.values()))
        self.assertAlmostEqual(math.fsum(result.volumes_m3.values()), 0.1, places=14)
        self.assertLess(abs(result.residual_m3), 1e-14)

    def test_random_closed_transfers_preserve_total(self):
        rng = random.Random(41371)
        cells = {str(i): rng.uniform(0, 100) for i in range(30)}
        edges = []
        for index in range(200):
            a, b = rng.sample(list(cells), 2)
            edges.append(EdgeProposal(str(index), a, b, rng.uniform(-100, 100)))
        result = transfer_volumes(cells, edges)
        self.assertTrue(all(value >= 0 for value in result.volumes_m3.values()))
        self.assertLess(abs(result.residual_m3), 1e-10)
        self.assertAlmostEqual(math.fsum(cells.values()), math.fsum(result.volumes_m3.values()), places=10)

    def test_empty_transfer_is_identity(self):
        self.assertEqual(transfer_volumes({"A": 5}, []).volumes_m3, {"A": 5})
        self.assertEqual(transfer_volumes({}, []).volumes_m3, {})

    def test_invalid_transfer_inputs(self):
        cases = (
            ({"A": -1, "B": 2}, []),
            ({"A": math.nan, "B": 2}, []),
            ({"A": 1, "B": 2}, [EdgeProposal("x", "A", "C", 1)]),
            ({"A": 1, "B": 2}, [EdgeProposal("x", "A", "A", 1)]),
            ({"A": 1, "B": 2}, [EdgeProposal("x", "A", "B", math.inf)]),
            ({"A": 1, "B": 2}, [EdgeProposal("x", "A", "B", 1), EdgeProposal("x", "B", "A", 1)]),
        )
        for values, edges in cases:
            with self.subTest(values=values, edges=edges), self.assertRaises(ValueError):
                transfer_volumes(values, edges)


class ReservoirAndBudgetTests(unittest.TestCase):
    def test_below_crest_and_lake_at_rest(self):
        self.assertEqual(crest_transfer_proposal(0.9, 0, 1, 2, 1), 0)
        # Unequal beds/depths but equal free surfaces must produce no flow.
        a_stage = stage_for_volume([[10, 0]], 20)
        b_stage = stage_for_volume([[4, 1]], 4)
        self.assertEqual(crest_transfer_proposal(a_stage, b_stage, 0, 2, 1), 0)

    def test_crest_crossing_and_external_rain_budget(self):
        demo = run_demo()
        final = demo["pond_crest"]["volumes_m3"]
        self.assertAlmostEqual(final["upstream"], 11.6)
        self.assertAlmostEqual(final["downstream"], 0.4)
        self.assertAlmostEqual(demo["pond_budget_residual_m3"], 0)

    def test_linear_two_pond_head_difference(self):
        proposal = crest_transfer_proposal(2, 0, 0, 1, 1)
        result = transfer_volumes({"A": 20, "B": 0}, [EdgeProposal("AB", "A", "B", proposal)])
        difference = result.volumes_m3["A"] / 10 - result.volumes_m3["B"] / 10
        self.assertAlmostEqual(difference, 1.6)
        self.assertAlmostEqual(math.fsum(result.volumes_m3.values()), 20)

    def test_ledger_detects_missing_water(self):
        self.assertEqual(balance_residual(10, 12, imported=3, exported=1), 0)
        self.assertEqual(balance_residual(10, 11, imported=3, exported=1), -1)

    def test_invalid_step_and_budget(self):
        for operation in (lambda: crest_transfer_proposal(2, 0, 0, 1, -1),
                          lambda: crest_transfer_proposal(2, 0, 0, -1, 1),
                          lambda: balance_residual(10, -1),
                          lambda: stage_volume([[1, 0]], True)):
            with self.assertRaises(ValueError):
                operation()


if __name__ == "__main__":
    unittest.main(verbosity=2)
