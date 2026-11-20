# Optional generation recipes for polygon terrain

Use these recipes to construct an initial landscape or an explicitly disposable preview. Choose only the controls the game needs. Once materials and water become authoritative, route player edits through [terrain operations](terrain-operations.md); rerunning a shaping function does not account for excavation or imported fill.

The formulas below are original, engine-neutral examples inspired by the cited generation techniques. They are not a reproduction of Mapgen2 and do not prescribe geological realism.

## Contents

- [Declare the field contract](#declare-the-field-contract)
- [Shape hills, ridges and terraces](#shape-hills-ridges-and-terraces)
- [Guarantee a submerged perimeter explicitly](#guarantee-a-submerged-perimeter-explicitly)
- [Sample polygons at the required meaning and scale](#sample-polygons-at-the-required-meaning-and-scale)
- [Generate chunks and periodic fields](#generate-chunks-and-periodic-fields)
- [Use Mapgen2 as a replaceable pipeline](#use-mapgen2-as-a-replaceable-pipeline)
- [Control distributions without confusing quantities](#control-distributions-without-confusing-quantities)
- [Check the selected recipe](#check-the-selected-recipe)
- [Sources and interpretation](#sources-and-interpretation)

## Declare the field contract

Record the noise implementation/version, seed derivation, coordinate scale, output range and octave convention. A function returning a signed value is not interchangeable with one returning a value in `[0,1]`. Some libraries already combine octaves. Do not unknowingly apply a second octave stack.

For a normalized signed field \(f\in[-1,1]\), use

\[
u=(f+1)/2\in[0,1].
\]

See [initialization and generation](initialization-and-generation.md) for the octave and domain-warp formulas. Their amplitude normalization does not produce a uniform probability distribution. Check the provider's documented bounds; a sampled minimum/maximum is not proof of a global bound. Clamp only when clipping is a declared design operation, not to conceal an incorrect range assumption.

Use distinct, stable random streams for elevation, climate, placement and decorative variation. Spatial offsets or different seeds can reduce unwanted correlation; neither should be described as a universal proof of statistical independence. Adding trees must not change previously generated relief.

## Shape hills, ridges and terraces

Let \(u\) be dimensionless. A simple elevation mapping is

\[
z=z_0+Hq(u),\qquad q(u)=u^\gamma,
\]

where \(H>0\) is a height range in metres and \(\gamma>0\) is a designer control. Larger exponents lower intermediate values. Apply a fractional exponent only to a valid nonnegative input. This curve changes slopes as well as elevation proportions: its derivative is \(\gamma u^{\gamma-1}\), which becomes large near zero when \(\gamma<1\).

A bounded ridge transform is

\[
r(u)=1-|2u-1|.
\]

It peaks at the middle of the input range. Applying it to individual octaves or to their sum produces different terrain. Combining ridge fields does not establish a geologically meaningful mountain range or drainage network.

For terraces of physical height \(\Delta z>0\), one explicit rounding convention is

\[
z_T=z_{\rm ref}+\Delta z\left\lfloor
\frac{z-z_{\rm ref}}{\Delta z}+\frac12
\right\rfloor.
\]

Halfway cases go toward the larger elevation, including negative values. A blend \((1-\beta)z+\beta z_T\), \(0\leq\beta\leq1\), reduces the step amplitude but retains discontinuities for any \(\beta>0\); use a genuinely smooth transition curve if continuous derivatives are required. Terrace flats need an explicit drainage rule and their risers need matching collision and hydraulic geometry.

**Synthetic arithmetic:** \(f=-0.5\) gives \(u=0.25\). With \(\gamma=2\), \(H=160\ \mathrm m\), and \(z_0=-10\ \mathrm m\), elevation is \(0\ \mathrm m\). The same \(u\) gives ridge value \(0.5\). Independently, \(z=14\ \mathrm m\), \(z_{\rm ref}=0\), and \(\Delta z=4\ \mathrm m\) yield terrace height \(16\ \mathrm m\).

## Guarantee a submerged perimeter explicitly

A weak blend toward an island shape may leave land at the boundary. If submerged edges are a requirement, enforce that property mathematically and test every boundary segment.

For a rectangular domain, normalize its coordinates to \(\xi,\upsilon\in[-1,1]\), then set

\[
s=\max(|\xi|,|\upsilon|),\quad
t=\operatorname{clamp}\left(\frac{s-s_0}{1-s_0},0,1\right),\quad
b=t^2(3-2t),
\]

with \(0\leq s_0<1\). Choose \(z_{\rm edge}<z_{\rm sea}\) and use

\[
z'=(1-b)z+bz_{\rm edge}.
\]

The outer boundary has \(s=t=b=1\), hence \(z'=z_{\rm edge}\) regardless of the original noise value. The inner region \(s\leq s_0\) is unchanged. This guarantees a submerged perimeter, not land in the center, a particular island count, or natural-looking coastlines. For another domain shape, construct a boundary-distance mask with equivalent endpoint properties.

Apply this constraint after other elevation detail, or require subsequent effects to vanish at the boundary. Enforce it in the actual surface representation: constrained cell-center samples alone do not guarantee the reconstructed boundary height.

**Synthetic arithmetic:** take \(z=50\ \mathrm m\), \(z_{\rm edge}=-2\ \mathrm m\), and sea level \(0\ \mathrm m\). At \(t=0.5\), \(b=0.5\) and \(z'=24\ \mathrm m\); at the perimeter, \(z'=-2\ \mathrm m\).

A low-elevation mask alone does not identify ocean connectivity. Flood from the declared ocean boundary or use an equivalent connectivity procedure; separately decide which enclosed basins contain lakes and how much water they hold. Do not automatically fill every below-sea-level hollow with an unlimited ocean supply.

## Sample polygons at the required meaning and scale

Specify whether a stored field is a point sample, a cell mean, or an extensive integral. Sampling noise at one cell center is convenient but generally differs from the cell mean:

\[
\bar f_i=\frac{1}{A_i}\int_{\Omega_i} f(\mathbf x)\,dA
\approx\frac{1}{A_i}\sum_q w_q f(\mathbf x_q),
\qquad \sum_qw_q=A_i.
\]

Quadrature weights \(w_q\) have units of square metres. Choose quadrature or subdivision according to the variation and required accuracy; averaging vertices is not an exact general polygon integral. An elevation field may instead belong on surface vertices and define a piecewise-linear patch. Keep that interpretation distinct from a cell's material stores.

Physical amplitude and wavelength jointly set relief: reducing wavelength while retaining height amplitude increases typical slopes. Resolve important ridges, channels and barriers in the physical representation, or give them explicit subcell geometry. Decorative octaves must not silently change building support or water connectivity.

Initialize layer thickness, porosity, mass and surface elevation consistently using [layered materials](layered-materials.md). A generated elevation or biome label alone cannot determine the subsurface material column.

## Generate chunks and periodic fields

Evaluate persistent procedural fields in stable world coordinates. Chunk index and camera position may determine which coordinates are sampled; they must not change the field at an already identified location. Give shared boundaries the same samples and conventions. Retain the generator manifest, and save evolved state as described in [persistence and streaming](persistence-and-streaming.md).

For a field periodic over lengths \(L_x,L_y>0\), embed coordinates into four-dimensional noise space:

\[
\mathbf p(x,y)=\left(
R_x\cos\frac{2\pi x}{L_x},R_x\sin\frac{2\pi x}{L_x},
R_y\cos\frac{2\pi y}{L_y},R_y\sin\frac{2\pi y}{L_y}
\right),\qquad
R_x=\frac{L_x}{2\pi\ell},\quad R_y=\frac{L_y}{2\pi\ell}.
\]

Here \(\ell>0\) is a physical length scale, so \(\mathbf p\) is dimensionless. Evaluate \(N_4(\mathbf p)\); multiplying the embedding by an octave frequency multiplier preserves the periods. Test seam agreement with a declared floating-point tolerance or canonicalize equivalent boundary coordinates if identical samples are required.

A seamless field does not make the mesh periodic. Pair opposite physical boundaries, define wrapped distances and neighbors, and account for transfers exactly once if the simulated world wraps. Wind, rivers, storage and external boundaries need compatible semantics. Conversely, a repeating decorative texture does not require a periodic physical world.

## Use Mapgen2 as a replaceable pipeline

The current Mapgen2 repository separates mesh connectivity from generated fields and lets callers assemble point placement, boundary construction, triangulation and dual-mesh setup. Its map calculation then assigns land/water, ocean connectivity, elevation/downslopes, river paths, moisture and biomes. These are useful stage boundaries rather than mandatory dependencies.

Its elevation construction uses coast-distance traversal and derives downslope links. It is not simply a noise heightmap on polygons. Its river accumulator increments a counter for each selected source along a downslope route; that count is not discharge in cubic metres per second. Its moisture procedure uses freshwater distance and subsequent rank redistribution; that field is not stored pore water.

For a persistent game, define each stage's inputs, outputs, units and revision. Convert the selected initial surface and material design into physical stores; initialize hydraulic boundaries and volumes explicitly. Keep topological ghost elements out of physical inventories unless they have a deliberately defined boundary role. Generic flood fills and distance traversals used in generation do not require implementing agent navigation in this skill.

## Control distributions without confusing quantities

Rank redistribution can target attractive elevation or biome proportions, but ranking cells equally controls cell counts rather than land area. An area-weighted empirical distribution is

\[
F_A(v)=\frac{\sum_i A_i\,\mathbf 1[f_i\leq v]}{\sum_i A_i}.
\]

Choose the domain being ranked explicitly, such as land only. Ties and finite cells may prevent an exact requested area fraction. Define empty-domain and single-cell behavior instead of dividing by zero. Recomputing ranks independently per chunk creates incompatible mappings; changing the global sample set can also alter distant values.

**Synthetic arithmetic:** three eligible cells have areas \(10,30,60\ \mathrm{m^2}\) and increasing field values. A threshold selecting the first two includes two thirds of cells but only \(40\%\) of the area. Use that distinction when requesting “half the world is forest.”

A normalized moisture suitability score can choose a biome or initial vegetation. If the game simulates soil water, derive its quantities from an explicit initialization and capacity rule. Recoloring or reranking the biome field must not add or remove water.

## Check the selected recipe

Check declared ranges, physical units, the exact perimeter condition, meaningful slope extremes, seam compatibility and sampling error. Include a case with unequal cell areas. Verify that no generator stage overwrites persisted player edits and that changing visual parameters leaves physical budgets unchanged. Test seed/version reproducibility on the actual supported platforms before promising identical output.

Use [generation examples](../assets/generation-examples.json) for the synthetic arithmetic above. They are illustrations rather than mandatory world parameters.

## Sources and interpretation

- [Red Blob: Terrain from Noise](https://www.redblobgames.com/maps/terrain-from-noise/): field shaping, biome inputs, periodic sampling and placement alternatives; a procedural design tutorial, not a material or water solver.
- [Red Blob: Mapgen2](https://www.redblobgames.com/maps/mapgen2/): explicitly game-directed island generation.
- [Mapgen2 repository](https://github.com/redblobgames/mapgen2): replaceable setup stages and separate mesh/map structures.
- [Mapgen2 calculation](https://github.com/redblobgames/mapgen2/blob/main/map.js), [elevation](https://github.com/redblobgames/mapgen2/blob/main/elevation.js), [rivers](https://github.com/redblobgames/mapgen2/blob/main/rivers.js), and [moisture](https://github.com/redblobgames/mapgen2/blob/main/moisture.js): the reference implementation. Pin a revision before integrating; repository branches and APIs may change.
