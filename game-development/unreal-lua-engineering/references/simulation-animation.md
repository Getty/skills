# Simulation, performance and animation boundaries

Use this when Lua is proposed for many entities, production chains, jobs, needs, terrain interaction or character behavior. The architecture below is a starting design to measure, not a capacity claim.

## Assign work by responsibility

| Responsibility | Proposed owner | Lua-facing interface |
|---|---|---|
| Rules and content | Lua modules/data | Recipes, requirements, priorities, decisions, event reactions |
| Dense state and bulk transformations | Measured choice of native or Lua implementation | Batches, snapshots and command buffers |
| Spatial indexing, terrain rebuilds, route search | Existing engine/native systems unless measurement supports another choice | Query/request/result contracts |
| Authoritative state transitions | One simulation owner | Validated commands and versioned results |
| Pose evaluation, mesh deformation, rendering | Unreal animation/rendering systems | Intent, speed, stance, action and timing parameters |
| UI/input and cosmetic responses | Client/local-player logic | Selection, preview, status and presentation events |

Lua can contain substantial real gameplay logic. Do not reduce it to configuration only without a measured reason. Equally, do not translate every existing native data access into a separate reflected Lua call merely to keep all source in one language.

## Update scheduling

Choose update frequency from the simulated phenomenon, rather than the rendered frame rate. Hunger, production completion, job selection and camera movement need different schedules. Use event-triggered decisions and scheduled deadlines where useful. Define overload behavior: catch up a bounded number of simulation steps, slow simulation deliberately, or surface missed deadlines according to game requirements.

Use explicit simulation time, deterministic ordering where needed, and a supplied RNG/state rather than unrelated clock reads scattered through scripts. Those choices improve reproducibility; they do not establish cross-platform determinism by themselves. Floating-point operations, unordered traversal, asynchronous completion order and native navigation can still differ. Validate determinism against recorded commands/state hashes if replay or lockstep actually requires it.

Batch APIs should specify the meaning of partial failure. A script that mutates inventories and then errors leaves a different problem from a pure evaluator that returns an invalid command. For transactional rules, evaluate against a snapshot or record a command buffer, validate its invariants, then commit as one native operation.

## Measure the boundary, not only the script body

Capture native dispatch time, Lua execution, allocation/collection, marshaling, number of cross-language calls, native bulk work and replicated payload volume. Report entity count together with active count, work frequency, target frame/tick budget, hardware and build configuration.

Start with a representative workload: several building recipes, failed reservations, route requests, entity removal and a burst of completed jobs. A tight arithmetic benchmark cannot establish population capacity or tail latency.

Epic supplies [Unreal Insights](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-insights-in-unreal-engine) for runtime trace capture and analysis. Add coarse scopes around bridge entry, simulation phases and callbacks, then refine only the measured hot path. Track distributions and worst relevant bursts, not merely average frame time.

If an ECS is already used, preserve its intended data flow. [MassEntity](https://dev.epicgames.com/documentation/en-us/unreal-engine/mass-entity-in-unreal-engine) is a data-oriented gameplay framework; that does not imply arbitrary Lua closures can run inside its worker-thread processors. Copy or expose an appropriate batch contract and dispatch script work on its owning execution context. Keep any Apparatus or other ECS integration version-specific and separately verified.

## Use existing skeletal animation assets

Lua chooses an action such as walking, carrying, working or resting. An Unreal presentation component derives animation parameters, while Animation Blueprints evaluate the resulting pose. Epic documents Animation Blueprints as controlling skeletal-mesh animation, blending and pose logic: [Animation Blueprints](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-blueprints-in-unreal-engine).

Prefer a small action/state vocabulary over Lua manually driving every bone or reproducing a blend tree. Decide how interruption, locomotion transitions, carrying variants and animation completion affect gameplay. For distant characters, choose the required visual fidelity deliberately and measure the complete representation cost.

Separate authoritative action completion from optional visual callbacks. A production result must have defined behavior even when its character is offscreen, has reduced animation updates or is running on a headless server. If animation timing, root motion or notifies are essential to gameplay, declare and verify that server-side dependency explicitly rather than assuming every client sees the same timeline.

Epic documents game-thread Event Graph execution and worker-thread-capable animation paths in [Animation Optimization](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-optimization-in-unreal-engine). Consequently, never call a shared game-thread Lua VM from a thread-safe animation update merely because the function is marked thread-safe in Blueprint. Publish copied/approved state for worker evaluation.

## Save data and code versions

Persist explicit entity IDs, component/domain data, simulation time, pending jobs, required RNG state and schema/content versions. Reconstruct transient callbacks, UObject wrappers and VM-local resources on load. Arbitrary Lua closures or native pointers are not a useful stable save schema.

A content update needs a migration policy for removed buildings, renamed item IDs, changed recipe durations and pending actions. Test a save made before the change. Avoid making object identity depend on source filenames or table iteration position.

## Incremental implementation order

For a terrain-led prototype: first verify the polygon surface and editing; next attach one controllable character and the existing animation pipeline; then add one Lua-defined production building and a local presentation. Establish one correct command/state boundary before multiplying systems. Add networking, mass scheduling and reload only as the project requires, using the concrete gates in `verification-troubleshooting.md`.
