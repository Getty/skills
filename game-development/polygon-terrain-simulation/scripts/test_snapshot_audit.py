#!/usr/bin/env python3
"""Focused valid and malformed snapshot checks for the bounded fixture auditor."""

import copy
import json
from pathlib import Path
import unittest

from audit_snapshot import AuditError, audit_snapshot


ASSETS = Path(__file__).resolve().parents[1] / "assets"
WORLD = json.loads((ASSETS / "world-state-example.json").read_text(encoding="utf-8"))
MATERIALS = json.loads((ASSETS / "material-examples.json").read_text(encoding="utf-8"))


class SnapshotTests(unittest.TestCase):
    def assert_rejected(self, mutate, message=None):
        snapshot, materials = copy.deepcopy(WORLD), copy.deepcopy(MATERIALS)
        mutate(snapshot, materials)
        with self.assertRaises(AuditError) as context:
            audit_snapshot(snapshot, materials)
        if message:
            self.assertIn(message, str(context.exception))

    def test_fixture_geometry_budgets_and_equilibrium(self):
        result = audit_snapshot(WORLD, MATERIALS)
        self.assertTrue(result["valid"])
        self.assertTrue(result["expected_checks_verified"])
        self.assertEqual(result["geometry"], {"cell_count": 4, "internal_face_count": 4,
                                             "boundary_face_count": 8, "domain_area_m2": 400})
        self.assertEqual(result["totals"]["dry_mobile_mass_kg"], 636000)
        self.assertEqual(result["totals"]["total_water_m3"], 190)
        self.assertEqual(result["one_step"]["maximum_volume_change_m3"], 0)
        self.assertTrue(all(rate == 0 for rate in result["internal_flow_m3_s"].values()))
        for cell in result["cells"].values():
            self.assertEqual(cell["layers"][0]["thickness_m"], 1)
            self.assertEqual(cell["layers"][0]["pore_capacity_m3"], 40)

    def test_ring_and_face_orientation_are_independent(self):
        snapshot = copy.deepcopy(WORLD)
        for cell in snapshot["cells"]:
            cell["vertices_m"].reverse()
        for face in snapshot["internal_faces"] + snapshot["boundary_faces"]:
            face["endpoints_m"].reverse()
        self.assertEqual(audit_snapshot(snapshot, MATERIALS)["totals"]["total_water_m3"], 190)

    def test_nonequilibrium_state_reports_conservative_step(self):
        snapshot = copy.deepcopy(WORLD)
        del snapshot["expected_checks"]
        snapshot["cells"][0]["surface_water_m3"] = 110
        result = audit_snapshot(snapshot, MATERIALS)
        self.assertFalse(result["expected_checks_verified"])
        self.assertAlmostEqual(result["internal_flow_m3_s"]["sw_se"], 0.02)
        self.assertAlmostEqual(result["internal_flow_m3_s"]["sw_nw"], 0.02)
        self.assertAlmostEqual(result["one_step"]["surface_volumes_m3"]["sw"], 109.96)
        self.assertAlmostEqual(result["one_step"]["water_residual_m3"], 0)

    def test_wrong_area(self):
        self.assert_rejected(lambda s, m: s["cells"][0].update(area_m2=99), "polygon area")

    def test_wrong_center(self):
        self.assert_rejected(lambda s, m: s["cells"][0].update(center_m=[5.1, 5]), "centroid")

    def test_duplicate_cell_id(self):
        self.assert_rejected(lambda s, m: s["cells"][1].update(cell_id="sw"), "duplicate cell")

    def test_overlapping_cells(self):
        def mutate(snapshot, _):
            snapshot["cells"][1]["vertices_m"] = copy.deepcopy(snapshot["cells"][0]["vertices_m"])
            snapshot["cells"][1]["center_m"] = [5, 5]
        self.assert_rejected(mutate, "overlapping")

    def test_unsupported_nonrectangle(self):
        self.assert_rejected(lambda s, m: s["cells"][0]["vertices_m"].pop(), "rectangles only")

    def test_duplicate_face_id(self):
        self.assert_rejected(lambda s, m: s["internal_faces"][1].update(face_id="sw_se"), "duplicate face")

    def test_missing_boundary(self):
        self.assert_rejected(lambda s, m: s["boundary_faces"].pop(), "missing internal or boundary")

    def test_face_is_not_cell_edge(self):
        self.assert_rejected(lambda s, m: s["internal_faces"][0].update(endpoints_m=[[10, 0], [10, 9]]),
                             "complete cell edge")

    def test_wrong_geometric_neighbors(self):
        self.assert_rejected(lambda s, m: s["internal_faces"][0].update(neighbor="ne"), "ownership")

    def test_wrong_normal_or_distance(self):
        self.assert_rejected(lambda s, m: s["internal_faces"][0].update(normal_owner_to_neighbor=[-1, 0]), "normal")
        self.assert_rejected(lambda s, m: s["internal_faces"][0].update(normal_distance_m=9), "distance")
        self.assert_rejected(lambda s, m: s["boundary_faces"][0].update(outward_normal=[1, 0]), "normal")

    def test_unknown_material(self):
        self.assert_rejected(lambda s, m: s["cells"][0]["layers_bottom_to_top"][0].update(material_id="unknown"),
                             "unknown material")

    def test_pore_capacity_and_negative_stores(self):
        self.assert_rejected(lambda s, m: s["cells"][0]["layers_bottom_to_top"][0].update(pore_water_m3=41),
                             "pore capacity")
        self.assert_rejected(lambda s, m: s["cells"][0].update(surface_water_m3=-1))
        self.assert_rejected(lambda s, m: s["cells"][0].update(suspended_sediment_kg={"mineral_fill_demo": -1}))

    def test_material_fraction_sum(self):
        self.assert_rejected(lambda s, m: m["materials"][0]["texture_mass_fractions"].update(sand=0.9), "fraction sum")

    def test_wrong_expected_budget(self):
        self.assert_rejected(lambda s, m: s["expected_checks"].update(total_water_m3=191), "total_water")

    def test_unsupported_process_boundary_or_operation(self):
        self.assert_rejected(lambda s, m: s["model"]["enabled_processes"].append("erosion"), "only the surface_transfer")
        self.assert_rejected(lambda s, m: s["boundary_faces"][0].update(boundary_type="open_outlet"), "unsupported boundary")
        self.assert_rejected(lambda s, m: s["operations"].append({"operation_id": "active"}), "active terrain operations")

    def test_crest_below_flat_terrain(self):
        self.assert_rejected(lambda s, m: s["internal_faces"][0].update(crest_m=9), "below adjacent terrain")

    def test_nonfinite_and_bad_revision(self):
        self.assert_rejected(lambda s, m: s["cells"][0].update(surface_water_m3=float("nan")), "nonfinite")
        self.assert_rejected(lambda s, m: s["cells"][0].update(geometry_revision=True), "revision")


if __name__ == "__main__":
    unittest.main(verbosity=2)
