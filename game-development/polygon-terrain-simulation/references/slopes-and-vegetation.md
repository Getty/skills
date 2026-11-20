# Slopes, soil movement, and vegetation coupling

## Contents

- [Select a slope model](#select-a-slope-model)
- [Use a conservative linear transport law](#use-a-conservative-linear-transport-law)
- [Derive a timestep from the actual mesh](#derive-a-timestep-from-the-actual-mesh)
- [Limit transport by mobile material](#limit-transport-by-mobile-material)
- [Offer a bounded slope-relaxation heuristic](#offer-a-bounded-slope-relaxation-heuristic)
- [Add nonlinear transport or weathering when needed](#add-nonlinear-transport-or-weathering-when-needed)
- [Connect vegetation to named processes](#connect-vegetation-to-named-processes)
- [Validate changes and time scaling](#validate-changes-and-time-scaling)

## Select a slope model

Keep natural slope evolution optional. A city builder may require only designed embankments and construction slope constraints. A landscape-evolution game may need slow soil creep, rapid failures, and weathering. Distinguish these behaviors instead of using one smoothing pass for all of them.

| Model | Suitable purpose | Important omission |
|---|---|---|
| Construction slope limit | Restrict or reshape earthworks | Does not predict natural failure |
| Conservative slope relaxation | Settle loose piles after edits | Designer rule rather than geotechnical prediction |
| Linear hillslope transport | Slow, low-gradient landscape smoothing | Omits threshold failure and detailed soil depth effects |
| Nonlinear/depth-dependent transport | Slope-dependent creep and finite cover | More demanding parameter and timestep choices |
| Limit equilibrium / landslide model | Failures affect gameplay materially | Needs geometry, water, and material-strength data |

Keep rock weathering separate from loose-soil movement. The height of bare rock should not decrease merely because a generic soil smoother treats it as an unlimited mobile store.

## Use a conservative linear transport law

**Purpose:** move homogeneous mobile material downhill using a low-gradient approximation.

\[
\mathbf q_b=-D\nabla z,\qquad
\frac{\partial z}{\partial t}=-\nabla\cdot\mathbf q_b.
\]

Here \(z\) is elevation [m], \(D\) diffusivity [m²/s], and \(\mathbf q_b\) **bulk-volume flux per width** [m²/s], including pore volume. The elevation equation assumes unchanged bulk density/porosity, a suitable mobile supply, and no other local source. For spatially uniform \(D\), it becomes \(\partial z/\partial t=D\nabla^2z\). Use the sign convention that flux points downhill.

The [Landlab LinearDiffuser reference](https://landlab.csdms.io/generated/api/landlab.components.diffusion.diffusion.html) supplies an explicit finite-volume implementation example. Read its component and boundary assumptions before using it as a dependency. The formulas below are a direct finite-volume derivation for the stated mesh, not a promise about every package implementation.

For an orthogonal two-point connection between cells \(i,j\), shared-face length \(L_f\), normal separation \(d_{ij}>0\), and face diffusivity \(D_f\ge0\):

\[
Q_{b,ij}=D_f L_f\frac{z_i-z_j}{d_{ij}}.
\]

\(Q_b\) is m³/s and positive from \(i\) to \(j\). Calculate it once and subtract/add the same volume to the respective cells. Divide each cell's net volume rate by its own area. Do not take an unweighted average of neighbors on an irregular mesh.

If cell-center connections are not normal to faces, this link difference is not automatically the face-normal gradient. Use appropriate gradient reconstruction/nonorthogonal correction or select a compatible mesh and solver. Decorative polygon borders are not a substitute for physical face metrics.

**Original synthetic example:** cells have areas 100 and 200 m², elevations 3 and 1 m, face length 10 m, center separation 15 m, and \(D_f=0.01\,\mathrm{m^2/s}\). The requested transfer is 0.013333 m³/s. Over 60 s it moves 0.8 m³, giving elevations 2.992 and 1.004 m under the constant-density, sufficient-cover assumptions. The area-weighted height sum remains \(100(3)+200(1)=500\,\mathrm{m^3}\). This is a numerical example, not a calibrated natural creep rate.

## Derive a timestep from the actual mesh

**Purpose:** keep the simple explicit linear update monotone under its assumptions.

Define \(w_{ij}=D_fL_f/d_{ij}\) [m²/s]. Without sources:

\[
z_i^{n+1}=\left(1-\frac{\Delta t}{A_i}\sum_jw_{ij}\right)z_i^n
+\frac{\Delta t}{A_i}\sum_jw_{ij}z_j^n.
\]

For nonnegative symmetric face weights and the basic fixed-geometry scheme, a sufficient nonnegative-weight condition is:

\[
\Delta t\le\min_i\frac{A_i}{\sum_jw_{ij}}.
\]

An isolated cell with zero weight sum imposes no restriction. This bound follows by requiring the central update coefficient to be nonnegative. Include boundary contributions consistently. For a square grid with four neighbors, constant \(D\), and spacing \(\Delta x\), it reduces to \(\Delta t\le\Delta x^2/(4D)\).

Use a margin below the bound for implementation robustness; still check accuracy by reducing the timestep. This condition does not guarantee finite-soil availability, prevent every individual slope from reversing, or establish stability for nonlinear, anisotropic, nonorthogonal, or coupled schemes. Re-derive the relevant operator bound when changing the scheme.

For a 10 m square cell and synthetic \(D=0.001\,\mathrm{m^2/s}\), the four-neighbor bound is 25,000 s. A game-time acceleration that multiplies \(D\) by 100 reduces that bound to 250 s. Skipping this rescaling changes numerical behavior, not just animation speed.

## Limit transport by mobile material

Calculate all outbound requests from a layer before granting them. If total proposed outbound dry mass exceeds the donor's available material, scale those requests together or substep. Apply the resulting face amount identically at both ends. Avoid lowering the surface below bedrock and then restoring its height without returning the corresponding material.

The simple bulk-volume height equation assumes compatible bulk density. If donor and receiver packing differ, conserve dry mass and derive both volume changes independently:

\[
\Delta z_i=-\frac{\Delta M}{\rho_{b,i}A_i},\qquad
\Delta z_j=+\frac{\Delta M}{\rho_{b,\mathrm{deposit}}A_j}.
\]

Do not claim bulk volume is conserved across a compaction change. Coordinate pore-water transport/displacement with the chosen wet-soil model. For constituent mixtures, transfer each dry mass and use the layer-geometry identities rather than a single fixed density.

Differentiate transportable cover, deposited debris, cohesive banks, and bedrock. A universal neighbor smoother will otherwise blur rock cliffs, remove artificial retaining structures, and destroy foundation geometry regardless of their intended mechanics.

## Offer a bounded slope-relaxation heuristic

**Purpose:** settle a loose pile to a selected maximum pairwise slope. Label this a game heuristic, not a prediction of saturated slope stability.

For a higher donor \(i\), lower receiver \(j\), constant common bulk density, and chosen maximum slope \(S_{\max}\):

\[
V_{ij}^*=\frac{\max(z_i-z_j-S_{\max}d_{ij},0)}{1/A_i+1/A_j}.
\]

The denominator converts a moved bulk volume into the reduction of the two-cell height difference. Limit \(V_{ij}^*\) to available mobile volume and any per-step rate constraint. On many edges, coordinate requests; sequential sweeps otherwise introduce order dependence. If using sweeps intentionally, fix the ordering or use a deterministic schedule and measure its bias.

**Original synthetic example:** \(A_i=100\,\mathrm{m^2}\), \(A_j=50\,\mathrm{m^2}\), \(d=10\,\mathrm m\), height difference 8 m, and \(S_{\max}=0.5\). The pairwise target transfer is 100 m³. It lowers the donor 1 m and raises the receiver 2 m, leaving a 5 m difference. If only 60 m³ is mobile, move at most 60 m³ and retain the remaining excess slope unless a separate rock/failure mechanism applies.

Use local terrain support rather than whole-cell slopes where a building platform, retaining wall, or narrow bank matters. An average cell elevation can hide a hazardous local face or incorrectly imply that a stable engineered terrace must slump.

## Add nonlinear transport or weathering when needed

For steeper hillslopes, a finite polynomial example is:

\[
\mathbf q_b=-D\nabla z\sum_{k=0}^{N}\left(\frac{|\nabla z|}{S_c}\right)^{2k},\qquad S_c>0.
\]

This is one model family, not an automatic upgrade. The [Landlab Taylor diffuser tutorial](https://landlab.csdms.io/tutorials/hillslope_geomorphology/taylor_diffuser/taylor_diffuser.html) describes its use. \(S_c\) is a dimensionless model scale; a truncated polynomial remains finite at \(|\nabla z|=S_c\). Do not present that scale as a hard angle-of-repose threshold. Effective sensitivity grows with slope, so the linear timestep estimate using only \(D\) is insufficient; evaluate the actual nonlinear operator and substep.

An optional weathering law can use bedrock-lowering speed:

\[
P(H)=P_0e^{-H/H_*},\qquad
\frac{dz_r}{dt}=-P(H),\qquad
\frac{dH}{dt}=\frac{\rho_r}{\rho_b}P(H),
\]

where \(H\) is soil thickness [m], \(H_*>0\) a characteristic depth [m], \(P_0\) [m/s], and \(\rho_r,\rho_b\) are dry bulk densities of consumed rock and produced soil. These equations assume all weathered dry mass becomes soil locally, constant densities, and no other process during the exchange. Soluble export or chemical mass changes need extra budget terms.

The [Landlab integrated-weathering reference](https://landlab.csdms.io/generated/api/landlab.components.weathering.exponential_weathering_integrated.html) illustrates why density ratio and changing soil depth matter. Derive the total surface change from \(z=z_r+H\); weathering can increase volume through looser packing without adding dry mass. Declare whether a borrowed coefficient measures rock lowering or soil production before applying a density factor.

## Connect vegetation to named processes

Use only couplings needed by the game:

| Mechanism | Terrain interface | Accounting/limitation |
|---|---|---|
| Canopy interception | Rainfall reaching ground, canopy store | Evaporation/drip closes the water budget |
| Surface roughness | Hydraulic resistance parameters | Specify cover and scale dependence |
| Root water uptake | Requested soil-water withdrawal | Grant only available water |
| Root reinforcement | Strength-law parameter contribution | Requires depth/time/material assumptions |
| Surface protection | Selected entrainment response | Do not silently change all transport laws |
| Litter/organic deposition | Added material with explicit provenance | Model an external biomass source if tracking its mass |

Let ecology own species, growth, and succession when those systems exist; let terrain expose soil, moisture, inundation, and support. A simple vegetation cover fraction is enough for many games. It need not import population needs or farming logistics into the terrain solver.

These are proposed coupling points, not calibrated universal relationships. Keep recovery/decay time explicit: clearing visible plants need not remove every root immediately, and flooding duration can matter more than a momentary wet flag. Avoid a single unexplained “vegetation reduces erosion by X percent” rule applied to unrelated mechanisms.

## Validate changes and time scaling

Test conservative movement between unequal-area cells, no transport from absent cover, slope relaxation at its threshold, and a protected terrace. Check both dry mass and pore water when packing differs. Compare a flat surface against a perturbed one; no unforced flux should arise on the flat case.

Use the actual chosen timestep bound, then test convergence separately. Compare closed-domain material totals and limit activations across mesh refinement. Run paired vegetation scenarios that differ in one named coupling so unintended effects are visible. Document physical time, simulation time, and any accelerated morphology factor; the same printed parameter value cannot silently mean m²/s in one module and m²/year in another.
