# Dependencies and execution

Checked: 2026-11-25. **Getty contract proposal v0.2:** the rules below are our integration policy. The starters that execute them are built in agent-bun-runtime (phase 1); the SDK and consumer bundles are not. Read [contract.md](contract.md) for ownership, runtime keys, and the starter interface.

## Ship a bundled entry (normal case)

A consumer commits the output of `bun build --target=bun`: its entry plus `@getty/agent-bun-runtime` and any pure-JS dependency (ADR 0003). User machines download exactly one artifact, the pinned Bun, and never run `bun install`; there is no registry access at hook time.

- Bun documents `--target=bun` as "for bundles that run in the Bun runtime"; such output gets a `// @bun` pragma. Packages are bundled by default; anything marked `external` stays an import resolved at runtime, which a bundled consumer must not have. [Bun bundler](https://bun.com/docs/bundler) (documented, not executed)
- The consumer's CI rebuilds with the pinned Bun and compares byte for byte with the committed bundle.
- Keep `package.json` and `bun.lock` in the repository as build inputs; they are resolved in CI, not on user machines.
- `@getty/agent-bun-runtime` stays bundle-friendly: ESM, no dynamic requires, no filesystem lookups of its own package files. Until its first npm release, consumers pin a git commit of `Getty/agent-bun-runtime` (ADR 0006; the names, ADR 0008); it is a build-time dependency only.
- A consumer that needs native add-ons or runtime-resolved packages cannot bundle; see the later option below.

## Execute through the starter

Hooks and binaries call `getty-bun.sh run <entry> [args...]` or `getty-bun.ps1 run <entry> [args...]`. The starter ensures the slot, then runs the slot's Bun by absolute path with `--no-install`. Never PATH, a `current` link, `bun upgrade`, `bunx`, or a shebang. Bun documents `--no-install` as disabling runtime auto-installation. [Runtime options](https://bun.com/docs/runtime)

- `<entry>` is relative to the consumer root, the parent of the starters' `bootstrap/` directory. Pass the user project as an explicit application argument; the working directory selects nothing.
- stdout belongs to the entry (hook JSON, MCP); starter messages go to stderr. The starter passes stdin and stdout byte for byte, including end of input. It never exits 2 for its own failures (they exit 1); the entry's exit code passes through unchanged. Executed, scenario 8.
- On Windows the entry's exit code arrives as 0–255: Bun 1.4.5 itself exits with the low byte (executed, agent-bun-runtime CI 45589361806). Use codes within 0–255 on every OS, 2 only for the host's meaning of 2.
- No entry argument begins with `-`: under `-File` PowerShell may bind it as its own parameter ([contract.md](contract.md), "Starter interface").
- Bun 1.4.5 on Windows: an empty `Bun.write` to stdout on a pipe fails with `EINVAL` (`ftruncate`) and exit 9, bare and through the starter (executed, agent-bun-runtime CI 45589361806; card `agent-bun-runtime k11`). Write nothing rather than an empty buffer.
- Codex may keep stdin open after the hook object (comment in claude-mem `4dc8e48`, `plugin/scripts/bun-runner.js`; not traced in the Codex source). The starters end when the entry ends even then (`getty-bun.ps1`: executed, scenario 8b; `getty-bun.sh` `exec`s Bun). A measurement point for phase 3a; if it holds, the entry must stop reading at one complete JSON object instead of waiting for end of input, which the plan settles for the SDK.
- Windows: the PowerShell starter runs Bun through `System.Diagnostics.Process` with raw byte copies, never through `&` (measured by windows-developer: Windows PowerShell 5.1 did not pass the end of stdin to a native program). Details in [paths-platforms.md](paths-platforms.md).
- A missing import fails at run time with an actionable error; `--no-install` prevents an on-demand package download. Do not substitute `bunx` or `npx`.
- Start Bun child processes from the entry with the same absolute executable (`process.execPath`, with `--no-install`); audit scripts and shebangs rather than assuming they inherit runtime selection through PATH.
- Preserve exit codes and cancellation; do not report success for skipped or failed application work. Test paths containing spaces and non-ASCII characters, and execution from an unrelated working directory.

## Later/optional: dependency install on the user machine

Plan phase 5, only for the first consumer that cannot bundle. Not part of the MVP and not implemented; the procedure below is kept as the contract for that case.

Ship the real `package.json`, application sources, and `bun.lock`. **Explicitly check that the shipped `bun.lock` exists before installation.** Bun documents that `--frozen-lockfile` can succeed without any lockfile by installing from `package.json`, and can migrate another lockfile in memory; a successful frozen command does not prove the intended lockfile was shipped. [Bun install](https://bun.com/docs/pm/cli/install)

Stage each consumer release in its own content-identified cache outside the user's repositories and the shared runtime store. Include manifest/lockfile digests and runtime key in the install identity. Never share a mutable `node_modules` tree merely because consumers share Bun.

1. Resolve the absolute Bun for the consumer's exact version and target through the starter.
2. Acquire consumer-specific coordination (a consumer lock) before mutating its staged dependencies or binding. The runtime-slot mutex protects neither; see [installation-locking.md](installation-locking.md).
3. With the staged package as `cwd`, run that executable with `install --frozen-lockfile`. Do not regenerate the shipped lockfile on the target machine. Fail on disagreement.
4. Set a reviewed lifecycle-script policy. Use `--ignore-scripts` when compatible. Bun supports `trustedDependencies` and also has a default trusted list; absence of a custom list is not a universal script prohibition. [Lifecycle scripts](https://bun.com/docs/pm/lifecycle)
5. Check native dependencies and generated assets on each supported target. Verify imports and a consumer smoke test, then publish the machine-local binding ([contract.md](contract.md), "Consumer binding").

Which component runs this install (a starter command or the consumer) is not decided; v0.2 adds no starter command for it.
