# Validation record — 2026-10-12

## Executed here

The original Python helper suite passed **32 synthetic tests** on Linux. Tests cover bounded stdout/stderr capture, timeouts, literal argument passing without a shell, exclusive file creation, MCP initialization and pagination, notifications, invalid JSON, wrong response IDs, duplicate/missing schemas, repeated cursors, unsupported protocol revisions, unoffered client capabilities, plan-only behavior, mock recipe execution, original-file preservation and stopping on first failure.

The mocks are local Python subprocesses. They are not Storytold applications and do not establish editor feature correctness. See [the raw test log](validation/helper-tests.log).

The offline collection validator checks JSON/JSONL and Python syntax, frontmatter, the 650-word SKILL ceiling, local links, skill independence, source identifiers, case structure, byte-identical copied helpers and per-file SHA-256 manifests. See [the machine-readable report](validation/report.json).

## Not executed here

All twelve editor CLI names were searched on PATH; none was found. No Storytold application was built or run. The twelve source-reviewed application smoke recipes were **not executed against actual Craft binaries**. Native save/reopen, rendering quality, audio output, formula correctness, PDF sanitization, cross-platform operation and fresh-agent evaluations remain untested in this package's build environment.

The **80 evaluation cases** are authored test plans with expected and forbidden behaviors, not passed LLM tests. They must be run in fresh agent contexts against selected real application versions before reporting a pass rate.

## Source scope

The 47 source records include relevant documentation, selected implementation excerpts and targeted search excerpts. Some responses were truncated; those limits are explicit. The source identities are not a synchronized release lock across repositories. No complete-source audit or proof that every feature is automated is claimed.

## Reproduce

```sh
python tools/validate_collection.py .
python -m unittest discover -s tools -p test_helpers.py -v
```

Each skill's `MANIFEST.json` lists every file of its folder except itself, so a modified skill needs that manifest regenerated before the validator passes. The validator prints to stdout unless `--report` is requested; the stored report was rewritten on 2026-10-13, after the skill folders moved from `skills/` up into the group directory and the collection-level manifest was dropped. Python bytecode caches are excluded from inventory.
