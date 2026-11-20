# Layered materials and soil state

## Contents

- [Choose the state you need](#choose-the-state-you-need)
- [Keep material meanings separate](#keep-material-meanings-separate)
- [Derive geometry from conserved quantities](#derive-geometry-from-conserved-quantities)
- [Mix constituents consistently](#mix-constituents-consistently)
- [Compact without losing water](#compact-without-losing-water)
- [Excavate and deposit by layer](#excavate-and-deposit-by-layer)
- [Preserve useful detail](#preserve-useful-detail)
- [Validate and extend](#validate-and-extend)

## Choose the state you need

Start with a bedrock surface and an ordered stack of loose layers wherever excavation, erosion, filling, or changing permeability matters. Derive the ground surface from the bedrock elevation and layer thicknesses. Keep a homogeneous material column for games that do not expose stratigraphy. Add grain classes, chemistry, soil horizons, or consolidation only for a gameplay requirement.

Use this candidate state, adapting field names to the project:

| Quantity | Suggested authority | Reason |
|---|---|---|
| Cell/patch footprint | Mesh geometry | Defines the area on which column amounts apply |
| Bedrock top and lithology | Persistent terrain | Distinguishes rock from mobile cover |
| Dry mass per constituent | Persistent layer amounts, kg | Supports conservation through excavation and mixing |
| Porosity or placement density | Persistent material state | Determines current bulk volume |
| Pore-water volume | Persistent water store, m³ | Supports saturation and displacement |
| Thickness and bulk density | Derived values | Avoids independent quantities contradicting mass |
| Surface cover | Separate cover state | Grass, paving, litter, and material are different concepts |
| Strength/conductivity parameters | Material law plus state | Allows saturation and compaction effects where modeled |

An alternative thickness-authoritative design is legitimate if it derives mass consistently and records every conversion. Do not independently edit mass, thickness, density, and porosity without an explicit reconciliation rule.

Landlab's [Lithology/LithoLayers example](https://landlab.csdms.io/tutorials/lithology/lithology_and_litholayers.html) provides a useful precedent for exposing material properties as overlying layers disappear. Treat it as an architectural reference; do not assume its storage layout or every component is suitable for the game's polygon mesh.

## Keep material meanings separate

Keep soil texture, lithology, biome, surface cover, and resource identity separate. A sandy surface can cover clay; vegetation can grow over an imported fill; the same geological material can be fractured or intact.

Distinguish porosity, hydraulic conductivity, mechanical strength, and erodibility. Pore volume alone does not describe how connected pores transmit water. A soil's resistance to hydraulic scour is also different from its resistance to shear failure. Give parameters descriptive names and units instead of a universal `hardness` scalar that silently controls every process.

Declare whether a material amount is dry solids, total wet mass, solid-grain volume, or bulk volume including pores. Use dry mass as a convenient exchange quantity between terrain and logistics. If the game transports wet soil, transfer its water explicitly as a second amount.

The [USDA NRCS bulk-density guide](https://www.nrcs.usda.gov/sites/default/files/2022-10/Soil%20Bulk%20Density%20Moisture%20Aeration.pdf) explains the relationship between compaction, bulk density, pore space, and water storage. Its illustrative mineral density is not a universal constant for peat, mixed fills, or every rock.

## Derive geometry from conserved quantities

**Purpose:** convert a uniform layer's dry mass into thickness and storage.

For area \(A\), thickness \(H\), particle density \(\rho_s\), dry mass \(M_s\), and porosity \(\phi\):

\[
V_s=\frac{M_s}{\rho_s},\qquad
V_b=\frac{V_s}{1-\phi},\qquad
H=\frac{M_s}{\rho_s(1-\phi)A},
\]

\[
\rho_b=\frac{M_s}{AH}=\rho_s(1-\phi),\qquad
V_p=\phi AH=V_b-V_s.
\]

Use kg, m, m², m³, and kg/m³; \(\phi\) is dimensionless. These are volume-accounting identities for the stated uniform representation, not constitutive laws predicting porosity. Require \(A>0\), \(\rho_s>0\), \(M_s\ge0\), and \(0\le\phi<1\). Represent an absent layer explicitly instead of assigning it an arbitrary nonzero density or thickness.

**Original synthetic example:** let \(A=100\,\mathrm{m^2}\), \(M_s=159{,}000\,\mathrm{kg}\), \(\rho_s=2650\,\mathrm{kg/m^3}\), and \(\phi=0.40\). Then solid volume is 60 m³, bulk volume 100 m³, thickness 1 m, dry bulk density 1590 kg/m³, and pore volume 40 m³. These values illustrate arithmetic; they are not a recommended soil preset.

If pore water occupies \(W\) m³, volumetric water content is \(\theta=W/V_b\), and saturation is \(S_w=W/V_p\) when \(V_p>0\). Require \(0\le W\le V_p\) for this incompressible pore-storage model. A fully saturated store need not make all its water drainable or plant-available. Add retention and specific-yield concepts only when needed.

## Mix constituents consistently

For constituent masses \(M_k\) and particle densities \(\rho_{s,k}\), assume additive solid volumes:

\[
V_s=\sum_k\frac{M_k}{\rho_{s,k}},\qquad
\rho_{s,\mathrm{mix}}=\frac{\sum_kM_k}{V_s}.
\]

Equivalently, with mass fractions \(f_k\), \(1/\rho_{s,\mathrm{mix}}=\sum_k f_k/\rho_{s,k}\). An arithmetic average of densities is generally wrong when weights are mass fractions. Use \(V_b=V_s/(1-\phi_{\mathrm{mix}})\), with the mixture's porosity supplied by a placement or material rule. Packing, conductivity, and cohesion do not follow automatically from this density identity.

**Original synthetic example:** mix 1000 kg of a 2500 kg/m³ constituent with 1000 kg of a 2000 kg/m³ constituent. Their solid volumes total 0.9 m³, so effective particle density is approximately 2222.22 kg/m³. At porosity 0.40, bulk volume is 1.5 m³. Averaging the two densities to 2250 kg/m³ would not preserve the specified solid volume.

Do not preserve both every old layer's bulk volume and a new arbitrary mixture porosity. Choose the physical or game rule for repacking, calculate the new volume, and account for affected pore water. Keep grain-size fractions and chemical composition as different dimensions if both matter.

## Compact without losing water

**Purpose:** change packing while preserving solids. At unchanged constituent masses, decrease porosity according to a chosen compaction law and recompute geometry. The accounting does not itself predict how machinery, time, stress, or moisture changes porosity.

For the single-material example above, changing \(\phi\) from 0.40 to 0.30 gives:

\[
V_b'=60/0.70=85.714286\,\mathrm{m^3},\quad
H'=0.857143\,\mathrm m,\quad
V_p'=25.714286\,\mathrm{m^3}.
\]

If the initial layer holds 35 m³ of water, at least 9.285714 m³ must leave the layer under this simplified incompressible model. Transfer it to an allowed surface, drainage, neighboring, or exported-water store; then update the water balance. If no route exists, reject/defer that compaction or use a model that represents pressure and drainage delay. Instant displacement is a game approximation, not a consolidation solver.

Do not interpret lower porosity as an automatic numerical value for conductivity. Choose and document an empirical or mechanistic relation, or preserve conductivity independently until the game needs that coupling.

## Excavate and deposit by layer

Intersect the work footprint with the simulation support. Remove material from the exposed layer downwards, splitting a layer when the cut ends within it. For each removed volume, use that layer's current density to determine dry mass and record any accompanying pore water.

**Original synthetic example:** excavate a 20 m² patch to depth 0.50 m. Its upper 0.20 m has dry bulk density 1200 kg/m³; the next material has density 1600 kg/m³. Remove 4 m³ / 4800 kg from the upper layer and 6 m³ / 9600 kg from the lower layer. The excavated dry mass is 14,400 kg. Placing it at 1500 kg/m³ occupies 9.6 m³, even though the excavation occupied 10 m³.

If the footprint covers only part of a polygon, do not remove that thickness from the entire cell. Preserve a subpatch representation, refine locally, or accept and disclose the coarse spatial approximation. An area-weighted amount alone does not encode the new pit's shape or drainage connection.

Give deposited material an explicit identity and placement state. Merge adjacent layers only when their required identities and state are compatible. A stockpile may be represented geometrically by terrain and administratively by logistics, but assign one authoritative owner to its material amount to avoid counting it twice.

## Preserve useful detail

Use a short active-layer stack for frequently changing surface deposits and a compressed deeper stratigraphy if memory requires it. Define merge tolerances in physical units and preserve total constituent mass and water across merges. Retain interfaces that control excavation cost, impermeable barriers, resources, or slope failure even if visually thin.

Treat bedrock as finite where resource exhaustion matters. An inexhaustible basal material is an explicit boundary assumption, not an accidental consequence of a missing bottom layer. Weathering and rock excavation transfer material out of that store; they do not invent loose sediment.

A column model supports open pits and surface cuts. It cannot represent a tunnel beneath intact overlying terrain or an overhang without additional geometry. Use local volumetric structures or separate subsurface domains when those features are needed; do not force the whole world into voxels solely for a basement.

## Validate and extend

Check dry mass by constituent, pore-water totals, positive geometry, and exposed material after each operation. Test excavation across an interface, emptying the final loose layer, redepositing at a different porosity, mixing different particle densities, and compaction of a nearly saturated layer.

Extend only for a named behavior: organic matter for fertility/decay, grain classes for sorting, consolidation for delayed settlement, or chemistry for contamination. Store parameter provenance, valid units, chosen process timescale, and whether a value is synthetic, calibrated, or measured. A material name alone is insufficient evidence for a numerical constant.
