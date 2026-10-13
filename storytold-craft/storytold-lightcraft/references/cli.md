# CLI operations and their output defaults

**Read when:** building shell workflows or selecting between catalog operations, rendering, merge and model services.

## Discover before constructing a command

Capture both `commands --json` and `controls --json`: command IDs and develop-slider ranges are different catalogs. `run` accepts multiple command IDs followed by `key=value` or JSON-object arguments. A token without `=` starts another command unless it is part of the parser's documented JSON form. Use argument arrays or script files to prevent shell quoting errors.

```sh
lightcraft-cli render input.dng -o developed.png --set light.exposure=0.5
lightcraft-cli run --import input.dng develop.set control=light.exposure value=0.5 \
  app.export path=preview.jpg longEdge=1600
```

`run --script FILE` reads JSON lines containing `{command,params}` or control `{method,...}` forms; `--script -` reads stdin. It normally stops after a command failure; `--keep-going` requests continuation. Each reply reports the command, success/error, result and timing. A run without a persistent library is not a durable catalog edit.

## Different render surfaces have different defaults

The direct `render IN -o OUT` command defaults to full cropped size. `--size` sets the long edge; `--set` adjusts controls; `--settings` merges develop JSON; `--preset` applies a discovered preset. `--opt KEY=VALUE` forwards an export option, including color space, bit depth and metadata policy. Some options can send output to another application such as Apple Photos; those are side effects requiring permission, not merely image encoding.

The MCP `export` helper has a different default: a 3000-pixel long edge. Use an explicit size in reproducible work and `longEdge:0` there for native cropped resolution. Do not infer either default from the other interface.

## Other operator surfaces

`snapshot` renders the full UI without a window/GPU using CPU-rasterized egui. Its script uses control methods, not develop-only command steps, and can continue after failed requests while returning an overall failing status. A UI snapshot is not a full-resolution photo export.

`merge` supports HDR, panorama and HDR-panorama. Without preview-only mode it writes a derived file beside the first source. `calibrate` can write camera profiles into the active user's profile directory. `denoise-serve` runs a network service. Route these operations to their dedicated reference and authorize their filesystem, model-download or network consequences before execution.

## Evidence

- [light-cli](https://github.com/storytold/lightcraft/blob/main/apps/lightcraft-cli/src/main.rs)
- [light-mcp](https://github.com/storytold/lightcraft/blob/701f78ea2e586d4748705f10fdf5c4181dc1fd49/docs/mcp.md)
