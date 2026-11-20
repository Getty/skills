# Navigation meshes, portals and agent clearance

Use a navigation mesh when continuous walkable surfaces and varied obstacle geometry justify it. A small grid or explicit waypoint graph remains a valid simpler choice.

## Contents

- [Separate terrain from navigability](#separate-terrain-from-navigability)
- [Specify the agent profile](#specify-the-agent-profile)
- [Account for finite size](#account-for-finite-size)
- [Construct and inspect the navigation surface](#construct-and-inspect-the-navigation-surface)
- [Search a corridor and refine it](#search-a-corridor-and-refine-it)
- [Preserve costs during refinement](#preserve-costs-during-refinement)
- [Handle changing geometry](#handle-changing-geometry)
- [Validate the representation](#validate-the-representation)

## Separate terrain from navigability

Keep physical terrain, rendered triangles, collision and navigation as distinct representations. Terrain describes ground and water. Navigation describes where a particular movement profile can go and what traversals cost.

A hydrology polygon is not automatically a navigation polygon. A river may connect water cells while separating pedestrians; a bridge may connect pedestrians above the water; a pipe may conduct water without admitting either a person or a cart. Store stacked surfaces separately so projection onto the closest point does not teleport an agent from a bridge to the riverbank beneath it.

Use stable world features and versioned navigation references. Mesh polygon IDs can change during a rebuild and should not be permanent building or citizen identities.

## Specify the agent profile

Include only constraints used by the game:

| Property | Meaning |
|---|---|
| Radius or footprint | Horizontal swept body, including selected margin |
| Height/headroom | Vertical clearance required above the support surface |
| Step/climb limit | Allowed discontinuity at a transition |
| Maximum slope | Allowed sustained surface inclination |
| Movement modes | Walking, swimming, flying, climbing, crawling, driving |
| Access capability | Door permission, jump ability, ladder use, equipment |
| Cost model | Time, distance, energy or declared game objective |

Different profiles can use separately built meshes, a clearance-annotated representation, or filters plus suitable geometric tests. A filter cannot make an oversized body fit through a narrow passage that the underlying representation treats as a point transition.

Changing posture, vehicle orientation or movement mode may require additional state in the planning graph. A nonholonomic vehicle cannot follow every point-agent polyline even if its center remains inside walkable space.

## Account for finite size

### Configuration-space view

For a fixed-orientation translating footprint \(B\) and obstacle set \(O\), forbidden reference-point positions are

\[
C_{\mathrm{obs}}=O\oplus(-B).
\]

The symbol \(\oplus\) denotes a Minkowski sum. For a circular footprint of radius \(r\), this means expanding obstacles by \(r\), or equivalently shrinking free space. Rotation of a nonsymmetric body adds configuration dimensions; one fixed inflated map is not a general rotating-vehicle solution.

Source basis: [LaValle, configuration-space obstacles](https://www.lavalle.pl/planning/node156.html).

For a straight passage between parallel walls with physical width \(W\), disc radius \(r\), and additional margin \(m\),

\[
W_{\mathrm{center}}=W-2(r+m).
\]

All lengths use the same units. A positive value supplies a feasible interval of center positions in this simplified geometry; corners, turns and irregular bodies still require swept-shape tests.

**Original example:** \(W=1.2\ \mathrm m\), \(r=0.4\ \mathrm m\), \(m=0.05\ \mathrm m\) leave \(0.3\ \mathrm m\) of center-position width. A cart approximated by \(r=0.7\ \mathrm m\) cannot use the passage under the same margin.

Apply clearance exactly once. If a mesh has already been eroded for the selected radius, blindly shrinking every portal by that full radius again can reject valid routes. Conversely, using an unshrunk mesh with point-only collision tests admits invalid routes.

### Quantized construction

Recast's configuration distinguishes horizontal cell size, vertical cell height, walkable radius, headroom, climb and slope. Its radius/headroom parameters include voxel-based values; convert deliberately rather than inserting world metres into an integer voxel field. See [Recast rcConfig](https://recastnav.com/structrcConfig.html).

For radius \(r\) and horizontal voxel width \(c_s\), a conservative radius conversion is \(r_{\mathrm{vox}}=\lceil r/c_s\rceil\). With \(r=0.35\ \mathrm m\) and \(c_s=0.1\ \mathrm m\), this produces four voxels, corresponding to \(0.4\ \mathrm m\). That quantization can close a narrow passage. Smaller voxels may restore detail at a higher construction/storage cost. Headroom uses vertical resolution instead.

Do not infer the exact physical clearance from one nominal setting alone. Rasterization, contour simplification, cell boundaries and geometry tolerances also affect the result.

## Construct and inspect the navigation surface

Build from the geometry that determines actual movement support and obstruction. Select collision geometry or an explicitly reconciled navigation proxy; visual decoration alone is not authoritative.

Check:

1. Connected regions, portals and off-mesh links agree with intended physical access.
2. Polygon winding, portal endpoints and coordinate axes are consistent.
3. Headroom, ledges, stairs and slopes are tested with the actual agent profile.
4. Multi-level geometry does not create accidental cross-floor adjacency.
5. Start/goal projection stays within a bounded, appropriate search region.
6. Areas and links carry required permissions and cost semantics.

Projection is a query result, not permission to teleport. Return the requested point, projected point, distance and region when they differ materially. If a goal is inside a wall, the caller should choose a nearby valid interaction position or accept an explicitly partial result.

## Search a corridor and refine it

A common pipeline searches adjacency to obtain a polygon corridor, extracts the shared portals in order, then computes a path through those portals. Detour separates its polygon path query from straight-path extraction; [its query documentation](https://recastnav.com/classdtNavMeshQuery.html) also describes partial and buffer-limited results.

Inspect result status, reached endpoint and capacity limits. A nonempty path may stop short of the requested goal. A truncated polygon list must not be reported as a complete route.

For a valid planar simple corridor with consistently ordered portals and a point agent in already clearance-adjusted space, a funnel/string-pulling method gives the shortest Euclidean route constrained to that corridor. It does not prove that the corridor selected by a polygon graph search is globally best among every possible corridor.

An orientation predicate used in a planar implementation is

\[
\operatorname{orient}(a,b,c)
=(b_x-a_x)(c_y-a_y)-(b_y-a_y)(c_x-a_x).
\]

Its units are squared length. The sign convention depends on the coordinate system and portal ordering. Treat coincident points, collinear portals and floating-point tolerances explicitly. A generic planar funnel is not automatically an exact shortest geodesic over an arbitrary folded 3D surface.

Use [Mikko Mononen's funnel implementation discussion](https://digestingduck.blogspot.com/2010/03/simple-stupid-funnel-algorithm.html) as a primary implementation reference. Keep corridor quality, portal extraction, clearance and endpoint projection in the test harness; a correct funnel cannot repair an invalid corridor.

The [Detour path corridor API](https://recastnav.com/classdtPathCorridor.html) is a useful example of maintaining and locally adjusting a corridor as an agent moves. It is an implementation option, not a requirement.

## Preserve costs during refinement

A shortest geometric polyline need not minimize the chosen gameplay objective. For spatial cost density \(\kappa(x)\) and discrete transition charges,

\[
C(\gamma)=\int_\gamma \kappa(x)\,ds+\sum_{\ell\in\gamma}p_\ell.
\]

If \(\kappa\) is seconds/metre, this is travel time in seconds. Add door, ladder or mode-change charges only when their transitions occur. A line-of-sight shortcut must be collision-free **and** re-evaluated under this objective.

**Original example:** a 6 m shortcut through mud at \(3\ \mathrm{s/m}\) costs 18 s. A 10 m route on a road at \(1\ \mathrm{s/m}\) costs 10 s. Geometric shortening worsens the objective. Ordinary Euclidean funneling does not solve arbitrary weighted-region optimization.

Likewise, smoothing a corner into a spline can cross outside the clearance-adjusted corridor or remove a required door/jump action. Validate the swept body and preserve action markers. For a vehicle, verify curvature and acceleration constraints or choose a planner that represents them.

## Handle changing geometry

Distinguish:

- **Cost/filter change:** mud, permissions, danger or allowed movement modes.
- **Connectivity change:** a closed door, destroyed bridge or enabled jump link.
- **Geometry change:** excavation, new floor, collapsed wall or altered clearance.
- **Transient occupancy:** another moving agent.

Choose the cheapest correct update mechanism. A temporary agent usually belongs in local avoidance or reservations, while a new traversable floor requires appropriate navigation geometry. A cost modifier alone cannot invent missing support geometry.

Version inputs and results. A query should identify its graph/navmesh revision and agent profile. Reject or revalidate stale routes before execution; check the upcoming corridor segment while moving. Store an immutable query snapshot or synchronize mutation with a library's actual thread-safety guarantees.

Rebuild affected tiles plus necessary margins. Keep collision and navigation readiness coordinated. A region can remain unavailable until both describe the committed terrain revision. Do not assume old polygon references remain valid after replacement.

## Validate the representation

Use narrow corridors for several radii, stairs near the climb threshold, low ceilings, a bridge over another walkable surface, a door link and a newly created floor. Test a blocked target, disconnected islands, path-buffer truncation and a route invalidated during execution.

Compare graph-reported cost with the cost of the actual refined path under the same model. Draw obstacles, inflated boundaries, corridor polygons, portals, clearance and final swept path separately. Those diagnostics reveal whether a failure belongs to world geometry, graph search, corridor selection, refinement or movement.
