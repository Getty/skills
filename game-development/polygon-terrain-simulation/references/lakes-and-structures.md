# Lakes, subcell storage and hydraulic structures

## Contents

- [Storage geometry](#storage-geometry)
- [Connectivity and hydraulic faces](#connectivity-and-hydraulic-faces)
- [Reservoir and outlet models](#reservoir-and-outlet-models)
- [Terrain edits beneath water](#terrain-edits-beneath-water)
- [Boundaries and inactive regions](#boundaries-and-inactive-regions)
- [Validation scenarios](#validation-scenarios)
- [Primary references](#primary-references)

## Storage geometry

A computational polygon may contain finer terrain. Preserve enough information to calculate storage and connectivity without making every rendering triangle an independently simulated cell. HEC-RAS provides a precedent: cell stage-volume relations and face hydraulic tables are derived from underlying terrain. This supports a useful design direction; it does not imply that arbitrarily coarse cells resolve every channel or barrier.

### Formula card: stage-volume relation

For a hydraulically connected region with approximately level water surface,

\[
V_i(\eta)=\int_{\Omega_i}[\eta-z(x,y)]_+\,dA,
\qquad
A_{w,i}(\eta)=\frac{dV_i}{d\eta}.
\]

Use elevation \(\eta,z\) [m], plan area [m²], volume [m³], and wetted plan area \(A_w\) [m²]. The derivative is understood one-sided at terrain breakpoints. Invert a monotone storage curve to find stage from persistent volume. A level surface assumption is appropriate only when unresolved internal gradients are acceptable.

For flat weighted subpatches,

\[
V(\eta)=\sum_k a_k[\eta-z_k]_+.
\]

Sort unique elevations, accumulate wet areas and their elevation-weighted sums, then solve each linear interval exactly. For wet patches \(W\), the candidate stage is

\[
\eta=\frac{V+\sum_{k\in W}a_kz_k}{\sum_{k\in W}a_k}.
\]

Accept it only if it lies in that interval. For triangulated sloping terrain, integrate the clipped submerged triangles or build an accurate monotone table; flat-point sampling is an approximation to that geometry. Reject negative areas, nonfinite values and impossible table orderings.

**Original example:** use 30 m² at elevation 0 m and 70 m² at elevation 1 m. Stage 0.5 m stores 15 m³; stage 1.5 m stores 80 m³. Therefore the latter volume inverts to 1.5 m, with wet area 100 m². Averaging terrain elevation to 0.7 m would incorrectly flood the entire cell at tiny volumes.

**Dry convention:** zero volume does not uniquely determine a water surface below the lowest bed. Return `dry=true` and a conventional stage equal to the minimum bed, without implying a physical sheet of water. Never derive an external driving head from an arbitrary “dry level” without a wet/dry rule.

### Avoid false internal connectivity

Two pits separated by a ridge cannot exchange water below that ridge merely because they share one polygon. Choose one of these representations:

- Refine the computational mesh along the divider.
- Keep multiple storage compartments inside the cell, joined by a spill threshold.
- Aggregate the pits only after establishing that their separate behavior is irrelevant at the game's scale.

A single area-elevation histogram loses spatial connectivity. Store spill topology as well when multiple basins matter. A fine visual heightmap cannot repair a solver that has already merged disconnected stores.

## Connectivity and hydraulic faces

Represent ordinary faces and special hydraulic connections explicitly. Useful fields include owner/neighbor IDs, physical face length, normal, crest profile, wetted cross-section versus stage, roughness, blocked fraction, structure state and geometry version. A culvert may connect compartments that are not direct terrain neighbors.

Distinguish plan wetted area [m²] from flow cross-section [m²]. They share dimensions but have different meanings. Derive face cross-section by integrating water depth along the physical opening; multiplying plan area by velocity gives the wrong discharge.

### Formula card: simplified open-face cross-section

For a face coordinate \(s\) [m] and bed/crest profile \(z_f(s)\), a geometric cross-section at stage \(\eta\) is

\[
A_c(\eta)=\int_f[\eta-z_f(s)]_+\,ds.
\]

This is only a geometry function. Selecting upstream/downstream stage, reconstructing the water surface and choosing a flux law remain solver decisions. A face with varying crest may need subdivisions or a more detailed conveyance calculation.

**Example:** a 4 m wide rectangular opening whose bed is at 2 m has 1.2 m² of submerged cross-section at stage 2.3 m. An adjacent 6 m barrier with crest 3 m contributes none at that stage. Do not treat the entire 10 m face as open.

Align simulation faces or embedded structure constraints with hydraulically important roads, embankments and narrow passages. A walkable road can obstruct water. A culvert can pass water without creating a navigation connection. Store navigation and water connectivity separately.

## Reservoir and outlet models

### Formula card: level-pool reservoir balance

\[
\frac{dV}{dt}=I(t)+rA_r-eA_w(\eta)-Q_{out}(\eta,\eta_d,t)-U(t).
\]

All terms are volume rates [m³/s]; \(r,e\) are depth rates [m/s], \(U\) withdrawal, \(\eta_d\) downstream stage. This model assumes a sufficiently uniform reservoir level. Solve it with the storage curve, not with a constant area unless that is the declared geometry.

**Example:** net input 0.02 m³/s for 600 s adds 12 m³ to a sealed reservoir. If its wetted area throughout that interval is 40 m², stage rises 0.3 m. If the expanding shoreline changes area, invert the curve instead of using that constant-area result.

Use event-aware substeps around crest elevations, gate changes and emptying. An implicit or averaged-inflow method may improve stability, but check conservation and the physical validity of its solution.

### Formula card: free weir discharge

A common free-overflow form is

\[
Q=C_w b H_u^{3/2},\qquad H_u=[E_u-z_c]_+.
\]

Use crest length \(b\) [m], upstream energy elevation \(E_u\) and crest \(z_c\) [m]. With this convention \(C_w\) has units m^(1/2)/s; it is not dimensionless. A convention that exposes \(\sqrt{g}\) has a different coefficient. For slow reservoirs, stage may approximate energy elevation; a fast approach requires velocity head.

**Original synthetic example:** \(C_w=1.7\) m^(1/2)/s, \(b=2\) m and \(H_u=0.25\) m give 0.425 m³/s. This calculation illustrates units and sensitivity, not a universal spillway coefficient.

This free-flow equation does not cover submerged outlets, arbitrary bidirectional flow or every crest shape. Supply a tailwater/submergence treatment and regime selection from the adopted model. Avoid switching formulas discontinuously at nearly equal stages. Limit actual discharge by available volume without claiming the resulting heavily limited step is accurate.

### Culverts, pipes and pumps

Treat a culvert as an opening with its own invert, size, length, roughness, entrance/exit losses and possible blockage. Depending on head and geometry it may have inlet control, outlet control, partly full flow or pressure flow. A single universal “culvert coefficient” omits those distinctions. A game can use a calibrated rating table \(Q(\eta_u,\eta_d,\text{opening})\), provided its assumed operating range is documented.

For a fully submerged short orifice, the familiar restricted form is

\[
Q=C_dA_o\sqrt{2g\,\Delta H},
\]

with dimensionless \(C_d\), opening area \(A_o\) [m²] and positive upstream-minus-downstream head [m]. This is an optional conceptual reference, not a replacement for a long-culvert model. Apply orientation separately and use the appropriate head definition for each regime.

A pump requests transfer subject to intake submergence, power/control logic and available water. Return the actual transferred volume to other domains. Buildings or logistics should not assume that a nearby “water” label guarantees an unlimited resource.

## Terrain edits beneath water

Use the following transaction for excavation, filling, sediment deposition or bank collapse:

1. Snapshot authoritative water volume and the affected material quantities.
2. Apply the authorized material movement and new geometry.
3. Rebuild affected storage curves, compartments and face geometry.
4. Recover stage from the preserved water volume.
5. Route overflow or intentional pumping through accounted transfers.
6. Publish changed hazard/buildability data after dependent state is consistent.

**Original example:** the 30/70 m² cell above contains 80 m³. Raise its low patch from 0 to 0.5 m while keeping water in the cell. The new stage solves \(30(\eta-0.5)+70(\eta-1)=80\), yielding 1.65 m. It rises by 0.15 m; the water does not disappear into the fill. Conversely, excavating storage capacity does not automatically create water.

If fill physically occupies an entire compartment, transfer displaced water to connected recipients, an explicit temporary reservoir, or a declared boundary before removing that compartment. If connectivity changes, assign old water to the new compartments by actual overlap/physical occupancy; do not distribute it uniformly across separated pits without justification.

The example isolates the geometry update and excludes infiltration into newly placed fill. If dry porous fill can absorb water in the selected model, transfer an explicitly computed amount from surface water to its pore store and derive stage from the remaining surface volume. Preserve combined water, not an artificially fixed surface volume across that additional exchange. Choose instantaneous saturation or a finite infiltration rate deliberately.

For wet soil excavation, distinguish free surface water from pore water carried with the excavated material. The optional soil-water model determines how that pore water follows the material or drains. Account for each store once.

## Boundaries and inactive regions

Declare boundaries: closed wall, prescribed inflow, prescribed stage, rating relation or coupled neighboring region. Prescribed sea level allows water exchange; include that exchange in the ledger. A closed map is a different physical model.

An unloaded chunk should not become a wall or drain. Continue a compatible coarse reservoir representation or exchange boundary fluxes with a synchronized neighbor. Persist forcing time, actual boundary transfers and storage. When reactivating, reconstruct a state with the same stored volume and valid connectivity; do not merely paint the old water depth onto new geometry.

A small dam edit may affect a large upstream lake or distant downstream cells. Recompute based on hydraulic dependencies. Keep local render updates local, but do not use their radius as a bound on physical consequences.

## Validation scenarios

| Scenario | Expected result |
|---|---|
| Water below a sealed crest | No over-crest transfer |
| Culvert below a road crest | Culvert flow may occur before road overtopping |
| Equal stages on both sides | No head-driven exchange |
| Two pits below their internal sill | Independent storage |
| Partial cell flooding | Wet area follows geometry |
| Bed raised beneath pond | Water conserved; stage/overflow changes |
| Gate closes during a step | Event timing respected |
| Reservoir loads/unloads | No storage jump from visibility state |

Compare outlet curves, residuals and timestep-halving results. A beautiful shoreline is not evidence of a correct storage curve.

## Primary references

- [HEC-RAS: cell and face hydraulic property tables](https://www.hec.usace.army.mil/confluence/rasdocs/r2dum/6.4/development-of-a-2d-or-combined-1d-2d-model/creating-hydraulic-property-tables-for-2d-flow-areas) — subgrid storage and geometry precedent.
- [HEC-HMS: spillways](https://www.hec.usace.army.mil/confluence/hmsdocs/hmstrm/reservoir-modeling/reservoir-modeling-concepts-and-equations/spillways) — weir relations and tailwater treatment.
- [HEC-RAS: overflow gates](https://www.hec.usace.army.mil/confluence/rasdocs/ras1dtechref/6.6/modeling-gated-spillways-weirs-and-drop-structures/hydraulic-computations-through-gated-spillways/overflow-gates) — coefficient convention and gated overflow.
- [HEC-RAS hydraulic reference manual 6.6](https://www.hec.usace.army.mil/software/hec-ras/documentation/HEC-RAS_Hydraulic_Reference_Manual_v6.6.pdf) — culvert, gate and pressure-flow regimes.

The transaction policies, discretization examples and synthetic calculations are original engineering guidance for a game implementation.
