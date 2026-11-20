#!/usr/bin/env python3
"""Small SI terrain accounting kernels; not a terrain engine or flow solver.

Run ``python3 reference_math.py demo`` for synthetic analytical examples.
All stores are nonnegative. Elevations and signed face proposals may be negative.
Floating-point conservation is checked within a scale-aware numerical tolerance,
not claimed to be exact integer or cross-platform deterministic arithmetic.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import math
from numbers import Real
from pathlib import Path
from typing import Mapping, Sequence


def _number(name: str, value: float, minimum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a real number")
    result = float(value)
    if not math.isfinite(result) or (minimum is not None and result < minimum):
        raise ValueError(f"{name} must be finite and >= {minimum}" if minimum is not None
                         else f"{name} must be finite")
    return result


def _positive(name: str, value: float) -> float:
    result = _number(name, value)
    if result <= 0.0:
        raise ValueError(f"{name} must be > 0")
    return result


def _porosity(value: float) -> float:
    result = _number("porosity", value, 0.0)
    if result >= 1.0:
        raise ValueError("porosity must be < 1")
    return result


def _cross(a: tuple[float, float], b: tuple[float, float],
           c: tuple[float, float]) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _on_segment(a: tuple[float, float], b: tuple[float, float],
                p: tuple[float, float]) -> bool:
    return (_cross(a, b, p) == 0.0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def _segments_intersect(a: tuple[float, float], b: tuple[float, float],
                        c: tuple[float, float], d: tuple[float, float]) -> bool:
    x1, x2, x3, x4 = _cross(a, b, c), _cross(a, b, d), _cross(c, d, a), _cross(c, d, b)
    if ((x1 > 0 > x2 or x2 > 0 > x1) and (x3 > 0 > x4 or x4 > 0 > x3)):
        return True
    return (_on_segment(a, b, c) or _on_segment(a, b, d)
            or _on_segment(c, d, a) or _on_segment(c, d, b))


def polygon_metrics(vertices_m: Sequence[Sequence[float]]) -> dict[str, object]:
    """Area, signed area, centroid and perimeter of a simple planar polygon.

    Accept an open ring or one repeated closing point. Reject repeated vertices,
    self intersections and zero area. Predicates use ordinary floating point;
    use a robust geometry library for near-degenerate production geometry.
    """
    points: list[tuple[float, float]] = []
    for point in vertices_m:
        if len(point) != 2:
            raise ValueError("each vertex must contain x and y")
        points.append((_number("x", point[0]), _number("y", point[1])))
    if len(points) > 1 and points[-1] == points[0]:
        points.pop()
    if len(points) < 3 or len(set(points)) != len(points):
        raise ValueError("a polygon needs at least three distinct vertices")
    count = len(points)
    for i in range(count):
        for j in range(i + 1, count):
            if j == i + 1 or (i == 0 and j == count - 1):
                continue
            if _segments_intersect(points[i], points[(i + 1) % count],
                                   points[j], points[(j + 1) % count]):
                raise ValueError("polygon has intersecting nonadjacent edges")
    # Translate before shoelace sums to reduce cancellation for offset worlds.
    origin = points[0]
    local = [(x - origin[0], y - origin[1]) for x, y in points]
    nxt = local[1:] + local[:1]
    cross = [a[0] * b[1] - b[0] * a[1] for a, b in zip(local, nxt)]
    twice_area = _number("twice signed area", math.fsum(cross))
    if twice_area == 0.0:
        raise ValueError("polygon has zero area")
    cx = origin[0] + math.fsum((a[0] + b[0]) * c for a, b, c in zip(local, nxt, cross)) / (3.0 * twice_area)
    cy = origin[1] + math.fsum((a[1] + b[1]) * c for a, b, c in zip(local, nxt, cross)) / (3.0 * twice_area)
    perimeter = math.fsum(math.hypot(a[0] - b[0], a[1] - b[1]) for a, b in zip(local, nxt))
    return {"signed_area_m2": twice_area / 2.0, "area_m2": abs(twice_area) / 2.0,
            "centroid_m": [_number("centroid x", cx), _number("centroid y", cy)],
            "perimeter_m": _number("perimeter", perimeter)}


def cut_fill(patches: Sequence[Sequence[float]]) -> dict[str, float]:
    """Sum (overlap area m2, old elevation m, target elevation m) patches.

    Each patch is piecewise constant. The caller must clip the footprint and
    subdivide varying terrain/layer boundaries before this quadrature is valid.
    """
    cuts, fills = [], []
    for patch in patches:
        if len(patch) != 3:
            raise ValueError("each cut/fill patch needs area, old z, target z")
        area = _positive("patch area", patch[0])
        difference = _number("target z", patch[2]) - _number("old z", patch[1])
        cuts.append(_number("cut volume", area * max(-difference, 0.0), 0.0))
        fills.append(_number("fill volume", area * max(difference, 0.0), 0.0))
    cut, fill = math.fsum(cuts), math.fsum(fills)
    return {"cut_m3": cut, "fill_m3": fill, "net_fill_m3": fill - cut}


def dry_mass_from_volume(bulk_volume_m3: float, particle_density_kg_m3: float,
                         porosity: float) -> float:
    """Return dry solids mass, excluding water and air, for homogeneous material."""
    volume = _number("bulk volume", bulk_volume_m3, 0.0)
    density = _positive("particle density", particle_density_kg_m3)
    fraction = _porosity(porosity)
    return _number("dry mass", volume * density * (1.0 - fraction), 0.0)


def layer_state(dry_mass_kg: float, particle_density_kg_m3: float,
                porosity: float, area_m2: float) -> dict[str, float]:
    """Derive homogeneous layer geometry from authoritative dry mass/porosity."""
    mass = _number("dry mass", dry_mass_kg, 0.0)
    density = _positive("particle density", particle_density_kg_m3)
    fraction = _porosity(porosity)
    area = _positive("area", area_m2)
    bulk = _number("bulk volume", mass / density / (1.0 - fraction), 0.0)
    return {"dry_mass_kg": mass, "bulk_volume_m3": bulk,
            "thickness_m": _number("thickness", bulk / area, 0.0),
            "pore_capacity_m3": _number("pore capacity", fraction * bulk, 0.0),
            "dry_bulk_density_kg_m3": density * (1.0 - fraction)}


def compact_layer(dry_mass_kg: float, particle_density_kg_m3: float, area_m2: float,
                  old_porosity: float, new_porosity: float,
                  pore_water_m3: float) -> dict[str, float]:
    """Compact at fixed dry mass; report expelled water as an explicit transfer.

    The caller must deliver expelled water to a receiving store. This function
    neither drains it to an implicit sink nor solves consolidation mechanics.
    """
    old_phi, new_phi = _porosity(old_porosity), _porosity(new_porosity)
    if new_phi > old_phi:
        raise ValueError("new porosity must not exceed old porosity for compaction")
    old = layer_state(dry_mass_kg, particle_density_kg_m3, old_phi, area_m2)
    new = layer_state(dry_mass_kg, particle_density_kg_m3, new_phi, area_m2)
    water = _number("pore water", pore_water_m3, 0.0)
    if water > old["pore_capacity_m3"]:
        raise ValueError("initial pore water exceeds initial pore capacity")
    retained = min(water, new["pore_capacity_m3"])
    return {**new, "old_thickness_m": old["thickness_m"],
            "retained_pore_water_m3": retained, "expelled_water_m3": water - retained}


def _storage_patches(patches: Sequence[Sequence[float]]) -> list[tuple[float, float]]:
    if not patches:
        raise ValueError("at least one storage patch is required")
    result = []
    for patch in patches:
        if len(patch) != 2:
            raise ValueError("each storage patch needs area and bed elevation")
        result.append((_positive("patch area", patch[0]), _number("bed elevation", patch[1])))
    return result


def stage_volume(patches: Sequence[Sequence[float]], stage_m: float) -> float:
    """V(eta) = sum area * max(eta - bed, 0), for connected level water."""
    stage = _number("stage", stage_m)
    return _number("storage volume", math.fsum(
        area * max(stage - bed, 0.0) for area, bed in _storage_patches(patches)), 0.0)


def stage_for_volume(patches: Sequence[Sequence[float]], volume_m3: float) -> float:
    """Invert a piecewise-linear flat-patch storage curve without iteration.

    At zero volume, choose the minimum bed elevation as a dry-state convention.
    Disconnected hollows need separate reservoirs; this function does not detect
    connectivity or automatically stop storage at an outlet elevation.
    """
    volume = _number("volume", volume_m3, 0.0)
    groups: dict[float, list[float]] = {}
    for area, bed in _storage_patches(patches):
        groups.setdefault(bed, []).append(area)
    levels = sorted(groups)
    level, area, remaining = levels[0], 0.0, volume
    for index, level in enumerate(levels):
        area = math.fsum([area, *groups[level]])
        if index == len(levels) - 1:
            return _number("stage", level + remaining / area)
        next_level = levels[index + 1]
        capacity = _number("incremental capacity", area * (next_level - level), 0.0)
        if remaining <= capacity:
            return _number("stage", level + remaining / area)
        remaining -= capacity
    raise AssertionError("unreachable empty storage curve")


@dataclass(frozen=True)
class EdgeProposal:
    """One physical connection: positive requested m3 moves from a to b."""

    edge_id: str
    a: str
    b: str
    requested_m3: float


@dataclass(frozen=True)
class TransferResult:
    volumes_m3: dict[str, float]
    actual_transfers_m3: dict[str, float]
    donor_scales: dict[str, float]
    residual_m3: float


def transfer_volumes(volumes_m3: Mapping[str, float],
                     proposals: Sequence[EdgeProposal]) -> TransferResult:
    """Apply closed-domain shared-edge transfers with collective donor limiting.

    Aggregate every outward proposal against the donor's start-of-step water.
    Do not spend incoming water in the same step. Store each actual transfer once
    and use it at both ends. Edge-ID sorting gives stable allocation order. The
    remaining donor budget caps any rounding overshoot before transfer; no
    negative final store is clamped after updating. This is not a flux law.
    """
    initial = {}
    for cell, volume in volumes_m3.items():
        if not isinstance(cell, str) or not cell:
            raise ValueError("cell IDs must be nonempty strings")
        initial[cell] = _number(f"water in {cell}", volume, 0.0)
    outbound: dict[str, list[tuple[str, str, float, float]]] = {cell: [] for cell in initial}
    seen: set[str] = set()
    for proposal in proposals:
        if not isinstance(proposal.edge_id, str) or not proposal.edge_id or proposal.edge_id in seen:
            raise ValueError("each physical connection needs a unique nonempty edge ID")
        seen.add(proposal.edge_id)
        if proposal.a not in initial or proposal.b not in initial or proposal.a == proposal.b:
            raise ValueError("each connection needs two different known cells")
        value = _number("requested transfer", proposal.requested_m3)
        donor, recipient = (proposal.a, proposal.b) if value >= 0.0 else (proposal.b, proposal.a)
        outbound[donor].append((proposal.edge_id, recipient, abs(value), 1.0 if value >= 0.0 else -1.0))
    remaining = dict(initial)
    incoming: dict[str, list[float]] = {cell: [] for cell in initial}
    actual: dict[str, float] = {}
    scales = {}
    for donor in sorted(initial):
        edges = sorted(outbound[donor])
        demand = _number("total outward demand", math.fsum(item[2] for item in edges), 0.0)
        scale = min(1.0, initial[donor] / demand) if demand else 1.0
        scales[donor] = scale
        for edge_id, recipient, request, sign in edges:
            amount = min(request * scale, remaining[donor])
            remaining[donor] -= amount
            incoming[recipient].append(amount)
            actual[edge_id] = sign * amount
    final = {cell: _number("final water", math.fsum([remaining[cell], *incoming[cell]]), 0.0)
             for cell in initial}
    residual = math.fsum([*final.values(), *(-v for v in initial.values())])
    return TransferResult(final, actual, scales, residual)


def balance_residual(initial: float, final: float, imported: float = 0.0,
                     exported: float = 0.0) -> float:
    """Return final - initial - imported + exported, all in the same units."""
    old = _number("initial total", initial, 0.0)
    new = _number("final total", final, 0.0)
    added = _number("imported total", imported, 0.0)
    removed = _number("exported total", exported, 0.0)
    return math.fsum([new, -old, -added, removed])


def crest_transfer_proposal(stage_a_m: float, stage_b_m: float, crest_m: float,
                             conductance_m2_s: float, dt_s: float) -> float:
    """Educational thresholded linear connection, NOT a weir/culvert formula.

    Q = C * ([eta_a - crest]+ - [eta_b - crest]+); return Q * dt.
    Donor limiting is still required. Large steps can overshoot head equilibrium
    even when water remains nonnegative; choose and verify a stable timestep.
    """
    a, b, crest = (_number("stage a", stage_a_m), _number("stage b", stage_b_m),
                   _number("crest", crest_m))
    conductance = _number("conductance", conductance_m2_s, 0.0)
    step = _number("time step", dt_s, 0.0)
    return _number("proposed volume", conductance * (max(a - crest, 0.0) - max(b - crest, 0.0)) * step)


def run_demo(fixtures_path: Path | None = None) -> dict[str, object]:
    path = fixtures_path or Path(__file__).resolve().parents[1] / "assets" / "numeric-fixtures.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    layer = data["compaction"]
    storage = data["storage_edit"]
    transfer = data["transfers"]
    crest = data["crest"]
    result = transfer_volumes(transfer["volumes_m3"], [EdgeProposal(**item) for item in transfer["edges"]])
    old_stage = stage_for_volume(storage["old_patches"], storage["volume_m3"])
    new_stage = stage_for_volume(storage["new_patches"], storage["volume_m3"])
    pond_volumes = {"upstream": crest["initial_upstream_m3"] + crest["rain_added_m3"],
                    "downstream": crest["initial_downstream_m3"]}
    proposed = crest_transfer_proposal(
        stage_for_volume(crest["pond_patches"], pond_volumes["upstream"]),
        stage_for_volume(crest["pond_patches"], pond_volumes["downstream"]),
        crest["crest_m"], crest["conductance_m2_s"], crest["dt_s"])
    pond = transfer_volumes(pond_volumes, [EdgeProposal("crest", "upstream", "downstream", proposed)])
    return {"origin": data["metadata"]["origin"], "polygon": polygon_metrics(data["polygon"]["vertices_m"]),
            "cut_fill": cut_fill(data["cut_fill"]["patches"]),
            "compaction": compact_layer(**layer["inputs"]),
            "terrain_edit": {"old_stage_m": old_stage, "new_stage_m": new_stage,
                             "preserved_volume_m3": storage["volume_m3"],
                             "reconstructed_volume_m3": stage_volume(storage["new_patches"], new_stage)},
            "shared_transfers": asdict(result), "pond_crest": asdict(pond),
            "pond_budget_residual_m3": balance_residual(
                crest["initial_upstream_m3"] + crest["initial_downstream_m3"],
                math.fsum(pond.volumes_m3.values()), imported=crest["rain_added_m3"])}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["demo"])
    parser.add_argument("--fixtures", type=Path, help="Optional fixtures JSON with the bundled schema")
    args = parser.parse_args()
    print(json.dumps(run_demo(args.fixtures), indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
