# Persistent earthworks and terrain operations

Model excavation, grading and filling as persistent changes to material and geometry. A visual displacement brush is sufficient only when the game intentionally has no quantity or hydraulic consequences.

## Contents

- [Define the target surface](#define-the-target-surface)
- [Compute cut and fill](#compute-cut-and-fill)
- [Excavate layers](#excavate-layers)
- [Execute bounded progress](#execute-bounded-progress)
- [Couple with water](#couple-with-water)
- [Commit and invalidate](#commit-and-invalidate)
- [Choose slope and support behavior](#choose-slope-and-support-behavior)

## Define the target surface

Store a spatial footprint and a target function, not only “flatten by 30%.” A planar foundation target can be

\[
z_t(x,y)=z_0+p_x(x-x_0)+p_y(y-y_0),
\]

where \(z_0\) and coordinates are metres and \(p_x,p_y\) are dimensionless grades. Horizontal grading uses zero grades; a drained pad can use a small intentional grade chosen by game design.

Define transitions to untouched ground. For blend weight \(w(x,y)\in[0,1]\),

\[
z_{\text{planned}}=(1-w)z_{\text{snapshot}}+wz_t.
\]

The weight describes the *planned surface* relative to a snapshot. Reapplying this expression to the continually changing current surface without a stored plan gives different semantics and can cause repeated edits after load.

Possible target tools:

| Tool | Geometric target | Additional constraints |
|---|---|---|
| Pad | Plane over footprint | Support, drainage, access, edge transition |
| Road | Profile along centerline + crossfall | Grade, width, bridges/cuts/fills |
| Trench/canal | Bottom profile and side slopes | Connectivity, outlet, seepage if modeled |
| Embankment/dam | Crest, width and side profiles | Hydraulic barrier and controlled outlets |
| Borrow pit | Excavation surface | Material layer availability and access |
| Restoration | Explicit replacement profile | Required materials and water consequences |

Hydraulic structures can be separate from earthwork geometry. A concrete wall may block flow without being a soil column; a culvert passes through an embankment without removing the whole barrier.

## Compute cut and fill

For affected area \(\Omega\):

\[
V_{\mathrm{cut}}=\int_\Omega\max(z_o-z_t,0)\,dA,\qquad
V_{\mathrm{fill}}=\int_\Omega\max(z_t-z_o,0)\,dA.
\]

Volumes are \(\mathrm{m^3}\), elevations metres. These are bulk geometric volumes, not dry material mass. Include only the footprint intersection and modeled transition zone.

For weighted samples or flat subpatches:

\[
V_{\mathrm{cut}}\approx\sum_k a_k\max(z_{o,k}-z_{t,k},0).
\]

Use a corresponding expression for fill. This is exact for piecewise constant patches; quantify sampling error for a continuous surface. A single sample per large polygon can miss a trench or hill within it.

**Original example:** three covered subareas are \(20,30,10\ \mathrm{m^2}\), with old elevations \(10.4,9.8,10.1\ \mathrm m\) and a target of \(10.0\ \mathrm m\). Cut is \(20(0.4)+10(0.1)=9\ \mathrm{m^3}\). Fill is \(30(0.2)=6\ \mathrm{m^3}\). The footprint covers \(60\ \mathrm{m^2}\); do not include uncovered parts of the parent cells.

### Select a balanced pad height

If grades are fixed and only \(z_0\) varies, search a monotonic material residual:

\[
R(z_0)=M_{\mathrm{usable\ cut}}(z_0)-M_{\mathrm{required\ fill}}(z_0).
\]

Bracket and bisect when the material rules make this residual monotonic. Report infeasible intervals from protected rock, unsuitable fill, foundation constraints or limited disposal. Do not call the area-weighted mean height a universal “balanced cut/fill” solution: it balances geometric volume only under matching area/footprint and equal-volume material assumptions.

The game may instead minimize a cost:

\[
C=\sum_m c_{\mathrm{cut},m}M_{\mathrm{cut},m}
+\sum_m c_{\mathrm{haul},m}M_{\mathrm{haul},m}d_m
+\sum_m c_{\mathrm{fill},m}M_{\mathrm{fill},m}+C_{\mathrm{support}}.
\]

Choose coefficient units deliberately (for example game currency/kg and currency/(kg·m)). This is a proposed game cost model, not a calibrated construction estimate.

## Excavate layers

Clip the excavation depth against every intersected layer, from top downward. Compute class-resolved dry mass from excavated bulk volume and the layer's state:

\[
M_m=\rho_{b,m}V_m=\rho_{s,m}(1-\phi_m)V_m.
\]

If layers are mixtures, transfer constituent masses and associated water rather than one ambiguous “soil” tag. Expose the next layer when a layer's mass reaches zero. Preserve geological base/bedrock semantics: eroding mobile cover is not the same operation as breaking rock.

**Original example:** a \(10\ \mathrm{m^2}\) patch loses \(0.2\ \mathrm m\) of synthetic topsoil at \(1400\ \mathrm{kg/m^3}\) and \(0.3\ \mathrm m\) of synthetic subsoil at \(1700\ \mathrm{kg/m^3}\). Outputs are \(2800\) and \(5100\ \mathrm{kg}\). If the topsoil is reserved for landscaping, only the \(5100\ \mathrm{kg}\) subsoil is available for generic fill. At placed dry density \(1800\ \mathrm{kg/m^3}\), it supplies \(2.8333\ \mathrm{m^3}\), not the entire \(5\ \mathrm{m^3}\) cut.

Layer thickness, porosity, density and mass are linked; use the authoritative-state rules in [layered materials](layered-materials.md).

## Execute bounded progress

Store at least:

- Operation ID, command ID, accepted plan and geometry/source revisions.
- Footprint, target and material specification.
- Already applied work and per-class mass transfers.
- Outstanding reservations, conflict policy and status.
- Hydraulic/structural prerequisites and any region lock.

Advance by actual feasible work. If a dry-material budget \(\Delta M\) is supplied, find the corresponding excavation depth through layers rather than lowering every vertex by an arbitrary equal percentage.

A simple uniform-progress construction can use

\[
z(p)=z_{\text{snapshot}}+p(z_{\text{target}}-z_{\text{snapshot}}),
\quad p\in[0,1].
\]

Apply only \(z(p_{\text{new}})-z(p_{\text{old}})\), and compute the associated incremental mass from layers. This is an optional geometric work distribution; it does not imply constant labor cost with \(p\), and it must resolve conflicts with intervening erosion or edits.

Define overlap behavior: reject, queue, combine into a new plan, or serialize by revision. Avoid order-dependent edits hidden by render smoothing.

## Couple with water

For each physical change:

1. Preserve current water stores before changing geometry.
2. Rebuild affected cell storage and face geometry.
3. Recompute stage from stored surface volume.
4. Release pore water exceeding changed soil capacity to a named destination.
5. Re-evaluate hydraulic exchange and boundaries.

Digging creates storage capacity; it does not spawn water. Raising a submerged bed increases water level for the same volume, until exchange or explicitly modeled displacement carries water elsewhere.

For saturated excavation, choose and document whether water is carried with excavated material, drains back into the pit, or is split by a drainage rule. Preserve the total across surface, soil, loads and exports.

If the game simplifies wet material to dry mass only, expose that approximation instead of pretending to conserve a pore-water state it never stores.

## Commit and invalidate

Validate a candidate state, commit material/water ownership and geometry together, then invalidate derived data. Appropriate dependencies include:

- Local terrain patches, normals, collision and vegetation placement.
- Soil capacity and exposed surface parameters.
- Storage curves, face profiles, channel and catchment connectivity.
- Building support and regional hazard queries.
- Navigation and access.

Only some dependencies are local. A raised stream barrier can alter upstream storage and downstream discharge far beyond the brush radius.

Publish a usable revision after the required render/collision/navigation updates or keep the work area unavailable until ready. Use a progress event for UI that does not incorrectly claim the new foundation is already safe to use.

## Choose slope and support behavior

Decide whether an over-steep edit:

- Is rejected by the placement rules.
- Automatically expands its cut/fill footprint to a selected slope.
- Requires a retaining structure.
- Is allowed and later fails through the chosen material model.

A geometric maximum grade is a game rule unless supported by a material/stability model. It is not the same as a measured angle of repose or a factor of safety.

Demolition removes the building object; earthwork remains until another operation changes it. If undo is supported, define whether it restores a snapshot (editor semantics) or performs inverse material movements (physical gameplay semantics). Do not mix the two silently.

### Source basis

The integrals and transactions above are original derivations and engineering patterns. Material-density relationships are grounded in [USDA NRCS bulk density guidance](https://www.nrcs.usda.gov/sites/default/files/2022-10/Soil%20Bulk%20Density%20Moisture%20Aeration.pdf). Storage-geometry separation is supported by [HEC-RAS hydraulic property tables](https://www.hec.usace.army.mil/confluence/rasdocs/r2dum/6.4/development-of-a-2d-or-combined-1d-2d-model/creating-hydraulic-property-tables-for-2d-flow-areas). Example values are synthetic.
