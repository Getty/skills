# Erosion, transport, and deposition

## Contents

- [Select the required behavior](#select-the-required-behavior)
- [Close the sediment budget](#close-the-sediment-budget)
- [Convert mass changes into bed change](#convert-mass-changes-into-bed-change)
- [Use stream power with a stated convention](#use-stream-power-with-a-stated-convention)
- [Transport suspended material](#transport-suspended-material)
- [Model settling as an optional closure](#model-settling-as-an-optional-closure)
- [Handle supply, layers, and feedback](#handle-supply-layers-and-feedback)
- [Validate the selected model](#validate-the-selected-model)

## Select the required behavior

Choose a model from the gameplay outcome. Recomputing drainage after a player digs a ditch does not require natural erosion. Visible mud transport requires a mobile sediment store. Channel filling requires deposition coupled to terrain geometry. Sorting, armoring, and detailed bedload transport require additional state and calibration.

| Choice | State to add | Main limitation |
|---|---|---|
| Immutable natural terrain | None beyond player operations | Natural channels do not evolve |
| Simple erosion with accounted export | Removed dry mass and an export ledger | Cannot predict where local deposition occurs |
| One mobile sediment class | Bed supply, suspended/mobile mass, deposition | Omits size sorting and mixed-material effects |
| Several classes and active bed layer | Per-class transport and bed composition | Requires class-specific closures and exchange rules |
| Detailed morphodynamics | Appropriate flow, transport, bed, and bank models | Needs resolution studies and calibration |

Use [Landlab SPACE](https://landlab.csdms.io/tutorials/landscape_evolution/space/SPACE_user_guide_and_examples.html) as a reference for distinguishing sediment cover, bedrock erosion, entrainment, and deposition. Do not present a small stream-power formula as a complete SPACE implementation or assume example time units and grid support match the game.

## Close the sediment budget

**Purpose:** update mobile material without creating or deleting it.

For mobile mass \(M_{i,k}\) of class \(k\) in cell \(i\):

\[
M_{i,k}^{n+1}=M_{i,k}^{n}
+\Delta t\left[-\sum_f s_{if}F_{f,k}
+A_{e,i}E_{i,k}-A_{d,i}D_{i,k}+S_{i,k}\right].
\]

Here \(F\) is signed shared-face transport in kg/s; \(s_{if}\) orients the face outward from the cell; \(E,D\) are entrainment/deposition mass rates in kg/(m² s); the corresponding areas are in m²; and \(S\) contains explicit imports/exports in kg/s. Do not silently substitute total cell area for the actual eroding or depositional support.

Calculate each internal face transfer once and add equal and opposite amounts. Bound all simultaneous outbound transfers from a store against the total available mass. Bound entrainment against the exposed material inventory and deposition against the mobile inventory. Clamping a negative result after updating breaks the budget.

Maintain an encompassing ledger:

\[
M_{\mathrm{ground}}+M_{\mathrm{mobile}}+M_{\mathrm{piles}}+M_{\mathrm{in\ transit}}
=M_{\mathrm{initial}}+M_{\mathrm{imports}}-M_{\mathrm{exports}}.
\]

Include constructed fills in exactly one ground or inventory category. Track bedrock transfers too if the model erodes rock. An explicit exported-fines sink is acceptable; an unrecorded disappearance is not.

These discrete equations are direct control-volume bookkeeping. They do not select the physical transport law, and conservation alone does not establish physical accuracy.

## Convert mass changes into bed change

**Purpose:** relate local material exchange to terrain elevation.

For a uniform bed of fixed particle density \(\rho_s\) and fixed porosity \(\phi\), with no other height-changing process:

\[
\rho_s(1-\phi)\frac{\partial z_b}{\partial t}=D_m-E_m.
\]

Use \(z_b\) in m and \(D_m,E_m\) in kg/(m² s). This restricted form describes exchange between mobile material and the bed. The [USACE bed-change reference](https://www.hec.usace.army.mil/confluence/rasdocs/d2sd/ras2dsedtr/6.2/model-description/bed-change-equation) documents a broader sediment-continuity formulation and class-specific terms.

If bedload is represented as a separate horizontal mass flux per width \(\mathbf q_b\) [kg/(m s)], add \(-\nabla\cdot\mathbf q_b\) on the right. Do not add the same bedload divergence again when it is already included in the chosen deposition/entrainment formulation. Declare which reservoir and flux each term represents.

**Original synthetic example:** deposit 100 kg uniformly over 20 m² with \(\rho_s=2500\,\mathrm{kg/m^3}\) and \(\phi=0.40\). The bulk volume is \(100/1500=0.066667\,\mathrm{m^3}\); the bed rises 0.003333 m. Remove exactly 100 kg from the mobile store. Preserve surface-water volume while rebuilding the bed's storage curve and deriving the new water level.

For changing porosity or mixtures, update constituent masses and derive the layer geometry instead of applying this fixed-density equation unchanged. Compaction can lower the surface without exporting solids. Rock uplift can move the surface without being sediment deposition; record such boundary forcing separately.

## Use stream power with a stated convention

**Purpose:** obtain a simplified erosion-speed response to drainage or discharge.

Two common model forms are:

\[
E_z=K_A A_d^{a}S^{b},\qquad
E_z=K_Q Q^{a}S^{b}.
\]

Here \(E_z\) is a lowering speed [m/s], \(A_d\) drainage area [m²], \(Q\) water discharge [m³/s], and \(S\ge0\) a dimensionless slope. The coefficient dimensions differ:

\[
[K_A]=\mathrm{m}^{1-2a}\,\mathrm{s}^{-1},\qquad
[K_Q]=\mathrm{m}^{1-3a}\,\mathrm{s}^{a-1}.
\]

Specify whether slope is a routing-link bed slope, channel slope, or another quantity. Do not feed a negative slope into a fractional power. Threshold erosion, sediment shielding, and transport capacity are additional choices; this bare formula includes none of them.

If uniform effective runoff \(r\) gives \(Q=rA_d\), equivalent coefficients obey \(K_Q=K_A/r^a\). That conversion relies on the runoff assumption and does not make area a universal discharge substitute. Avoid transferring a calibrated coefficient between area/discharge forms, exponent choices, or second/year conventions.

**Original synthetic example:** choose \(a=0.5\), \(b=1\), \(K_A=10^{-8}\,\mathrm{s^{-1}}\), \(A_d=10{,}000\,\mathrm{m^2}\), and \(S=0.02\). Then \(E_z=2\times10^{-8}\,\mathrm{m/s}\), or 1.728 mm over 86,400 seconds under unchanged inputs. The number is a deliberately synthetic arithmetic example, not a predicted natural rate.

For a finite mobile layer, requested lowering cannot exceed available cover unless an explicitly selected bedrock law takes over. Convert lowering into removed dry mass using the material actually exposed. Substep when the proposed change would cross a significant layer boundary, alter routing, or reverse a controlling slope.

## Transport suspended material

**Purpose:** move a well-mixed suspended class with water.

For water volume \(V_i>0\), concentration \(C_{i,k}=M_{i,k}/V_i\) [kg/m³]. A simple first-order advective face flux is:

\[
F_{f,k}=Q_f C_{\mathrm{donor},k},
\]

with \(Q_f\) in m³/s and the donor chosen by the water-flow sign. Use the **accepted**, water-limited face transfer, not a larger proposed flux. For an explicit well-mixed update with no new sources, exporting fraction \(\alpha\) of donor water exports fraction \(\alpha\) of each suspended class. Sum all outflows before limiting.

This is a numerical transport closure, not a bedload formula. Higher-order reconstruction requires positivity and monotonicity treatment, and suspended sediment may need settling or mixing physics. At very low water volume, use an explicit dry-state rule: deposit remaining material, retain a dry mobile residue, or transfer it elsewhere. Dividing by an arbitrary epsilon and discarding the resulting excess mass is not a physical dry-state rule.

Keep large concentrations within the validity range of the dilute-flow assumption. If solids materially change the fluid density or rheology, this simple water-plus-tracer model is insufficient.

## Model settling as an optional closure

**Purpose:** exchange a dilute, well-mixed suspension with a depositional bed under stated conditions.

\[
D_m=v_s C,
\]

where settling speed \(v_s\) is in m/s. Apply over a declared depositional area; constrain deposition to available mass. The formula omits upward turbulent mixing, resuspension thresholds, flocculation, and spatial concentration gradients. Near-bed concentration is generally the relevant quantity; substituting cell-average concentration is the selected well-mixed approximation. The [USACE deposition reference](https://www.hec.usace.army.mil/confluence/rasdocs/d2sd/ras2dsedtr/6.3/model-description/deposition) documents richer deposition closures; its correction factors and concentration conventions must be checked before porting them.

For an isolated, constant-volume, well-mixed water store with fixed depositional area \(A_w\), integration gives:

\[
M(t+\Delta t)=M(t)\exp\left(-\frac{v_sA_w}{V}\Delta t\right).
\]

This follows directly by substituting \(C=M/V\) into the mass balance. The exponent is dimensionless. Use it only while \(V\), area, and settling speed remain fixed over that exchange step; recompute for changing geometry and flow.

**Original synthetic example:** with \(V=10\,\mathrm{m^3}\), \(A_w=20\,\mathrm{m^2}\), \(v_s=0.001\,\mathrm{m/s}\), \(M=5\,\mathrm{kg}\), and \(\Delta t=100\,\mathrm s\), the retained mass is 4.093654 kg and deposit is 0.906346 kg. Their sum remains 5 kg. An explicit step would instead require a sufficiently small exchange fraction to avoid over-deposition.

## Handle supply, layers, and feedback

Process exposed material rather than averaging erodibility through the entire subsurface. A thin protective cover can control incision; removing it changes the next process evaluation. If several processes draw from the same mobile layer during one step, coordinate their requests so they cannot each consume the original full amount.

For multiple classes, conserve each class through entrainment, advection, deposition, and active-layer exchange. A coarse surface can reduce access to finer underlying material, but an armoring rule needs explicit state and calibration. Do not merely reduce all erosion by a constant after an arbitrary time.

After meaningful bed change, invalidate storage curves, wetted cross-sections, hydraulic connections, routing, surface material, and affected geometry. Hold water volume constant during the geometry conversion. Iterate or subcycle the coupled system if transport appreciably changes the flow within a step. A fast erosion multiplier changes feedback timing and must be declared as a gameplay approximation.

## Validate the selected model

Use closed-transfer tests, known deposition mass-to-height calculations, depletion of a thin cover, and concentration-preserving water advection. Compare total dry mass before and after a bank failure or excavation/export. Verify sediment entering a reservoir reduces its capacity only through the corresponding deposited volume.

Halve the timestep and check bed-change and export convergence for the actual coupling. Inspect both mass residuals and physical patterns: exact mass balance can coexist with wrong routing, excessive numerical diffusion, or oscillating bed elevations. Add detailed bedload, grain sorting, or morphodynamic acceleration only after a simpler model's limits affect the intended game.
