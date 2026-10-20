# Maps, canvas, diagrams, and 3D rendering

**Read when:** integrating geospatial views, canvas scenes, or 3D content.

## Select by interaction and data

React Three Fiber provides a React renderer for Three.js; it is not ordinary DOM rendering. Verify compatible React/renderer/Three versions and resource lifecycle. MapLibre, Leaflet, deck.gl, Konva, PixiJS, and Drei are catalog discovery options. Inspect their installed-version React bindings rather than assuming any wrapper shares the same lifecycle or license.

Separate the domain model from the scene graph and GPU resources. Keep large geometry, textures, map sources, and imperative handles outside serializable application state. Decide who creates and disposes each resource, and whether it is shared. A React unmount alone is not sufficient evidence that all third-party/native/GPU allocations were released.

## Product constraints

Define coordinate reference system, precision, units, map attribution, tile licensing, offline rights, and geolocation privacy. Do not mix latitude/longitude order or projected and geographic coordinates. For 3D, establish asset budgets, texture resolution, animation frequency, device capability limits, and a fallback when WebGL/WebGPU is unavailable or loses context.

Provide a nonvisual or simplified alternative for essential information. Canvas pixels do not automatically expose semantic controls. Keep interaction overlays aligned with the canvas coordinate system and handle device pixel ratio, zoom, resize, and hidden containers deliberately.

## Acceptance

Test resize, context loss, low-powered devices, offline tiles, missing textures, many markers/objects, and repeated scene switching. Inspect attribution and permission prompts. Verify resource disposal with memory/GPU tools and avoid a permanent animation loop for a static scene. Treat imported assets and external tile URLs as untrusted resources governed by size, origin, and content policies.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R65: React Three Fiber](https://r3f.docs.pmnd.rs/getting-started/introduction)
- [R04: Effects decision guide](https://react.dev/learn/you-might-not-need-an-effect)
- [R74: Vite](https://vite.dev/guide/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
