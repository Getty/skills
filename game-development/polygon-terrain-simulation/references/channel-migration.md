# Changing channels, banks, and floodplains

## Contents

- [Separate three kinds of change](#separate-three-kinds-of-change)
- [Choose a representation](#choose-a-representation)
- [Account for bank retreat](#account-for-bank-retreat)
- [Use excess shear with correct units](#use-excess-shear-with-correct-units)
- [Treat bank failure separately](#treat-bank-failure-separately)
- [Define an optional game heuristic](#define-an-optional-game-heuristic)
- [Handle topology-changing events](#handle-topology-changing-events)
- [Validate migration rather than appearance](#validate-migration-rather-than-appearance)

## Separate three kinds of change

Resolve what “the water moves over time” means before choosing physics:

| Intended behavior | Required change |
|---|---|
| Digging changes the runoff route | Terrain/connectivity and drainage update |
| A flood occupies a different area | Water storage, stage, and hydraulic flow |
| A river erodes sideways | Bank material, transport, and evolving channel geometry |

Implement the first two without natural channel migration when that suits the game. Vertical incision and routing updates can alter a drainage network, but they do not automatically model meander growth, bank undercutting, or sediment-supported bars.

The [USACE BSTEM overview](https://www.hec.usace.army.mil/confluence/rasdocs/rassed1d/1d-sediment-transport-technical-reference-manual/bstem-technical-reference-manual/overview) separates bank failure, hydraulic toe scour, and vertical bed change. This distinction is useful even for a simplified game model: a lowered bed can destabilize a bank, and collapsed material must enter a sediment store before it is transported away.

## Choose a representation

Keep a fixed computational mesh for the first implementation. Store evolving bed/bank geometry in local subpatches, cross-sections, or refined terrain where necessary. Moving the visible river centerline without altering terrain and storage creates contradictory collision, flooding, and material state.

| Representation | Appropriate use | Limitation to disclose |
|---|---|---|
| Channels follow whole cells/faces | Strategic world map | Movement is quantized by mesh size |
| Local bank profiles and subcell channel | Buildings, bridges, and smaller streams | Requires consistent subcell connectivity and storage |
| Detailed 2D morphodynamics | Floodplain/river behavior is central gameplay | Flow and sediment resolution become major costs |
| Moving/adaptive simulation mesh | Specialized solver needs | Requires conservative remapping and persistent-ID handling |

Separate the hydraulic channel graph from navigation. Keep bridges, culverts, levees, and bank protection attached to physical footprints or structures, not a transient river-rendering vertex. A structure can be undermined without its administrative building entity changing identity.

The [Langston and Tucker lateral-erosion paper](https://esurf.copernicus.org/articles/6/1/2018/) supplies a model family for bedrock-channel widening. The [Landlab LateralEroder implementation](https://landlab.csdms.io/generated/api/landlab.components.lateral_erosion.lateral_erosion.html) documents square-cell raster input. Treat its algorithm as research to adapt and verify; do not assume it runs unchanged on arbitrary polygons or predicts alluvial meandering.

## Account for bank retreat

**Purpose:** turn a geometric bank movement into a conserved material transfer.

For an approximately vertical, uniform bank of active height \(H_b\), segment length \(L_b\), small outward retreat \(\Delta n\), and dry bulk density \(\rho_b\):

\[
\Delta V_b\approx L_bH_b\Delta n,\qquad
\Delta M_s=\rho_b\Delta V_b.
\]

Use m, m³, and kg. This local swept-volume approximation assumes a simple bank profile and small displacement relative to geometric variation. For sloped or layered banks, integrate the removed cross-section/volume and apportion the mass by the intersected layers. Avoid counting the same overlapping swept area twice at bends.

A normal mass erosion rate \(E_m\) [kg/(m² s)] implies normal retreat speed \(v_n=E_m/\rho_b\) [m/s] under the same uniform-bank assumption. Its active area is the **bank face**, not the horizontal plan area of an entire terrain polygon.

When material detaches, specify the receiver: near-bank debris, bed material, suspended load, bedload, or an explicit export. Do not simultaneously deposit its full mass locally and add its full mass to suspension. Represent delayed remobilization if collapsed blocks remain at the toe.

Rebuild stage-volume and conveyance geometry after retreat. Preserve existing water volume during that change, then allow the water model to refill new capacity through actual flows. Newly created channel space is not a water source.

## Use excess shear with correct units

**Purpose:** represent one possible cohesive-scour response above a threshold.

\[
E_m=M_0\max\left(\frac{\tau}{\tau_c}-1,0\right),\qquad \tau_c>0.
\]

Here \(E_m\) and \(M_0\) have units kg/(m² s), while applied shear \(\tau\) and critical shear \(\tau_c\) are in Pa. An alternative convention is:

\[
E_m=K_d\max(\tau-\tau_c,0),\qquad M_0=K_d\tau_c.
\]

Then \(K_d\) has units kg/(m² s Pa). These coefficients are not interchangeable numeric values. The [USACE coefficient-convention reference](https://www.hec.usace.army.mil/confluence/rasdocs/rassed1d/1d-sediment-transport-technical-reference-manual/cohesive-transport/krone-and-partheniades-methods/kd-vs-m) documents this distinction. Other erosion models use volumetric or length rates; convert their coefficients before use.

**Original synthetic example:** let \(M_0=0.01\,\mathrm{kg/(m^2\,s)}\), \(\tau=3\,\mathrm{Pa}\), and \(\tau_c=2\,\mathrm{Pa}\). Then \(E_m=0.005\,\mathrm{kg/(m^2\,s)}\). Across a bank 10 m long and 2 m high for 60 s, removal is 6 kg. At \(\rho_b=1500\,\mathrm{kg/m^3}\), volume is 0.004 m³ and uniform retreat is 0.0002 m.

These synthetic values check dimensional conversions; they are not calibrated erosion parameters. Supply the bank shear from an appropriate hydraulic approximation or solver. Treating whole-cell discharge or bed shear as exact bank shear needs a declared approximation. Limit each step by available bank material, layer boundaries, geometric validity, and the acceptable movement of the hydraulic boundary.

## Treat bank failure separately

**Purpose:** represent loss of mechanical stability after undercutting, saturation, excavation, or bed lowering.

A basic effective-stress strength relation is:

\[
\tau_{\mathrm{strength}}=c'+(\sigma_n-u)\tan\varphi',
\]

where cohesion \(c'\), total normal stress \(\sigma_n\), pore-water pressure \(u\), and strength are in Pa; friction angle \(\varphi'\) is dimensionless but must use the expected radian/degree convention in code. This relation applies to a specified material and stress state; it is not a complete slope-failure solver. Handle tensile states, suction, stratification, and drainage using the chosen model rather than extending it blindly.

**Original synthetic example:** with \(c'=2000\,\mathrm{Pa}\), \(\sigma_n=12{,}000\,\mathrm{Pa}\), \(u=4000\,\mathrm{Pa}\), and \(\varphi'=30^\circ\), strength is approximately 6618.8 Pa. Raising \(u\) to 8000 Pa gives approximately 4309.4 Pa. Whether failure occurs still depends on driving stress, geometry, boundary forces, and the selected failure surface.

For a force-based limit-equilibrium calculation:

\[
FS=\frac{\text{resisting forces}}{\text{driving forces}}.
\]

Keep all force terms in compatible units and define what \(FS<1\) triggers. The [USACE soil-force reference](https://www.hec.usace.army.mil/confluence/rasdocs/rassed1d/1d-sediment-transport-technical-reference-manual/bstem-technical-reference-manual/bank-failure/layer-method/soil-forces) and [hydraulic-force reference](https://www.hec.usace.army.mil/confluence/rasdocs/rassed1d/1d-sediment-transport-technical-reference-manual/bstem-technical-reference-manual/bank-failure/layer-method/hydraulic-forces) distinguish material resistance, gravity, pore pressure, and channel-water effects. Rapidly lowering channel water need not instantly drain the bank.

A game can instead use a declared angle/unsupported-volume rule. Apply it to actual movable material, conserve the resulting collapse mass, and label it a heuristic. A triangular removed section 2 m high, 3 m wide, and 5 m long has volume 15 m³; at 1600 kg/m³ it contributes 24,000 kg. Record where those solids and their pore water go.

## Define an optional game heuristic

Use a deterministic, bounded procedure when visible migration matters more than resolving detailed hydraulics:

1. Identify candidate banks adjacent to sustained channel flow.
2. Estimate a scour exposure from the chosen local flow approximation.
3. Apply material/cover resistance and compute a limited retreat amount.
4. Integrate the actual swept layered volume and transfer its constituents.
5. Evaluate a separate collapse rule if geometry becomes unsupported.
6. Update bed/bank geometry, hydraulic storage, and affected dependencies.
7. Let the water and sediment models respond before accumulating large further changes.

Curvature can be a designer-controlled bias, but do not label an arbitrary outside-bend multiplier a universal physical law. A purely curvature-driven centerline can self-intersect, erode uphill through barriers, or create sediment without a source. Constrain changes against terrain, protection, available material, and topology.

Keep a game-speed multiplier separate from physical coefficients and timestamps. Increasing morphological speed without adjusting coupled water/sediment responses changes the modeled system. Use the approximation deliberately and test the intended time horizon.

## Handle topology-changing events

Treat a cutoff, avulsion, levee breach, blocked channel, or divided flow as a connectivity event with conserved state transfer. A new route may activate after its entrance threshold is reached; proximity alone does not establish a hydraulic connection. Preserve disconnected pools until a real path connects them.

For coarse meshes, expose migration resolution to the designer. If a channel is narrower than a cell, an entire-cell state switch can produce abrupt jumps. Use local refinement or subcell geometry when those jumps affect foundations, bridges, or property boundaries. Reassigning river labels alone is insufficient.

Keep consequences in their owning domains. Terrain reports changed support, flood hazard, and access geometry. Building management decides damage/repair policy; logistics manages transported cargo; population systems decide evacuation. None of those domains must be embedded in the erosion solver.

## Validate migration rather than appearance

Check a protected bank, an erodible bank, a stratified bank, and an unsupported block. Confirm the removed volume matches transferred dry mass and water, and that new space does not create water. Compare movement at smaller timesteps and a finer local representation.

Test a cutoff with separate residual pools and a breach that redirects upstream storage. Observe mesh alignment bias and migration quantization. A visually sinuous river is not evidence that bank processes, conservation, or hydraulic connectivity are correct. Leave migration disabled if a simpler changing-water model already satisfies the game.
