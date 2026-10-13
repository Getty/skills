# Partial batches, video jobs and recovery

**Read when:** running action chains, exporting a timeline, or handling a failed or cancelled call.

## Never equate command count with undo count

`command_batch` preserves earlier successful mutations. Read `completed`, per-step results and actual history. Some commands add no undo entry; others can have different grouping. Undo one inspected history entry at a time only when the operation is known to be undoable. Files already written are outside document undo.

A reply-size/budget failure can follow a completed mutation. Recovery is inspect-first: compare the expected postcondition, document identity and history revision; then decide whether to continue, undo, or restart from a checkpoint. Blind retries can duplicate layers, exports or placements.

## Render Video is a special path

For `file.export.renderVideo`, create/open the document and a timeline before exporting. In the reviewed MCP implementation, a direct headless `command_run` can report per-frame progress when the request carries a progress token. PNG sequences and animated GIF use the engine renderer. The scoped writer targets a directory under the write root and refuses existing target filenames, traversal and escaping links.

Cancellation stops at a frame boundary; a current frame or encoding unit may finish. Cleanup removes only files created by that job, not unrelated files or the destination directory. The document and playhead remain unchanged. Render Video is synchronous even with `wait:false`; do not expect that flag to manufacture a background job ID. Other job-capable operations retain their own jobs interface.

Batch exports do not acquire the same per-step progress/cancellation contract. Nested engine actions and bridged Render Video remain restricted by filesystem policy. A generic tool catalog entry therefore does not prove that every transport can execute every variant.

## Acceptance gate

Save the editable parent document, reopen it, inspect structure, render a bounded preview, and verify final file dimensions/alpha/profile separately. For sequences verify frame count, ordering, timing and partial-output absence. A tool success, a PNG preview and a correct editable file are three different observations; report each independently.

## Evidence

- [photo-mcp](https://github.com/storytold/photocraft/blob/184c226a76c9ca6234d473912d438feaa48c1cb0/docs/mcp.md)
- [photo-cli-guide](https://github.com/storytold/photocraft/blob/184c226a76c9ca6234d473912d438feaa48c1cb0/book/src/automation/cli.md)
