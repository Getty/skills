# Contracts with terrain, buildings, logistics and behavior

Keep navigation independently useful in a flat test map, an indoor game, a polygon landscape or a headless simulation. These are proposed contracts to adapt, not a required engine API.

## Contents

- [Assign responsibility](#assign-responsibility)
- [Define query inputs and outcomes](#define-query-inputs-and-outcomes)
- [Keep route and movement contracts distinct](#keep-route-and-movement-contracts-distinct)
- [Integrate terrain changes](#integrate-terrain-changes)
- [Coordinate resource ownership](#coordinate-resource-ownership)
- [Handle failure honestly](#handle-failure-honestly)

## Assign responsibility

| Domain | Owns | Supplies/requests |
|---|---|---|
| Terrain/environment | Surface geometry, physical water/material state | Geometry and observations such as slope, water depth and surface condition |
| Buildings | Structural geometry, entrances, doors, action state and support requirements | Access points, blocked space, door/lift capabilities |
| Navigation | Agent-dependent traversability, route queries, path/corridor validity | Reachability, costs, usable routes and navigation readiness |
| Movement/physics | Actual position, velocity, collisions and executable motion | Route-following progress, contact, stuck/arrival status |
| Logistics/tasks | Cargo/resource reservations, job ownership and destinations | Accepted goal candidates, loads and work priorities |
| Population/behavior | Needs, intentions, schedules and decisions | Goal selection and relevant agent capabilities |

The terrain skill needs only its navigation adapter boundary. Do not add A*, navmesh construction or crowd planning to it merely because terrain changes affect routes.

Separate **physical facts** from **profile policy**. Terrain can report 0.4 m water depth; navigation decides whether a particular pedestrian, swimmer or boat can traverse it. A global walkable flag can be a cache for one declared profile, not a universal fact for all actors.

## Define query inputs and outcomes

A minimal request can contain:

~~~text
FindRoute(
  query_id,
  intent_id,
  start_state,
  accepted_goal_set,
  agent_profile,
  objective,
  snapshot_or_revision,
  optional_budget
)
~~~

Return:

~~~text
RouteResult(
  status,
  route_or_corridor,
  reached_goal,
  objective_cost,
  optional_travel_time,
  profile_version,
  geometry_revision,
  cost_revision,
  guarantee,
  dependency_or_revalidation_data
)
~~~

For a small synchronous game, these may be plain function arguments and a struct. Do not require distributed messages or globally unique service IDs.

Use typed outcomes for found, unreachable in the searched graph, budget exhausted, cancelled, stale, invalid input, unavailable streamed data and partial results. A partial corridor must identify the endpoint and why it ends there.

An estimate can be cheaper than a full path query, but label it:

- Geometric lower bound.
- Exact graph cost for the current model.
- Approximate/hierarchical cost.
- Measured or modeled travel-time estimate including specified waits.

Do not substitute a lower bound for a promise that a delivery will arrive at that time.

## Keep route and movement contracts distinct

A route edge describes an executable action. A follower should receive enough geometry and preconditions to perform it: corridor/waypoints, mode, target tolerance, speed constraints and any required door/jump/lift action.

Report movement outcomes such as:

- Progress along route.
- Arrived within the required goal region.
- Waiting for a named resource/action.
- Temporarily blocked.
- Route invalidated.
- Unable to execute an action.

Arrival at a building's bounding box is not necessarily arrival at its loading bay. Let the caller define valid interaction states. Navigation supplies a path to them; logistics decides whether unloading can occur.

Local avoidance may temporarily move an agent away from the ideal path. The follower must stay within its valid corridor or request repair. A velocity recommendation does not authorize walking through a wall.

## Integrate terrain changes

Use a transaction boundary at which the physical world changes:

1. Terrain/buildings commit their geometry or state revision.
2. Navigation receives affected geometry/IDs and the new facts.
3. Navigation updates applicable profile-specific representations.
4. Movement consumes a compatible collision/navigation revision.
5. Affected routes are revalidated or replaced.

If a road becomes muddy, its geometry may remain valid while travel cost changes. If a trench cuts the road, connectivity may change. If water rises, different profiles may become blocked at different depths.

Navigation should not calculate the water balance or excavate the trench. It consumes the resulting environmental state. Conversely, terrain should not choose where a hungry citizen goes.

Provide mock adapters for tests: a flat graph, one-way door, flood threshold, changing bridge and differently sized agents. The navigation module can be tested without a full terrain simulator.

## Coordinate resource ownership

Distinguish three claims that may all involve the same building:

| Claim | Owner and meaning |
|---|---|
| Resource reservation | Logistics: material or output is assigned to a job |
| Interaction slot | Building/task system: a loading bay or workstation is assigned |
| Space-time occupancy | Navigation/coordination: an actor may occupy/traverse a passage at a time |

They can be coordinated through the game integration layer. None implies the other automatically.

**Original example:** a warehouse has enough stone for two builders but one narrow loading doorway. Logistics can reserve both loads. Navigation may queue doorway traversal, while the building assigns its loading slot. Reserving stone does not give either builder permission to occupy the doorway indefinitely.

When a loaded wagon has different radius, speed or capabilities, supply a new relevant profile/cost version. Hunger may alter available work or speed through the behavior model; navigation receives the resulting movement parameters instead of importing the entire need simulation.

Do not reserve all tiles along every ordinary walking route unless the game needs that coordination model. Local avoidance or a small bottleneck queue may suffice.

## Handle failure honestly

Let higher-level logic respond to a failed route:

- Logistics may choose another eligible source or postpone delivery.
- Buildings may request a road, bridge or alternate entrance.
- Behavior may select another reachable goal.
- A construction operation may wait until workers can reach the site.

Navigation reports evidence and scope: which snapshot, profile, goal set and horizon were searched. It should not silently fulfill a job, create resources, teleport an actor or alter terrain to hide a failure.

For retryable async requests, associate results with current intent and query versions. A completed old query must not overwrite a newer destination. If a command reserves passage capacity, give it explicit ownership, release and recovery semantics.

Use `assets/query-contract-example.json` as an illustrative record shape. It is independent of the reference search-fixture schema; adapt it rather than treating it as a mandatory interchange standard.
