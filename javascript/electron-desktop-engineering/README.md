# Electron desktop engineering

Version **1.0.0** · primary-source review snapshot **2026-10-15** · all operative content in English.

**36 topical references plus an index, 18 catalog entries, 43 reviewed primary-source entries, 82 packaged files.** Catalog entries have explicit depth: workflow/comparison/discovery. Neither catalog size nor source count implies complete upstream API coverage or installed compatibility.

## Contents

Process/renderer/preload boundaries, capability-oriented IPC, custom protocols/CSP, navigation/permissions, files/data/secrets, native ABI, workers, multi-window and OS integration, performance/debugging, packaging, signing/notarization, fuses, updates, release operations, and React integration.

Start with [SKILL.md](SKILL.md). The [reference index](references/00-index.md) routes to individual chapters. Use [templates and machine-readable assets](assets/README.md), [offline tools](scripts/README.md), [sources](SOURCES.md), and [validation evidence](VALIDATION.md). Examples: [Constrained Electron shell](examples/secure-shell/README.md) and [React bridge adapter](examples/react-adapter/README.md).

## Install

Extract the complete `electron-desktop-engineering/` directory into the skills location configured for your agent. Keep the folder name, `SKILL.md`, references, assets, scripts, examples, and tests together. This package does not require a particular proprietary tool namespace or an external memory service.

**README is optional human guidance.** The agent's operative instructions and routing are in SKILL.md and its linked resources. Copying only SKILL.md breaks progressive loading and removes examples/tools.

No dependency install is required to read the skill or run its pure Node/Python tests. Framework/desktop examples require separate reviewed dependency installation and the validation stages their README describes.

## Use selectively

Load SKILL.md, inspect the actual project, then open two to four relevant references. Do not paste the entire reference directory into every prompt. Use `python scripts/library_lookup.py TERM` to find a library route. A discovery-only entry must be researched against official installed-version documentation before generating concrete integration code.

## Offline verification

From this directory:

```sh
node --test tests/policy.test.cjs
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/validate_bundle.py
```

For the declaration-only TypeScript contract fixture, with TypeScript installed:

```sh
tsc --noEmit --strict --module NodeNext --moduleResolution NodeNext --target ES2022 --lib ES2022,DOM tests/type-contracts.ts
```

The declaration check does not typecheck React/Electron integrations or execute the JavaScript implementation. Read [VALIDATION.md](VALIDATION.md) for actual commands, results, and unexecuted checks.

## Integrity and maintenance

[MANIFEST.json](MANIFEST.json) records SHA-256 for every packaged file except itself. The separately delivered archive checksums cover the ZIPs. Generated dependency/build/cache directories are excluded from the local verifier; modifying source/package files intentionally invalidates the original manifest. Refresh versions, advisories, peer/ABI compatibility, and licensing before adoption or upgrades. The original material is provided under [MIT](LICENSE); upstream projects retain their own licenses.
