# Memory and context providers

Select memory for knowledge retained across conversations. Select a context engine for what enters a request and how a conversation is compacted. Select a plain retrieval tool when the user wants explicit lookup without automatic persistence.

## Memory provider contract

Follow the [MemoryProvider guide](https://hermes-agent.nousresearch.com/docs/developer-guide/memory-provider-plugin). Implement the ABC, register the provider with its own loader, and select it through `memory.provider`. The external provider selection is single-active; general-plugin precedence does not apply.

Use initialization context: profile home, session identity, platform, logical workspace, gateway identity, and primary/cron/subagent scope when supplied. Do not use a generated session title as a verified person identifier.

Keep availability checks passive. Make turn synchronization nonblocking and preserve profile context when offloading. The documented helper `spawn_context_thread` exists because a bare thread does not inherit context variables.

Define what is persisted: user statements, assistant summaries, tool outputs, or derived facts have different evidential meaning. Keep provenance and deletion semantics. Do not silently mix conversations from different people in a shared external namespace.

## Context engine contract

The [ContextEngine guide](https://hermes-agent.nousresearch.com/docs/developer-guide/context-engine-plugin) defines token accounting, compression decisions, message transformation, and optional lifecycle/selection methods. Activation uses `context.engine`; loading a package alone does not choose it.

Preserve valid message and tool-call/result structure. Keep the current user request and necessary instructions. Test model changes, long tool output, manual compression, resumed sessions, and context-window errors. Define how state clones for another agent; copying a live database connection or lock is not meaningful cloning.

Optional per-turn selection is different from compression. Do not trigger artificial compression just to run retrieval every turn when the supported engine offers a dedicated selection hook.

## Durable evidence before compaction

If a provider promises to archive direct evidence before lossy compaction, use the documented checkpoint contract and test its enforcement. The optional v2 checkpoint mode can require a durable commit before compaction; older best-effort hooks do not provide that guarantee. A required checkpoint without a capable active provider blocks progress.

Make writes idempotent because retries can present overlapping transcripts. Separate direct messages from earlier summaries. Verify every compaction authority involved; a delegated external agent may own its own compaction and bypass a Hermes-local hook.

## Evaluation

Compare retrieval quality, unrelated-session leakage, recall latency, token cost, write amplification, deletion behavior, and restart recovery. Include adversarial-looking quoted text and misleading summaries so a stored claim does not automatically become an instruction.

Document whether stored data leaves the machine, retention, identity mapping, and account ownership as concrete behavior. For UI management, expose a scoped backend route and separate Desktop/Dashboard contributions instead of coupling storage to a frontend.

