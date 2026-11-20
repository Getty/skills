# Primary sources and implementation pointers

Use sources to understand a model, then check its assumptions against the game. The skill's proposed architecture, contracts, test catalog, synthetic data and worked examples are original engineering material. Source links do not imply validation or endorsement of the bundled utilities.

Stable mathematical relations remain useful, but verify live software interfaces and component limitations before integration.

## Contents

- [Generation and mesh](#generation-and-mesh)
- [Water and hydraulic structures](#water-and-hydraulic-structures)
- [Soil and groundwater](#soil-and-groundwater)
- [Sediment and evolving terrain](#sediment-and-evolving-terrain)
- [Runtime and engine integration](#runtime-and-engine-integration)
- [Use code and evidence carefully](#use-code-and-evidence-carefully)

## Generation and mesh

| Primary source | Use | Limit |
|---|---|---|
| [Red Blob: Polygon Map Generation](https://theory.stanford.edu/~amitp/game-programming/polygon-map-generation/) | Graph-based map initialization and semantic regions | Does not specify persistent hydraulic/material state |
| [Red Blob: Terrain from Noise](https://www.redblobgames.com/maps/terrain-from-noise/) | Field construction and designer controls | Noise alone does not establish consistent drainage |
| [Red Blob: Alternatives to Voronoi](https://www.redblobgames.com/x/1721-voronoi-alternative/) | Distinguish circumcentric and barycentric duals | Visual preferences do not determine numerical suitability |
| [Red Blob: Mapgen4](https://www.redblobgames.com/maps/mapgen4/) | Authored terrain with procedural follow-up | Generator updates are not persistent material/water evolution |
| [Mapgen4: painting revisited](https://simblob.blogspot.com/2018/09/mapgen4-elevation-painting-revisited.html) | Why direct elevation painting replaced categorical constraint interpolation | Historical design iteration; other distance-field uses remain |
| [Mapgen4: rainfall](https://simblob.blogspot.com/2018/09/mapgen4-rainfall.html) | Wind ordering and rain-shadow design | Climate proxies are not a conservative atmospheric solver |
| [Mapgen4 source](https://github.com/redblobgames/mapgen4) | Inspect painting, map and worker responsibilities | Pin a revision when reproducing behavior; distinguish current code from earlier posts |
| [Red Blob: Mapgen2](https://www.redblobgames.com/maps/mapgen2/) and [source](https://github.com/redblobgames/mapgen2) | Replaceable island-generation stages | Deliberately game-shaped landscape; source-count flow and moisture rank are not physical stores |
| [Red Blob: maps with image filters](https://www.redblobgames.com/x/1446-svg-filters/) | Field-driven map rendering, palettes and relief | Appearance adapter with browser-dependent details |
| [W3C Filter Effects](https://www.w3.org/TR/filter-effects-1/) | SVG filter primitive and color-space semantics | Check document status and actual renderer support; no terrain physics |
| [Landlab grid guide](https://landlab.csdms.io/user_guide/grid.html) | Field locations, grids and connectivity | Each component has its own grid requirements |
| [Landlab gradients and divergences](https://landlab.csdms.io/user_guide/grid_methods/06_gradients.html) | Metric-aware operations | Link gradients require geometry interpretation |
| [Barnes et al.: Priority-Flood](https://rbarnes.org/sci/2014_barnes_depressions_published.pdf) | Depression handling in elevation analysis | Conditioning is not automatic physical excavation |
| [Génévaux et al.: Hydrology-based terrain generation](https://cs.purdue.edu/homes/bbenes/papers/Genevaux13ToG.pdf) | River-structured initialization | Generation is separate from runtime evolution |

## Water and hydraulic structures

- [HEC-RAS cell/face hydraulic property tables, 6.4](https://www.hec.usace.army.mil/confluence/rasdocs/r2dum/6.4/development-of-a-2d-or-combined-1d-2d-model/creating-hydraulic-property-tables-for-2d-flow-areas): stage-volume storage and face geometry from finer terrain; unresolved circulation still requires adequate computational resolution.
- [HEC-RAS shallow-water equations](https://www.hec.usace.army.mil/confluence/rasdocs/hecras/latest/technical-reference/hydraulic-equations/shallow-water-equations): continuity and momentum assumptions.
- [HEC-RAS diffusive-wave equations](https://www.hec.usace.army.mil/confluence/rasdocs/hecras/latest/technical-reference/hydraulic-equations/diffusive-wave-equation): friction-dominated approximation.
- [HEC-RAS choosing shallow-water versus diffusion wave](https://www.hec.usace.army.mil/confluence/rasdocs/r2dum/latest/running-a-model-with-2d-flow-areas/shallow-water-or-diffusion-wave-equations): model choice by hydraulic regime.
- [HEC-RAS grid size and timestep](https://www.hec.usace.army.mil/confluence/rasdocs/r2dum/6.0/running-a-model-with-2d-flow-areas/selecting-an-appropriate-grid-size-and-time-step): scheme-specific practical guidance.
- [HEC-HMS spillways](https://www.hec.usace.army.mil/confluence/hmsdocs/hmstrm/reservoir-modeling/reservoir-modeling-concepts-and-equations/spillways): hydraulic structure relations and regime limits.
- [HEC-RAS hydraulic reference manual 6.6](https://www.hec.usace.army.mil/software/hec-ras/documentation/HEC-RAS_Hydraulic_Reference_Manual_v6.6.pdf): culverts, gates and pressure-flow regimes.
- [Landlab flow accumulation](https://landlab.csdms.io/generated/api/landlab.components.flow_accum.flow_accumulator.html): routing and runoff accumulation, distinct from transient hydraulic storage.

## Soil and groundwater

- [USDA NRCS bulk density, moisture and aeration](https://www.nrcs.usda.gov/sites/default/files/2022-10/Soil%20Bulk%20Density%20Moisture%20Aeration.pdf): bulk-density and pore-space distinctions; do not convert illustrative mineral density into a universal value.
- [Landlab Lithology and LithoLayers](https://landlab.csdms.io/tutorials/lithology/lithology_and_litholayers.html): changing exposed material through layered terrain.
- [EPA SWMM hydrology reference](https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P100NYRA.txt): infiltration and groundwater model families.
- [EPA Darcy explanation](https://www3.epa.gov/ceampubl/learn2model/part-two/onsite/darcy.html): flux, conductivity and gradient.
- [Groundwater Project: hydraulic conductivity](https://books.gw-project.org/hydrogeologic-properties-of-earth-materials-and-principles-of-groundwater-flow/chapter/hydraulic-conductivity/): conductivity versus intrinsic permeability and fluid properties.
- [USGS MODFLOW 6 documentation](https://www.usgs.gov/publications/documentation-modflow-6-groundwater-flow-model): reference for more complete groundwater formulations.
- [Landlab Dupuit groundwater component](https://landlab.csdms.io/generated/api/landlab.components.groundwater.dupuit_percolator.html): a restricted shallow-aquifer implementation; inspect boundary and storage assumptions.

## Sediment and evolving terrain

- [USACE bed-change equation](https://www.hec.usace.army.mil/confluence/rasdocs/d2sd/ras2dsedtr/6.2/model-description/bed-change-equation): sediment continuity and porosity conventions.
- [USACE deposition](https://www.hec.usace.army.mil/confluence/rasdocs/d2sd/ras2dsedtr/6.3/model-description/deposition): settling closures and concentration interpretation.
- [Landlab SPACE guide](https://landlab.csdms.io/tutorials/landscape_evolution/space/SPACE_user_guide_and_examples.html): sediment cover and bedrock/sediment separation; verify supported grid and units.
- [USACE cohesive erodibility conventions](https://www.hec.usace.army.mil/confluence/rasdocs/rassed1d/1d-sediment-transport-technical-reference-manual/cohesive-transport/krone-and-partheniades-methods/kd-vs-m): normalized versus unnormalized excess-shear coefficients.
- [USACE BSTEM overview](https://www.hec.usace.army.mil/confluence/rasdocs/rassed1d/1d-sediment-transport-technical-reference-manual/bstem-technical-reference-manual/overview): bank scour, failure and bed processes.
- [USACE bank soil forces](https://www.hec.usace.army.mil/confluence/rasdocs/rassed1d/1d-sediment-transport-technical-reference-manual/bstem-technical-reference-manual/bank-failure/layer-method/soil-forces) and [hydraulic forces](https://www.hec.usace.army.mil/confluence/rasdocs/rassed1d/1d-sediment-transport-technical-reference-manual/bstem-technical-reference-manual/bank-failure/layer-method/hydraulic-forces): effective stress and water forces.
- [Langston & Tucker 2018](https://esurf.copernicus.org/articles/6/1/2018/): lateral erosion in a landscape-evolution model.
- [Landlab lateral erosion component](https://landlab.csdms.io/generated/api/landlab.components.lateral_erosion.lateral_erosion.html): implementation reference with documented square-raster assumptions, not a drop-in arbitrary-polygon solver.
- [Landlab linear diffuser](https://landlab.csdms.io/generated/api/landlab.components.diffusion.diffusion.html), [Taylor nonlinear diffuser](https://landlab.csdms.io/tutorials/hillslope_geomorphology/taylor_diffuser/taylor_diffuser.html), and [integrated exponential weathering](https://landlab.csdms.io/generated/api/landlab.components.weathering.exponential_weathering_integrated.html): optional hillslope and soil-production models.

## Runtime and engine integration

- [Landlab timesteps](https://landlab.csdms.io/user_guide/time_steps.html) and [units](https://landlab.csdms.io/user_guide/units.html): component coupling and unit consistency.
- [Unity 6000.3 SetHeightsDelayLOD](https://docs.unity3d.com/6000.3/Documentation/ScriptReference/TerrainData.SetHeightsDelayLOD.html): a version-specific heightmap adapter, not a polygon simulation architecture.
- [Epic navigation modification overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-how-to-modify-the-navigation-mesh-in-unreal-engine): dynamic generation and modifier-only capabilities; terrain collision support remains an independent integration decision.

## Use code and evidence carefully

Prefer a reference implementation whose assumptions match the chosen model. Check grid types, variable locations, boundary conventions, time units, physical parameters, license and maintenance status. A framework supporting Voronoi grids does not imply every one of its components supports them.

Do not make Landlab, HEC-RAS, MODFLOW, Unity or Unreal mandatory dependencies of this skill. They are sources and optional implementation references. The bundled numerical utilities require only Python's standard library.

When source text, printed equations and code disagree, derive the units/signs and examine the implementation or underlying paper. Keep a note of the interpretation used in the game. Avoid treating a copied formula as validated merely because it came from an authoritative site.
