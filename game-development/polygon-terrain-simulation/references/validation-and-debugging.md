# Validation and debugging

Choose tests for the implemented mechanisms. The scenario catalog below is a design reference; it does not claim that the bundled arithmetic utilities implement or validate all these processes.

## Contents

- [Establish invariants](#establish-invariants)
- [Run the bundled checks](#run-the-bundled-checks)
- [Select scenario tests](#select-scenario-tests)
- [Inspect the right diagnostics](#inspect-the-right-diagnostics)
- [Check convergence and scale](#check-convergence-and-scale)
- [Diagnose common failures](#diagnose-common-failures)

## Establish invariants

Define the control-volume domain, included stores, external sources/sinks and tolerance. For constant-density water, sum surface water, relevant soil/aquifer stores, connected containers and transfers in flight without overlapping them. For solids, sum in-ground material, mobile sediment, loads, piles and placed fill under canonical ownership.

Require:

- Finite geometry and parameter values.
- Positive cell areas and appropriate distances.
- Nonnegative physical stores.
- Porosity in the chosen physically admissible range.
- Mixture fractions on one basis, summing to one.
- One shared flux at each internal connection.
- Internal transfer cancellation.
- Consistent derived thickness, stage and density.
- Revisions and operation IDs that prevent replayed edits.

Use the residual in [formula conventions](formulas-and-units.md). Track cumulative residuals and individual-step residuals. A gradual leak can be invisible in a screenshot and still alter a world over a long save.

## Run the bundled checks

From the skill directory:

~~~bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_reference_math.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/reference_math.py demo
PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_snapshot.py assets/world-state-example.json
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_snapshot_audit.py
~~~

Consult [numerical examples](numerical-examples.md) for the exact supported schema, APIs and limitations. The scripts are small standard-library reference utilities. They do not implement a full hydrodynamic, erosion or geotechnical engine.

The supplied tests use analytical answers, conservation, positivity, symmetry/orientation and invalid inputs. Adapt invariants to a game's schema; do not import toy material values as validation of a real landscape.

## Select scenario tests

| Scenario | Expected property | Capability required |
|---|---|---|
| Rectangle and reversed winding | Same physical area/centroid | Geometry |
| Linear scalar field on skew mesh | Correct normal gradient or explicit rejection | Chosen spatial operator |
| Partial foundation footprint | Only overlap contributes cut/fill | Earthworks |
| Excavate two layers | Correct materials and mass, exposed lower layer | Stratigraphy |
| Refill at new compaction | Same dry mass, different bulk volume | Placement state |
| Compact saturated soil | Excess pore water appears in a receiving store | Soil water |
| Closed rainfall basin | Storage change equals forcing minus explicit losses | Water stores |
| Donor with several exits | Combined outflow never overspends donor | Transfer limiter |
| Still lake over varied bed | No artificial circulation | Hydraulic closure/source balancing |
| Two disconnected pits | No exchange before a valid connection exists | Subcell connectivity |
| Road with culvert | Culvert path before crest overtopping when head allows | Structures |
| Raised bed beneath a pond | Volume preserved, stage changes | Geometry/water coupling |
| Thin sediment cover erodes away | Bedrock becomes exposed, regime updates | Erosion/layers |
| Sediment deposits in a channel | Bed/capacity changes with accounted solids | Morphodynamics |
| Bank fails | Failed mass enters a physical destination | Lateral morphology |
| Pump withdraws more than available | Actual grant bounded; downstream receives actual grant | Domain contracts |
| Save/load mid-earthworks | Same applied amount; no duplicated transfer | Persistence |
| Load/unload a watershed | No artificial sink, wall or new water | Streaming |
| Same world, different chunks | Equivalent budgets and acceptably close dynamics | Partitioning |
| Partial versus full recomputation | Equivalent affected result | Invalidation |
| Finer mesh/smaller step | Error approaches an accepted regime | Numerical model |

Some tests require a purpose-built solver harness and are deliberately not executable in the skill's small utilities. Report which ones were actually run.

## Inspect the right diagnostics

Render numerical facts separately from artistic presentation:

- Surface elevation, water stage and water depth as distinct layers.
- Face flux direction and magnitude, with hydraulic barriers.
- Cell and regional budget residuals.
- Wet area, storage curve and outlet threshold.
- Actual versus requested transfers and donor limiter factors.
- Material class, exposed layer, porosity and remaining mobile inventory.
- Current stable-step limit and the process setting it.
- Dirty dependencies and revision age for collision/navigation.
- Active/coarse region boundaries and cross-boundary transfer ledger.

A small clickable cell/face inspector often resolves problems faster than another global texture. Display units and sign convention in the inspector.

## Check convergence and scale

### Time refinement

Run the same forcing schedule at \(\Delta t\), \(\Delta t/2\) and, if needed to resolve a concrete uncertainty, \(\Delta t/4\). Compare quantities relevant to gameplay: peak stage, overflow time, cumulative discharge, material moved and hazard onset.

A conservation check can pass while peak timing is wrong. A positivity limiter can conceal an excessively large timestep by repeatedly starving outflows. Inspect how often limiting activates.

### Spatial refinement

Refine critical channels, barriers and footprints while holding the physical geometry and forcing consistent. Changing both random terrain and resolution is not a convergence experiment.

Use a transfer/remapping test separately from a solve test. A remesh that preserves total water may still destroy lake equilibrium or merge disconnected basins.

### Coupling refinement

Change the interval between water, infiltration and morphology updates. Individually stable components can still interact inaccurately. Compare process order if edits or forcing change quickly.

### Performance

Measure active cells/faces, process time, allocations, update latency and worst-case event cost on the actual target. Do not promise “millions of polygons at 60 FPS” without a benchmark. Report physical simulation interval separately from render frame rate.

## Diagnose common failures

| Symptom | Likely checks |
|---|---|
| Water created around a dam | Negative-store clamps, two independent face evaluations, stage recomputed as conserved depth |
| Lake slowly drains through closed walls | Boundary leakage, discarded small volumes, omitted soil/export accounts |
| Flow follows ground slope inside a lake | Used bed gradient instead of stage/head |
| Oscillating water levels | Excessive timestep, steep nonlinear closure, inconsistent implicit/explicit coupling |
| Unrealistic diagonal flow | Mesh/operator mismatch, wrong normals, metric omission |
| Dirt quantity changes after hauling | Bulk volume treated as mass, different compaction ignored, double-counted piles |
| Old soil properties remain after digging | Exposed-layer cache not invalidated |
| Building floats or agents fall | Render/collision/navigation revisions disagree |
| River never moves sideways | Only vertical incision/routing implemented |
| All rivers migrate instantly | Unbounded bank motion, scale/unit error, accelerated time applied twice |
| Reload repeats a cut | Progress/transaction replay not idempotent |
| Unloaded land floods differently | Boundary conditions changed with visibility |

Fix the physical/accounting cause before smoothing the visual output. If a feature is intentionally stylized, keep its approximation explicit and preserve the chosen quantity invariants.

### Source basis

The scenario catalog is original engineering guidance. General coupling caution is supported by [Landlab time-step guidance](https://landlab.csdms.io/user_guide/time_steps.html); hydraulic timestep selection is model-specific as described in [HEC-RAS grid/timestep guidance](https://www.hec.usace.army.mil/confluence/rasdocs/r2dum/6.0/running-a-model-with-2d-flow-areas/selecting-an-appropriate-grid-size-and-time-step).
