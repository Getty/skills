# Exports, progress, cancellation and delivery gates

**Read when:** rendering a sequence or recovering from an uncertain export outcome.

A direct engine/MCP `file.exportMedia` call with `wait:true` waits for the file while the job interface remains available. Without waiting, retain the returned job/path and poll `jobs.list`; cancellation uses the job interface or the supported MCP request cancellation path. The `_meta.progressToken` belongs to the MCP request metadata, not an invented codec setting.

Progress messages are throttled. A missing early ETA does not mean a stalled export: `etaSeconds` can be null until enough progress has been measured and while non-frame work is occurring. A completed transport response and a completed encoder job are different states when the call is asynchronous.

The engine/MCP result may report success while `offlineMedia` is nonempty. Treat that as a content-health exception. By contrast, the high-level CLI's export/render normally returns a failing status for such content unless explicitly allowed. Capture both status and semantic warnings in a job record.

## Cancellation and retries

Supported cancellation stops at an encoding boundary and cleans partial outputs produced by that job, including associated frames/caption sidecars where applicable. Do not generalize this cleanup to every export command. After a timeout, inspect the job and output before restarting; a second export may overwrite or duplicate a still-running result. A cancelled MCP request may intentionally receive no final response.

## Acceptance matrix

Check container/codec, actual frame count, duration, frame rate, dimensions, audio streams, channel layout and output range. Compare first/last frames, edit boundaries, effect-heavy frames, titles/captions and representative audio. Do not validate color work solely from an editor screenshot. Confirm that the saved project reopens with the intended sequence, no unresolved media exceptions and the same material edit decisions.

Return the editable project, dependency manifest, requested render, inspection evidence and unresolved limitations as separate artifacts. Never label an output production-ready solely because the encode process exited zero.

## Evidence

- [film-agents](https://github.com/storytold/filmcraft/blob/main/docs/agents.md)
- [film-cli](https://github.com/storytold/filmcraft/blob/main/apps/filmcraft-cli/src/main.rs)
