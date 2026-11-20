# Engine and library adapters

Keep the navigation model portable. Choose an engine adapter after defining agent shape, traversability, costs, dynamic changes, query status and movement ownership. The examples below are optional; no listed library is required by this skill.

Verify the exact installed version and packaged target before using an API. Live documentation aliases can advance independently of a project's version.

## Common adapter contract

Expose:

- A bounded start/goal projection with the actual projected endpoints.
- An agent profile, permissions and cost/filter revision.
- Complete, partial, unreachable, pending, invalid-input and budget-limited outcomes as supported.
- A route/corridor tied to navigation data revisions.
- Typed off-mesh transitions with execution prerequisites.
- Invalidation and readiness events after geometry or topology changes.

Keep caller-owned destinations independent of transient engine polygon references. Save physical position, goal and relevant task/transition state; rebuild or validate engine-specific paths after loading. Do not serialize an opaque polygon handle and assume it remains valid after a rebake.

One system should own actual character movement. If animation, physics and navigation all write transforms independently, apparent pathfinding failures can be control conflicts.

## Recast and Detour

Recast builds navigation data from input geometry. Detour provides query/runtime support; DetourCrowd and DetourTileCache are additional components for different runtime needs. Select only the components needed by the project and inspect the version's limits. Primary repository: [Recast Navigation](https://github.com/recastnavigation/recastnavigation).

Use [Recast build configuration](https://recastnav.com/structrcConfig.html) with deliberate world-unit/voxel conversions and an agent clearance policy. A baked radius is part of the navigation model, not a rendering setting.

Detour's [query interface](https://github.com/recastnavigation/recastnavigation/blob/main/Detour/Include/DetourNavMeshQuery.h) separates polygon-path queries, corridor straightening and sliced search. Preserve status details, partial results and buffer limits in the adapter rather than reducing them to “path array nonempty.”

Use a corridor and local movement strategy compatible with the mesh. A crowd component is not automatically a globally coordinated reservation planner. Check whether a chosen tile-cache operation supports the intended change; transient obstacles and newly created walkable geometry are different cases.

## Unity

The AI Navigation package's `@2.0` documentation served version **2.0.16** during review. Its [NavMeshSurface reference](https://docs.unity3d.com/Packages/com.unity.ai.navigation@2.0/manual/NavMeshSurface.html) defines a surface for a selected agent type and configurable source geometry. Use the installed package's documented build/update methods and its matching agent configuration.

The [obstacle documentation](https://docs.unity3d.com/Packages/com.unity.ai.navigation@2.0/manual/AboutObstacles.html) distinguishes local obstruction from carving holes into navigation data. Moving-agent avoidance and carving have different update semantics. Carving a hole does not create a new floor, bridge or excavated walkable surface; update the appropriate source geometry/navigation surface for those changes.

Do not assume a geometry update, path query, collision update and agent movement all become ready within one frame. Test the actual update sequence and status handling. Keep agent movement ownership consistent with physics/root motion, and implement off-mesh action completion deliberately.

## Unreal Engine

Epic's [navigation modification guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-how-to-modify-the-navigation-mesh-in-unreal-engine) describes navigation built from collision geometry, tiled regeneration, cost modifiers and navigation links. Distinguish `Dynamic` generation from `Dynamic Modifiers Only`: modifiers can alter existing navigation, but do not supply newly generated walkable surfaces.

Use the actual runtime geometry/collision path available in the project's engine version and platform. A regenerated navmesh cannot compensate for missing or stale collision support.

Epic documents [RVO and Detour Crowd avoidance options](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-avoidance-with-the-navigation-system-in-unreal-engine). Its RVO avoidance does not itself use the navmesh. Ensure movement remains constrained to valid surfaces and choose a coherent avoidance owner; enabling unrelated controllers together is not a coordination strategy.

## Godot

The [stable NavigationAgent guide](https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationagents.html) separates querying, following and avoidance. The agent node does not move its parent automatically. After setting `target_position`, the caller obtains `get_next_path_position()` during physics updates and applies movement itself, respecting completion state.

When avoidance is enabled, use the documented velocity submission and `velocity_computed` callback flow. Navigation-map synchronization is also a readiness boundary: querying before the map is synchronized can yield an empty result. Avoid treating every initial empty result as proof of disconnected terrain.

Test thresholds against speed and update rate. Repeatedly resetting targets or requesting fresh paths can create jitter even when the underlying search is correct.

## Integration acceptance cases

Verify a complete route, unreachable target, partial result, narrow passage for two profiles, door link, moving obstacle and new walkable geometry. Repeat near tile/region boundaries and while an asynchronous update is pending.

Measure search, data construction, collision and movement costs separately. Test in the packaged target, not only the editor. Report the actual library/engine version and which behavior was verified; do not promise performance or platform support from a generic algorithm description.
