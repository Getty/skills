# Formula conventions and navigation

Use this as an index. Read each linked formula in its full context before implementing it. The references state assumptions, worked examples and limits; this index is not an independent solver specification.

## Conventions

Use metres, seconds, kilograms, radians and a fixed elevation datum unless the game deliberately chooses another consistent system. Record conversions at module boundaries.

| Symbol | Meaning | SI dimension |
|---|---|---|
| \(A_i\) | Cell plan area | m² |
| \(a_k\) | Subpatch/overlap area | m² |
| \(L_f\) | Face width/length | m |
| \(d_{ij}\) | Point separation under the stated geometry | m |
| \(z\) | Ground/bed elevation | m |
| \(h\) | Water depth | m |
| \(\eta\) | Free-surface elevation | m |
| \(V,W\) | Surface/soil water volume | m³ |
| \(Q_f\) | Volumetric water discharge | m³/s |
| \(q_f\) | Depth-integrated flux per width | m²/s |
| \(\mathbf q_D\) | Darcy flux | m/s |
| \(M\) | Dry solid mass | kg |
| \(F_f\) | Sediment mass flux | kg/s |
| \(E_m,D_m\) | Erosion/deposition mass per area per time | kg/(m²·s) |
| \(\rho_s,\rho_b\) | Particle / dry bulk density | kg/m³ |
| \(\phi\) | Porosity | 1 |
| \(\theta\) | Volumetric soil water content | 1 |
| \(\varphi'\) | Effective friction angle | rad |
| \(K\) | Hydraulic conductivity in groundwater context | m/s |
| \(k\) | Intrinsic permeability | m² |
| \(n_M\) | SI Manning roughness | s/m^(1/3) |
| \(D\) | Linear hillslope diffusivity | m²/s |

Symbols are local to an equation. The \(n\) exponent in stream power is unrelated to Manning roughness. The \(F\) cumulative infiltration depth in Green-Ampt is unrelated to sediment mass flux. Prefer explicit field names in code.

## Formula index

| Question | Equation family | Full reference |
|---|---|---|
| How much area or cut/fill does a footprint cover? | Polygon integration and overlap quadrature | [Mesh and fields](mesh-and-fields.md), [terrain operations](terrain-operations.md) |
| Does a link gradient represent a face-normal derivative? | Orthogonality and reconstruction | [Mesh and fields](mesh-and-fields.md) |
| How much layer thickness follows from dry mass? | \(d=M/[\rho_s(1-\phi)A]\) | [Layered materials](layered-materials.md) |
| How much pore water is displaced by compaction? | Old/new pore-capacity comparison | [Layered materials](layered-materials.md) |
| Where does water go? | Shared-face volume continuity | [Surface water](surface-water.md) |
| How does volume determine level? | \(V(\eta)=\int[\eta-z]_+dA\) | [Lakes and structures](lakes-and-structures.md) |
| How much overflows a barrier? | Reservoir, weir, gate/culvert model selection | [Lakes and structures](lakes-and-structures.md) |
| How much infiltrates or drains? | Capacity/supply/storage bounds; optional Green-Ampt/Horton | [Soil water](soil-water-and-groundwater.md) |
| How does groundwater move? | Darcy law and optional shallow aquifer storage | [Soil water](soil-water-and-groundwater.md) |
| How does sediment change ground? | Solid continuity, Exner and finite availability | [Erosion and sediment](erosion-and-sediment.md) |
| How does a river move sideways? | Bank erosion/failure and migration models | [Channel migration](channel-migration.md) |
| How do hillslopes relax? | Diffusive flux, threshold alternatives and inventory limits | [Slopes and vegetation](slopes-and-vegetation.md) |
| How fast may a process step? | Scheme-specific stability and coupling accuracy | [Surface water](surface-water.md), [slopes](slopes-and-vegetation.md), [runtime](runtime-and-coupling.md) |
| How do we detect lost quantities? | Residual ledger | [Validation](validation-and-debugging.md) |

## Required formula card

When adding a new model, include:

1. **Purpose:** which observable behavior it supplies.
2. **Equation and variables:** state versus parameters, signs and units.
3. **Assumptions:** geometry, regime, material, scale and boundary conditions.
4. **Discretization:** field locations, shared fluxes, gradients and coupling order.
5. **Stability and positivity:** scheme-specific timestep and finite stores.
6. **Original worked example:** inputs, expected number and calculation.
7. **Failure cases:** where the approximation stops being adequate.
8. **Primary source and provenance:** distinguish quoted model, derivation and game closure.

Do not copy a printed equation without checking dimensional consistency. Authoritative documentation can contain typographical errors. Reconcile a suspected error against the derivation and implementation before using it.

## Dimensional checks

- \(Q\Delta t\) is a volume; \(qL\Delta t\) is also a volume.
- \(rA\Delta t\) converts a depth rate into water volume.
- \(\rho_s(1-\phi)\Delta z A\) is dry mass under the stated constant-density/porosity assumptions.
- A sediment concentration \(C\ [\mathrm{kg/m^3}]\) times actual water transfer \(\Delta V\) is a transported mass, bounded by available sediment.
- \(KA_c\Delta H/d\) is volumetric Darcy flow when \(A_c\) is the appropriate cross section.
- A coefficient with units fitted for years cannot be inserted into a seconds-based equation unchanged.

For SI area-based stream power \(E=K_AA^mS^n\) with erosion speed \(E\ [\mathrm{m/s}]\), \([K_A]=\mathrm{m^{1-2m}/s}\). For discharge-based \(E=K_QQ^mS^n\), \([K_Q]=\mathrm{m^{1-3m}s^{m-1}}\). Equal numerical coefficients do not imply equal models.

## Ledger residual

For any conserved quantity \(X\):

\[
\epsilon_X=X_{\mathrm{final}}-X_{\mathrm{initial}}
-X_{\mathrm{imported}}+X_{\mathrm{exported}}.
\]

Internal transfers cancel. State the scope: surface-only water treats infiltration as export, while total surface-plus-soil water treats it as internal. Include all stores in the chosen scope exactly once.

Use an acceptance scale such as

\[
|\epsilon_X|\le\epsilon_{\mathrm{abs}}+
\epsilon_{\mathrm{rel}}\max(X_{\mathrm{initial}},X_{\mathrm{final}},
X_{\mathrm{imported}},X_{\mathrm{exported}}).
\]

Choose tolerances from units, precision and operation counts. Do not loosen them until a visible leak disappears.
