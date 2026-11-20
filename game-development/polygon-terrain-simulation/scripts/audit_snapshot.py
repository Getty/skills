#!/usr/bin/env python3
"""Audit the bundled illustrative snapshot schema, not arbitrary game saves.

Accepted geometry: finite, conforming axis-aligned rectangles filling one closed
rectangular domain; exact shared endpoint coordinates, centroid samples, flat bed
per cell, fixed bedrock, homogeneous material layers. No holes, hanging nodes,
subgrid structures, open boundaries, active operations, or remeshing.
"""

from __future__ import annotations

import argparse
import json
import math
from numbers import Real
from pathlib import Path
import sys

from reference_math import (EdgeProposal, crest_transfer_proposal, layer_state,
                            polygon_metrics, transfer_volumes)


class AuditError(ValueError):
    """Invalid or unsupported illustrative snapshot."""


ABS_TOL = 1e-9
REL_TOL = 1e-12


def number(value, label, lower=None, strict=False):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise AuditError(f"{label}: expected a numerical value")
    value = float(value)
    if not math.isfinite(value):
        raise AuditError(f"{label}: nonfinite value")
    if lower is not None and (value <= lower if strict else value < lower):
        raise AuditError(f"{label}: value outside allowed range")
    return value


def identifier(value, label):
    if not isinstance(value, str) or not value:
        raise AuditError(f"{label}: expected a nonempty string")
    return value


def close(actual, expected, label):
    expected = number(expected, label)
    if not math.isclose(actual, expected, rel_tol=REL_TOL, abs_tol=ABS_TOL):
        raise AuditError(f"{label}: actual {actual!r}, declared/expected {expected!r}")


def point(value, label):
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise AuditError(f"{label}: expected a two-coordinate point/vector")
    return (number(value[0], label), number(value[1], label))


def edge_key(endpoints, label):
    if not isinstance(endpoints, (list, tuple)) or len(endpoints) != 2:
        raise AuditError(f"{label}: expected two endpoints")
    a, b = point(endpoints[0], label), point(endpoints[1], label)
    if a == b:
        raise AuditError(f"{label}: zero-length edge")
    return tuple(sorted((a, b)))


def material_registry(data):
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise AuditError("unsupported materials schema version")
    result = {}
    for item in data["materials"]:
        key = identifier(item["material_id"], "material ID")
        if key in result:
            raise AuditError(f"duplicate material ID: {key}")
        density = number(item["particle_density_kg_m3"], f"{key} density", 0, True)
        porosity = number(item["reference_porosity"], f"{key} porosity", 0)
        if porosity >= 1:
            raise AuditError(f"{key}: porosity must be below one")
        fractions = item["texture_mass_fractions"]
        if not isinstance(fractions, dict) or not fractions:
            raise AuditError(f"{key}: expected texture fractions")
        close(math.fsum(number(v, f"{key} texture fraction", 0) for v in fractions.values()),
              1, f"{key} texture fraction sum")
        for field in ("infiltration_capacity_m_s", "conductivity_m_s", "roughness_manning_s_m_neg_third"):
            number(item[field], f"{key} {field}", 0)
        result[key] = density
    if not result:
        raise AuditError("empty materials registry")
    return result


def _audit(snapshot, materials):
    if type(snapshot["schema_version"]) is not int or snapshot["schema_version"] != 1:
        raise AuditError("unsupported world schema version")
    if snapshot["model"]["water"] != "thresholded_linear_reservoir_connections":
        raise AuditError("unsupported water model")
    if snapshot["model"]["material_state"] != "dry_mass_and_porosity":
        raise AuditError("unsupported material state")
    if snapshot["model"]["enabled_processes"] != ["surface_transfer"]:
        raise AuditError("audit supports only the surface_transfer process")
    if snapshot["operations"]:
        raise AuditError("audit does not validate active terrain operations")
    number(snapshot["simulation_time_s"], "simulation time", 0)
    dt = number(snapshot["model"]["dt_s"], "time step", 0, True)
    densities = material_registry(materials)
    cells, layers, edge_owners = {}, set(), {}
    dry_layers, suspended, pore_water, surface_water = [], [], [], []

    for cell in snapshot["cells"]:
        cid = identifier(cell["cell_id"], "cell ID")
        if cid in cells:
            raise AuditError(f"duplicate cell ID: {cid}")
        vertices = [point(p, f"{cid} vertex") for p in cell["vertices_m"]]
        if len(vertices) == 5 and vertices[-1] == vertices[0]:
            vertices.pop()
        if len(vertices) != 4:
            raise AuditError(f"{cid}: audit accepts four-corner axis-aligned rectangles only")
        metrics = polygon_metrics(vertices)
        xs, ys = sorted(set(p[0] for p in vertices)), sorted(set(p[1] for p in vertices))
        if len(xs) != 2 or len(ys) != 2 or set(vertices) != {(x, y) for x in xs for y in ys}:
            raise AuditError(f"{cid}: unsupported nonrectangular geometry")
        # A simple ring through four rectangle corners must follow its perimeter.
        for a, b in zip(vertices, vertices[1:] + vertices[:1]):
            if a[0] != b[0] and a[1] != b[1]:
                raise AuditError(f"{cid}: unsupported diagonal cell edge")
            edge_owners.setdefault(tuple(sorted((a, b))), []).append(cid)
        area = number(cell["area_m2"], f"{cid} area", 0, True)
        close(metrics["area_m2"], area, f"{cid} polygon area")
        center = point(cell["center_m"], f"{cid} center")
        # Compare offsets to avoid allowing a large error at a large coordinate origin.
        for axis in (0, 1):
            close(center[axis] - metrics["centroid_m"][axis], 0, f"{cid} centroid")
        revision = cell["geometry_revision"]
        if isinstance(revision, bool) or not isinstance(revision, int) or revision < 0:
            raise AuditError(f"{cid}: invalid geometry revision")
        rock_id = identifier(cell["bedrock_material_id"], f"{cid} bedrock material")
        if rock_id not in densities and rock_id != "unmodeled_substrate":
            raise AuditError(f"{cid}: unknown bedrock material {rock_id}")
        bed = number(cell["bedrock_top_m"], f"{cid} bedrock top")
        derived_layers = []
        for layer in cell["layers_bottom_to_top"]:
            lid = identifier(layer["layer_id"], "layer ID")
            if lid in layers:
                raise AuditError(f"duplicate layer ID: {lid}")
            layers.add(lid)
            material = identifier(layer["material_id"], f"{lid} material")
            if material not in densities:
                raise AuditError(f"{lid}: unknown material {material}")
            state = layer_state(layer["dry_mass_kg"], densities[material], layer["porosity"], area)
            water = number(layer["pore_water_m3"], f"{lid} pore water", 0)
            if water > state["pore_capacity_m3"] and not math.isclose(
                    water, state["pore_capacity_m3"], rel_tol=REL_TOL, abs_tol=ABS_TOL):
                raise AuditError(f"{lid}: pore water exceeds pore capacity")
            for field in ("thickness_m", "pore_capacity_m3"):
                if field in layer:
                    close(state[field], layer[field], f"{lid} redundant {field}")
            bed += state["thickness_m"]
            dry_layers.append(state["dry_mass_kg"])
            pore_water.append(water)
            derived_layers.append({"layer_id": lid, **state, "pore_water_m3": water})
        for material, mass in cell["suspended_sediment_kg"].items():
            if material not in densities:
                raise AuditError(f"{cid}: unknown suspended material {material}")
            suspended.append(number(mass, f"{cid} suspended sediment", 0))
        volume = number(cell["surface_water_m3"], f"{cid} surface water", 0)
        surface_water.append(volume)
        stage = number(bed + volume / area, f"{cid} derived stage")
        cells[cid] = {"bounds": (xs[0], ys[0], xs[1], ys[1]), "center": center,
                      "area": area, "bed": bed, "stage": stage, "volume": volume,
                      "layers": derived_layers}
    if not cells:
        raise AuditError("empty cell set")

    items = list(cells.items())
    for index, (cid, cell) in enumerate(items):
        a = cell["bounds"]
        for oid, other in items[index + 1:]:
            b = other["bounds"]
            if min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1]):
                raise AuditError(f"overlapping cell interiors: {cid}, {oid}")
    bounds = (min(c["bounds"][0] for c in cells.values()), min(c["bounds"][1] for c in cells.values()),
              max(c["bounds"][2] for c in cells.values()), max(c["bounds"][3] for c in cells.values()))
    area = math.fsum(c["area"] for c in cells.values())
    close(area, snapshot["domain_area_m2"], "domain area")
    close(area, (bounds[2] - bounds[0]) * (bounds[3] - bounds[1]), "rectangular domain coverage")
    if any(len(owners) not in (1, 2) for owners in edge_owners.values()):
        raise AuditError("nonmanifold cell edge ownership")

    covered, face_ids, rates = set(), set(), {}
    proposals = []
    for kind, faces in (("internal", snapshot["internal_faces"]), ("boundary", snapshot["boundary_faces"])):
        for face in faces:
            fid = identifier(face["face_id"], "face ID")
            if fid in face_ids:
                raise AuditError(f"duplicate face ID: {fid}")
            face_ids.add(fid)
            edge = edge_key(face["endpoints_m"], f"{fid} endpoints")
            if edge not in edge_owners or edge in covered:
                raise AuditError(f"{fid}: face is not an uncovered complete cell edge")
            covered.add(edge)
            owner = identifier(face["owner"], f"{fid} owner")
            if owner not in cells:
                raise AuditError(f"{fid}: unknown owner")
            owners = edge_owners[edge]
            length = math.dist(*edge)
            close(length, face["length_m"], f"{fid} length")
            tangent = ((edge[1][0] - edge[0][0]) / length, (edge[1][1] - edge[0][1]) / length)
            if kind == "internal":
                neighbor = identifier(face["neighbor"], f"{fid} neighbor")
                if neighbor not in cells or owner == neighbor or sorted(owners) != sorted([owner, neighbor]):
                    raise AuditError(f"{fid}: internal ownership does not match geometric neighbors")
                normal = point(face["normal_owner_to_neighbor"], f"{fid} normal")
                delta = tuple(cells[neighbor]["center"][k] - cells[owner]["center"][k] for k in (0, 1))
                distance = math.hypot(*delta)
                for k in (0, 1):
                    close(normal[k], delta[k] / distance, f"{fid} owner-to-neighbor unit normal")
                close(distance, face["normal_distance_m"], f"{fid} orthogonal center distance")
                crest = number(face["crest_m"], f"{fid} crest")
                bed_limit = max(cells[owner]["bed"], cells[neighbor]["bed"])
                if crest < bed_limit and not math.isclose(crest, bed_limit, rel_tol=REL_TOL, abs_tol=ABS_TOL):
                    raise AuditError(f"{fid}: ordinary flat-cell crest lies below adjacent terrain")
                conductance = number(face["conductance_m2_s"], f"{fid} conductance", 0)
                rate = crest_transfer_proposal(cells[owner]["stage"], cells[neighbor]["stage"], crest, conductance, 1)
                rates[fid] = rate
                proposals.append(EdgeProposal(fid, owner, neighbor, rate * dt))
            else:
                if owners != [owner] or face["boundary_type"] != "closed_wall":
                    raise AuditError(f"{fid}: unsupported boundary or incorrect boundary ownership")
                if not (edge[0][0] == edge[1][0] and edge[0][0] in (bounds[0], bounds[2])
                        or edge[0][1] == edge[1][1] and edge[0][1] in (bounds[1], bounds[3])):
                    raise AuditError(f"{fid}: unmatched interior edge or nonconforming cell junction")
                midpoint = tuple((edge[0][k] + edge[1][k]) / 2 for k in (0, 1))
                delta = tuple(midpoint[k] - cells[owner]["center"][k] for k in (0, 1))
                distance = math.hypot(*delta)
                normal = point(face["outward_normal"], f"{fid} normal")
                for k in (0, 1):
                    close(normal[k], delta[k] / distance, f"{fid} outward unit normal")
            close(math.hypot(*normal), 1, f"{fid} normal length")
            close(math.fsum(normal[k] * tangent[k] for k in (0, 1)), 0, f"{fid} face orthogonality")
    if covered != set(edge_owners):
        raise AuditError("missing internal or boundary face records")

    totals = {"dry_mobile_mass_kg": math.fsum(dry_layers + suspended),
              "dry_layer_mass_kg": math.fsum(dry_layers), "suspended_sediment_kg": math.fsum(suspended),
              "surface_water_m3": math.fsum(surface_water), "pore_water_m3": math.fsum(pore_water),
              "total_water_m3": math.fsum(surface_water + pore_water)}
    expected = snapshot.get("expected_checks")
    if expected is not None:
        for field in ("dry_mobile_mass_kg", "surface_water_m3", "pore_water_m3", "total_water_m3"):
            close(totals[field], expected[field], field)
        for field, key in (("derived_surface_elevations_m", "bed"), ("derived_stages_m", "stage")):
            if set(expected[field]) != set(cells):
                raise AuditError(f"{field}: expected cell set differs")
            for cid, value in expected[field].items():
                close(cells[cid][key], value, f"{cid} {field}")
        for fid, rate in rates.items():
            close(rate, expected["all_internal_flow_m3_s"], f"{fid} expected flow")
    transfer = transfer_volumes({cid: cell["volume"] for cid, cell in cells.items()}, proposals)
    close(transfer.residual_m3, 0, "closed-domain transfer residual")
    return {"valid": True, "scope": "illustrative_schema_1_conforming_rectangles_closed_domain",
            "expected_checks_verified": expected is not None,
            "tolerances": {"absolute": ABS_TOL, "relative": REL_TOL},
            "geometry": {"cell_count": len(cells), "internal_face_count": len(snapshot["internal_faces"]),
                         "boundary_face_count": len(snapshot["boundary_faces"]), "domain_area_m2": area},
            "totals": totals, "fixed_bedrock_mass_excluded": True,
            "cells": {cid: {"surface_elevation_m": cell["bed"], "stage_m": cell["stage"],
                             "layers": cell["layers"]} for cid, cell in cells.items()},
            "internal_flow_m3_s": rates,
            "one_step": {"dt_s": dt, "surface_volumes_m3": transfer.volumes_m3,
                         "actual_transfers_m3": transfer.actual_transfers_m3,
                         "water_residual_m3": transfer.residual_m3,
                         "maximum_volume_change_m3": max(abs(transfer.volumes_m3[cid] - cell["volume"])
                                                          for cid, cell in cells.items())}}


def audit_snapshot(snapshot, materials):
    """Return derived quantities or raise AuditError for invalid/unsupported data."""
    try:
        return _audit(snapshot, materials)
    except AuditError:
        raise
    except (KeyError, IndexError, AttributeError, TypeError, ValueError, OverflowError, ZeroDivisionError) as error:
        raise AuditError(f"invalid illustrative snapshot: {error}") from error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", nargs="?", type=Path,
                        default=Path(__file__).resolve().parents[1] / "assets" / "world-state-example.json")
    parser.add_argument("--materials", type=Path, help="Explicit material catalog path")
    args = parser.parse_args()
    try:
        snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        if args.materials is None:
            filename = identifier(snapshot["materials_file"], "materials filename")
            if Path(filename).name != filename:
                raise AuditError("materials_file must be a local filename; use --materials for another path")
            material_path = args.snapshot.parent / filename
        else:
            material_path = args.materials
        materials = json.loads(material_path.read_text(encoding="utf-8"))
        result = audit_snapshot(snapshot, materials)
    except (AuditError, OSError, KeyError, TypeError, ValueError) as error:
        print(json.dumps({"valid": False, "error": str(error)}, allow_nan=False), file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
