# State, concurrency, and lifecycle

Treat one plugin instance as potentially serving multiple concurrent sessions and profiles. Determine whether state belongs to the installed package, active profile, session, turn, external account, or local Desktop app.

The [native context](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/plugins.py) exposes `plugin_id`, `profile_name`, `get_config`, `set_config`, `state`, `on_unload`, `spawn_task`, and host services. Prefer these to `ctx._cli_ref` or hardcoded paths.

## Settings versus durable state

Use `ctx.get_config(key, default)` / `ctx.set_config(key, value)` for plugin-relative operator settings. Use `ctx.state.get` / `ctx.state.set` for bounded JSON state. The [state implementation](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/plugins_state.py) supplies profile scoping, atomic writes, locking, and quotas.

An atomic single-key set does not make a read-increment-write sequence transactional. For counters or multi-record workflows, use a properly scoped datastore with transactions or a host-supported atomic operation after verifying it exists. Keep durable schema versions and migration functions in plugin-owned state.

Avoid storing secrets, entire transcripts, or large binary artifacts in a small JSON state store. Keep reproducible caches separate from durable user data.

## Lifetime management

Use `ctx.on_unload(callback)` for cleanup and `ctx.spawn_task(coroutine)` when a running async loop exists. Host-supervised tasks can be cancelled on unload/reload. Do not start one from synchronous registration merely because the method exists.

Close files, clients, sockets, and queues. Make cleanup idempotent and bounded. Do not assume a timeout terminates a Python thread: avoid blocking work that cannot be cancelled. Test repeated loading to detect duplicate callbacks and background-task growth.

## Child agents

The [public subagent lifecycle service](https://hermes-agent.nousresearch.com/docs/developer-guide/subagent-lifecycle-api) is `ctx.subagent_lifecycle`. It accepts `SubagentLaunchRequest` during an active parent turn and provides launch/status/wait/cancel/result/reconnect operations.

Use opaque returned handles; never synthesize them. Narrow child toolsets. Cancellation is a request until a terminal result is observed. The documented snapshot retains execution metadata in-process; after a process restart, reconnect cannot resurrect a lost child. Do not advertise durable workflows from serializable handles alone.

For work that must survive process loss, design a durable job record, an idempotent operation, and reconciliation that distinguishes incomplete from complete work.

## Profile context

Resolve paths and secrets at the operation's scope. A global `os.getcwd()`, environment cache, module-level client, or bare background thread can select the wrong profile. When a provider offers a context-preserving worker helper, use it; otherwise explicitly propagate the intended context and verify isolation.

