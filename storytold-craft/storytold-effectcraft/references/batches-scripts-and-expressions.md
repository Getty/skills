# Atomic batches versus sequential batches

**Read when:** grouping dependent edits or considering JavaScript/expression automation.

EffectCraft exposes two materially different batching contracts. `batch` drives `engine.batch`, provides result references such as `$N.key`, groups edits into one undo step and rolls back a failing edit batch under its documented atomic behavior. `command_batch` is the common cross-app wrapper: steps execute in order with per-step results and separate undo steps; previous successful edits remain after a later failure.

Choose based on the actual requirement. An atomic in-memory edit group still does not establish rollback of external files, remote work or arbitrary script side effects. Do not describe a renderer or filesystem export as transactional merely because it was triggered inside a batch. Scoped mode rejects result references used to smuggle file paths.

Use returned IDs in later dependent operations. The reference syntax belongs to EffectCraft's batch engine, not a universal JSON or MCP feature. Preserve the actual result path and step indexing from the installed command documentation. In scripts without that native facility, bind returned IDs in the controller rather than writing guessed numbers.

## Expressions and scripting

`set_property.expression` attaches an expression; `run_script` executes a JavaScript scripting object model. These are different lifecycles. An expression may be evaluated repeatedly during rendering and can produce time-varying values even when no explicit key is present. Record the expression text and inspect evaluated properties at relevant times.

Run only reviewed code in an authorized environment. In scoped mode scripts are refused; do not disable confinement automatically. Inspect returned script errors, including source location where provided, and inspect document state before retrying code that may have partially mutated a project. UI windows opened by scripts have their own ScriptUI inspection/interaction tools, but that does not make a script headless-compatible or permitted under every policy.

## Evidence

- [effect-agents](https://github.com/storytold/effectcraft/blob/main/docs/agents.md)
- [effect-mcp](https://github.com/storytold/effectcraft/blob/main/docs/mcp.md)
