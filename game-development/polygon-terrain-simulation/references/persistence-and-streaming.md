# Persistence, streaming and world continuity

## Contents

- [Save the evolved world](#save-the-evolved-world)
- [Create consistent snapshots](#create-consistent-snapshots)
- [Resume operations safely](#resume-operations-safely)
- [Own cross-chunk transfers](#own-cross-chunk-transfers)
- [Reduce inactive regions explicitly](#reduce-inactive-regions-explicitly)
- [Reactivate conservatively](#reactivate-conservatively)
- [Versioning and reproducibility](#versioning-and-reproducibility)
- [Validation scenarios](#validation-scenarios)

## Save the evolved world

A seed recreates an initial generation recipe only under compatible algorithms and parameters. It does not encode the player's excavations, moved materials, current lake contents, storms already processed or an unfinished dam. Save authoritative current state as the normal continuation path.

Use a manifest that identifies the world, schema, coordinate/unit conventions, simulation time and relevant versions. Include the following when enabled:

| State | Why it matters |
|---|---|
| Stable topology and geometry | Reattach cells, faces, layers and structures |
| Material identities, masses and placement state | Preserve quantities and exposed properties |
| Surface, soil and aquifer stores | Preserve water and pressure/storage interpretation |
| Suspended/mobile sediment | Preserve material outside the bed |
| Boundary and forcing state | Avoid repeating or skipping input |
| Operation progress and accepted receipts | Resume work without duplicating it |
| Simulation clocks and stochastic state | Continue the same selected process realization |
| Budget baselines and pending exchanges | Explain quantity changes across a save |

Store derived caches only when useful for load speed, with dependency revisions and an invalidation rule. A cache must be rebuildable from the authoritative state or explicitly promoted to saved authoritative state. Regenerating terrain over an edited chunk is not cache rebuilding.

## Create consistent snapshots

Choose a logical simulation barrier or use a coherent snapshot mechanism. Do not save half a face transfer with its donor at the new tick and recipient at the old tick. Capture the same transaction boundary across material ownership handoffs as described in `domain-contracts.md`.

Write a new snapshot generation, validate its manifest and required chunks, then atomically publish it as current using the persistence mechanism appropriate to the runtime. Preserve a last-known-valid generation until publication succeeds. A checksum detects corruption; it does not prove physical consistency.

Allow background serialization from immutable snapshots. Record the snapshot's simulation time rather than the later time at which disk writing finishes. If subsequent operation records supplement a snapshot, replay only those after its committed sequence and only once.

For a small single-process game, a transactional file or database snapshot may be enough. A journal, incremental chunk saves and remote persistence are optional scaling choices. Do not introduce a distributed protocol solely because the terrain uses chunks.

## Resume operations safely

Persist stable operation IDs, the accepted plan/target, baseline revisions, applied progress and material transfer receipts. Advance from an acknowledged progress value to a newer value; receiving the same command again should return the existing outcome rather than excavating twice.

Keep operation lifecycle distinct from building lifecycle. Deleting a house does not implicitly restore old terrain or return already moved soil. A rollback or restoration is a new physical operation with its own material and water consequences.

When the target region changed while an operation was paused, apply the declared conflict policy: revalidate/replan, serialize overlapping work, or reject stale progress. Never silently reinterpret an old absolute target as an additional relative height change. See `terrain-operations.md` for planning and execution semantics.

Continuous erosion need not generate an event for every tiny update. Save current physical state and meaningful events; choose snapshot frequency based on acceptable recovery loss and cost.

## Own cross-chunk transfers

A chunk boundary is an implementation boundary unless it is explicitly a physical boundary. Assign each shared face one canonical ID, orientation and computation owner. Its neighbors apply the same realized transfer with opposite signs, even when stored in different arrays or loaded at different times.

For region \(R\), maintain the water ledger

\[
\Delta V_R=I_R-O_R+S_R,
\]

where all entries are integrated m³ over the same interval. Internal transfers cancel; \(I_R,O_R\) cross the regional boundary; \(S_R\) is net external input not already counted there. Maintain an analogous kg ledger for each required solid class.

**Original example:** chunk A sends 5 m³ to B and receives 2 m³ back over one interval. Its net boundary change is −3 m³; B's is +3 m³. Saving or reactivating B must not add the 5 m³ again because an acknowledgement was delayed.

Prefer synchronized exchange at shared boundaries when practical. If transfers are journaled asynchronously, give each a unique interval/face identity and explicit ownership state. Either both stores commit together or a transfer-in-transit store accounts for the quantity between debit and credit. Do not count it in sender, transit and recipient simultaneously. Retries use the recorded outcome.

## Reduce inactive regions explicitly

An invisible area still participates in rivers, groundwater and weather under the selected model. Choose a documented inactive-region policy:

- Continue the full simulation for small worlds.
- Aggregate connected water bodies into reservoir models and keep boundary exchange.
- Use a cheaper routing/soil model where flood timing and local inundation are irrelevant.
- Pause the entire connected simulation domain under an explicit gameplay rule.

Freezing a single upstream chunk while downstream water continues is a different hydrological model. Treat it as an intentional approximation if used, and measure its consequences.

Save the reduced model's state, time, forcing cursor, boundary conditions and exchange history needed for continuation. Do not replay all rainfall since the last visual visit if that rainfall was already applied to a coarse reservoir.

## Reactivate conservatively

Advance the inactive model to the agreed activation time. Map its storage into valid detailed compartments while preserving total water and solid quantities. Use the actual fine storage curves and connectivity; uniform depths can place water on ridges or merge separate basins.

Aggregation loses information. A regional total does not uniquely determine local velocities, moisture profiles, sediment sorting or where separate pools formed. Preserve residual detail when continuity of those fields matters, or declare a reconstruction policy and its limitations. Do not claim exact reconstruction from an insufficient summary.

Rebuild operators and dependent caches, synchronize boundaries, then publish usable detail. If the coarse-to-fine transition would change the model abruptly, use a tested overlap/coupling procedure. A visual fade can hide a rendering transition but cannot correct a mass mismatch.

Changing render LOD should not trigger physical remeshing. When computational remeshing is enabled, use conservative geometry-overlap transfer or another justified remap, including layer identities, pore water, sediment and structure attachments. Quantity conservation alone does not guarantee spatially correct redistribution.

## Versioning and reproducibility

Separate schema version, generator version, physical model version and parameter-set version. Preserve an old save before migration. Validate units, totals, identities and required fields after conversion; explicitly document unavoidable changes in interpretation. Reconstruct missing optional data with declared defaults, not invented historical certainty.

Distinguish continuation from replay and bitwise determinism. Stable ordering, saved random-generator state and fixed input events improve repeatability. Different hardware, parallel reductions, compiler settings or solver versions may change floating-point results. Promise exact reproducibility only for a specified, tested configuration.

## Validation scenarios

Test save/reload at an operation boundary, during a storm, after compaction and with a pending cross-chunk transfer. Compare uninterrupted and resumed quantities and relevant outputs. Test duplicate receipts, failed snapshot publication, stale caches and migration of a representative old save.

Compare different chunk partitions and active/inactive transitions against an agreed reference tolerance. Inspect water and solid ledgers before judging visual continuity. This reference provides original architecture guidance; no specific database, networking framework or engine persistence API is required.
