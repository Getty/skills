# Initialization and generation

Use generation to create the initial state. Use explicit state evolution for subsequent changes. Preserve authored and player changes across generator upgrades.

## Contents

- [Evaluate the Red Blob approach](#evaluate-the-red-blob-approach)
- [Choose an initialization method](#choose-an-initialization-method)
- [Use coherent noise deliberately](#use-coherent-noise-deliberately)
- [Construct a consistent state](#construct-a-consistent-state)
- [Treat drainage preprocessing carefully](#treat-drainage-preprocessing-carefully)
- [Separate permanent state from disposable detail](#separate-permanent-state-from-disposable-detail)

## Evaluate the Red Blob approach

[Polygon Map Generation](https://theory.stanford.edu/~amitp/game-programming/polygon-map-generation/) is useful for graph connectivity, island layout and readable semantic regions. [Terrain from Noise](https://www.redblobgames.com/maps/terrain-from-noise/) offers controllable height and climate fields. Treat those as initialization/design techniques; add material ownership, physical storage, time and operation semantics for a persistent world.

Do not choose “Voronoi or noise” as though they are competing solutions. Voronoi describes a spatial partition; noise produces a field that can be sampled on many partitions. A polygon world can use noise, artist stamps, imported data and erosion preprocessing together.

The author later explains the [barycentric dual alternative](https://www.redblobgames.com/x/1721-voronoi-alternative/). Check actual geometry rather than inferring a solver's orthogonality from a generator calling itself Voronoi.

Choose additions by their role. Use [generation recipes](generation-recipes.md) for shaped noise, periodic fields and Mapgen2-style stages; [authored terrain and climate](authored-terrain-and-climate.md) for Mapgen4-inspired painting and climate initialization; and [terrain map rendering](terrain-map-rendering.md) for the SVG experiment's field-to-image ideas. These are optional modules. Distinguish generator scores, physical quantities and display coordinates even when a demonstration calls all of them "elevation", "moisture" or "flow".

## Choose an initialization method

| Method | Useful control | Main tradeoff |
|---|---|---|
| Multi-scale noise | Fast broad variation, reproducible parameterized fields | Drainage and geological structure need additional work |
| Graph/region constraints | Landforms, biome adjacency, intentional accessibility | Can look schematic without local variation |
| Drainage-first terrain | Designed river networks and watershed hierarchy | Requires a consistent elevation reconstruction; not every arbitrary network is realizable |
| Artist stamps and constraints | Playable sites, landmarks, route corridors | Must reconcile overlapping edits and physical connectivity |
| Erosion preprocessing | Incised channels and sediment-related shapes | Adds parameter/runtime complexity; visual plausibility is not calibrated evolution |
| Imported elevation/material maps | Specific landscape reference | Coordinate, resolution, licensing and missing-substrate issues |
| Hybrid | Global control plus local natural variation | Needs a clear precedence and persistence policy |

Use a coarse strategic map for biome/settlement planning if useful, then a separate computational mesh for physics. Do not force the watershed graph, province map and render triangulation to share one resolution.

## Use coherent noise deliberately

For zero-centered noise samples \(N\), a finite octave sum can be written

\[
f(\mathbf x)=
\frac{\sum_{k=0}^{K-1}a_0p^k\,N(\lambda^k\mathbf x/\ell)}
{\sum_{k=0}^{K-1}a_0p^k}.
\]

Here \(\ell\) is a reference length in metres, \(\lambda\) is a frequency multiplier, \(p\) an amplitude ratio, and \(K\) the number of octaves. The normalized field is dimensionless. Elevation can be

\[
z(\mathbf x)=z_{\mathrm{offset}}+Hf(\mathbf x)+z_{\mathrm{authored}}(\mathbf x).
\]

The elevation scale \(H\) is in metres. The normalization is a chosen amplitude convention, not a guarantee of a particular sample variance or terrain slope.

Domain warping can use

\[
\mathbf x'=\mathbf x+w\,\mathbf W(\mathbf x/\ell_w),
\]

where \(\mathbf W\) is dimensionless and \(w,\ell_w\) are lengths. Large warps can fold or excessively distort patterns; a warped visual field does not supply a valid simulation mesh.

If a visual octave has wavelength below the collision or hydraulic resolution, decide whether it is decorative only or is integrated into subgrid properties. Never let a bump rendered as a dam lack the corresponding hydraulic barrier.

**Original scale example:** wavelengths \(512,256,128,64\ \mathrm m\) sampled on \(16\ \mathrm m\) terrain patches have progressively fewer samples per feature. This does not establish numerical convergence; inspect slopes and drainage and refine where gameplay depends on features near the resolution limit.

## Construct a consistent state

Initialize in a declared order:

1. Generate or import the domain and coordinate system.
2. Build and validate simulation mesh geometry.
3. Set geological base/bedrock and deposited soil/sediment layers.
4. Derive elevation from the chosen authoritative layer state.
5. Apply authored earthworks through the same material rules, or declare them initial-world construction with explicit initial quantities.
6. Build water storage, connections, boundaries and drainage summaries.
7. Initialize surface and subsurface stores with physically allowed capacities.
8. Spin up selected processes if the game needs an approximately equilibrated starting state.
9. Save the actual initialized state with generator version and provenance.

Do not independently generate soil thickness, dry mass, porosity and elevation without reconciling their identities. An ocean boundary, spring or rainfall series must have an explicit water-source role.

For a settled world, choose whether initial roads and foundations are already included in terrain. Avoid applying the same stamped foundations again on the first load.

## Treat drainage preprocessing carefully

Depression filling and breaching help derive drainage on elevation models. They are modeling choices, not proof that every natural hollow should be removed. The [Priority-Flood paper](https://rbarnes.org/sci/2014_barnes_depressions_published.pdf) is a primary algorithm reference.

Keep separate:

- The physical elevation and material inventory.
- A conditioned surface used for routing analysis.
- Real lake/basin storage and spill thresholds.

Changing a routing surface need not excavate the physical world. If the game deliberately breaches a depression physically, account for the displaced material.

Route flats with a defined rule and store/update basin outlets. A graph that cycles unexpectedly cannot be accumulated by a simple topological pass; resolve flat/cycle semantics or model those cells as reservoirs.

Hydrology-first generation is another design option; see [Génévaux et al., Terrain Generation Using Procedural Models Based on Hydrology](https://cs.purdue.edu/homes/bbenes/papers/Genevaux13ToG.pdf). Evaluate its constraints against gameplay and runtime needs rather than treating any generator as a complete world simulator.

## Separate permanent state from disposable detail

Store evolved materials and water. Keep procedural detail deterministic and disposable only when it cannot affect gameplay or when the exact generator version is retained.

Use separate random streams for unrelated features so adding a decorative shrub does not reroll a watershed. For chunked generation, use stable spatial keys and boundary agreements; a chunk loaded in another order should not create a new outlet.

Record generator parameters, seed, version, coordinate convention and initialization recipe. A seed alone cannot recover a world after erosion, building or a changed generation algorithm.
