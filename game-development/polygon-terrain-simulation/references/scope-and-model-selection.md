# Scope and model selection

Use this reference to choose a sufficient model before selecting equations or libraries. The profiles below are recipes, not mandatory maturity levels. A finished game may deliberately remain on any profile.

## Contents

- [Define the observable behavior](#define-the-observable-behavior)
- [Select a profile](#select-a-profile)
- [Keep independent axes independent](#keep-independent-axes-independent)
- [Recommended first implementation](#recommended-first-implementation)
- [Model selection examples](#model-selection-examples)
- [Set an explicit boundary](#set-an-explicit-boundary)

## Define the observable behavior

Write down what a player must be able to change and observe:

1. The spatial scale: a house foundation, individual ditch, river corridor, or whole continent.
2. The time scale: seconds of flooding, days of drying, seasons, or centuries of erosion.
3. The allowed operations: grading, excavation, filling, dams, canals, soil movement, or only cosmetic painting.
4. The consequence: buildability, crop water, flood damage, navigability, resource yield, or visual variation.
5. The budget: active cells, memory, update interval, target platform, and acceptable lag.

If unspecified, choose an engine-neutral, fixed polygon simulation mesh with editable 2.5D material columns. Assume construction-scale earthworks and persistent water accounting. State these assumptions and continue; do not block a conceptual design on an engine choice.

Distinguish four meanings of “water moves over time”:

| Observation | Minimum relevant mechanism |
|---|---|
| Rain drains toward another outlet after a trench | Changed topography and routing |
| A pond rises, a road floods, a dam backs up water | Stored volume, stage, and hydraulic exchange |
| A well draws down water or an excavation seeps | Soil storage and a chosen groundwater/head model |
| A river shifts sideways or cuts through a bend | Bed/bank change, sediment movement, and lateral connectivity |

One mechanism does not establish the others. A routing arrow is not a water inventory.

## Select a profile

| Profile | State and behavior | Suitable use | Deliberate limitations |
|---|---|---|---|
| **Map and earthworks** | Material columns, immutable initialization parameters, editable geometry, cut/fill ledger; decorative or prescribed water | Builder prototype, dry terrain game | No claim of emergent flooding |
| **Catchments and reservoirs** | Runoff routing, bounded soil buckets if needed, explicit lake volumes and outlet rules | Water supply, seasonal management, distant regions | Limited flood timing and local inundation detail |
| **Conserved polygon hydraulics** | Cell water volume, storage curves, shared face flows, wet/dry handling, structures, local terrain changes | Dams, canals, flooded foundations, changing drainage | Accuracy depends on closure, mesh, and timestep |
| **Morphodynamic landscape** | Prior profile plus sediment inventory, entrainment, transport, deposition, optional bank motion | Long-lived evolving valleys, silting reservoirs, migrating channels | Requires explicit process/time-scale choices |
| **Specialized physical model** | Selected inertial hydraulics, aquifers, multiple grains, slope failure, conservative remeshing | Game mechanic or research question that depends on those effects | Greater parameter, verification, and integration cost |

The recommended *architecture* for an editable settlement world can accommodate conserved polygon hydraulics. The first *implementation* can still use reservoirs and simple face conductances.

Do not call a conductance toy model a shallow-water solver. Do not call plausible animation calibrated physical prediction. Conversely, do not reject a simple model when it supplies the requested gameplay.

## Keep independent axes independent

Choose independently:

- **Geometry:** regular grid, Voronoi cells, arbitrary polygons, triangular terrain patches, local subcells, or a hybrid.
- **Initialization:** noise, artist constraints, drainage-first terrain, imported elevation, erosion preprocessing, or combinations.
- **Material detail:** one bulk material, several layers, grain classes, mixed fractions, weathering.
- **Water detail:** routing, reservoirs, diffusion-like exchange, local-inertial equations, full shallow-water equations.
- **Subsurface detail:** none, bucket, lateral groundwater network, distributed aquifer.
- **Morphology detail:** none, vertical erosion/deposition, bank migration, slope failure.
- **Runtime detail:** always active, regional summaries, streamed chunks, adaptive computational mesh.

For example, rich layered excavation does not require full groundwater. Detailed water can run over fixed ground without erosion. A stylized polygon render can use a fine hidden computational grid. Different inactive-region approximations need a conservative exchange contract, not identical internal implementations.

## Recommended first implementation

Build a small closed test world with:

1. Stable cell and face IDs and checked geometry.
2. One authoritative definition of material quantity and derived surface elevation.
3. One cut/fill operation with partial footprint areas.
4. One surface-water inventory and explicit boundaries, if water affects gameplay.
5. One shared transfer per connection and a budget report.
6. One transaction that changes terrain while preserving material and water ownership.
7. Save/load of evolved state, operation progress, and model versions.
8. A render/collision adapter that consumes committed revisions.

Add a second material only when exposure or excavation matters. Add soil water when infiltration, plants, or compaction matters. Add momentum only when waves, rapid transitions, or flow dynamics make the simpler closure insufficient. Add lateral erosion when channel movement itself matters.

Do not require every field from the reference data dictionary in every game. A disabled process should have a declared behavior, such as “no infiltration; surface water leaves only through modeled outlets and evaporation,” rather than an unused parameter collection.

## Model selection examples

### A small village with flattenable foundations

Use material-aware grading, foundation footprint queries, a stored target surface, and operation progress. Use a coarse drainage warning or reservoir model if the only water consequence is “site can become wet.” Avoid groundwater and bank stability until a gameplay requirement calls for them.

### A town with irrigation canals and dams

Represent water volume and head, physical hydraulic connections, barriers and culverts, and withdrawal grants. Include a soil bucket if irrigation changes soil storage. Keep roughness and infiltration independent. Diagnose whether a diffusion-like model reproduces the intended transient response before adopting a more expensive solver.

### A river that changes course over many seasons

Add sediment availability, bank geometry, erosion/deposition and a stated lateral-motion model. Specify when channel incision, bend migration and avulsion should occur. Decide whether the world advances real physical time or uses an explicit accelerated morphology rule. Test whether those rules preserve material even when their timing is stylized.

### A world with underground tunnels

Keep the surface polygon system for terrain, catchments and soil columns. Add a separate volumetric or constructive geometry representation where tunnels need it, plus explicit hydraulic connections. A basement cut open from above does not by itself require the entire world to become voxels; intact overburden above a tunnel cannot be represented by a single-valued height surface.

## Set an explicit boundary

Deliver a model-selection record with:

- Required observations and smallest relevant feature.
- Chosen state, solver family and geometric assumptions.
- Included processes, intentional omissions and reasons.
- Units, boundaries, forcing, persistence and ownership rules.
- Validation cases and accepted error/latency.
- Upgrade points that retain the same public contracts.

Use a small number of measured budgets to decide upgrades. More equations increase fidelity only when their assumptions, parameter values, resolution and coupling are adequate.

### Sources and interpretation

[Red Blob's polygon generator](https://theory.stanford.edu/~amitp/game-programming/polygon-map-generation/) and [noise terrain article](https://www.redblobgames.com/maps/terrain-from-noise/) are useful initialization references. They are not specifications for persistent material or water simulation. The profiles and architecture choices above are original engineering recommendations.
