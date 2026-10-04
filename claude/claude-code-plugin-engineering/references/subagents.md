# Plugin subagents

## Define a delegation contract

Use an agent when work benefits from bounded context, specialist instructions, or a separate result. Define the input the caller supplies and the evidence the agent returns. Avoid giving several agents the same general description.

Original `agents/evidence-reviewer.md`:

```markdown
---
name: evidence-reviewer
description: Inspect a proposed change and report concrete correctness evidence.
tools: Read, Grep, Glob
model: inherit
maxTurns: 12
---

Inspect only the requested scope and the surrounding code needed to assess it.
Return findings with location, consequence, evidence, and a suggested
verification. If evidence is missing, label the item as a question. Do not edit.
```

Use tools actually available on the target. This omits a shell rather than pretending that removing `Write` makes a shell-enabled agent unable to change files.

## Respect plugin-specific restrictions

Plugin agents are namespaced. The current loader ignores their `permissionMode`, `hooks`, `mcpServers`, and `initialPrompt` frontmatter. Define plugin hooks and MCP servers through their own component mechanisms. Supported fields include tools, model/effort, turn limit, skills, memory, background, and worktree isolation. [Plugin agent fields](https://code.claude.com/docs/en/plugins/components#frontmatter-fields-in-plugin-agents).

Runtime filtering also limits tool availability. Background agents receive a narrower built-in tool set; listing a removed tool does not restore it. Preloaded skills inject their full content. A normal subagent's context differs from a conversation fork. Check current nesting limits rather than assuming agents can never spawn agents. [Subagents](https://code.claude.com/docs/en/sub-agents).

## Design state and concurrency

Use a handoff containing scope, verified inputs, output shape, and stop conditions. Avoid passing an entire conversation when a brief suffices; also avoid assuming the agent knows a decision never placed in its context.

Choose persistent memory only when cross-session learning is needed. Separate reusable knowledge from transient task data. Keep credentials and person-specific assumptions out of definitions and memory.

If parallel agents write, assign disjoint ownership or isolate worktrees. Check the actual worktree base; do not assume it begins at the caller's uncommitted state. Plan how the parent incorporates changes and handles interruption.

## Verify results as well as spawning

Test the scoped name, tools, model, input visibility, evidence, and bounded turn limit. Include missing-context and impossible-task cases. Mark an interrupted or turn-limited result partial; let the parent decide what remains.

To use a specialist as the main session agent, inspect the plugin's supported `agent` setting and precedence. This selects session behavior, not organization permissions.
