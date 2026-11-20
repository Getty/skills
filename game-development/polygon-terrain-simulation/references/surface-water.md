# Surface water on polygon cells

## Contents

- [Choose a model](#choose-a-model)
- [State and conservation](#state-and-conservation)
- [Conservative transfer algorithm](#conservative-transfer-algorithm)
- [Optional flow laws](#optional-flow-laws)
- [Timesteps and wetting](#timesteps-and-wetting)
- [Routing as a separate capability](#routing-as-a-separate-capability)
- [Checks and diagnostics](#checks-and-diagnostics)
- [Primary references](#primary-references)

## Choose a model

Select a model for the observable behavior, then document its limits. The following choices are alternatives, not implementation stages that every game must complete.

| Need | Suitable starting point | Additional state | Important omission |
|---|---|---|---|
| Drainage map or annual river size | Area/runoff accumulation | Routing graph | Transient storage and backwater |
| Ponds, dams, changing shorelines | Conservative cell/reservoir network | Water volume and connection geometry | Momentum unless explicitly modeled |
| Gradual overland flow | Diffusive-wave approximation | Geometry, roughness, water stage | Acceleration and momentum-driven circulation |
| Fast flood waves | Local-inertial or shallow-water solver | Discharge or momentum | Depends on the chosen approximation |

A graph storage model is a useful game abstraction. Label its adjustable conductances as such. A plausible animation does not establish hydraulic accuracy.

## State and conservation

Store surface water volume `surface_water_m3`. Derive stage from terrain storage geometry. For a flat cell, \(h_i=V_i/A_i\) and \(\eta_i=z_i+h_i\). For subcell terrain, use the storage curve in `lakes-and-structures.md`. Do not assign independent values to volume, depth and stage.

Declare orientation once: face \(f\) has owner \(i\), neighbor \(j\), and positive discharge \(Q_f\) from owner to neighbor. Define \(s_{if}=+1\) for an outward face and \(-1\) for an inward face.

### Formula card: volume continuity

**Purpose:** update a cell while preserving a global ledger.

\[
V_i^{n+1}=V_i^n+\Delta t\left(S_i-\sum_{f\in\partial i}s_{if}Q_f\right).
\]

Use \(V\) [m³], time [s], and both \(S\) and \(Q\) [m³/s]. Internal face contributions cancel because both cells use the same transfer. Rainfall, evaporation, infiltration, groundwater return, withdrawals and external boundaries form explicit source/sink entries.

For rain rate \(r\) [m/s], contributing area \(A_r\) [m²] gives \(R=rA_r\). Evaporation from open water instead uses its current wetted area. A roof may redirect rain to another location: apply the rain once, then transfer it. Infiltration is a surface-store loss but a soil-store gain, so it cancels in the combined water budget.

**Original example:** a 400 m² closed catchment receives 5 mm of rain: input is 2 m³. If 0.6 m³ infiltrates and 0.1 m³ evaporates, surface storage rises by 1.3 m³ and soil storage by 0.6 m³. The combined increase is 1.9 m³. Rain or evaporation rates integrated across a changing timestep must produce these volumes.

**Assumptions:** constant-density water; omitted stores are represented by declared boundary transfers. For saline/thermal models distinguish mass conservation from constant-density volume conservation.

**Reference:** HEC-RAS shallow-water documentation provides continuity and the distinction between bed, depth and free-surface elevation. The discrete ledger and example above are a proposed implementation contract.

## Conservative transfer algorithm

Use this explicit reference pattern for a simple network; sophisticated solvers may enforce positivity differently.

1. Apply known external inputs to provisional stores. Record their actual volumes.
2. Evaluate each face's candidate signed transfer \(T_f=Q_f\Delta t\) using a consistent snapshot.
3. Add other competing withdrawals, such as evaporation and pumping, to the donor's requested outflow. Define priorities if proportional sharing is inappropriate.
4. For each donor, sum requested positive outflows \(O_i\). Set \(\alpha_i=\min(1,V_i^*/O_i)\) for \(O_i>0\), otherwise 1.
5. Scale each requested transfer by its donor's factor. Apply the same realized amount negatively to the donor and positively to its destination.
6. Commit stores together. Record unmet demand separately from realized withdrawal.

Here \(V_i^*\) is available volume after the chosen source ordering. Do not spend speculative incoming transfers unless the scheme explicitly solves that dependency. This simple choice adds a timestep-dependent travel delay, which should diminish under refinement.

**Original example:** a donor contains 3 m³ and requests outward transfers of 4 m³ and 2 m³. The donor factor is 0.5, so destinations receive 2 m³ and 1 m³. Independently clamping the donor after sending 6 m³ would manufacture 3 m³. Scaling each edge against the full donor volume independently also fails when there are multiple exits.

Limit transported suspended sediment using the realized water transfers and available sediment mass. A donor concentration times requested, later-reduced flow produces inconsistent transport. A dry cell with deposited sediment needs a deposition/rewetting policy, not division by zero.

The limiter preserves nonnegative stores and transfer accounting; it does not make an arbitrarily large timestep hydraulically accurate or eliminate oscillation.

## Optional flow laws

### Formula card: deliberately simple reservoir connection

For a tunable, momentum-free game model, define

\[
Q_{ij}=G_{ij}\left([\eta_i-z_c]_+-[\eta_j-z_c]_+\right),
\qquad [x]_+=\max(x,0).
\]

\(G\) has units m²/s and \(z_c\) is a connection sill [m]. This is an original network closure, not a weir law or a full shallow-water discretization. It is useful for configurable fill/drain behavior. It gives zero flow when both sides are below the sill or stages are equal, but omits momentum and detailed approach losses.

**Example:** \(G=0.2\) m²/s, sill 10 m, stages 10.4 m and 9.9 m give \(Q=0.08\) m³/s. At a 5 s step the request is 0.4 m³, subject to available water. Explicitly handle the sea or other infinite reservoir as an external boundary, not an untracked ordinary cell.

### Formula card: Manning closure

For approximately uniform channel flow,

\[
Q=\frac{1}{n}A_cR_h^{2/3}\sqrt{S_f}.
\]

Use cross-sectional area \(A_c\) [m²], hydraulic radius \(R_h=A_c/P_w\) [m], wetted perimeter \(P_w\) [m], dimensionless friction slope \(S_f\), and SI roughness \(n\) [s/m^(1/3)]. The result is m³/s. The sign follows the modeled driving head gradient.

**Example:** \(A_c=2\) m², \(R_h=0.5\) m, \(S_f=0.001\), \(n=0.04\) s/m^(1/3) give about 0.996 m³/s. These are synthetic inputs, not a recommended material table.

A diffusive-wave closure substitutes water-surface slope under a gravity/friction balance. A center-to-center difference estimates a link gradient; it is a face-normal gradient only on compatible geometry or with an appropriate correction. Do not use a decorative polygon outline as hydraulic geometry.

Do not evaluate a formulation containing \(\nabla\eta/\sqrt{|\nabla\eta|}\) as an unguarded 0/0. Return zero flux at exactly equal stage and use the chosen solver's treatment near zero slope. A floor introduced to control stiffness is a numerical approximation whose sensitivity must be checked.

### Formula card: full shallow-water target

For a static bed, constant density, hydrostatic pressure and depth-averaged horizontal motion, a compact conservative form is

\[
\partial_t h+\nabla\cdot(h\mathbf u)=s,
\]
\[
\partial_t(h\mathbf u)+\nabla\cdot\left(h\mathbf u\otimes\mathbf u+
\tfrac12 gh^2\mathbf I\right)=-gh\nabla z+\mathbf f.
\]

Here \(h\) [m], \(\mathbf u\) [m/s], \(s\) [m/s], and \(\mathbf f\) [m²/s²] collects depth-integrated friction and other specified terms. Specify momentum carried by added/removed water. This equation is a model target, not enough information to implement a robust solver: select reconstruction, flux, bed-source balancing, wet/dry treatment and boundary conditions together. Terrain movement requires explicit coupling beyond the static-bed form.

## Timesteps and wetting

For an explicit shallow-water method, a characteristic face speed is

\[
c_f=|\mathbf u_f\cdot\mathbf n_f|+\sqrt{gh_f}.
\]

A mesh-aware estimate has the form

\[
\Delta t\le C\min_i\frac{A_i}{\sum_{f\in\partial i}L_fc_f}.
\]

The ratio has units of seconds: the numerator is m² and the denominator is m²/s. The admissible \(C\), wave-speed estimate and geometric factors depend on the numerical method; use its derivation and tests. This is not a universal guarantee. For a synthetic 100 m² cell with total contributing face length 40 m and \(c_f=2\) m/s, the ratio is 1.25 s before the solver's factor.

For a linear stage-storage network with fixed wetted area \(C_i=dV_i/d\eta\) [m²] and nonnegative connection conductances, \(\Delta t\le C_i/\sum_jG_{ij}\) makes a forward-Euler row a convex combination of adjacent stages under fixed geometry and no extra sinks. Nonlinear geometry, wet/dry switching and stronger accuracy requirements need additional treatment. An implicit method changes the stability constraints but does not remove accuracy requirements.

Choose dry thresholds in physical units, keep water below a visual wetness threshold in the ledger, and never repeatedly discard small stores without accounting. In a still lake, differing depths above different bed elevations must not generate flow when stage is equal. Test this equilibrium before storms or erosion.

## Routing as a separate capability

On an acyclic drainage graph, effective runoff accumulation can use

\[
Q_i=r_iA_i+\sum_j w_{ji}Q_j,
\]

where \(r_i\) [m/s] already reflects the chosen runoff model and outgoing weights sum to one for draining cells. Closed basins and lakes need an explicit storage/outlet representation. Calling rain “effective runoff” after also subtracting infiltration can remove the same water twice.

**Example:** 1 mm/h over 3,600 m² contributes 0.001 m³/s. Adding upstream 0.004 m³/s yields 0.005 m³/s. This result represents routed discharge, not a water depth or flood arrival time. Reroute after geometry changes; keep depression-filling analysis separate from changes to real terrain.

## Checks and diagnostics

Measure global and per-cell residuals, realized boundary transfers, stage, wet area, face flux, limited transfers and the process controlling the timestep. Use absolute plus relative tolerances tied to represented quantities.

Verify a still lake, closed rainfall basin, multiple competing outflows, dry-to-wet propagation, flow reversal, a sill, and a timestep-halving comparison. Repeat across chunk boundaries. If terrain or structures change, rebuild affected hydraulic geometry before using it. Resolve distant consequences through connected basins and downstream boundaries rather than a fixed visual-update radius.

## Primary references

- [HEC-RAS: shallow-water equations](https://www.hec.usace.army.mil/confluence/rasdocs/hecras/latest/technical-reference/hydraulic-equations/shallow-water-equations) — governing assumptions and continuity.
- [HEC-RAS: diffusive-wave approximation](https://www.hec.usace.army.mil/confluence/rasdocs/hecras/latest/technical-reference/hydraulic-equations/diffusive-wave-equation) — friction-dominated closure and its limits.
- [HEC-RAS: grid size and timestep](https://www.hec.usace.army.mil/confluence/rasdocs/r2dum/6.0/running-a-model-with-2d-flow-areas/selecting-an-appropriate-grid-size-and-time-step) — model-specific timestep selection.
- [Landlab: flow accumulation](https://landlab.csdms.io/generated/api/landlab.components.flow_accum.flow_accumulator.html) — graph runoff accumulation and routing choices.
- [Landlab: gradients and fluxes](https://landlab.csdms.io/user_guide/grid_methods/06_gradients.html) — geometry-aware field operations.

Treat implementation recipes and numerical examples here as original reference designs. They are not calibrated predictions or substitutes for a complete validated hydraulic solver.
