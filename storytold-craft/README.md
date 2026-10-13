![storytold-craft](../assets/storytold-craft.png)

# Storytold Craft skills

Operating the [Storytold Craft](https://github.com/storytold) applications as an
agent — twelve creative editors that each ship an operator CLI and an MCP server,
plus three integration skills and one overview. These are operator skills, not GUI
tutorials: how to choose the interface, discover the commands the installed binary
actually offers, preserve state and originals, make a bounded edit, verify the
output and recover from an uncertain one.

The editors share ideas, not an API. `--bridge` here is `--connect` there; indexes
are zero-based in one flag and one-based in the next; text offsets are UTF-8 bytes,
time is ticks, samples or seconds; one batch is atomic and its neighbour is not.
Every skill names its own product's rules instead of hiding them behind an invented
common grammar, and each folder is self-contained — install the one you need.

The skills are a source review dated 2026-10-12, written from the products'
documentation and selected implementation excerpts. No Craft binary was run to
produce them: the smoke recipes are source-checked, not executed, and the 80
evaluation cases are test plans, not results. Capture the catalog of the binary you
actually have before you trust a flag.

```bash
skilletor install storytold-photocraft@getty --project   # one editor
skilletor install 'storytold-*@getty' --project          # the whole group
```

## Start here

### [storytold-craft](storytold-craft/SKILL.md)

The overview: which product owns which editable object, and where the products
differ. Its references carry the cross-product tables — routing by task, the CLI
grammar of all twelve editors side by side, MCP startup modes and tool-name
families, filesystem authority per product and mode, persistence and retry
decisions, and the asset contract for a handoff between two editors.

Optional, never a dependency: every product skill works without it.

**Load when** picking the application for a task, or splitting work across several
of them.

## Images

### [storytold-photocraft](storytold-photocraft/SKILL.md)

Layered raster images through `photocraft-cli`: PSD/PSB documents, masks,
adjustments, smart objects and exports. `--cmd` takes a separate `--params`; direct
CLI paths are ambient while scoped MCP gets separately granted read and write
roots; an MCP batch is not atomic; smart-object contents are saved inward to
outward before the parent.

**Load when** editing or exporting layered images with PhotoCraft.

### [storytold-lightcraft](storytold-lightcraft/SKILL.md)

A persistent photo catalog through `lightcraft-cli`: RAW development, originals and
sidecars, exports. A library has one owning process, so a second client connects
instead of opening it again. A move import changes the original files and undo does
not bring them back; CLI render and the MCP export helper default to different
sizes.

**Load when** importing, developing or exporting photos with LightCraft.

### [storytold-vectorcraft](storytold-vectorcraft/SKILL.md)

Vector documents through `vectorcraft-cli`: object queries, transforms, live
appearance, artboard export. Bare `mcp` tries a running app before it falls back,
so deterministic work names `--headless`; `--artboard` is zero-based and `--range`
one-based; an import warning can mean lost content.

**Load when** creating, transforming or exporting vector artwork with VectorCraft.

## Video, motion and audio

### [storytold-filmcraft](storytold-filmcraft/SKILL.md)

Video projects and timelines through `filmcraft-cli`: media health, timing, export
jobs. Time is 254016000000 ticks per second — never frames or seconds by accident.
An export can succeed while drawing offline-media placeholders, and breaking the
stdout pipe cancels neither the run nor a pending save.

**Load when** inspecting, editing or rendering a timeline with FilmCraft.

### [storytold-effectcraft](storytold-effectcraft/SKILL.md)

Motion graphics through `effectcraft-cli`: compositions, layer properties,
keyframes, expressions, render jobs. Keyframe writes default to layer time, not
comp time; `batch` and `command_batch` roll back and undo differently; a render
owns a snapshot that later edits do not reach.

**Load when** animating properties or running render jobs with EffectCraft.

### [storytold-soundcraft](storytold-soundcraft/SKILL.md)

Multitrack audio sessions through `soundcraft-cli`: source media, mixing, routing,
automation, offline bounces. A headless session has no audio device, so a
successful transport proves nothing audible; a session depends on its audio-files
directory; `session.audio_health` is not a loudness or routing audit.

**Load when** editing, mixing or bouncing a session with SoundCraft.

## Documents

### [storytold-designcraft](storytold-designcraft/SKILL.md)

Page layout through `designcraft-cli`: spreads, frames, threaded stories, styles,
publication export. Story offsets are UTF-8 bytes; geometry is spread-space points
with y down; `--page`, `--scale` and `--pdf-options` apply to the exports that
follow them. Rendered text does not prove a story fits — overset is inspected.

**Load when** composing or exporting a layout with DesignCraft.

### [storytold-pdfcraft](storytold-pdfcraft/SKILL.md)

Existing PDFs through `pdfcraft-cli`: reading, organizing, annotating, forms,
editing, securing. Pages and positions are one-based; a document ID belongs to one
live session, so a multistep edit is one script or one MCP session. An incremental
save keeps the previous bytes — an overlay is not a redaction.

**Load when** inspecting, changing or redacting a PDF with PdfCraft.

### [storytold-wordcraft](storytold-wordcraft/SKILL.md)

Structured documents through `wordcraft-cli`: paragraphs and styles, sections,
tracked changes, export. `review.trackChanges` without a value toggles; unknown
character and paragraph properties can be ignored silently, so the result is read
back; `--help` does not exist on every subcommand.

**Load when** writing, revising or reviewing a document with WordCraft.

### [storytold-gridcraft](storytold-gridcraft/SKILL.md)

Spreadsheets through `gridcraft-cli`: cells, formulas, calculation oracles,
round-trip fidelity. XLSB and ODS import can turn formulas into cached values;
`check` exiting zero is not formula coverage; `run` stops at the first failing step
without rolling back the ones before it.

**Load when** editing a workbook or validating its calculation with GridCraft.

### [storytold-deckcraft](storytold-deckcraft/SKILL.md)

Presentations through `deckcraft-cli`: slides, shapes, layouts, export. A PNG
conversion can cover only the first slide; a static render verifies neither
animation nor embedded media; `--save` writes the editable document and an explicit
export writes the delivery.

**Load when** building, inspecting or exporting a deck with DeckCraft.

## CAD

### [storytold-cadcraft](storytold-cadcraft/SKILL.md)

Drawings through `cadcraft-cli`: geometry commands, structured inspection, layouts,
DXF/DWG interchange. Unsupported imported entities are not necessarily kept on
save; model-space units, paper-space points and viewport scale are three things;
command prompts are stateful. A matching SVG or PNG is not dimensional proof.

**Load when** creating or verifying a drawing with CADCraft.

## Integration boundaries

Three products without a verified operator CLI. Their skills exist to stop an agent
inventing one: they describe what the reviewed sources actually expose and where
the automation boundary is.

### [storytold-artcraft](storytold-artcraft/SKILL.md)

The generative desktop workflow and its Rust client. No `artcraft-cli` was found in
the reviewed sources, and a Rust HTTP binding is not a public automation contract.
Generation can upload user content and cost money — both are authorized explicitly.

**Load when** integrating with ArtCraft or judging an automation claim about it.

### [storytold-artcraftx](storytold-artcraftx/SKILL.md)

The experimental Tauri generation application: its IPC boundary and development
lifecycle. The Vite development port is not a generation API, and a registered
Tauri invoke handler is not reachable from outside the app.

**Load when** integrating with ArtCraft-X or working on its development setup.

### [storytold-craft-launcher](storytold-craft-launcher/SKILL.md)

Discovery, installation, version compatibility and update handoffs. The executable
is `artcraft-launcher`; a launcher management CLI was not verified. An installed
GUI does not put a compatible CLI on `PATH`.

**Load when** installing, updating or locating the Craft applications.

## What every folder carries

A `SKILL.md` under 650 words that routes into `references/` by task, a source
ledger and a runtime profile under `assets/`, a verification-record schema with an
example, and `tests/evaluation-cases.json`. The twelve editor skills add
`scripts/`: `capture_capabilities.py` records the binary's command catalog and,
optionally, its headless MCP tool list; `run_example.py` runs the skill's smoke
recipe on a copy of one explicit input. Both print a plan until `--execute` is
given, never call a shell, and are not sandboxes.

## Maintaining the group

Beside the skills, the group keeps what holds them together:

- `tools/` — the canonical copies of the three helper scripts and
  `validate_collection.py`, which checks frontmatter, the word ceiling, local
  links, skill independence, source identifiers, byte-identical helper copies and
  each skill's `MANIFEST.json`.
- [CAPABILITIES.json](CAPABILITIES.json) — machine-readable routing: per product
  the CLI, the catalog command and the hazards.
- [SOURCES.json](SOURCES.json) — the 47 reviewed sources with their identities and
  the limits of each read.
- [VALIDATION.md](VALIDATION.md) and [validation/](validation/report.json) — what
  was executed and what was not.

```sh
python tools/validate_collection.py .
python -m unittest discover -s tools -p test_helpers.py -v
```

A skill's `MANIFEST.json` lists the hash of every file in its folder, so an edit to
a skill needs that manifest regenerated before the validator passes again. After an
upstream release, refresh catalogs with a trusted local binary, re-read what
changed in defaults, security and persistence, and keep the evaluation cases marked
not-run until someone has run them.

The skills and helper scripts in this group carry their own
[MIT notice](LICENSE.md). The Storytold applications, their names and their assets
remain under their own licences and trademarks; nothing of theirs is bundled here.
