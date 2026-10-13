# CLI scripts and order-dependent export options

**Read when:** constructing a page-layout batch or exporting several variants.

`commands FILTER` emits JSON discovery data; `describe ID` narrows it to one command. `run` accepts an input `.designcraft`/`.idml` file or `--sample`, followed by repeated `--cmd 'ID=JSON'` operations and explicit exports. `script FILE|-` uses the engine's command-script language and can save/export after the script.

```sh
designcraft-cli run --sample --export working.designcraft --all-pages previews/
designcraft-cli commands frame
designcraft-cli describe frame.create
```

`--page`, `--scale` and `--pdf-options` apply to exports that follow them. This is a sequencing contract, not a global unordered option map. Preserve argv order in a job planner and capture the effective options for each output. A single `--export` and `--all-pages DIR` have different coverage; confirm actual page count.

Native `.designcraft` preserves the working document model. IDML is an interoperability format; do not infer support for opening an InDesign `.indd` binary from IDML support. PNG/JPEG, PDF and EPUB deliveries lose or transform different aspects of the editable model.

The CLI also exposes `app --port PORT COMMAND JSON` or `--method METHOD JSON` for a live desktop, and `mcp` for a headless/connected agent. These are not interchangeable with `run`'s file/save lifecycle. Benchmark/performance subcommands can be expensive and are not necessary for routine capability discovery.

`validate-pdf FILE.pdf` runs the built-in PDF/X-4 checks. Record exactly which validator ran; it is not a blanket guarantee that every publishing requirement, font license, accessibility requirement or printer-specific profile is satisfied.

## Evidence

- [design-cli](https://github.com/storytold/designcraft/blob/main/apps/designcraft-cli/src/main.rs)
- [designcraft-readme](https://github.com/storytold/designcraft/blob/main/README.md)
