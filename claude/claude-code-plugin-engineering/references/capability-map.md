# Capability map

## Separate packaging from behavior

A plugin packages components into one discoverable, installable unit. Choose a component for its execution semantics, then choose a plugin for distribution. A collection of instructions does not acquire deterministic enforcement merely by being packaged. The official [plugin overview](https://code.claude.com/docs/en/plugins/overview) and [components guide](https://code.claude.com/docs/en/plugins/components) are the starting contracts.

| Mechanism | Engineering use | Boundary to check |
|---|---|---|
| Skill | Teach a repeatable procedure or contextual knowledge | Model invocation, loaded context, available tools |
| Command file | Preserve an existing named Markdown prompt | Legacy layout and namespacing |
| Subagent | Delegate a bounded task with its own instructions | Context handoff, available tools, background restrictions |
| Settings-style hook | React to a documented lifecycle event | Exact input/result schema and blocking behavior |
| MCP | Expose typed operations from a service or process | Transport, authentication, scoped tool names |
| LSP | Supply language diagnostics and navigation | Binary availability, protocol, claimed extensions |
| Mod | Add in-process event middleware and UI | Target build's generated types, host rendering, authority |
| Workflow | Express a repeatable graph of agent work | Structured outputs, concurrency, interruption, budget |
| Monitor | Observe a process throughout an interactive session | Lifetime, notification volume, provider availability |
| Channel | Deliver external events into a live session | Explicit enablement, authenticated sender and conversation routing |

## Make the design decision concrete

Write: “When **trigger** occurs, **component** receives **input**, produces **result**, and may perform **authorized effects**.” Then test the mechanism against the failure path.

For example, a repository review helper could be one skill with optional evidence supplied by MCP. Add a subagent only if isolation or independent review improves the task. Add a hook when an event must trigger a deterministic check. Add a mod when the requirement needs its in-process API or interface. Avoid four competing ways of performing one action.

Choose an external application or the Agent SDK when the job needs a lifecycle independent of the interactive client. Keep a durable server or scheduler responsible for delivery; let the plugin translate that service's state into the current session.

## Define an observable contract

Record these before implementation:

- Invocation: human command, model selection, lifecycle event, timer, or external message.
- Inputs: trusted configuration versus untrusted project or remote content.
- State: request, agent, session, project, user, or service scope.
- Effects: files, tools, external writes, network, model usage, and messages.
- Failure: skip, deny, retry, mark partial, ask, or queue for later.
- Evidence: artifact or trace that proves the requested behavior occurred.

Use that contract in tests and the release description. Do not claim a feature only because a similarly named hook, setting, or SDK method exists.
