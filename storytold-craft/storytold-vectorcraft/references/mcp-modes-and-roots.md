# Explicit MCP mode selection and filesystem policy

**Read when:** starting VectorCraft safely or investigating file-access refusals.

Bare `vectorcraft-cli mcp` first tries the live app on 127.0.0.1:7979 and can fall back to headless. This is unsuitable when an unattended job must never attach to a person's open document. Use `mcp --headless` explicitly for isolation, or `mcp --connect HOST:PORT` explicitly for a known live session, then inspect identity.

Headless mode has a CPU renderer and no live window tools. UI inspection, text entry into the live interface and whole-window screenshots have different availability from engine edits and document rendering. Do not equate “everything is a command” with every UI tool working headlessly.

## Optional root policy

`--automation-read-root` and `--automation-write-root` activate confinement for headless MCP and imply headless mode. They cannot accompany `--connect`; a connected desktop must enforce its own roots at launch. Without either confinement flag, the reviewed guide describes the existing unconfined behavior, not PhotoCraft's deny-without-roots policy. Configure explicit roots rather than relying on defaults.

When scoped, an omitted read or write root grants none of that access. Roots must exist. Paths are made absolute against the server's working directory before containment checks, unlike PdfCraft's root-relative paths. Use absolute paths within approved roots to avoid ambiguity. Links are followed and escaping links are refused. The checks are not a race-proof defense against another hostile local process swapping links.

Confinement covers linked images, relinking, presets, templates, color profiles, font-search paths and many save/export/package operations, not just `open_file`. Some application-owned settings/recovery directories are explicitly outside the agent-named-path policy. Treat the roots as a documented authority restriction, not a complete OS sandbox.

The guide's statement suggesting one root configuration works across the suite is not a reliable universal contract: FilmCraft rejects those flags, and other apps differ in defaults and path resolution. Keep per-product launch descriptors.

## Evidence

- [vector-mcp](https://github.com/storytold/vectorcraft/blob/main/docs/mcp.md)
- [vector-cli](https://github.com/storytold/vectorcraft/blob/main/apps/vectorcraft-cli/src/main.rs)
