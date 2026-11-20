# Terrain fields as maps and diagnostic views

Use this optional adapter when a terrain task needs an editor preview, strategic map, export or diagnostic overlay. Keep the rendering recipe independent of terrain generation and physical evolution. These are original integration recipes; the linked demonstrations are design references, not numerical validation.

## Contents

- [What the SVG experiment contributes](#what-the-svg-experiment-contributes)
- [Define the field-to-image contract](#define-the-field-to-image-contract)
- [Choose a palette model](#choose-a-palette-model)
- [Show actual water and relief](#show-actual-water-and-relief)
- [Keep SVG and shader details optional](#keep-svg-and-shader-details-optional)
- [Check the adapter](#check-the-adapter)

## What the SVG experiment contributes

[Red Blob's image-filter experiment](https://www.redblobgames.com/x/1446-svg-filters/) turns elevation and moisture images into a styled map. It combines procedural texture, channel transforms, thresholds and an embossed appearance. The author also suggests a two-dimensional texture lookup for more flexible color mapping. Its useful contribution here is a compact visual adapter for scalar fields; it does not define polygon connectivity, soil layers or water storage.

Choose a representation for the intended output:

| Need | Reasonable starting point |
|---|---|
| Small region map with selectable cells | SVG polygon paths and explicit cell IDs |
| Interactive dense field view | Texture or mesh shader driven by committed data |
| Offline diagnostic image | Raster export with a legend, units and revision |
| Stylized preview | Optional filter or shader effects layered over the field view |

Measure the chosen implementation at the actual map size. An SVG file containing filter effects can still require raster intermediates; its format does not establish a performance advantage over a shader or canvas.

## Define the field-to-image contract

For each input specify its name, meaning, unit, location, revision and interpolation rule. Examples include physical surface elevation at vertices, cell-average pore-water volume, a categorical material ID and a dimensionless climate score. These are different data types even if each can be displayed with one color.

For a display range with finite bounds and \(z_{\max}>z_{\min}\), define

\[
e=\operatorname{clamp}\!\left(\frac{z-z_{\min}}{z_{\max}-z_{\min}},0,1\right).
\]

Clipping is acceptable for this display coordinate if the legend exposes the range. Retain the original physical value. A clipped color must not silently replace a height, a pore-water quantity or a save field. Provide an out-of-range or missing-data overlay when it matters.

Sample continuous fields according to their declared geometry. Use triangle interpolation for a continuous reconstructed surface, or constant cell color for an explicitly cell-based diagnostic. Do not bilinearly blend material IDs into invented intermediate IDs. For mixtures, render stored fractions or a deliberate dominant-material view.

Publish the map's `terrain_revision`, field revisions, palette version and coordinate transform. Picking a point on the map should query the actual terrain through that transform, not infer a material or height from the displayed RGB value. Keep the displayed cell identity separate from a transient triangle or texture index.

## Choose a palette model

The following equations are generic rendering choices. Let \(e,m\in[0,1]\) be declared display coordinates; \(m\) may be a climate score or a normalized measurement, but label which it is.

An affine color rule is

\[
\mathbf C(e,m)=\mathbf C_0+e\mathbf a+m\mathbf b.
\]

This is compact and suitable for a color-matrix implementation. It cannot express every joint response to elevation and moisture. For corner colors \(\mathbf C_{00},\mathbf C_{10},\mathbf C_{01},\mathbf C_{11}\), one affine rule fits all four exactly only when

\[
\mathbf C_{11}-\mathbf C_{10}-\mathbf C_{01}+\mathbf C_{00}=\mathbf0.
\]

Use bilinear blending when four independent corner colors are sufficient:

\[
\mathbf C(e,m)=(1-e)(1-m)\mathbf C_{00}
+e(1-m)\mathbf C_{10}
+(1-e)m\mathbf C_{01}+em\mathbf C_{11}.
\]

Use a two-dimensional lookup texture or a classifier when the palette needs more than those four controls. A smooth palette and a biome classification table have different purposes: interpolate colors for appearance; evaluate biome categories using explicit rules. Do not manufacture a hydrological state from the resulting biome or color.

**Synthetic linear-RGB example.** Choose corners
\(\mathbf C_{00}=(0.65,0.50,0.30)\),
\(\mathbf C_{10}=(0.80,0.80,0.75)\),
\(\mathbf C_{01}=(0.10,0.40,0.20)\),
\(\mathbf C_{11}=(0.45,0.60,0.50)\).
At \(e=0.25,m=0.75\), bilinear blending yields
\((0.3125,0.48125,0.309375)\).
The interaction vector is \((0.20,-0.10,-0.15)\), so an affine fit through the other three corners cannot reproduce the fourth. These values are an arithmetic fixture, not an ecological color standard. Convert to the chosen output color encoding after the defined blending step.

## Show actual water and relief

During initial world design, a height threshold can propose a coastline. In an evolved world, display water from actual water state and the selected storage reconstruction. A low basin separated from the ocean is not automatically seawater; an inland reservoir can exist well above ocean level. For subcell pools, use the relevant compartment's stage and wet geometry. A cell-average depth alone does not identify the exact shoreline.

Keep three distinct river concepts: the drainage network, the visual river stroke, and the physical channel/water geometry. Cartographic minimum stroke widths make streams readable but do not enlarge their hydraulic cross-section. Conversely, changing physical channel width must update the relevant water geometry even if the visible map style stays the same.

For a single-valued physical surface, an optional relief view can use

\[
\mathbf n=\frac{(-z_x,-z_y,1)}{\sqrt{1+z_x^2+z_y^2}},\qquad
I=a+(1-a)\max(0,\mathbf n\cdot\mathbf l),
\]

where \(z_x,z_y\) are slopes in consistent horizontal/vertical units, \(\mathbf l\) is a unit direction toward the light and \(a\in[0,1]\) is a display ambient term. Declare any visual vertical exaggeration. Pixel-space embossing is an appearance effect and must not become the slope used for erosion, flow or agent eligibility.

## Keep SVG and shader details optional

For an SVG implementation, inspect the relevant primitive definitions in [W3C Filter Effects](https://www.w3.org/TR/filter-effects-1/). `feTurbulence` supplies procedural imagery, `feColorMatrix` transforms channels, `feComponentTransfer` applies channel transfer functions, and `feConvolveMatrix` applies a kernel. Keep the field inputs, intermediate results and composition order explicit.

The cited W3C document specifies `linearRGB` as the initial `color-interpolation-filters` value. Explicitly choose the color space when matching a palette across renderers. Check filter regions, edge behavior, sampling scale and alpha handling in the target browser; the Red Blob experiment itself reports browser differences. Do not promise portable simulation determinism from a visually seeded SVG noise filter.

If generated image noise becomes an input to physical terrain, first extract and version a declared numeric field with known coordinates, range and sampling. The authoritative initial state should not depend on a later browser repaint. For ordinary map decoration, keep the noise entirely within the renderer.

## Check the adapter

Verify a few known samples and the palette endpoints before comparing whole images. Check the synthetic palette case in [generation examples](../assets/generation-examples.json). Then inspect one partial wet cell, one dry depression below ocean level but hydraulically disconnected, one material boundary and one edited tile seam.

Change only the palette and confirm that stored quantities and physical checksums remain unchanged. Display the correct revision while an asynchronous terrain update is pending. Treat image snapshots as rendering checks, not as evidence of water or sediment conservation.
