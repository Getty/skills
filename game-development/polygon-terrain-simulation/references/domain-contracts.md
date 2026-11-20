# Contracts with construction, logistics and population

Use this reference when integrating terrain with other game systems or deciding skill boundaries. These are proposed architecture contracts, not external standards. Rename and simplify them to fit the game.

## Contents

- [Divide by responsibility](#divide-by-responsibility)
- [Keep contracts small](#keep-contracts-small)
- [Define canonical ownership](#define-canonical-ownership)
- [Walk through a building operation](#walk-through-a-building-operation)
- [Handle partial work and failures](#handle-partial-work-and-failures)
- [Keep skills independent](#keep-skills-independent)

## Divide by responsibility

| Domain / possible separate skill | Owns | Requests or observes from terrain |
|---|---|---|
| Terrain, materials and water | Geometry, in-ground material, physical water, hydraulic connectivity, erosion, earthworks state | Its own physical revision |
| Inventory, storage and logistics | Item/bulk quantity ownership, capacity, reservations, hauling, containers, deliveries | Excavation yields, accessible pile footprints, flood exposure |
| Buildings and construction | Blueprints, footprint, foundation design, build phases, occupancy, maintenance, demolition | Support, grading plans, drainage impact, committed usable surface |
| Population and needs | Hunger, thirst, shelter, households, schedules, labor allocation and behavior | Environmental queries, hazards, access, actual granted water |
| Vegetation or farming, if separate | Plant lifecycle and crop management | Soil-water exchange, substrate, terrain, radiation/climate inputs |

These can be modules in one program, one ECS, or one datastore. Separate responsibilities do not require separate services, networking or asynchronous message brokers. A small game can combine inventory and construction under one implementation while retaining explicit quantity ownership.

Keep the terrain skill useful without any citizens or buildings. A scripted test should be able to request excavation and water withdrawal directly.

## Keep contracts small

Specify fields, units, revisions, failure behavior and effects. Use stable IDs and geometric footprints rather than render vertex indices.

### Queries

| Operation | Essential result |
|---|---|
| QueryFootprint | Coverage, sampled elevations, slope/support facts, exposed material, revisions and sampling resolution |
| QueryWater | Available extractable volume, level, model scope and quality/contamination fields only if modeled |
| QueryHazard | Current water depth or a prediction with horizon, forcing scenario, resolution and uncertainty |
| PreviewEarthworks | Stored target, cut/fill by material, displacement of water, constraints, affected region, source revisions |
| QueryOperation | Planned, applied and remaining work/material; conflict or wait status |

Distinguish a *current observation* from a *forecast*. A dry site today is not a certified flood-safe site. A simple routing model may answer catchment exposure but cannot honestly supply a detailed flood depth forecast.

### Commands

| Operation | Result and rule |
|---|---|
| ReserveWorkArea | Reservation token, expiry or explicit lifetime, conflict reason |
| StartEarthworks | Operation ID, accepted plan revision, quantity ownership/reservations |
| AdvanceEarthworks | Actual applied increment and actual material/water transfers |
| CancelEarthworks | Release unapplied reservations; preserve already moved material and ground |
| RequestWithdrawal | Requested versus granted volume; exact store and time interval |
| PlaceHydraulicStructure | Connection/barrier revision and domain owner |

Use granted quantities in downstream effects. A request for \(5\ \mathrm{m^3}\) from a store with \(2\ \mathrm{m^3}\) does not satisfy five units of downstream consumption. Return two granted units or reject according to the API contract.

### Events

Keep events factual and revisioned: TerrainRevisionCommitted, MaterialTransferCommitted, WaterWithdrawalGranted, HydraulicConnectivityChanged, HazardStateChanged, and OperationBlocked are examples.

Do not put decisions such as “evacuate all residents” inside a physical event. The building/population systems decide how to respond. An event can carry current evidence and its resolution.

## Define canonical ownership

### Bulk material

Choose which domain owns each mass at each moment:

| Physical state | Example owner |
|---|---|
| Undisturbed layer or committed construction fill | Terrain |
| Excavated, reserved at source and not yet transferred | Terrain or a clearly modeled pending transfer |
| In a truck/container | Logistics |
| Loose stockpile | Logistics quantity with terrain-derived pile geometry, **or** terrain quantity with an inventory view |
| Suspended sediment in flowing water | Terrain/hydrology |

A stockpile must not contribute its entire dry mass once as terrain and once again as inventory. If logistics owns the mass, its geometric representation reads that mass and placement state. If terrain owns it, inventory holds a reference and reservation view, not a second physical amount.

Record a transfer with:

- Unique operation and transfer IDs.
- Source and destination ownership accounts.
- Material/class identifier and dry solid mass in kilograms.
- Water carried with the material, if modeled, in cubic metres.
- Placement porosity/density used to derive bulk volume.
- Applied world revisions and transaction state.

Avoid making bulk volume the immutable material quantity when compaction changes volume. Inventory can still impose a volume-capacity constraint; evaluate it from material state.

**Original example:** move \(12{,}000\ \mathrm{kg}\) of a synthetic material with dry bulk density \(1500\ \mathrm{kg/m^3}\). It occupies \(8\ \mathrm{m^3}\) in its initial state. Placed at \(1800\ \mathrm{kg/m^3}\), the same mass occupies \(6.6667\ \mathrm{m^3}\). Logistics has moved twelve tonnes, not created \(1.3333\ \mathrm{m^3}\) of extra matter. Account separately for any pore water expelled during compaction.

### Water

Identify physical ownership across surface, soil, aquifer, container and atmospheric/export accounts. Infiltration changes accounts; it is not a global loss. Water stored in a household tank must have been withdrawn from a physical source or introduced by a declared import.

Separate water quality from volume when the game needs quality. A concentration field must be backed by constituent mass if transfers must conserve contaminants or nutrients.

### Work

Let the construction/worker system provide an accepted work increment, elapsed productive time, or equipment capacity. Terrain maps it to feasible material movement and returns actual progress. Terrain should not need to know a worker's hunger score or household.

Do not equate worker progress with arbitrary percentages if excavation costs depend on exposed material. Define the workload unit, such as kilograms moved under a chosen game cost model.

## Walk through a building operation

1. Construction proposes a footprint, target surface, foundation constraints and access requirements.
2. Terrain previews cut/fill, exposed strata, water displacement and affected connections against identified revisions.
3. Construction accepts a plan; logistics reserves fill material and disposal capacity if required.
4. Terrain and logistics reserve the operation using one transaction or an explicitly recoverable protocol.
5. Work arrives in increments. Terrain computes the amount that can actually be excavated/placed, checking current constraints.
6. Transfer the corresponding material ownership exactly once and update physical geometry atomically with the committed work increment.
7. Publish the committed terrain revision. Refresh collision, access and hazard projections.
8. Construction advances its next phase only when its declared prerequisites are satisfied.

The same terrain operation works when initiated by a player brush, autonomous machinery or a scripted event. Demolishing the building does not implicitly undo the earthworks. Restoration is a new operation with its own material budget.

## Handle partial work and failures

For a single-process game, prefer an atomic state change with validation before commit. Do not introduce a distributed protocol unless architecture actually requires one.

For independent persistence domains, record a durable pending transfer with a unique ID and recoverable state. Replays must find the previous outcome and return it rather than apply the transfer twice. “Exactly once” is an application invariant achieved through idempotency, ownership and recovery; it is not guaranteed by an event name.

Check a command's recorded receipt before rejecting it for a now-stale world revision. A successfully committed command naturally changed that revision. Return its original result when the same ID and payload are retried; reject reuse of the ID with different content. For a new command, then validate current revisions and prerequisites. Persist terrain, inventory effects, operation progress and the receipt in the same logical transaction or recoverable protocol.

If a truck is unavailable, pause excavation or create a modeled pile with capacity and geometry. If groundwater enters the excavation, either change the plan, pump accounted water, or block the operation. Do not silently delete the water to keep a construction animation running.

Store source revisions. If erosion, another operation or a dam changes the assumptions, mark the plan stale and re-evaluate the unexecuted remainder. Never recompute already executed earthworks as if they had not happened.

## Keep skills independent

Each future skill should include only its side of these contracts plus a shared versioned data vocabulary. Do not make one skill automatically load all neighboring domains.

Use optional adapters:

- Terrain can accept abstract work without a population module.
- Buildings can use a terrain-query stub for an indoor or flat-map game.
- Logistics can manage goods without geometric terrain piles.
- Needs can consume granted resources without knowing the fluid solver.

When implementing a game, let its integration layer choose authority, transaction boundaries and update ordering. Maintain contract fixtures for material handoff, water withdrawal, stale previews and save/load. This is the seam where many otherwise correct domain models can disagree.
