# Runtime scheduling and process coupling

## Contents

- [Keep domain state authoritative](#keep-domain-state-authoritative)
- [Declare process contracts](#declare-process-contracts)
- [Advance simulation time deliberately](#advance-simulation-time-deliberately)
- [Couple processes through conserved transfers](#couple-processes-through-conserved-transfers)
- [Invalidate by dependency](#invalidate-by-dependency)
- [Parallel work and publication](#parallel-work-and-publication)
- [Measure the right costs](#measure-the-right-costs)
- [References](#references)

## Keep domain state authoritative

Treat material columns, water and sediment stores, physical connections, boundary conditions and active terrain operations as the world. Rendering, collision, navigation and regional summaries are projections of that state. A projection can have a different resolution and update schedule; it cannot silently overwrite the quantities it displays.

Keep stable cell/face IDs separate from compact array indices, GPU buffers and engine object handles. Store explicit field locations and units. A value at a cell center, a layer, a vertex or a face has different semantics even when represented by the same scalar type.

Adopt the smallest scheduling machinery that works. A single-process loop with clear ownership is sufficient for many games; an event bus, distributed runtime or full entity-component framework is optional. The contracts in `domain-contracts.md` need not become network services.

## Declare process contracts

Give each process a compact descriptor:

| Contract | Example |
|---|---|
| Inputs and field locations | Cell water volumes; face geometry |
| Outputs | Realized face transfers; updated cell volumes |
| Units | Seconds, meters, cubic meters |
| Validity assumptions | Orthogonal mesh; fixed bed during hydraulic substep |
| Step constraint | Stability limit plus chosen accuracy bound |
| Dependencies | Storage curve and structure revisions |
| Invalidations | Water stage, hazard summaries, sediment transport inputs |
| Budget entries | External inputs, outputs and internal transfers |

A cache is usable only when its dependency revisions match the snapshot being evaluated. Avoid one global `dirty` flag that hides which geometry, material or forcing changed. Check parameter units at the adapter boundary; a component using years cannot consume a timestep in seconds without conversion.

## Advance simulation time deliberately

Separate simulation seconds, game calendar and rendering frame time. For a selected simulation interval, stop at the earliest process constraint or scheduled event:

\[
\Delta t=\min(\Delta t_{remaining},\Delta t_{stable},
\Delta t_{accuracy},t_{event}-t).
\]

All terms have units seconds. Handle events at the current time before advancing; do not enter a zero-step loop. Stability may be local or computed by a solver; accuracy limits also constrain forcing interpolation and coupling. An implicit solver still needs accuracy checks.

**Original example:** an interval from 100 to 110 s has a gate change at 103 s and a hydraulic limit of 2 s. Advance 2 s, then 1 s, apply the gate event, then continue. Advancing directly to 104 s with the old gate creates a timing error even if water remains conserved.

Use a fixed outer tick when it helps gameplay, with adaptive physical substeps inside it. Accumulate the actual substep durations so each component reaches the same endpoint. Keep numerical time tolerances small and explicit; integer tick identifiers can coexist with fractional substeps.

For fast-forward, decide whether to spend more computation, reduce model fidelity under an explicit policy, or limit the requested acceleration. Dropping elapsed simulation time or enlarging an unstable step is not a valid substitute. Checkpoint long catch-up operations so they can resume.

## Couple processes through conserved transfers

A simple first-order split may apply forcing and soil exchange, advance surface flow, advect sediment using realized water transfers, then update bed layers and derived geometry. Choose and document one ordering; this example is not a universal sequence. Strong interactions may require tighter substeps or iterations.

Every transfer must have one actual amount and identified stores. If infiltration, evaporation, pumps and boundary flow compete for surface water, coordinate their withdrawals instead of letting each process independently spend the same old volume. Apply the same principle to loose sediment consumed by hillslope transport, excavation and hydraulic erosion.

For morphology on a slower schedule, accumulate physically meaningful drivers over the intervening hydraulic steps. A mean discharge inserted into a nonlinear erosion law is not generally equivalent to integrating that law through a flood. Decide whether this approximation is acceptable and test the observable effect. Recompute flow geometry once the bed changes enough to invalidate the hydraulic step's assumptions.

Keep forcing interpolation explicit: piecewise constant, linear or event-resolved rainfall produce different timing. Record whether a rate is instantaneous, interval-mean or already integrated. Do not multiply an integrated transfer by the timestep again.

Landlab's timestep guidance illustrates the key distinction: individually stable components can still yield inaccurate coupled results when their exchange interval is too large. Test coupling-interval reduction separately from each solver's internal timestep reduction.

If accelerating erosion relative to water for gameplay, expose a named dimensionless multiplier or separate morphology clock. Document which quantities it scales and keep the solid ledger consistent. Do not silently reinterpret a per-year coefficient as per-second.

## Invalidate by dependency

Classify changes by what they affect:

| Change | Likely dependents |
|---|---|
| Vertex/height edit | Local render normals, collision, storage geometry |
| Face crest or culvert change | Hydraulic connectivity, reservoir outlets, downstream transfer |
| Material exposed or compacted | Excavation resistance, infiltration, erosion and slope parameters |
| Water stage change | Wet area, hazard queries, shoreline, possibly navigation cost |
| Bed deposition | Channel cross-section, layer stack, downstream morphology |

Geometric locality and physical influence are different. A small dam can affect an entire upstream reservoir. Follow basin, routing and boundary dependencies; do not stop physical recomputation at the rendering tile's radius. Conversely, a remote river response need not rebuild all terrain rendering.

Distinguish invalidated derived data from an advancing physical process. A flood is not “recomputed instantly” from a static downhill map unless that is the declared model. Rebuild the operators and then simulate the selected transient response.

## Parallel work and publication

Read immutable snapshots for independent computations. Assign one owner to each shared face transfer, then gather/apply contributions with a controlled reduction. Parallel workers must not each decrement a neighbor's old store with uncoordinated limits.

Attach source revisions to asynchronous collision, mesh and navigation jobs. Discard or reschedule a result if its source state is obsolete; do not publish a late old surface over a newer edit. Coalesce repeated visual work while preserving operation and simulation semantics.

Define a readiness policy: either publish compatible render/collision/navigation revisions together, or temporarily keep the changed region unavailable for affected actions. The player may see construction progress before navigation is ready, but agents should not use a newly drawn bridge whose usable surface has not been published. See `engine-integration.md` for adapters.

## Measure the right costs

Profile hydraulic steps, geometry rebuilds, collision cooking, navigation updates and serialization separately. Record active cell counts, face counts, substeps, solver iterations and dirty queue lengths. Report measured workloads and hardware; polygon count alone does not predict performance.

Sleep regions only through a declared inactive-state model, not by deleting small stores. Batch visual updates independently from conservative simulation work. Verify full versus incremental recomputation, thread-count sensitivity where relevant, and response to event timing. Stop optimization when the measured budget is satisfied and remaining error fits the gameplay requirements.

## References

- [Landlab: time steps](https://landlab.csdms.io/user_guide/time_steps.html) — component substepping and coupled-model accuracy.
- [Landlab: unit consistency](https://landlab.csdms.io/user_guide/units.html) — component input/output unit contracts.

The ownership, invalidation and publication policies here are original architecture recommendations, independent of an engine or task scheduler.
