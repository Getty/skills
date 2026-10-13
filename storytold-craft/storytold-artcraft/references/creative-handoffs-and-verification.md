# Handoff from generation to specialized editors

**Read when:** moving generated assets into an editable Craft workflow.

Choose the next editor by the required operation: raster compositing to PhotoCraft, RAW/catalog development to LightCraft, vector cleanup to VectorCraft, timeline editing to FilmCraft, motion/composition work to EffectCraft, page layout to DesignCraft, or audio editing to SoundCraft. These are workflow recommendations, not claims of a universal shared project file.

Transfer an explicit asset bundle: media file, source/request provenance that may be shared, dimensions or duration, frame/sample rate where applicable, alpha/color interpretation, and any known limitations. A generated image/video is not automatically a layered or semantically editable document. Do not claim preserved scene structure unless an actual interchange representation was exported and reopened successfully.

Validate the consuming editor independently. Discover its installed CLI/MCP interface, import the actual file, inspect warnings and render/bounce a bounded sample. A successful ArtCraft generation does not prove that another application's decoder supports the output's particular codec/profile.

Preserve private prompts, credentials and source material according to the user's sharing intent. A public creative asset need not include the full private generation transcript. For reproducibility record only the necessary approved provenance and disclose when a remote provider cannot promise exact deterministic regeneration.

Finish with evidence tied to actual operations: what was generated, through which verified interface, what was transferred, which application reopened it, and which content/format checks passed. Do not count a proposed integration or code reading as a completed generation.

## Evidence

- [artcraft-readme](https://github.com/storytold/artcraft/blob/main/README.md)
- [artcraft-client](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_client/AGENTS.md)
