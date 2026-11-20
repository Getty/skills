# Engine integration through derived terrain adapters

## Choose representations independently

Keep the physical terrain domain independent of the rendering and gameplay engine. A polygon simulation can drive a triangulated mesh, a heightmap, tiled collision or a stylized surface. Political regions, render triangles, navigation polygons and hydrological cells need not share boundaries or IDs.

Use adapters for terrain rendering, water rendering, collision, navigation, vegetation/decals and spatial queries. Each adapter reads a committed domain revision and publishes the revision it represents. It should not infer authoritative water quantity from a shader or modify material mass because a visual triangle changed size.

For optional editor previews, strategic maps and SVG/shader diagnostics, use [terrain map rendering](terrain-map-rendering.md). Keep color lookup, hillshade and decorative river width downstream of the declared fields.

Choose a heightfield when one elevation per horizontal location is enough. Use separate structures or local volumetric geometry for caves, tunnels and overhangs when needed. A basement does not automatically require voxelizing the whole world; decide which solid and void interfaces its gameplay uses.

## Define a publication contract

After terrain edits, rebuild the affected projections with their required margins: normals may depend on adjacent vertices, collision on tile cooking, and navigation on changed geometry and links. Do not assume all updates finish during one frame.

Accept an asynchronous result only if its source revision is still valid. Either swap compatible projections together or mark affected actions unavailable until their required projections are ready. A visible new floor must not be used for movement against old collision. Query APIs should state whether they read authoritative terrain, latest collision or an approximation.

Use one conversion boundary between simulation units and engine coordinates. Handle axis orientation, origin shifts and vertical scale explicitly. Keep stable domain IDs out of transient GPU vertex indices. Test seams and normals across tile edges; visual LOD should not alter a cell's stored water or soil mass.

## Unity example: heightmap projection

Verified reference: Unity 6000.3 `TerrainData.SetHeightsDelayLOD`. Its samples are normalized to [0,1] and the supplied array is indexed `[y,x]`. It delays LOD and vegetation updates; the documented completion step is `TerrainData.SyncHeightmap`.

Treat this as an adapter option for a chosen heightmap representation. Convert physical heights using the terrain origin and configured vertical scale. Detect out-of-range values before upload; silently clamping them would render a different surface from the simulation. Batch changes to the intended region and complete the engine's update sequence at the chosen publication point.

This API does not by itself define the game's navigation, water solver, persistence or material layers. Verify collision and navigation behavior in the target player build and engine version rather than assuming height upload is a complete terrain transaction.

Primary source: [Unity 6000.3 SetHeightsDelayLOD](https://docs.unity.com/en-us/engine/6000.3/script-reference/unityengine/terraindata/setheightsdelaylod).

## Unreal example: navigation after geometry changes

Epic's navigation overview describes navigation derived from collision and rebuilt in affected tiles. Its `Dynamic` mode supports regeneration from changed navigation-relevant data. `Dynamic Modifiers Only` changes existing navigation through modifiers and does not generate new navigable surfaces.

Therefore choose a regeneration path compatible with genuinely changed walkable geometry. A cost modifier can mark mud or flooded ground; it is insufficient by itself to create a newly excavated passage or raised platform. Keep bridge/navigation links separate from hydraulic openings.

Select and verify the actual runtime geometry path for the project: built-in terrain, a mesh component, a plugin or custom code. Check packaging, collision cooking and platform support in the selected engine version. Do not infer universal support or impossibility of terrain deformation from an editor tool or from navigation documentation alone.

Primary source: [Epic: modifying the navigation mesh](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-how-to-modify-the-navigation-mesh-in-unreal-engine).

## Integration acceptance checks

Verify one excavation and one fill through simulation, rendering, collision and navigation. Repeat near a tile seam and during an unfinished asynchronous update. Test save/reload in a packaged build, raycasts against the intended surface, objects standing on altered terrain, and flooded-area access rules.

Measure geometry upload, collision and navigation costs separately from the physical solver. Report the actual tested engine version and platform. Keep engine adapters optional so the same terrain concepts remain usable in a different engine or a headless simulation.
