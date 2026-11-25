# Codex adapter

Checked: 2026-11-25. Status: **Getty contract proposal v0.2**. Codex is the first host in the getty-bun plan (phase 3a, consumer briefing); nothing below has run yet, and the starters are planned, not built. Read [contract.md](contract.md) for the canonical `package.json` requirement and the starter interface. Facts from the Codex documentation are marked **documented, not executed**; facts read in the Codex source are marked **source-checked** with the commit.

## Contents

- [Run hooks through the starter](#run-hooks-through-the-starter)
- [Hook facts that shape the adapter](#hook-facts-that-shape-the-adapter)
- [Review trust and activation](#review-trust-and-activation)
- [Setup skill and onboarding](#setup-skill-and-onboarding)
- [Distribution surfaces](#distribution-surfaces)
- [Validate the integration](#validate-the-integration)

## Run hooks through the starter

Each Bun-dependent hook carries a POSIX `command` and a Windows `commandWindows`. Proposed shape, **not executed**:

```json
{
  "hooks": {
    "SubagentStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "sh \"${PLUGIN_ROOT}/<starter-dir>/getty-bun.sh\" run <entry>",
            "commandWindows": "powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File \"${PLUGIN_ROOT}\\<starter-dir>\\getty-bun.ps1\" run <entry>",
            "timeout": 600
          }
        ]
      }
    ]
  }
}
```

- `<starter-dir>` and `<entry>` are the consumer's committed paths; `<entry>` is relative to the consumer root, which the starter derives from its own path.
- How Codex runs the two lines, source-checked (openai/codex `3f65e9f`, read by the hub-researcher, hub `agent-developer`, `docs/windows-referenzen.md`, question 2), not executed: Codex replaces `${PLUGIN_ROOT}` (likewise `${CLAUDE_PLUGIN_ROOT}`, `${PLUGIN_DATA}`, `${CLAUDE_PLUGIN_DATA}`) **textually** in the command string before a shell sees it (`codex-rs/hooks/src/engine/discovery.rs:747-749`); the variables are also set in the hook environment. On Windows it takes `commandWindows`, else `command`. `command` runs through `$SHELL`/`/bin/sh -lc`. `commandWindows` runs in the session shell: by default PowerShell (`pwsh`, else `powershell.exe`) as `-NoProfile -Command <line>`, otherwise `cmd /C`. There is no exec form.
- Write `"${PLUGIN_ROOT}"` inside double quotes in both lines: the substituted Windows path carries backslashes and may carry spaces. Keep `commandWindows` valid in PowerShell and in `cmd` alike: a bare `powershell.exe`, double-quoted path arguments, no `&`, `$env:` or `%VAR%`.
- Derived, not measured: under the default session shell a Windows hook starts PowerShell twice (the session shell, then the starter's `powershell.exe`), about twice the 720 ms windows-developer measured for one start. It belongs in the per-hook cost measurement of phase 1 and 3a.
- Derived: since the substitution is textual, a plugin root containing `"`, `$` or `` ` `` (and `%` under `cmd`) breaks the quoting in sh and PowerShell before the starter runs. It belongs in the path tests.
- Do not share this `hooks.json` with Claude Code until its Windows adapter is decided: Claude Code has no `commandWindows` and would run the `sh` line on Windows, which fails without Git Bash (not measured for this line).
- The `timeout` value is illustrative; keep it above `GETTY_BUN_LOCK_WAIT` (default 300 s) plus one download.
- No hook needs a Bun on PATH, and no separate install hook exists: the first hook after a plugin install or update installs.

## Hook facts that shape the adapter

All documented, not executed ([Hooks](https://learn.chatgpt.com/docs/hooks.md)):

| Fact | Consequence |
| --- | --- |
| `command` and `mcp_tool` handlers are supported; `prompt` and `agent` are parsed but skipped. | The starter is a `command` handler. |
| `commandWindows` is an optional Windows-only command override. | Windows gets the PowerShell starter line. |
| Plugin hook commands receive `PLUGIN_ROOT` (installed plugin root) and `PLUGIN_DATA` (writable data); Codex also sets `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA` for compatibility. | Locate the starter from the plugin root; keep the runtime store under `<GETTY_HOME>`, not in plugin data. |
| Commands run with the session `cwd` as working directory. | The starter derives the consumer root from its own path. |
| Multiple matching command hooks for the same event launch concurrently. | Concurrent first hooks wait on the starter's lock; order is no barrier. |
| `timeout` is in seconds; 600 by default for most hooks; `SessionEnd` and `Interrupt` default to 1 s, at most 3 s. | Never put a possibly installing starter call on `SessionEnd` or `Interrupt`. |
| `SessionStart` plain stdout can supply developer context. | stdout belongs to the entry; starter messages go to stderr. |

What Codex does with a non-zero exit other than 2 on `SessionStart` or `SubagentStart` is not documented; measure it in phase 3a. The starter never exits 2 for its own failures; the entry's exit code passes through unchanged.

## Review trust and activation

Installing or enabling a plugin does not trust its hooks. Codex associates non-managed hook trust with the current definition's hash; new or changed definitions are skipped pending review in `/hooks`. [Review and trust hooks](https://learn.chatgpt.com/docs/hooks.md#review-and-trust-hooks) (documented, not executed)

**A plugin update that changes a bundled script needs a new review even if the hook definition stays the same** (documented, not executed). What counts as a bundled script here (the starter, the bundled entry, or both) is measured in phase 3a (plan, "Open decisions"). Expect a re-review after every Bun pin bump (re-rendered starters) and every rebuilt entry, and say so in the consumer's `Changes`.

Prepare concrete files before a required review; never bypass it or mistake natural-language authorization for a persisted trust entry. After edits, use the client's supported reload flow and inspect the active definitions.

## Setup skill and onboarding

Bundle `skills/setup/SKILL.md` for repair and diagnosis ([setup-and-installation.md](setup-and-installation.md)). The portable root `plugin.json` can name it as onboarding skill:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "example-getty-consumer",
  "version": "0.1.0",
  "description": "Example consumer of the proposed Getty Bun contract.",
  "extensions": {
    "com.openai": {
      "onboardingSkill": "./skills/setup/SKILL.md"
    }
  }
}
```

The path is relative to the plugin root. Onboarding runs when the user invokes the setup action after installation; it is not an install hook, and in v0.2 it is not the install path either. The compatibility manifest places `onboardingSkill` in `.codex-plugin/plugin.json`; an inline `extensions.com.openai` object replaces that overlay rather than merging with it. [Plugin packaging and onboarding](https://developers.openai.com/plugins/build/plugins.md#add-an-onboarding-skill) (source-checked manifest example, not a tested plugin). Do not invent a `codex plugin setup` command.

## Distribution surfaces

Current packaging guidance supports lifecycle hooks for manually installed Codex desktop plugins and excludes plugins containing lifecycle hooks from the public plugin directory; the local runtime separately documents hooks supplied by enabled plugins. Treat distribution eligibility and runtime capability as separate checks. [Packaging rules](https://developers.openai.com/plugins/build/plugins.md#bundled-mcp-servers-and-lifecycle-hooks), [local hook discovery](https://learn.chatgpt.com/docs/hooks.md#where-codex-looks-for-hooks). The committed starters and bundle must exist in the execution environment; a plugin installed elsewhere supplies nothing locally.

## Validate the integration

Plan gate for phase 3a: real Codex (0.153.4 on the development machine) with isolated `HOME`, `CODEX_HOME` and `GETTY_HOME`: plugin install, hook trust, the first session installs Bun, the hook's effect arrives (for briefing: a subagent receives its skills). Also check: concurrent sessions (one download), a lock wait that runs out, a wrong `bun` on PATH, a changed starter or bundle triggering re-review, stdout byte for byte, and whether Codex closes stdin after the hook object (claude-mem `4dc8e48` reads one complete JSON object because "Codex can keep stdin open"; not traced in the Codex source; see [dependencies-and-execution.md](dependencies-and-execution.md)). Windows goes as a card to the windows-developer board. Record the Codex version, surface, package format, and distribution route; source and schema checks alone establish neither runtime support nor directory eligibility.
