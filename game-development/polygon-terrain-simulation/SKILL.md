---
name: polygon-terrain-simulation
description: "Use when building or debugging editable polygon or Voronoi terrain for a game — map generation and climate, layered soils and bedrock, excavation and cut/fill, dams and canals, surface water and groundwater, erosion and sediment, map rendering, saving or streaming an evolving landscape."
---

# Polygon Terrain Simulation

Build a persistent physical world with the smallest model that supplies the requested gameplay. Treat this skill as an extensible knowledge base, not a requirement to implement every listed process.

Keep construction management, inventory/logistics and population needs independent. Define explicit interfaces and quantity ownership; do not make the terrain solver depend on a citizen or building lifecycle.

## Start with the required behavior

1. Identify the observable mechanic, spatial scale, time scale, target platform and existing state model.
2. Inspect relevant project instructions and current code before proposing replacements.
3. If context is absent, use an engine-neutral fixed polygon mesh, editable 2.5D material columns and SI units as provisional assumptions. State them and continue.
4. Select a profile using [scope and model selection](references/scope-and-model-selection.md). Keep advanced processes optional.
5. Read only the references relevant to the task. Do not load the entire knowledge base by default.

Distinguish drainage rerouting, changing flood extent, groundwater movement and channel migration. Each requires different state and processes.

## Choose the task reference

| Task or uncertainty | Read |
|---|---|
| Scope, fidelity, prototype versus advanced model | [Scope and model selection](references/scope-and-model-selection.md) |
| Red Blob, noise, initialization, hydrology-first generation | [Initialization and generation](references/initialization-and-generation.md) |
| Noise shaping, island borders, ridges, terraces, periodic fields, Mapgen2 stages | [Generation recipes](references/generation-recipes.md) |
| Painted terrain, Mapgen4, climate scores, rainfall and biome initialization | [Authored terrain and climate](references/authored-terrain-and-climate.md) |
| SVG/shader map previews, color lookup, relief and field diagnostics | [Terrain map rendering](references/terrain-map-rendering.md) |
| Polygon topology, field placement, metrics, nonorthogonal gradients, remeshing | [Mesh and fields](references/mesh-and-fields.md) |
| Layers, dry mass, density, porosity, compaction, exposed substrate | [Layered materials](references/layered-materials.md) |
| Building pads, roads, excavation, fill and partial work | [Terrain operations](references/terrain-operations.md) |
| Surface water, routing, shared-face flux, timestep and wet/dry handling | [Surface water](references/surface-water.md) |
| Storage curves, disconnected pools, sills, dams, culverts, water under edits | [Lakes and structures](references/lakes-and-structures.md) |
| Buckets, infiltration, Darcy flow, wells and aquifer choices | [Soil water and groundwater](references/soil-water-and-groundwater.md) |
| Sediment availability, transport, deposition and bed change | [Erosion and sediment](references/erosion-and-sediment.md) |
| Riverbank erosion, lateral migration, cutoffs and avulsion | [Channel migration](references/channel-migration.md) |
| Hillslope transport, failure approximations and vegetation coupling | [Slopes and vegetation](references/slopes-and-vegetation.md) |
| Time scheduling, operator coupling, dirty dependencies, projections | [Runtime and coupling](references/runtime-and-coupling.md) |
| Save/load, revisions, chunk boundaries, inactive regions, reproducibility | [Persistence and streaming](references/persistence-and-streaming.md) |
| Render, collision, navigation, optional Unity/Unreal adapters | [Engine integration](references/engine-integration.md) |
| Separate building/logistics/needs systems and material handoff | [Domain contracts](references/domain-contracts.md) |
| Parameter meaning, synthetic data, units and calibration | [Parameter data and calibration](references/parameter-data-and-calibration.md) |
| Equation symbols, dimensions and formula-card template | [Formulas and units](references/formulas-and-units.md) |
| Conservation, equilibrium, scenario tests, convergence and diagnostics | [Validation and debugging](references/validation-and-debugging.md) |
| Runnable arithmetic, fixtures and bounded snapshot audit | [Numerical examples](references/numerical-examples.md) |
| Primary literature, implementations and source limits | [Sources and implementations](references/sources-and-implementations.md) |

## Establish the world contract

Specify:

- **Authoritative state:** material quantities and layers, water/sediment stores, geometry, connections, boundaries and active operations.
- **Derived state:** elevation where mass determines it, water stage, render mesh, collision, navigation, vegetation placement and regional summaries.
- **Identity:** stable world/cell/face/operation IDs, independent of GPU indices and dense array positions.
- **Units and orientation:** consistent length/time/mass units, vertical datum, face signs, and extensive versus intensive quantities.
- **Ownership:** exactly one canonical owner for every physical quantity; derived piles and inventory views do not duplicate mass.
- **Optional processes:** declare disabled behavior and extension points instead of inserting unused mandatory fields.

Use the sample assets as illustrations, not a required production schema:

- [Material records](assets/material-examples.json): synthetic, uncalibrated parameters.
- [World snapshot](assets/world-state-example.json): four orthogonal polygon cells with analytical budgets.
- [Numeric fixtures](assets/numeric-fixtures.json): independently checkable calculations.
- [Domain transfer](assets/domain-transfer-example.json): idempotent material handoff.
- [Generation examples](assets/generation-examples.json): synthetic shaping, brush, climate/runoff and palette arithmetic; optional recipes, not calibrated world parameters.

## Preserve physical and numerical invariants

1. Use geometry compatible with the chosen operator. A visually modified Voronoi/barycentric dual is not automatically orthogonal.
2. Compute each internal transfer once and apply equal opposite contributions.
3. Distinguish per-width flux from volumetric discharge; multiply by face width exactly once.
4. Limit all competing withdrawals by actual available donor stores. Do not repair overspending with a post-update clamp.
5. Preserve water volume when changing terrain geometry; derive stage from the new storage curve.
6. Preserve dry material mass across excavation, transport, filling and compaction. Account for displaced/carried pore water if that store exists.
7. Keep drainage analysis distinct from physical terrain edits and transient hydraulic storage.
8. Match sediment removal to finite available material and update exposed-layer properties.
9. Treat local edits as potentially nonlocal hydraulic changes.
10. Save evolved state, not only a generation seed. Resume operations idempotently.

Treat these as correctness conditions for included mechanisms. Do not demand groundwater, erosion or mass-based construction if the chosen game explicitly omits them.

## Implement or explain in a bounded workflow

1. State the chosen model and deliberate omissions.
2. Define fields, units, ownership, boundaries and geometric assumptions.
3. Select governing relations with assumptions, parameter provenance and a small worked example.
4. Define discrete transfers, timestep/accuracy limits, process ordering and events.
5. Implement the requested behavior through existing project conventions.
6. Invalidate and rebuild affected projections by revision; synchronize usability with required collision/navigation readiness.
7. Verify the relevant invariants and one observable scenario. Broaden tests only for a concrete remaining risk.
8. Report what changed, what was actually checked, model limits and next compatible extension points.

For concept-only requests, deliver the same design decisions without manufacturing a full engine implementation. For implementation requests, carry through to code and meaningful verification.

## Use the reference utilities

Run from this skill's directory:

~~~bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/reference_math.py demo
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_reference_math.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_snapshot.py assets/world-state-example.json
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_snapshot_audit.py
~~~

Use `reference_math.py` for weighted cut/fill, layer geometry, compaction, stage-volume inversion, shared-edge limiting and budget residuals. Its linear crest rule is a teaching closure, not a calibrated weir model.

Use `audit_snapshot.py` only for its documented illustrative schema and conforming rectangular-domain geometry. Do not claim it verifies arbitrary polygon tessellations or production saves. General polygon metrics in the arithmetic helper use ordinary floating-point predicates.

Keep reference checks distinct from validation of a game-specific hydraulic or morphology solver.

## Keep evidence and depth honest

- Label synthetic values, fitted coefficients, measured data and game tuning separately.
- Prefer primary documentation/papers for physical models. Verify current engine APIs when integrating.
- Check dimensions and signs independently; do not reproduce a source's typographical error.
- Include an explicit source and limits for a model; do not invent universal soil constants.
- Avoid promising realistic river migration from downhill routing or vertical erosion alone.
- Avoid treating subgrid storage as unlimited resolution or full 3D flow.
- Keep tunnels/overhangs in an additional representation when a single-valued surface cannot describe them.
- Do not claim cross-platform deterministic replay without deliberately engineered and tested support.
- Preserve this skill's modularity when adding future references or neighboring skills.
