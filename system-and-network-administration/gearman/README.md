# Gearman engineering skill

An English, standalone agent skill covering Gearman from application contracts to job-server internals. Start at [SKILL.md](SKILL.md); load focused references rather than every chapter.

## Install

Copy the **entire `gearman/` directory** into the skill location used by your agent. This package does not assume a particular agent installation path, install dependencies, activate MCP servers, or modify services. A reasonable repository category is `software/gearman/`; operational references remain part of the same skill.

This README contains no exclusive technical instructions and can be omitted from an agent's context. Deleting it from the package changes the manifest; regenerate the manifest deliberately if maintaining a modified distribution.

## Start locally

```sh
python3 scripts/verify.py
python3 -m unittest discover -s tests -v
python3 scripts/gearman_ops.py inventory
python3 scripts/run_lab.py                 # prints the proposed isolated test plan only
python3 scripts/run_lab.py --execute       # requires an installed gearmand executable
```

Network access, package installation, or a real server is **not** required for the offline tests. The lab runner never connects to an existing server. It starts its own loopback daemon on an ephemeral port and cleans up its processes and temporary storage.

For manual integration use [the lab guide](examples/README.md). See [VALIDATION.md](VALIDATION.md) before interpreting any example as verified against a running Gearman release.

## Package areas

`references/` contains the knowledge; `scripts/` contains read-only tools, the protocol lab, and validators; `examples/` contains programming examples; `assets/` contains schemas and deployment/planning templates; `tests/` contains offline regression tests; `validation/` contains recorded results. [CONTENTS.md](CONTENTS.md) lists every deliverable.

The snapshot date is 2026-10-14. The server source baseline is gearmand 2.1.0. Distribution package versions can differ. Older public documentation is not treated as authoritative for changed defaults.
