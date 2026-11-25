# Claude Code adapter

Checked: 2026-11-25. Status: **Getty contract proposal v0.2**. Claude Code follows Codex in the getty-bun plan (phase 3b, first consumer skilletor); no Claude Code adapter through the starter has run yet, and the starters themselves are planned, not built. Use [contract.md](contract.md) for the canonical declaration and the starter interface.

## Contents

- [Run hooks through the starter](#run-hooks-through-the-starter)
- [Windows: open decision](#windows-open-decision)
- [Optional repair hint](#optional-repair-hint)
- [Review activation and validate](#review-activation-and-validate)

## Run hooks through the starter

Every hook that needs Bun calls the committed starter, which installs the pinned Bun on demand and then runs the bundled entry. Proposed shape for Linux (macOS later), **not executed**:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "sh \"${CLAUDE_PLUGIN_ROOT}/<starter-dir>/getty-bun.sh\" run <entry>",
            "timeout": 600
          }
        ]
      }
    ]
  }
}
```

- `<starter-dir>` and `<entry>` are the consumer's committed paths; `<entry>` is relative to the consumer root, which the starter derives from its own path.
- Set `timeout` explicitly on every starter hook, above `GETTY_BUN_LOCK_WAIT` (default 300 s) plus one download; 600 is illustrative. Documented ([hooks reference](https://code.claude.com/docs/en/hooks), "Common fields"): command hooks default to 600 s, lowered to 30 s on `UserPromptSubmit`, `PreModelSwitch` and `PostModelSwitch` and to 10 s on `MessageDisplay`.
- Never put a starter call on `SessionEnd`: its hooks share a 1.5 s budget, and a timeout set on a plugin-provided hook does not raise it (documented, hooks reference, "SessionEnd").
- Quote `"${CLAUDE_PLUGIN_ROOT}"` in shell form. Measured by windows-developer (Git Bash shell form): unquoted, a path with spaces breaks with exit 127; quoted, it survives. Exec form (below) needs no quoting.
- Matching hooks run concurrently ([hooks reference](https://code.claude.com/docs/en/hooks)); neither array order nor a prompt hook is a setup barrier. The starter's lock is the barrier: after a plugin install or update the first hooks wait on it and exactly one downloads.
- stdout is the entry's hook JSON; the starter writes only stderr, never exits 2 for its own failures, and passes the entry's exit code through unchanged. Measured by windows-developer: Claude Code passes stdout through unchanged and reports a non-zero exit with stderr verbatim.
- Do not make any hook require a Bun found on PATH, and do not add a separate install hook: the starter is the only installer.

## Windows: open decision

Documented ([hooks reference](https://code.claude.com/docs/en/hooks), "Exec form and shell form"; looked up by the hub-researcher, hub `agent-developer`, `docs/windows-referenzen.md`, question 1):

- With `args` a command hook runs in **exec form**: `command` is resolved on `PATH` and spawned without a shell; `${CLAUDE_PLUGIN_ROOT}` is substituted as a plain string into `command` and every `args` element. On Windows `command` must resolve to a real `.exe`. Exec form exists since 2.1.139 (source-checked, `anthropics/claude-code` `4cc5e8b`, `CHANGELOG.md`).
- Without `args` it runs in **shell form**: `sh -c` on Linux and macOS, Git Bash on Windows, PowerShell when Git Bash is not installed; `"shell": "powershell"` selects PowerShell explicitly.
- `hooks.json` has no per-OS field: none among the documented command hook fields, none in the CHANGELOG. One entry must start on Linux and on Windows alike.

Measured by windows-developer (Claude Code 2.1.287, `docs/hook-start-windows.md`). Git Bash could not be hidden on that machine, so the PowerShell fallback was measured with `"shell": "powershell"` per hook as a stand-in. **Windows without Git for Windows is not measured.**

- Shell form with Git Bash present runs `sh`; `getty-bun.sh` would then forward to `getty-bun.ps1`. The target, though, is Windows **without** Git Bash.
- Exec form with `command: "sh"` depends on the Claude process's PATH; started from PowerShell, `sh` is not found. Exec form on an extensionless script fails with ENOENT, on a `.cmd` with EINVAL.
- Windows-only entries start too: exec form `powershell -NoProfile -ExecutionPolicy Bypass -File ...` (probe x9; the hooks reference shows the same call as its Windows example), `cmd /c ...` (x10), `node` plus a script (x8). None serves Linux from the same entry: `powershell.exe` and `cmd` are Windows programs, and the getty-bun chain has no Node.
- Of the entries that start on Linux and on Windows from one `hooks.json`, two remain without Git Bash: exec form on an extensionless path with a `.exe` next to it (Claude Code starts the `.exe`, probe y1), or a dot-sourced `.cmd` polyglot in shell form (probe q6 under the `"shell": "powershell"` stand-in, r6 under Git Bash), which pays a PowerShell start (about 720 ms) per hook. Their Linux side was not part of these probes.

Options in the plan ("Open decisions"): a tiny native shim (like winlaunch, built reproducibly with zig, x64 only) that runs the slot's Bun directly and calls `getty-bun.ps1` only to install, or the polyglot. A shim that starts Bun itself must read the pin block, detect the target and check the fast path: a third reader beside the two starters, part of the open decision. The owner decides before phase 3b, with the per-hook cost measured in phase 1. Until then, ship no Claude Code Windows adapter, share no `hooks.json` with Codex ([codex.md](codex.md)), and claim no Claude Code support on Windows.

## Optional repair hint

The setup skill is for repair and diagnosis, not installation. Where the target supports native mods, a small mod may point the agent to it without requiring Bun. A mod uses `.claude-plugin/plugin.json`, `hooks/hooks.json`, and a module exporting `register(on, options)`; the module path is relative to `hooks/hooks.json`. [Mods reference](https://code.claude.com/docs/en/plugins/mods/reference)

In `hooks/hooks.json`:

```json
{
  "modules": ["./register.js"]
}
```

In `hooks/register.js`:

```javascript
/** @type {import("claude-code").Register} */
export const register = (on) => {
  on("prompt.context", async ($, event, next) => {
    const base = await next(event);
    const root = $.plugin.root;
    const name = `${$.plugin.name}:getty-bun-repair`;
    return {
      ...base,
      blocks: [
        ...base.blocks.filter((block) => block.name !== name),
        {
          name,
          text:
            `This plugin's hooks install and run the shared, pinned Bun. ` +
            `If they report a getty-bun failure or stay silent, read ` +
            `${root}/skills/setup/SKILL.md to diagnose and repair within ` +
            `the current session's authorization. This is guidance, ` +
            `not a report that the runtime is ready.`,
        },
      ],
    };
  });
};
```

The API shape was checked against `Register`, `CoreEngineInterface.plugin`, `Events['prompt.context']`, and `PromptContextResult` in the [published declarations at commit fa0dece](https://github.com/anthropics/claude-code/blob/fa0dece70669a54b3104c618de9eebaaa78af19f/mods/types/claude-code.d.ts) (source-checked). **It has not run in a Claude Code client.** `prompt.context` is computed for conversation context and cached; a block already sent is not a live status channel, so keep the text conditional. Do not submit automatic setup turns: installation already happens in the hooks.

## Review activation and validate

Respect workspace trust and the client's hook controls. After editing manifests or hook code, follow the client's supported reload flow and inspect which definition is active; a file write alone does not prove activation. [Claude Code hook behavior](https://code.claude.com/docs/en/hooks)

Validate with isolated `HOME` and `GETTY_HOME` and exercise: Bun absent (the first `SessionStart` installs); two simultaneous sessions (one download, both run); a lock wait that runs out (clear stderr, no partial slot); a wrong `bun` on PATH (ignored); a mismatching slot (fails closed); a plugin path with spaces; hook stdout byte for byte; exit-code passthrough. Record client versions and results; do not promote the proposed hook shape to a tested adapter without those observations. Windows checks go as cards to the windows-developer board.
