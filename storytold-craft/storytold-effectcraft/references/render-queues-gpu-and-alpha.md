# Render snapshots, cancellation and alpha delivery

**Read when:** rendering a composition or validating GPU/CPU output.

A render job owns a project snapshot taken when it starts. Edits during the render affect the live project, not that snapshot. A second render is refused while one is running. Record the project revision/checkpoint associated with each output so an edited live preview is not mistaken for the content currently being encoded.

The direct headless blocking `renderQueue.render` command supports progress/cancellation through the documented MCP path. `wait:false` instead returns promptly; poll `renderQueue.list` and stop with `renderQueue.stop`. Bridge, batch and single-frame tools do not automatically inherit the direct blocking MCP cancellation semantics.

Cancellation removes files recorded as opened by that job, not everything in the output directory. Previously completed queue items and skipped pre-existing frames remain. A positive failed count or a removed queue item can make the overall result fail even though some files are valid. Inspect queue-item results and actual files.

## Renderer and delivery contracts

A present GPU is not proof that the selected effect/color-depth pipeline uses it. Inspect the active backend, effect capabilities and reasons for CPU fallback. Compare representative output when backend consistency matters. Rendering success is not a cross-backend pixel-equivalence guarantee.

For compositing handoff, specify RGB versus RGBA and a format that retains alpha. `render_frame` with `transparent:true` preserves alpha instead of compositing the background. Review edge halos and transparency in the consuming application, not only against the editor's background. Record resolution, frame rate, duration, alpha convention and color interpretation in the handoff.

Do not import an After Effects `.aep`/`.aepx` assumption or third-party AE plugin compatibility into this engine. Lottie and other interchange outputs have their own supported feature subsets. Export warnings and a reopened consumer-side sample are required before claiming interchange fidelity.

## Evidence

- [effect-mcp](https://github.com/storytold/effectcraft/blob/main/docs/mcp.md)
- [effect-agents](https://github.com/storytold/effectcraft/blob/main/docs/agents.md)
- [effect-cli](https://github.com/storytold/effectcraft/blob/main/apps/effectcraft-cli/src/main.rs)
- [effectcraft-readme](https://github.com/storytold/effectcraft/blob/main/README.md)
