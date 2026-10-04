# Instructions, configuration, and scope

Distinguish three things:

| Mechanism | Purpose | Incorrect use |
|---|---|---|
| `AGENTS.md` | Working instructions for a project or user | Treating prose as a security boundary |
| `SKILL.md` | Task-selected workflow | Loading all procedural documentation on every task |
| `config.toml` and managed requirements | Runtime defaults and enforced constraints | Shipping a plugin that silently rewrites global policy |

Codex builds its `AGENTS.md` chain from global instructions and project-root-to-working-directory instructions. `AGENTS.override.md` can replace a same-level `AGENTS.md`; closer project instructions appear later. Discovery is bounded by the configured document limit. [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

Current configuration precedence places CLI overrides above trusted project layers, selected profile files, user config, cloud-managed defaults, system defaults, and built-ins. Requirements constrain permitted settings. Do not apply ordinary last-wins assumptions to every setting family; hooks and policies can have different merge behavior. [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)

## Project plugin state

For a local-marketplace plugin, a documented project configuration is:

```toml
[plugins."release-review@engineering-tools"]
enabled = true
```

This is an enablement setting, not a marketplace manifest or proof of authentication. Verify the trusted project and effective setting with the current [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

## Generic implementation procedure

1. Read existing instructions and configuration in the target scope.
2. Change the narrowest scope that solves the requested problem.
3. Preserve unrelated user defaults and comments where possible.
4. Record which host actually reads the changed file.
5. Test both a matching directory and a nearby directory outside the intended scope.
6. Report managed constraints that prevent a local preference from taking effect.

Keep plugin-specific user settings in a documented plugin/backend configuration mechanism. Use an explicit schema for those settings and explain where they live. Avoid treating arbitrary keys in the host's global config as a plugin-owned database.

Use environment variables for runtime indirection only where the relevant loader supports them. JSON placeholders, shell variables, YAML dependency fields, and TOML strings are different languages.
