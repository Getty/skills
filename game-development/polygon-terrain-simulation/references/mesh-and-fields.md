# Mesh, geometry and field placement

Treat geometry as input to numerical operators. A visually regular polygon network can still be a poor computational mesh.

## Contents

- [Choose representations](#choose-representations)
- [Store identities and metrics](#store-identities-and-metrics)
- [Compute geometric quantities](#compute-geometric-quantities)
- [Match gradients to geometry](#match-gradients-to-geometry)
- [Use one flux convention](#use-one-flux-convention)
- [Represent subcell detail](#represent-subcell-detail)
- [Refine only with a transfer plan](#refine-only-with-a-transfer-plan)

## Choose representations

Keep separate responsibilities even if a prototype stores them in one object:

| Representation | Responsibility |
|---|---|
| Simulation cells | Extensive stores, material columns, local parameters |
| Hydraulic faces/connections | Exchange, barriers, structures and boundaries |
| Terrain surface samples | Elevation, partial footprints, subcell relief |
| Render mesh | Visual detail, texture, tessellation and LOD |
| Collision surface | Contacts, support and physical interaction |
| Navigation graph/mesh | Traversability, clearance, costs and agent size |
| Political or ownership regions | Gameplay control and permissions |

A road can be traversable while obstructing water. A culvert can pass water without passing people. Decorative river polygons need not be the exact hydraulic control volumes. Render LOD must not silently change the simulation state.

Landlab documents distinct field locations and connectivity for grids; use that pattern as a design reference, not a requirement to adopt its API. See [Landlab gridding](https://landlab.csdms.io/user_guide/grid.html).

## Store identities and metrics

For each cell, store a stable ID, ordered boundary references, area \(A_i>0\), a valid representative point, coordinate reference/datum, and geometry revision. Store extensive values such as water volume and material mass at the chosen control-volume location.

For each internal face, store:

- Stable face ID, left and right cell IDs, ordered endpoints.
- Face length \(L_f>0\), unit normal from left to right, and center.
- Center-to-center vector, its length, and normal projection.
- Boundary/structure type, hydraulic profile and state revision.

A boundary face has one cell and a typed external condition, not a fake cell with an infinite supply by accident. A nonlocal pipe or pump is a hydraulic connection, not necessarily a geometric face.

Keep persistent IDs distinct from dense array slots, render vertex indices, chunk-local offsets and GPU buffers. Never serialize only a transient array index as a permanent building attachment.

Perform these geometry checks before a physical solve:

1. Every polygon is simple, finite, consistently wound and nondegenerate.
2. Adjacent cells agree on shared endpoints and length; internal faces have two owners.
3. Domain coverage has no unintended gaps or overlaps.
4. Face normals are unit length and opposite for the two incident cells.
5. The chosen representative points and normal distances satisfy solver assumptions.
6. Sliver cells, tiny faces and extreme area ratios are identified.
7. Sum of cell areas matches the intended domain area within a declared tolerance.

## Compute geometric quantities

### Polygon area and centroid

For a simple planar polygon with vertices \((x_k,y_k)\), close the loop with vertex \(0\):

\[
A_s=\frac12\sum_k (x_k y_{k+1}-x_{k+1}y_k),\qquad A=|A_s|.
\]

\[
C_x=\frac{1}{6A_s}\sum_k(x_k+x_{k+1})
(x_k y_{k+1}-x_{k+1}y_k),
\]

with the corresponding expression for \(C_y\).

Coordinates are metres; area is square metres. These formulas assume a simple polygon with straight segments. Handle holes as separately oriented rings. Validate self-intersection separately; the shoelace sum alone cannot detect it. Translate coordinates near the local origin for better conditioning when a small cell sits far from the world origin.

The geometric centroid is not automatically the location required by a discretization. For a Voronoi dual, the generating site is the relevant paired point; replacing it by the polygon centroid can destroy orthogonality.

**Analytical check:** the rectangle \((0,0),(4,0),(4,3),(0,3)\) has area \(12\ \mathrm{m^2}\) and centroid \((2,1.5)\ \mathrm m\). Reversing vertex order flips signed area, not physical area or centroid.

### Overlap-weighted values

For clipped subareas \(a_k\), approximate an integral by

\[
\int_\Omega f\,dA\approx\sum_k a_k f_k.
\]

Use true overlap areas with a footprint. A cell touched by a tiny building corner must not contribute its whole area. For linear triangular height patches, integrate exactly or use quadrature with a documented error; point samples are an approximation.

## Match gradients to geometry

The two-point expression

\[
g_{ij}=\frac{\psi_j-\psi_i}{d_{ij}}
\]

is a gradient **along the center link**. It is a face-normal gradient only when that link is normal to the face, with compatible sampling locations and metric assumptions.

On a nonorthogonal mesh let \(\mathbf d=\mathbf x_j-\mathbf x_i\), \(\mathbf n\) be the unit face normal, \(d_n=\mathbf d\cdot\mathbf n\), and \(\mathbf d_t=\mathbf d-d_n\mathbf n\). A linear-field reconstruction gives

\[
\partial_n\psi\approx
\frac{\psi_j-\psi_i-\nabla\psi_f\cdot\mathbf d_t}{d_n}.
\]

The face gradient \(\nabla\psi_f\) must be reconstructed consistently, for example using a suitable least-squares gradient with boundary treatment. This is a consistency relation, not a complete stable solver. A small or wrongly signed \(d_n\), unbounded correction, or a poor reconstruction requires a different mesh/operator. Limiters and correction iteration must match the PDE.

Red Blob's later [barycentric dual discussion](https://www.redblobgames.com/x/1721-voronoi-alternative/) explains that moving dual vertices to triangle centroids changes perpendicularity. Preserve that distinction when adapting its visual map geometry to a physical model.

**Linear-field check:** set \(\psi(x,y)=2x-3y+1\). Its exact gradient is \((2,-3)\). Test every reconstructed face derivative against \((2,-3)\cdot\mathbf n_f\), including skew faces and boundaries.

## Use one flux convention

Choose the orientation of each shared face once. Let \(Q_f>0\) mean left-to-right volumetric transfer \([\mathrm{m^3/s}]\), and \(s_{if}=+1\) for a cell from which that orientation points outward, \(-1\) for its neighbor.

\[
\frac{dV_i}{dt}=S_i-\sum_{f\in\partial i}s_{if}Q_f.
\]

Here \(S_i\) is net external volume rate. Summing over cells cancels every internal transfer exactly in real arithmetic. Use the same evaluated and limited value on both sides.

If an equation instead supplies normal depth-integrated flux \(q_f\ [\mathrm{m^2/s}]\),

\[
Q_f=L_fq_f,\qquad
(\nabla\cdot\mathbf q)_i\approx
\frac{1}{A_i}\sum_f s_{if}L_fq_f.
\]

Multiply by face width once. Do not multiply an already volumetric \(Q_f\) by width again.

**Numerical example:** a \(5\ \mathrm m\) face with \(q_f=0.02\ \mathrm{m^2/s}\) transfers \(0.1\ \mathrm{m^3/s}\). In \(10\ \mathrm s\), it transfers \(1\ \mathrm{m^3}\). Flat cells of \(20\) and \(50\ \mathrm{m^2}\) change depth by \(-0.05\) and \(+0.02\ \mathrm m\). Equal depth changes would violate volume conservation.

The same structure applies to dry-sediment mass flux \(F_f\ [\mathrm{kg/s}]\); do not use water concentration itself as a conserved quantity.

Reference: [Landlab gradients, fluxes and divergences](https://landlab.csdms.io/user_guide/grid_methods/06_gradients.html).

## Represent subcell detail

A cell can contain a height patch, material samples, a stage-volume table, and face cross sections. Make ownership precise: either subpatches own mass and the cell sums them, or the cell owns mass with a documented reconstruction. Do not treat independently editable cell mass and subpatch mass as two sources of truth.

Use consistent terrain for:

- Surface elevation and cut/fill integration.
- Water storage and face barriers.
- Collision, foundation support and exposed materials.

A narrow channel can be represented through storage and conveyance curves when its relevant behavior is adequately one-dimensional. It cannot recover unresolved transverse velocities or separated pools merely from a fine visual mesh. See [HEC-RAS hydraulic property tables](https://www.hec.usace.army.mil/confluence/rasdocs/r2dum/6.4/development-of-a-2d-or-combined-1d-2d-model/creating-hydraulic-property-tables-for-2d-flow-areas).

## Refine only with a transfer plan

Prefer a fixed computational mesh initially. If remeshing becomes necessary:

1. Intersect old and new control volumes.
2. Transfer extensive stores conservatively using overlap and an explicit reconstruction.
3. Transfer material classes and vertical layers without losing composition or order.
4. Recompute intensive quantities, levels and capacities.
5. Reattach structures, operations, spatial claims and boundaries.
6. Validate global budgets and local positivity before replacing the old revision.

A basic piecewise-constant transfer is

\[
M'_j=\sum_i M_i\,\frac{|\Omega_i\cap\Omega'_j|}{A_i}.
\]

It conserves total mass when the meshes cover the same domain and overlaps partition each old cell. It assumes uniform density in each old cell; it does not preserve detailed banks, stratigraphy or hydraulic equilibrium by itself. Refine the transfer representation when those features matter.

Test remapping a constant field, a localized store, a dry/wet interface and a layered column. Report numerical residuals and topology changes.
