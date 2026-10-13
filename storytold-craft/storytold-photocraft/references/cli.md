# CLI grammar and persistent headless sessions

**Read when:** choosing a PhotoCraft subcommand, constructing argument vectors, or deciding whether state survives.

## Choose the execution surface

`commands --json` supplies the current registry; `--filter TEXT` narrows it. `info FILE --compact` returns document structure and warning data. For a bounded edit use `run`; for multiple documents use `batch` or `droplet`; for a stateful agent conversation use MCP or `serve`. A new process is not a continuation of the previous process's document IDs or history.

```sh
photocraft-cli info source.psd --compact
photocraft-cli commands --json --filter adjustment
photocraft-cli run source.psd --cmd image.adjustments.invert --out edited.pcraft
photocraft-cli convert edited.pcraft preview.png
```

`run` takes a positional input or `--new JSON`. Each `--params JSON` belongs to the preceding `--cmd ID`. Do not translate this into another Craft application's `--cmd 'ID=JSON'` convention. Parameters must be an object; discover the actual fields before construction. Repeated commands execute in order and print their JSON results. A successful edit without `--out` does not establish durable output.

`convert IN OUT` chooses formats from extensions unless `--format` is supplied. JPEG/WebP quality is 1–100. WebP with an explicit quality is lossy; without quality it is lossless in the reviewed implementation. TIFF is flattened unless `--tiff-layers` is requested. TGA's 24/32-bit option changes alpha handling. These are output semantics, not interchangeable quality knobs.

## Batch/action boundary

`batch --actions FILE --in DIR --out DIR` accepts action lists made from command IDs, `[id, params]` pairs, or `{command, params}` steps. Named action sets may require `--action NAME`; retain the whole set when actions call other actions. `droplet FILE.pcdroplet FILE_OR_DIR...` is another executable action container, not an inert image asset. Treat both as untrusted instructions until reviewed.

Direct CLI operations use ordinary OS paths. The `run` parser does not accept MCP filesystem-root flags. Same-directory batch output requires explicit `--in-place`; do not add it to silence a refusal. CLI syntax errors and unknown flags are usage failures, not successful no-ops.

## Long-lived JSON-lines mode

`serve` keeps one headless session on stdio, or loopback TCP with `--port`. Its method family is the control-style `engine.execute`, `doc.*`, `jobs.*`, `batch`, `methods`, not MCP `tools/call`. Use `methods` and `engine.commands` to discover both layers. Filesystem authority and TCP authentication must be configured separately. Never send an MCP initialize frame to this control protocol.

## Evidence

- [photo-cli](https://github.com/storytold/photocraft/blob/184c226a76c9ca6234d473912d438feaa48c1cb0/apps/photocraft-cli/src/lib.rs)
- [photo-cli-guide](https://github.com/storytold/photocraft/blob/184c226a76c9ca6234d473912d438feaa48c1cb0/book/src/automation/cli.md)
