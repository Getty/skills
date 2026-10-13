# Launcher scope and product identity

**Read when:** finding/installing the specialized Craft editors.

The repository is named `craft-launcher`, while the product executable is `artcraft-launcher`. Its documented catalog covers the twelve specialized editors: PhotoCraft, LightCraft, VectorCraft, FilmCraft, EffectCraft, DesignCraft, PdfCraft, WordCraft, GridCraft, DeckCraft, CADCraft and SoundCraft.

The launcher discovers appropriate release assets and installs/updates/starts applications. That does not make it their document-editing API. Use each editor's verified CLI/MCP after installation rather than trying to issue document operations through the launcher.

No `craft-launcher-cli` management interface was verified in the reviewed sources. Developer `cargo xtask` commands are build/release tooling, not an operator package-management contract. Do not invent `install --all`/`update --silent` commands from familiar package-manager conventions.

Treat catalog entries as installation choices, not proof of local availability. Record which package was actually installed, OS/architecture, version, binary location and whether a separate CLI asset is needed. The default branch may contain capabilities newer than the installed release.

When no authorized GUI/management interface is available, provide the verified package/location procedure rather than claiming to have installed or updated anything. This skill is an installation/update handoff skill, not a fictional remote-control layer.

## Evidence

- [craft-launcher-readme](https://github.com/storytold/craft-launcher/blob/main/README.md)
- [launcher-xtask](https://github.com/storytold/craft-launcher/blob/1aaf7b27be2dba970d1a77f96aef6aad52352730/xtask/src/main.rs)
