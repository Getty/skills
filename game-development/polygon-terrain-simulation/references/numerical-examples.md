# Numerical reference examples

## Contents

- [Scope and execution](#scope-and-execution)
- [API and units](#api-and-units)
- [Geometry and partial-footprint earthworks](#geometry-and-partial-footprint-earthworks)
- [Material mass and compaction](#material-mass-and-compaction)
- [Storage and terrain edits](#storage-and-terrain-edits)
- [Conservative face transfers](#conservative-face-transfers)
- [Pond crest example](#pond-crest-example)
- [Illustrative world snapshot audit](#illustrative-world-snapshot-audit)
- [Budgets and verification limits](#budgets-and-verification-limits)

## Scope and execution

Use the bundled Python kernels to check quantities, explain invariants, and build small regression fixtures. Treat them as educational building blocks. They do not implement a production hydraulic solver, infiltration model, mesh generator, sediment solver, or game engine adapter. They require Python 3.10 or later and only the standard library.

Run from the skill directory:

```bash
python3 scripts/reference_math.py demo
python3 scripts/test_reference_math.py
python3 scripts/audit_snapshot.py
python3 scripts/test_snapshot_audit.py
```

The demo reads `assets/numeric-fixtures.json` relative to the script, so it also works from another working directory. `--fixtures /absolute/path/example.json` accepts a replacement with the same documented structure. Output is JSON on stdout; the command does not modify world state or write a save file.

Treat every fixture value as `synthetic_illustrative_not_calibrated`. The fixture is an analytical teaching example, not measured soil data or an appropriate default for every game. Retain this provenance when copying values. The tests use known numerical answers, conservation, representation invariance, and invalid-input cases.

## API and units

| Function | Inputs | Result / responsibility |
|---|---|---|
| `polygon_metrics(vertices_m)` | Ordered planar `(x,y)` vertices in metres | Area, signed area, centroid and perimeter; basic simple-ring validation |
| `cut_fill(patches)` | `(overlap_area_m2, old_z_m, target_z_m)` | Separate cut/fill bulk volumes and signed net fill |
| `dry_mass_from_volume(volume, density, porosity)` | Bulk m³, particle kg/m³, dimensionless pore fraction | Dry solid kg, excluding water |
| `layer_state(mass, density, porosity, area)` | Dry kg, particle kg/m³, pore fraction, m² | Bulk m³, thickness m and pore capacity m³ |
| `compact_layer(...)` | Dry solids, old/new porosity, area, initial pore water | New geometry and explicit expelled water m³ |
| `stage_volume(patches, stage)` | `(area_m2, bed_z_m)` subpatches, water elevation m | Water volume m³ for one connected level water body |
| `stage_for_volume(patches, volume)` | Same subpatches, volume m³ | Piecewise-linear storage-curve inverse |
| `transfer_volumes(stores, proposals)` | Cell volumes m³; one signed proposed transfer per physical connection | Actual transfers, new nonnegative volumes, donor factors and residual |
| `crest_transfer_proposal(...)` | Two stages, crest, conductance m²/s, interval s | Signed proposed m³ for a simplified thresholded linear connection |
| `balance_residual(initial, final, imported, exported)` | All quantities in the same unit | Unexplained balance discrepancy in that unit |

Require finite numerical inputs, positive geometric areas and particle density, nonnegative stores, and \(0\leq\phi<1\). Elevations and signed transfers may be negative. Recheck domain constraints in the game adapter; these kernels do not validate a complete save schema.

## Geometry and partial-footprint earthworks

For an ordered simple polygon, the signed area is

\[
A_s=\frac12\sum_k(x_k y_{k+1}-x_{k+1}y_k).
\]

Reverse the ring to reverse the sign while retaining physical area \(|A_s|\). The kernel translates coordinates before computing shoelace sums to reduce cancellation in offset worlds. The rectangle \((0,0),(2,0),(2,1),(0,1)\) has area \(2\,\mathrm{m^2}\), centroid \((1,0.5)\,\mathrm m\), and perimeter \(6\,\mathrm m\).

The geometric checks are \(O(n^2)\) small-fixture checks using floating-point predicates. They do not certify a tessellation, shared-face consistency, orthogonality, or near-degenerate geometry. Use a robust geometry implementation and mesh diagnostics for production editing. A positive polygon area does not establish solver compatibility.

Approximate footprint quantities with actual overlap areas:

\[
V_{cut}=\sum_k a_k\max(z_{old,k}-z_{target,k},0),\qquad
V_{fill}=\sum_k a_k\max(z_{target,k}-z_{old,k},0).
\]

For \(20\,\mathrm{m^2}\) cut by \(0.5\,\mathrm m\) and \(5\,\mathrm{m^2}\) filled by \(0.5\,\mathrm m\), obtain \(10\,\mathrm{m^3}\) of cut and \(2.5\,\mathrm{m^3}\) of fill. These are different operations, even though their signed net is \(-7.5\,\mathrm{m^3}\). The overlap covers \(25\,\mathrm{m^2}\), which need not equal any cell's full area.

This is exact for piecewise-constant patches. Subdivide or integrate varying surfaces and layer interfaces; sampling one height per large polygon can miss a ditch or narrow ridge. The function does not decide which materials were removed. Perform layer intersections separately before converting volumes to dry mass.

## Material mass and compaction

For uniform particle density \(\rho_s\), dry solid mass \(M_s\), area \(A\), and porosity \(\phi\):

\[
V_b=\frac{M_s}{\rho_s(1-\phi)},\quad
d=\frac{V_b}{A},\quad V_p=\phi V_b.
\]

Use \(V_b\) for bulk material volume and \(V_p\) for pore capacity. Keep pore-water volume \(W\) distinct from both. In the fixture, \(M_s=159000\,\mathrm{kg}\), \(\rho_s=2650\,\mathrm{kg/m^3}\), \(A=100\,\mathrm{m^2}\), and \(\phi=0.40\) give \(V_b=100\,\mathrm{m^3}\), \(d=1\,\mathrm m\), and \(V_p=40\,\mathrm{m^3}\).

Change porosity to 0.25 without changing solids mass. Bulk volume becomes \(80\,\mathrm{m^3}\), thickness becomes \(0.8\,\mathrm m\), and pore capacity becomes \(20\,\mathrm{m^3}\). With \(30\,\mathrm{m^3}\) of initial pore water:

\[
W_{retained}=\min(W,V_{p,new})=20,\qquad
W_{expelled}=W-W_{retained}=10\,\mathrm{m^3}.
\]

Transfer that expelled water to surface/subsurface storage or an explicit exported-water ledger. Do not discard it. The kernel reports the transfer requirement but does not choose its destination or solve time-dependent consolidation. Unsaturated material with only \(10\,\mathrm{m^3}\) of water retains all of it in this simplified instantaneous geometry change.

Interpret 2650 kg/m³ only as a chosen fixture parameter. Particle density, bulk density and porosity depend on material and state; use measured or explicitly tuned values in a game. See [USDA NRCS bulk density, moisture and aeration](https://www.nrcs.usda.gov/sites/default/files/2022-10/Soil%20Bulk%20Density%20Moisture%20Aeration.pdf) for the physical distinctions. Material mixtures and effective density require constituent-volume accounting beyond this homogeneous example.

## Storage and terrain edits

For connected water with one stage \(\eta\), use flat terrain subpatches:

\[
V(\eta)=\sum_k a_k\max(\eta-z_k,0).
\]

The inverse walks sorted bed-elevation breakpoints, adding wet area at each level. No iterative root finder is needed for this piecewise-linear representation. At zero volume, choose the minimum bed elevation as a dry-state convention; no physically observable free surface exists in an empty reservoir.

The fixture has \(60\,\mathrm{m^2}\) at elevation 0 and \(40\,\mathrm{m^2}\) at elevation 1 m. At \(\eta=1.5\,\mathrm m\):

\[
V=60(1.5)+40(0.5)=110\,\mathrm{m^3}.
\]

Raise the lower patch to 0.5 m while retaining the same water volume. The new stage is 1.8 m because \(60(1.8-0.5)+40(1.8-1)=110\). Holding the old stage at 1.5 m would leave only \(80\,\mathrm{m^3}\), silently deleting \(30\,\mathrm{m^3}\).

This instantaneous example excludes overflow and infiltration into new material during the edit. In a runtime operation, update the storage curve, derive the new stage from retained volume, and solve or explicitly transfer resulting displacement. If a porous fill receives water, debit the surface store and credit its pore store before deriving the resulting stage; preserve their combined total. Give disconnected hollows separate compartments; otherwise this equation creates instantaneous unphysical communication. The function has no automatic outlet and no maximum storage elevation.

For the larger architectural idea of storage curves and face geometry from detailed terrain, consult [USACE hydraulic property tables for 2D flow areas](https://www.hec.usace.army.mil/confluence/rasdocs/r2dum/6.4/development-of-a-2d-or-combined-1d-2d-model/creating-hydraulic-property-tables-for-2d-flow-areas). The flat-patch kernel is a deliberately smaller model.

## Conservative face transfers

Represent a proposed transfer by `EdgeProposal(edge_id, a, b, requested_m3)`. Positive values move water from `a` to `b`; negative values reverse direction. A proposal is an integrated volume for the current interval, not a discharge. Multiply a discharge in m³/s by its interval once before calling the function.

For each donor, collect all outgoing requested volumes \(T_e\) from the same initial state:

\[
\alpha_i=\min\left(1,\frac{V_i}{\sum_{e\in out(i)}|T_e|}\right).
\]

Use factor 1 when total demand is zero. Apply the same actual edge volume with opposite signs at its endpoints. Limit transfers against the remaining donor budget before applying them, including any final floating-point rounding overshoot. Never solve a negative final store by silently replacing it with zero.

In the fixture, A starts with 5 m³ and proposes 4 m³ to B and 6 m³ to C. Its common factor is 0.5, so the actual transfers are 2 and 3 m³. B starts dry and proposes 7 m³ to C; its actual transfer is zero. It cannot spend its incoming 2 m³ in this same explicit step. Final stores are A=0, B=2, C=13 m³; the initial and final totals are both 15 m³.

The routine allows several distinct physical connections between the same cell pair, such as separate pipes. Give each a unique ID. Do not duplicate the same physical face under two IDs. Boundary sources, infiltration, pumps to external domains and evaporation require explicit source/receiver accounting outside this closed-domain helper.

Conservation and positivity do not prove a valid hydraulic solution. The routine accepts any proposal; choose its physics, geometry assumptions and stable timestep separately. Edge-ID sorting makes allocation order stable for these examples, but this is not a claim of bit-identical simulation across platforms.

## Pond crest example

Use this teaching connection only to illustrate a threshold and a water ledger:

\[
Q=C\big([\eta_a-z_c]_+-[\eta_b-z_c]_+\big),\qquad T=Q\Delta t.
\]

Here \(C\) is conductance in m²/s, \(z_c\) is crest elevation in m, and \([x]_+=\max(x,0)\). This is a thresholded linear reservoir rule, **not a weir equation, culvert design relation, or shallow-water solver**. For a physical structure use a suitable hydraulic closure and inlet/outlet conditions.

Two flat ponds each have area 10 m². The upstream pond initially contains 9 m³ and has stage 0.9 m; the downstream pond is dry. A crest at 1 m blocks the connection. Rain adds 3 m³ upstream, raising its stage to 1.2 m. With \(C=2\,\mathrm{m^2/s}\) and \(\Delta t=1\,\mathrm s\), the proposed and available transfer is 0.4 m³. Final volumes are 11.6 and 0.4 m³, totaling 12 m³: initial water 9 plus rainfall 3.

For two fully active flat reservoirs without threshold changes, the head difference follows an explicit factor

\[
1-\Delta t C(1/A_a+1/A_b).
\]

Keeping this factor between 0 and 1 gives monotone relaxation for that restricted pair. A network, wet/dry switching and another flux law need their own stability analysis. Donor limiting alone will not prevent oscillation or produce timestep-converged results.

## Illustrative world snapshot audit

Use `scripts/audit_snapshot.py` to audit `assets/world-state-example.json` against `assets/material-examples.json`. Both are synthetic fixtures. The script loads its default files relative to its own location; it prints a JSON report without modifying them. To inspect an adapted copy of the same bounded format:

```bash
python3 scripts/audit_snapshot.py /absolute/path/world.json --materials /absolute/path/materials.json
```

The optional `--materials` argument overrides the snapshot's local `materials_file` filename. Import `audit_snapshot(snapshot, materials)` to audit parsed dictionaries. A valid audit returns derived quantities; invalid or unsupported input raises `AuditError`. The CLI writes an error JSON to stderr and exits with status 1 on rejection.

**Accepted geometry is deliberately narrow:** conforming axis-aligned rectangular cells with centroid samples, filling one rectangular domain with closed-wall boundaries. Shared vertices must have exactly matching stored coordinates. Cells may have unequal dimensions if their shared edges still conform. The auditor rejects nonrectangular cells, hanging-node interfaces, interior holes, overlaps, and open boundaries. It does not perform approximate vertex snapping or certify general Voronoi/barycentric meshes. Production geometry needs robust predicates and the chosen solver's mesh-quality requirements.

The checks cover:

- Unique cell, layer, face, and material IDs; finite values and nonnegative stores.
- Polygon areas against declared areas, centroid samples, overlapping rectangle interiors, and total rectangular domain coverage.
- Every actual cell edge represented exactly once by an internal or boundary record; internal ownership matches geometric neighbors.
- Actual face lengths, unit normals, orthogonal center distances and exterior boundary normals.
- Known layer/suspended-material identities, dry mass, derived thickness, pore capacity, and pore-water bounds.
- Closed-domain totals and the fixture's supplied expected results.
- One surface-transfer step using the stated thresholded linear rule, reporting proposed rates, actual donor-limited volumes, and the water-budget residual.

The four cells each occupy 100 m² and have one 159,000 kg layer of thickness 1 m, pore capacity 40 m³, and stored pore water 10 m³. Their surface elevations are 9, 9.5, 10 and 10.5 m. Surface-water stores are 100, 50, 0 and 0 m³. The first two stages are 10 m; the dry cells use their bed elevations as the dry-stage convention. Each face's thresholded head difference is zero, including the higher dry cell behind its crest.

Expected audit totals are:

| Quantity | Result |
|---|---:|
| Domain area | 400 m² |
| Cells / internal faces / boundary faces | 4 / 4 / 8 |
| Dry loose-layer mass | 636,000 kg |
| Suspended sediment | 0 kg |
| Surface water | 150 m³ |
| Pore water | 40 m³ |
| Combined modeled water | 190 m³ |
| All internal flow rates | 0 m³/s |
| Maximum water-store change after 1 s | 0 m³ |

Keep `unmodeled_substrate` as an explicitly allowed fixed-bedrock placeholder. Bedrock mass is excluded from this example's solids total; the audit does not invent a geological base depth. Other material references must resolve to the catalog. The unused catalog's conductivity and infiltration values are checked for basic numerical validity, not calibrated or exercised as physical processes.

The auditor accepts only the `surface_transfer` process and no active operations. It does not implement infiltration, groundwater, erosion, momentum, structure hydraulics, remeshing, construction transactions, or save/load continuation. The independent `domain-transfer-example.json` contract is not a transfer executed by this audit. Remove `expected_checks` from an adapted nonequilibrium snapshot to calculate its quantities without asserting the original fixture's equilibrium; geometry and state checks remain active.

The accompanying 20 tests check the valid fixture, ring/face endpoint reversal, a nonequilibrium conservative step, and malformed cases including false areas, overlapping cells, missing/duplicate faces, wrong neighbors/normals/distances, unknown materials, excess pore water, invalid texture fractions, negative/nonfinite stores and unsupported models. These complement the 30 reference-math tests. Default tolerances are absolute \(10^{-9}\) and relative \(10^{-12}\) in each compared quantity's stated unit; adapt numerical tolerances consciously for other scales.

## Budgets and verification limits

Track the residual

\[
\epsilon=\text{final}-\text{initial}-\text{imported}+\text{exported}.
\]

Set absolute and relative tolerances from world scale and numerical precision. Investigate systematic drift; do not relabel it as a source or hide it by renormalizing totals. For solids, include terrain layers, mobile sediment, stockpiles, cargo and explicit exports in the selected system boundary. An internal transfer must appear once as a debit and once as a credit.

The tests cover polygon orientation/translation, partial-area partitioning, material and pore-water accounting, storage breakpoints/inversion, terrain edits, common donor limiting, input order and edge orientation, dry donors, invalid/nonfinite data, a level lake under the teaching rule, and rainfall balance. Random closed transfers use a fixed seed and assert positivity and conservation.

These checks validate the supplied kernels. They do not validate an engine integration, mesh-wide momentum balance, sediment transport law, aquifer model, save/load replay, performance target or published hydraulic benchmark. Add those tests only when implementing the corresponding optional capability.
