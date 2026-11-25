# Codex adapter

Checked: 2026-11-25. Status: **Getty contract proposal v0.1**. The provider is not implemented or released by this skill. Read [contract.md](contract.md) for the canonical `package.json` requirement and runtime contract.

## Contents

- [Package an explicit setup skill](#package-an-explicit-setup-skill)
- [Use hooks only on supported surfaces](#use-hooks-only-on-supported-surfaces)
- [Keep hooks independent of setup](#keep-hooks-independent-of-setup)
- [Review trust and activation](#review-trust-and-activation)
- [Validate the integration](#validate-the-integration)

## Package an explicit setup skill

Bundle `skills/setup/SKILL.md`. For the portable root `plugin.json`, the documented onboarding metadata has this shape:

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

The path is relative to the plugin root. Setup runs when the user invokes the setup action after installation, in a new or existing conversation. The field is not an automatic installation hook. The compatibility manifest places `onboardingSkill` in `.codex-plugin/plugin.json`; an inline `extensions.com.openai` object replaces that overlay rather than merging with it. [Plugin packaging and onboarding](https://developers.openai.com/plugins/build/plugins.md#add-an-onboarding-skill)

Treat this as a source-checked manifest example, **not an end-to-end tested plugin**. Verify that the target surface exposes onboarding. If it does not, document direct invocation of the packaged setup skill using the target client's actual skill name. Do not invent a `codex plugin setup` command or assume CLI onboarding UI parity.

Write setup instructions that can be followed before Bun exists. Resolve the package's declared requirement through [contract.md](contract.md), install or reuse only the required version/target, provision frozen dependencies, and verify the actual runtime. Respect authorization already established in the session.

## Use hooks only on supported surfaces

Current packaging guidance supports lifecycle hooks for manually installed Codex desktop plugins and excludes plugins containing lifecycle hooks from the public plugin directory. Separately, the local runtime documents hooks supplied by enabled plugins. Treat distribution eligibility and runtime capability as separate checks. [Packaging rules](https://developers.openai.com/plugins/build/plugins.md#bundled-mcp-servers-and-lifecycle-hooks), [local hook discovery](https://learn.chatgpt.com/docs/hooks.md#where-codex-looks-for-hooks)

Prefer a setup skill without lifecycle hooks when that fits the delivery surface. If hooks are necessary, establish the supported surface and deployment path before authoring them. Hook scripts must exist in the execution environment; a plugin installed elsewhere does not supply a local executable by implication.

## Keep hooks independent of setup

The inspected hook documentation supports `command` and `mcp_tool`; `prompt` and `agent` handlers are parsed but skipped. `SessionStart` plain stdout can supply developer context. Matching command hooks run concurrently, so array order is not a sequencing barrier. `commandWindows` supplies a Windows command override. [Hook behavior](https://learn.chatgpt.com/docs/hooks.md)

For Getty integration:

1. Use a tiny hint adapter that already runs on the target. It may direct the agent to `skills/setup/SKILL.md`; it must not require the Bun being installed.
2. Emit conditional instructions, not a cached assertion that setup is complete. Context injection does not itself run the setup skill.
3. Keep readiness checks in each actual Bun-dependent execution path. Resolve an absolute executable under `~/.getty/runtimes/bun/<version>/<target>/bin/bun` or `bun.exe` in the current environment.
4. Use `--no-install` on normal runtime calls. Dependency installation and runtime upgrades belong to setup/provisioning, not recurring hooks.
5. Gate only this consumer's functionality while unready. Do not block the shell, reads, or edits required for setup. Do not assume another matching hook has completed installation.
6. Quote paths for the actual host shell, keep executable/arguments separate where supported, and resolve package files from the plugin root rather than the user's current working directory.

## Review trust and activation

Installing or enabling a plugin does not trust its hooks. Codex associates non-managed hook trust with the current definition's hash; new or changed definitions are skipped pending review. The CLI exposes `/hooks` to inspect and trust them. [Review and trust hooks](https://learn.chatgpt.com/docs/hooks.md#review-and-trust-hooks)

Prepare concrete files before a required native review. Do not bypass that review or mistake prior natural-language authorization for a persisted hook-trust entry. After edits, use the installed client's supported reload/activation flow and inspect the active definitions. Do not promise that a mid-turn file edit has already taken effect.

## Validate the integration

Record the exact Codex version, surface, package format, and distribution route. Check onboarding discoverability or the named-skill fallback, untrusted and changed hook behavior, missing Bun, concurrent sessions, Windows paths, wrong runtime target/version, and an interrupted setup. Observe the selected absolute executable and confirm normal hooks perform no dependency installation. Source/schema checks alone do not establish runtime support or public-directory eligibility.
