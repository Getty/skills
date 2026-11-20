# Following routes and avoiding local collisions

Treat route planning, path following, local avoidance and locomotion as separate responsibilities. Add only the layers needed by the game; grid-based turn movement can execute a route without a continuous crowd solver.

## Contents

- [Define the execution contract](#define-the-execution-contract)
- [Follow a path without frame-dependent errors](#follow-a-path-without-frame-dependent-errors)
- [Respect stopping and turning constraints](#respect-stopping-and-turning-constraints)
- [Predict pairwise collisions](#predict-pairwise-collisions)
- [Use reciprocal avoidance under stated assumptions](#use-reciprocal-avoidance-under-stated-assumptions)
- [Handle congestion and failed progress](#handle-congestion-and-failed-progress)
- [Verify movement separately from route quality](#verify-movement-separately-from-route-quality)

## Define the execution contract

| Layer | Input | Output |
|---|---|---|
| Route planner | Start, goal, movement profile, graph revision | Route/corridor, cost and result status |
| Path follower | Route, actual position and progress | Preferred local direction or velocity |
| Local avoidance | Preferred velocity, nearby bodies/obstacles | Feasible or best-effort adjusted velocity |
| Locomotion/physics | Control and body constraints | Actual resulting position and velocity |
| Recovery policy | Progress and failure evidence | Wait, yield, replan or fail |

Feed actual movement back into navigation. Do not assume an agent moved by its commanded velocity when collision, animation, acceleration or platform motion changed the result.

Represent doors, jumps, ladders, elevators and boarding as typed transitions with execution state. Reaching a link endpoint does not mean the action has completed. A higher-level task system supplies destinations and priorities; navigation need not know hunger, inventory value or building purpose.

## Follow a path without frame-dependent errors

For segment \(a\rightarrow b\) and position \(x\), a simple projection is

\[
u=\operatorname{clamp}\!\left(
\frac{(x-a)\cdot(b-a)}{\|b-a\|^2},0,1\right),\qquad
p=a+u(b-a).
\]

Skip zero-length segments before dividing. Positions use metres; \(u\) is dimensionless. Use projection and corridor membership to track progress, then choose a look-ahead point along the route. A large look-ahead distance can cut a corner outside the valid corridor; validate the intended movement segment.

Do not require the character to hit an exact waypoint coordinate. Advance when the waypoint/segment has been acceptably passed under the route's topology and action constraints. A simple point-radius check can miss a waypoint when a fast agent crosses the entire acceptance region between updates.

For an uncomplicated final approach, a preferred velocity can be

\[
\mathbf v_{\mathrm{pref}}=
v_{\mathrm{desired}}\frac{p_{\mathrm{target}}-x}{\|p_{\mathrm{target}}-x\|},
\]

with an explicit zero-distance case and a speed reduced near arrival. The chosen target must remain within the permitted corridor. Arrival should satisfy an application-defined position tolerance and, where needed, a low-speed or orientation condition.

Keep thresholds in world units and relate them to speed, body size and update interval. Do not retarget every frame unless the target changed enough to matter; route jitter can otherwise be created by the application itself.

## Respect stopping and turning constraints

For speed \(v\) and constant available deceleration \(a_b>0\), the idealized stopping distance is

\[
d_{\mathrm{stop}}=\frac{v^2}{2a_b}.
\]

Add \(v\,t_{\mathrm{delay}}\) when the response includes a delay under a constant-speed approximation. Both terms are metres. This is a one-dimensional bound under the stated assumptions, not a vehicle dynamics model.

**Original example:** at \(v=4\ \mathrm{m/s}\), \(a_b=2\ \mathrm{m/s^2}\), stopping takes 4 m; a 0.2 s response delay adds 0.8 m. A controller cannot safely rely on a 0.2 m waypoint threshold to stop that body.

For a discrete acceleration-limited controller,

\[
\|\mathbf v^{n+1}-\mathbf v^n\|\le a_{\max}\Delta t,\qquad
\|\mathbf v^{n+1}\|\le v_{\max}.
\]

Turning radius, angular speed, traction and mode transitions may add further constraints. An avoidance velocity chosen without these limits may be unreachable. Clamping it afterward can violate the collision-avoidance constraints that produced it. Solve compatible constraints together, use a suitable kinematic model, or explicitly treat the result as best effort.

For a kinematic character, move the swept body through the collision system rather than teleporting to the next waypoint. Animation/root motion should either follow the same controller or report its displacement back for correction.

## Predict pairwise collisions

For two discs with positions \(x_i,x_j\), velocities \(v_i,v_j\), and combined radius \(R=r_i+r_j\), let

\[
p=x_j-x_i,\qquad w=v_j-v_i.
\]

Under constant velocities, separation at time \(t\) is \(\|p+tw\|\). The time of closest approach over horizon \(\tau\) is

\[
t_*=\operatorname{clamp}\!\left(-\frac{p\cdot w}{w\cdot w},0,\tau\right)
\]

when \(w\cdot w>0\). Check whether \(\|p+t_*w\|<R\), with the selected contact/margin convention. For equal velocities, use current separation. This test predicts a conflict under constant velocities; it does not choose a collision-free response.

**Original example:** agents are 4 m apart and approach at a relative 2 m/s, with \(R=0.8\ \mathrm m\). Their boundaries meet after \((4-0.8)/2=1.6\ \mathrm s\). A 3 s prediction horizon detects the threat before their center paths cross.

Use a spatial index for candidate neighbors, then accurate narrow-phase tests. A small neighbor radius or neighbor-count cap can omit relevant bodies. Fast movers and long horizons require a corresponding search envelope; visibility-based culling is not a physical guarantee.

## Use reciprocal avoidance under stated assumptions

ORCA constructs pairwise velocity constraints, sharing a corrective relative-velocity change between cooperating agents. A typical pair contributes a half-plane for agent \(i\):

\[
\left(\mathbf v-\left[\mathbf v_i+\tfrac12\mathbf u\right]\right)
\cdot\mathbf n\ge0.
\]

Here \(\mathbf u\) is the required relative-velocity correction and \(\mathbf n\) the normal of the selected safe half-plane. Their construction depends on the velocity obstacle, horizon and overlap case. This equation alone is not a complete ORCA implementation.

The agent selects a velocity near its preference within the intersection of those half-planes and a speed bound:

\[
\arg\min_{\mathbf v\in\mathcal F}\|\mathbf v-\mathbf v_{\mathrm{pref}}\|^2.
\]

Use the original [ORCA project/papers](https://gamma-web.iacs.umd.edu/ORCA/) and [RVO2 implementation documentation](https://gamma-web.iacs.umd.edu/RVO2/documentation/2.0/index.html) when adopting this method. Its local collision conditions rely on model assumptions such as represented shapes, consistent observed states, relevant neighbors and execution of the selected motions. They do not establish that every agent eventually reaches its destination.

Treat initial overlaps, infeasible constraint sets, uncooperative bodies and discrete/accelerated motion explicitly. If the feasible set is empty, a compromise velocity is not magically collision-free. A stationary wall also does not take half the responsibility like another cooperating agent.

The [RVO2 parameter reference](https://gamma-web.iacs.umd.edu/RVO2/documentation/2.0/params.html) distinguishes agent and obstacle horizons, maximum speed, neighbor distance and neighbor count. Increasing a horizon causes earlier reaction but also restricts choices; do not copy one parameter set as a universal crowd configuration.

Keep navmesh boundaries in the execution constraints. An agent-agent avoidance routine can otherwise steer a character off a platform or through a wall even when the original route was valid.

## Handle congestion and failed progress

Local steering does not decide who owns a single-lane bridge, whether a truck should reverse, or which job should receive priority. Use a small bottleneck controller or explicit reservation when that behavior matters.

Track remaining route progress over a time window, actual speed, contact state and available alternatives. Distinguish:

- Waiting for a legitimate resource or doorway.
- Temporarily obstructed by another moving body.
- Oscillating without progress.
- Following a stale or invalid corridor.
- Unable to reach the goal under its movement profile.

Choose a bounded recovery policy: pause, yield at a safe point, request a local detour, replan against current topology, or report failure. Replanning the same unchanged route every frame does not resolve symmetric congestion.

Avoid feeding volatile instantaneous crowd density directly into every global path cost without damping. Many agents may repeatedly select and abandon the same “cheapest” corridor. Use explicit averaging/hysteresis or scheduled capacity where appropriate, and label that policy as a game design choice.

## Verify movement separately from route quality

Test narrow passages, head-on encounters, overtaking, crossings, stationary obstacles, sudden stops, initial overlap and a queue at a blocked goal. Verify clearance and progress, not merely that a solver returned velocities.

Run at different physics update rates while preserving speed and acceleration units. Measure minimum separation, collision count, arrival time, stalls and recovery frequency. Test route invalidation during movement and an off-mesh action interrupted by a world change.

For a simple game, collision-aware waypoint following may be sufficient. Add reciprocal avoidance or coordinated schedules only when actual traffic behavior requires them. Keep the resulting movement controller independently testable from terrain generation and population decisions.
