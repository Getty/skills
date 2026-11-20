# Authored terrain and climate

Use these optional recipes when a game needs controllable landscape generation, terrain painting, or inexpensive climate patterns. They do not require a climate simulator. The equations and examples below are original engineering recipes unless explicitly attributed; example values are synthetic and uncalibrated.

## Contents

- [Separate design intent from execution](#separate-design-intent-from-execution)
- [Choose visible controls and precise brush semantics](#choose-visible-controls-and-precise-brush-semantics)
- [Construct optional wind and climate fields](#construct-optional-wind-and-climate-fields)
- [Convert rainfall into area-aware runoff](#convert-rainfall-into-area-aware-runoff)
- [Keep biome labels descriptive](#keep-biome-labels-descriptive)
- [Preserve edits through asynchronous work and saves](#preserve-edits-through-asynchronous-work-and-saves)

## Separate design intent from execution

[Mapgen4](https://www.redblobgames.com/maps/mapgen4/) combines painted landscape features with generated rivers and biomes. Its [repository introduction](https://github.com/redblobgames/mapgen4) states goals of interactive regeneration and attractive results rather than realistic terrain. Use that interaction model as inspiration while retaining the world's declared material and water rules.

Give each edit an explicit role:

| Role | Result and ownership |
|---|---|
| Initial-world authoring | Establish a target landscape, then construct consistent initial layers, material quantities, water stores, and boundaries. |
| Operation preview | Produce proposed geometry, affected footprint, cut/fill quantities, and validity information against a specified world revision. |
| Runtime execution | Change authoritative state through the selected terrain-operation rules; preserve the resulting world rather than regenerating it afterward. |

A height brush can express the same target in all three roles. A construction order also needs execution progress and, when modeled, material availability. Store the proposal separately from its realized geometry. See [terrain operations](terrain-operations.md) for physical edits and [initialization](initialization-and-generation.md) for creating the starting state.

Combine broad authored forms with procedural variation through an explicit precedence policy. For example, allow low-amplitude detail on a hillside while masking it out on a completed foundation. Adding noise after flattening without such a rule can undo the desired result. Freeze gameplay-relevant generated geometry into authoritative state at initialization; retain disposable decoration separately.

## Choose visible controls and precise brush semantics

The author's [2018 painting revision](https://simblob.blogspot.com/2018/09/mapgen4-elevation-painting-revisited.html) abandoned interpolation between painted mountain/valley/ocean categories because users could not infer hidden constraints from the output. Direct height painting with a feathered brush behaved more clearly. This does **not** mean all distance fields disappeared: the inspected [map.ts](https://github.com/redblobgames/mapgen4/blob/main/map.ts) still uses an approximate randomized field around predefined peaks for mountain shapes.

If constraints remain useful, expose their locations and precedence in the editor. Distinguish Euclidean distance, graph distance, and intentionally distorted artistic fields. A fast approximation that gives appealing ridges is not automatically a metric or an exact shortest-distance computation.

### Original target-height brush

For distance \(r\) from the brush center, choose radii \(0\le r_{\mathrm{inner}}<r_{\mathrm{outer}}\), all in metres:

\[
u=\operatorname{clamp}\!\left(
\frac{r-r_{\mathrm{inner}}}{r_{\mathrm{outer}}-r_{\mathrm{inner}}},0,1\right),
\qquad w(r)=1-(3u^2-2u^3).
\]

The dimensionless weight is one in the inner disk and zero outside the outer disk. Blend toward a target elevation \(z_\star\,[\mathrm m]\):

\[
\alpha=1-\exp(-k w\Delta t),\qquad
z^{n+1}=z^n+\alpha(z_\star-z^n),
\]

with \(k\ge0\,[\mathrm{s^{-1}}]\), \(\Delta t\ge0\,[\mathrm s]\). Numerically, compute alpha as `-expm1(-k*w*dt)` when small arguments matter. This is the exact solution of a local relaxation equation with fixed weight and target, so splitting a stationary exposure into smaller time steps preserves its effect, apart from arithmetic error. It does not make arbitrarily sampled moving pointer paths equivalent.

**Synthetic example:** take radii 4 and 8 m, sample distance 6 m, rate \(k=2\ \mathrm{s^{-1}}\), duration 1 s, old height 20 m, and target 12 m. Then \(u=w=0.5\), \(\alpha=1-e^{-1}\approx0.6321205588\), and

\[
z^{n+1}=12+8e^{-1}\approx14.9430355294\ \mathrm m.
\]

Two stationary half-second steps give the same final height. Reaching the target exactly requires an explicit final snap or stamp rule; relaxation approaches it asymptotically. Raising/lowering can instead use \(\Delta z=v_b w\Delta t\), with signed speed \(v_b\,[\mathrm{m/s}]\).

Define whether overlapping strokes accumulate, overwrite, or use a saved pre-stroke surface. The inspected [painting.ts](https://github.com/redblobgames/mapgen4/blob/main/painting.ts) maintains pre-stroke elevations and time/strength fields; its particular blend is distinct from the recipe above. Specify path resampling, units, pressure behavior, and undo semantics independently of frame rate. Store before-images or a valid reversible operation; negating a height change does not generally undo clipping, relaxation, compaction, or water movement.

On irregular polygons, integrate the intended local height change over actual overlap. A centroid sample is an approximation, especially for a brush narrower than a cell. Separate positive and negative changes before computing cut/fill: their net volume can hide simultaneous excavation and filling within one polygon. Feed physical execution into the existing material and water rules.

## Construct optional wind and climate fields

The author's [rainfall article](https://simblob.blogspot.com/2018/09/mapgen4-rainfall.html) describes a cheap prevailing-wind pass with evaporation and mountain-related precipitation. It can generate wet and dry regions independently of proximity to rivers. This is useful for a river crossing a desert. The article's moisture averaging and simplified precipitation treatment are not a conservative atmospheric-water solver.

For an original engine-neutral version, choose a constant unit wind direction and project region positions onto it:

\[
\mathbf d=(\cos\theta,\sin\theta),\qquad s_i=\mathbf x_i\cdot\mathbf d.
\]

Sort by \((s_i,\mathrm{stableId}_i)\). Define upstream neighbors by strictly smaller \(s\); equal-projection neighbors contribute nothing in this simple pass. This creates an acyclic dependency order. Curving winds, recirculation, and periodic windward boundaries require another model or an iterative boundary treatment.

One illustrative dimensionless proxy rule is:

\[
H_i^*=\frac{\sum_{j\in U_i}w_{ji}H_j}{\sum_{j\in U_i}w_{ji}}+E_i,
\quad O_i=\max(0,H_i^*-C_i),
\quad H_i=H_i^*-O_i,
\quad R_i=R_{0,i}+\beta_i O_i.
\]

Use nonnegative weights, evaporation score \(E_i\), capacity proxy \(C_i\), baseline rain score \(R_{0,i}\), and factor \(\beta_i\). Require a positive weight sum for the average. For an empty upstream set or zero total weight, substitute a declared nonnegative boundary humidity before adding \(E_i\). A capacity proxy that decreases with authored elevation can create a rain shadow. Choose its mapping explicitly; it is not a universal atmospheric law. Different directional passes may be averaged as seasonal design inputs, without implying a time-integrated climate model.

These \(H,R,E,C\) values are scores, not cubic metres, relative humidity, or precipitation rates. Neighbor averaging can duplicate or dilute an extensive quantity. Preserve that limitation in field names and interfaces. A real water budget needs explicit source/sink quantities and conservative transfers; do not repair this proxy by merely attaching SI units to it.

## Convert rainfall into area-aware runoff

If climate drives gameplay water, explicitly map its score to a nonnegative precipitation rate \(P_i\,[\mathrm{m/s}]\), using a calibrated relationship or declared game tuning. For cell area \(A_i\,[\mathrm{m^2}]\), rainfall contributes

\[
\Delta V_{\mathrm{rain},i}=P_i A_i\Delta t.
\]

For a static routing diagnostic or a steady-flow initialization, let \(c_i\in[0,1]\) be an illustrative runoff coefficient. Then

\[
q_i^{\mathrm{local}}=c_i P_i A_i,
\qquad Q_i=q_i^{\mathrm{local}}+\sum_{j:\,j\to i}Q_j.
\]

Both rates have units \(\mathrm{m^3/s}\). Evaluate the directed acyclic drainage graph from tributaries to outlets. With multiple receivers, allocate nonnegative fractions whose sum is one unless an explicit sink takes the remainder. Handle cycles, lakes, closed basins, and boundary outlets deliberately. On unequal polygons, summing rain scores or counting contributing cells misrepresents catchment supply.

**Synthetic example:** two tributary cells of 200 and 300 m² receive 10 mm/h, with \(c_i=1\). Their local rates are 2 and 3 m³/h; the confluence receives 5 m³/h. Over 1,800 s the rainfall volumes are 1 and 1.5 m³. Their sum, 2.5 m³, is available to leave only under the stated no-storage, instantaneous-routing assumption.

For \(c_i<1\), declare where the remaining rainfall goes. Never add full rainfall to surface storage and independently inject its runoff fraction again as new water. Transient flood behavior requires storage, travel time, hydraulic connections, and transfer limits; the recurrence above supplies none of these. The inspected `map.ts` uses artistic moisture-based flow and may adjust downstream elevations during generation; use its river patterns as design evidence, not as a physical excavation or sediment rule.

## Keep biome labels descriptive

For a tunable temperature initialization, one original design rule is \(T_i=T_{\rm ref}(\varphi_i)-\Gamma(z_i-z_{\rm ref})+\delta T_i\). Declare the latitude coordinate \(\varphi_i\), temperature in kelvin, altitude in metres, a chosen \(\Gamma\,[\mathrm{K/m}]\), and an optional temperature-variation field \(\delta T_i\,[\mathrm K]\). This is a generation control valid over a chosen altitude range, not a universal atmospheric lapse law. A synthetic \(\Gamma=0.004\ \mathrm{K/m}\) lowers the reference temperature by 2 K over a 500 m rise. Games may instead use dimensionless hot/cold scores; label them accordingly.

An optional lookup \(b_i=\mathcal B(T_i,R_i,z_i,\ldots)\) can assign vegetation or art categories. Specify whether its inputs mean long-term climate, instantaneous weather, or soil moisture. A biome label does not determine geological layers or override measured water storage. If labels change during gameplay, use a declared averaging window or hysteresis to avoid flickering classifications near thresholds. Keep ecological succession optional.

## Preserve edits through asynchronous work and saves

Mapgen4's inspected [worker.ts](https://github.com/redblobgames/mapgen4/blob/main/worker.ts) regenerates terrain-related fields and returns geometry buffers. For a persistent game, attach input revisions and request identity to every asynchronous preview or derived result. Publish only a result compatible with the current authoritative state and current intent. Coalesce obsolete previews without silently dropping committed terrain operations.

Save authored intent when it must remain editable, and save realized terrain/water state after execution. Record generator version, parameters, stable identities, and independently seeded feature streams. Recomputing a climate or rendering projection must not erase player earthworks or restart initial generation. A changed ridge can alter climate or drainage beyond the brush footprint; invalidate dependencies according to the selected model. See [runtime coupling](runtime-and-coupling.md) and [persistence](persistence-and-streaming.md).

Repository links above refer to a live branch. Pin a revision when reproducing implementation-specific behavior; historical articles document design experiments rather than a promise about every later version.

The [generation examples](../assets/generation-examples.json) include the brush, temperature and rain/runoff arithmetic. Use them as inspectable examples, not calibrated settings.
