# Skills and commands

## Choose invocation and context

Prefer `skills/<task>/SKILL.md` for new instructions; retain `commands/` for existing command files. A plugin skill runs as `/plugin-name:skill-name`. Write descriptions distinguishing the task from neighboring skills. [Components](https://code.claude.com/docs/en/plugins/components#skills), [skill reference](https://code.claude.com/docs/en/skills).

| Field | Use |
|---|---|
| `description` | State the task and situations where it applies |
| `disable-model-invocation: true` | Require the user to invoke the skill |
| `user-invocable: false` | Make contextual knowledge model-invoked only |
| `argument-hint`, `arguments` | Explain and name task input |
| `allowed-tools` | Pre-approve relevant tools for the invoking turn; not a sandbox |
| `context: fork`, `agent` | Execute a task in a separate subagent context |
| `background: false` | Wait for a forked task instead of its current background default |
| `model`, `effort` | Select supported execution settings when justified |
| `hooks` | Register lifecycle behavior; inspect its lifetime |

These are Claude Code fields, not universal Agent Skills guarantees. A forked skill does not inherit the conversation history. Current skill hooks persist for the rest of the session once invoked. [Frontmatter and fork behavior](https://code.claude.com/docs/en/skills#frontmatter-reference).

## Example: a user-invoked review brief

Save at `skills/review-brief/SKILL.md`:

```markdown
---
name: review-brief
description: Prepare a review brief from a specified change or diff.
argument-hint: "[change identifier or path]"
disable-model-invocation: true
---

Prepare a review brief for $ARGUMENTS.

1. Resolve the requested change and read its relevant context.
2. State the intended behavior and identify the evidence for it.
3. Record correctness concerns with file references and reproduction steps.
4. Distinguish verified findings from questions requiring a test.
5. Return a brief; do not publish it unless requested.
```

This example leaves tool choice to the session. Add a tool grant only when repeated prompting is a real problem and the exact scope has been reviewed.

## Design supporting references

Put the dispatch procedure in `SKILL.md`. Put detailed schemas, variants, worked cases, and checklists in nearby files linked with a reason to open them. Keep the normal path short enough to leave room for the current request.

Treat `$ARGUMENTS` and positional input as data. If a skill uses dynamic shell preprocessing, inspect its commands: an instruction template is not a shell-quoting mechanism. Prefer helpers receiving structured arguments over interpolation of free text.

Test the full slash name, a natural-language request that should trigger it, and a neighboring request that should not. Then test the resulting artifact. Recognition and task quality are separate failures.

During command migration, verify names, links, arguments, tool grants, and conversation behavior. Do not repeat all shared guidance in every command; let each task load relevant references.
