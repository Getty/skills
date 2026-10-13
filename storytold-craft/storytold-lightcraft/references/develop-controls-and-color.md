# RAW development, process versions and white balance

**Read when:** changing exposure, color, crops or presets without silently changing the rendering interpretation.

Begin with `get_develop` and `list_controls`. Retain the reported process version, current settings and source metadata as a baseline. Develop settings depend on the process implementation and source characteristics; blindly copying a parameter object between revisions is not an appearance guarantee.

`set_develop.values` maps control IDs to numbers and uses the control path's interpretation. `settings` merges partial develop JSON instead. Record which form was used. A missing field means retain current state, not reset to a default. Preset application similarly needs a discovered preset ID, amount and explicit target photo set.

## White balance has two scales

For RAW sources with color matrices, slider values for `wb.temp`/`wb.tint` use Kelvin interpretation; elsewhere the reference scale is relative, with 6500 representing as-shot. A direct `settings.wb` object without `scale:"kelvin"` uses the relative interpretation even on a RAW image. Two numerically identical temperature fields can therefore mean different edits. Preserve the source's scale and compare a neutral region after changes.

## Crops and coordinate spaces

The crop helper takes a normalized rectangle `[x0,y0,x1,y1]`; do not substitute pixel bounds or UI-screen coordinates. Angle changes keep the crop when it fits, otherwise shrink it to fit the rotated source. The control-value path fits crop changes, while a raw settings merge is applied as supplied rather than using that same fitting logic. Inspect the resulting crop and export dimensions instead of assuming the requested rectangle survived unchanged.

## Review in controlled increments

For an adjustment chain, record the initial image, apply one conceptual change, and compare a bounded preview using fixed output dimensions. Check highlights, shadows, skin/neutral tones and edge behavior appropriate to the brief. These are operator acceptance rules, not claims of numerical identity with another RAW processor. Preserve the original RAW and the settings/process information necessary to reproduce the result.

## Evidence

- [light-mcp](https://github.com/storytold/lightcraft/blob/701f78ea2e586d4748705f10fdf5c4181dc1fd49/docs/mcp.md)
