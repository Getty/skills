# Soil water, infiltration and groundwater

## Contents

- [Select the necessary depth](#select-the-necessary-depth)
- [Stores and terminology](#stores-and-terminology)
- [Bounded bucket baseline](#bounded-bucket-baseline)
- [Optional infiltration models](#optional-infiltration-models)
- [Darcy flow and groundwater](#darcy-flow-and-groundwater)
- [Terrain changes and coupling](#terrain-changes-and-coupling)
- [Calibration and verification](#calibration-and-verification)
- [Primary references](#primary-references)

## Select the necessary depth

Use a soil bucket for finite infiltration, drying and basic wetness. Add connected groundwater when wells, springs, baseflow or excavations below a water table matter. Use richer unsaturated flow only when the game's behavior justifies the parameter and solver burden. A sophisticated hydrology reference is optional knowledge, not a requirement for every terrain implementation.

| Model | State | Useful behavior | Limitation |
|---|---|---|---|
| Bounded bucket | Stored soil water | Wet/dry ground, finite capacity, drainage delay | No resolved pressure profile |
| Multiple buckets/layers | Water per layer | Perched storage, layered infiltration approximation | Vertical discretization and closures remain simplified |
| Shallow unconfined groundwater | Head or drainable storage | Lateral groundwater, wells, return flow | Restricted aquifer geometry and flow assumptions |
| Richards/3D groundwater family | Pressure/head fields and constitutive laws | Detailed unsaturated/saturated coupling | Much higher complexity and calibration demand |

Do not claim “groundwater simulation” if the implementation only stores a moisture color with no storage or hydraulic connection.

## Stores and terminology

Keep surface water, unsaturated soil water and any saturated aquifer storage distinct. Ensure they cover different physical volumes or clearly partition a common column; summing a full saturated column and overlapping bucket storage would double-count water.

For a layer of plan area \(A\) [m²], thickness \(d\) [m], total porosity \(\phi\) and volumetric water content \(\theta\),

\[
W=Ad\theta,\qquad W_{sat}=Ad\phi,\qquad 0\le\theta\le\phi.
\]

\(W\) and \(W_{sat}\) are m³. A residual or plant-inaccessible store may be retained if needed; it is still water in the ledger. Distinguish total porosity, effective transport porosity, field-capacity concepts, specific retention and specific yield. They are not interchangeable tuning names.

Hydraulic conductivity \(K\) [m/s] describes transmission for a specified fluid and medium. Intrinsic permeability \(k\) [m²] relates through

\[
K=\frac{k\rho_wg}{\mu}.
\]

Use fluid density \(\rho_w\) [kg/m³], gravity [m/s²], and dynamic viscosity \(\mu\) [Pa·s]. Porosity alone does not determine \(K\). An anisotropic conductivity requires a tensor, not a scalar with an arbitrary “flow direction.”

**Original example:** with synthetic \(k=10^{-12}\) m², \(\rho_w=1000\) kg/m³, \(g=9.81\) m/s² and \(\mu=0.001\) Pa·s, \(K=9.81\times10^{-6}\) m/s. This arithmetic illustrates the conversion; use fluid properties and material evidence appropriate to the game model.

## Bounded bucket baseline

### Formula card: actual infiltration

For a simple operator-split step, define available surface volume \(V^*\), exposed permeable area \(A_p\), infiltration capacity \(f_c\) [m/s], and empty bucket volume \(W_{sat}-W\). Transfer

\[
\Delta V_{inf}=\min\left(V^*,\,f_cA_p\Delta t,\,[W_{sat}-W]_+\right).
\]

Apply \(-\Delta V_{inf}\) to surface water and \(+\Delta V_{inf}\) to soil water. Supply rain either to \(V^*\) first or through an explicit direct-infiltration path, never both. On a cell with multiple disconnected wet/pervious patches, compute local availability instead of letting every patch access the entire cell's water.

**Original example:** \(A_p=100\) m², \(d=0.5\) m, \(\phi=0.4\) give 20 m³ saturated capacity. With \(W=18\) m³, surface water 1 m³, \(f_c=10^{-5}\) m/s and \(\Delta t=600\) s, actual infiltration is 0.6 m³. Surface ends at 0.4 m³ and soil at 18.6 m³. The rate capacity alone cannot create infiltrating water on a dry surface.

### Formula card: optional linear drainage

An explicitly labeled game closure is

\[
Q_{drain}=\frac{[W-W_{ref}]_+}{\tau_d}.
\]

\(W_{ref}\) [m³] is a chosen retained-storage threshold and \(\tau_d\) [s] a drainage timescale. It is not a universal soil law. For fixed parameters and no simultaneous input, the exact excess-storage decay gives

\[
\Delta W_{drain}=[W-W_{ref}]_+\left(1-e^{-\Delta t/\tau_d}\right).
\]

Send the drained amount to a lower layer, aquifer, spring or explicit external boundary. Define actual evaporation and root uptake separately and cap their combined withdrawals by available soil water. Moisture recovery means water moves or capacity state changes; it never means automatically recreating previously evaporated water.

For \(W-W_{ref}=2\) m³ and \(\Delta t=\tau_d\), drainage is about 1.264 m³. Update exact closures consistently with the chosen splitting order and test sensitivity to that order when inputs change rapidly.

## Optional infiltration models

### Formula card: Green-Ampt capacity

Under a simplified sharp wetting front, homogeneous soil, initial moisture deficit \(\Delta\theta=\theta_s-\theta_i\), and negligible ponding head,

\[
f_c=K_s\left(1+\frac{\psi_f\Delta\theta}{F}\right),\qquad F>0.
\]

Use saturated conductivity \(K_s\) [m/s], positive suction-head magnitude \(\psi_f\) [m], and cumulative infiltration depth \(F\) [m]. The formula gives capacity, not guaranteed infiltration. Track ponding transitions and available water. When ponding head is significant, use the corresponding hydraulic-gradient formulation rather than silently applying the negligible-head equation.

**Example:** synthetic \(K_s=5\times10^{-6}\) m/s, \(\psi_f=0.15\) m, \(\Delta\theta=0.2\), \(F=0.03\) m give \(f_c=10^{-5}\) m/s. The implied wetting-front depth is \(F/\Delta\theta=0.15\) m under these assumptions.

At \(F=0\), avoid a literal singular division. Use the rainfall-limited/ponding branch and solve the integrated ponded equation once that regime applies. With \(a=\psi_f\Delta\theta\),

\[
\Delta t=\frac{1}{K_s}\left[F_2-F_1-a\ln\!\left(\frac{F_2+a}{F_1+a}\right)\right].
\]

Bracket \(F_2\ge F_1\), check convergence and bound by available supply and compatible storage. Handle \(a=0\) as constant capacity. If the front reaches a layer boundary, switch the model/parameters rather than letting the same homogeneous-soil assumption continue indefinitely. Persistent multi-storm behavior needs a dry-period recovery rule, not a daily blind reset.

### Formula card: Horton capacity

A simple empirical wetting trajectory is

\[
f_c(t_w)=f_\infty+(f_0-f_\infty)e^{-k_dt_w}.
\]

\(f_0,f_\infty\) [m/s], decay \(k_d\) [s^-1], and effective wetting time \(t_w\) [s] define this curve. Track capacity-state recovery separately during dry periods. Calendar time since world creation is not wetting time. Under supply limitation, the selected Horton variant determines how its state advances.

**Example:** \(f_0=2\times10^{-5}\), \(f_\infty=5\times10^{-6}\) m/s and \(k_dt_w=1\) give about \(1.052\times10^{-5}\) m/s. Actual infiltration still uses availability and storage constraints.

EPA SWMM's hydrology reference documents both families and their event/recovery logic. The formulas here introduce choices; adopting a full variant requires following its complete state machine. Do not mix parameters or recovery semantics from different variants without documenting a new approximation.

## Darcy flow and groundwater

### Formula card: Darcy flux

\[
\mathbf q=-\mathbf K\nabla H.
\]

Head \(H\) [m] combines elevation and pressure head. Darcy flux \(\mathbf q\) [m/s] is discharge per gross cross-sectional area. It differs from average pore velocity, approximately \(\mathbf v_p=\mathbf q/\phi_e\) where effective porosity \(\phi_e\) and the transport assumptions support that interpretation.

For an isotropic, orthogonal connection,

\[
Q_{ij}=K_fA_{x,f}\frac{H_i-H_j}{d_{ij}},
\]

with flow cross-section \(A_x\) [m²] and distance \(d\) [m]. With layered serial resistance, use a resistance-based/harmonic interface value; a simple arithmetic mean can greatly overstate leakage through a low-conductivity barrier. General nonorthogonal or anisotropic meshes need a compatible discretization.

**Example:** \(K_f=10^{-5}\) m/s, \(A_x=20\) m², \(\Delta H=0.2\) m, \(d=10\) m give \(Q=4\times10^{-6}\) m³/s, or 0.3456 m³/day. With \(\phi_e=0.25\), pore velocity is four times Darcy flux; this does not multiply the volume discharge by four.

### Formula card: shallow unconfined aquifer

Under Dupuit-type predominantly horizontal flow, saturated thickness \(b\), transmissivity \(T=Kb\) [m²/s], and specific yield \(S_y\), a simplified form is

\[
S_y\partial_tH=\nabla\cdot(T\nabla H)+r_g-u_g.
\]

Recharge and pumping per plan area \(r_g,u_g\) have units m/s. For fixed geometry, a water-table change \(\Delta H\) implies drainable-storage change \(\Delta W=S_yA\Delta H\). This represents incremental drainable storage, not all water in the rock. Choose a reference state and account for retained water if total pore water is tracked.

**Example:** \(A=100\) m², \(S_y=0.2\), and rise 0.3 m require 6 m³ of additional drainable storage. Total porosity need not equal 0.2.

For a frozen linear orthogonal network, conductance is \(G_{ij}=T_fL_f/d_{ij}\) [m²/s]. A forward-Euler monotonicity condition is \(\Delta t\le S_yA_i/\sum_jG_{ij}\). Nonlinear saturated thickness, drying, seepage and coupling need their own safeguards and accuracy checks. Do not transfer surface-water CFL values to this diffusive system.

## Terrain changes and coupling

Excavation can expose permeable layers, intersect a saturated zone or remove aquifer material. Filling and compaction can reduce pore volume or block pathways. Recompute affected geometry and transmission parameters, preserve dry solids and stored water, and route any displaced water explicitly.

For simple surface/groundwater exchange use a declared conductance times head difference, bounded by donor availability and valid seepage conditions. Prevent simultaneous duplicate infiltration and groundwater leakage over the same interface. A prescribed water table is an external reservoir assumption and can provide unlimited water unless its exchange is bounded and recorded.

Separate physical connectivity from visibility. Aquifer flux across an inactive chunk must continue under its chosen reduced model or explicit boundary exchange. A local pit can draw water from beyond the rendering update region.

## Calibration and verification

Keep source-reported measurements, derived quantities and synthetic game parameters labeled separately. Save units, material state, scale, provenance and valid operating range. Soil class is a prior for parameter choice, not proof of one exact conductivity or suction value. Avoid copying a table's mm/h or days^-1 into an SI solver unchanged.

Test dry soil without supply; a bucket near capacity; multiple competing sinks; drainage into a second store; compaction displacing pore water; equal-head groundwater; a barrier layer; excavation beneath groundwater; and combined surface/soil/aquifer budget closure. Check convergence when refining timestep and coupling interval. Document omitted stores so an external loss is not mistaken for numerical leakage.

## Primary references

- [EPA SWMM Hydrology Reference Manual](https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P100NYRA.txt) — infiltration families and continuous-event state handling, Chapters 4–5.
- [EPA: Darcy's law](https://www3.epa.gov/ceampubl/learn2model/part-two/onsite/darcy.html) — flux, conductivity, gradient and porosity distinction.
- [Groundwater Project: hydraulic conductivity](https://books.gw-project.org/hydrogeologic-properties-of-earth-materials-and-principles-of-groundwater-flow/chapter/hydraulic-conductivity/) — conductivity versus intrinsic permeability and fluid properties.
- [Landlab: GroundwaterDupuitPercolator](https://landlab.csdms.io/generated/api/landlab.components.groundwater.dupuit_percolator.html) — an implementation with explicit shallow-aquifer assumptions and adaptive stepping.
- [USGS: MODFLOW 6 groundwater model documentation](https://www.usgs.gov/publications/documentation-modflow-6-groundwater-flow-model) — advanced finite-volume groundwater formulations and boundaries.

The bucket closures, contract recommendations and synthetic examples are original design aids. They are not calibrated soil or aquifer data.
