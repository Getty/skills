# Observability and troubleshooting

Diagnose the first failed boundary. A loaded plugin, registered tool, connected bot, responsive HTTP server, and functioning feature are different observations.

| Symptom | Check first | Next evidence |
| --- | --- | --- |
| Plugin absent from list | Effective home/profile, layout, manifest, category, project opt-in | Discovery log and parser diagnostic |
| Listed but inactive | Enable/deny state, selected provider, dependency admission | Activation result and import error |
| Loaded with missing tool | Registration rejection, schema, toolset exposure, duplicate name | Actual tool registry for that surface |
| Works in CLI but not gateway | Private CLI reference, scope, missing gateway process/context | Hook payload and active profile |
| Native command works but button fails | Native handler wiring/pattern/authorization | Channel update fixture and callback result |
| Other profile's files/account used | Global cwd/env/client cache, lost thread context | Profile-bound home, secret provenance, target IDs |
| Desktop pane absent | Local plugin root, ESM parsing/imports, ID match, enable decision | Renderer error and registered contributions |
| Desktop panel has API 404 | Correct backend/profile, route declaration, backend enable/restart | HTTP route inventory |
| Desktop misses completion event | Producer process, correct event prefix, remote OAuth socket | Poll/read endpoint and actual event transport |
| Cron cannot deliver on custom platform | Process-local adapter assumption | Standalone sender and target resolution |
| Memory/session mix-up | Routing key vs conversation ID, group/thread policy | Source identity and persistent namespace |

## Useful diagnostics

Use `HERMES_PLUGINS_DEBUG=1 hermes plugins list` for detailed discovery on a trusted machine. Use `hermes plugins doctor <path-or-id> --ci` for actual registration. Use the target build's gateway status command to identify the service/process actually handling traffic. See the [plugin guide](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins) and [gateway guide](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/).

Do not print an entire configuration, environment, authentication cache, or raw callback object merely to find a key. Select the smallest redacted diagnostic fields.

## Trace the right spans

The [observer contract](https://hermes-agent.nousresearch.com/docs/developer-guide/observer-hooks) distinguishes turn, API attempt, tool call, auxiliary request, and child session. Record IDs, timestamps, outcome, bounded error category, and relevant model/provider. Do not compare turn latency directly to one provider request.

Measure startup/import latency separately from first call, hot call, platform queueing, inference, external operation, and final delivery. A desktop connection indicator can remain healthy while a specific agent turn is stalled.

## Concurrency and leaks

Use two profiles and two sessions to expose global-state bugs. Repeat load/reload/disable/reconnect and count listeners, tasks, sockets, and registered tools. Include background workers and failed startup cleanup.

For a blocking plugin, capture thread/event-loop evidence before restarting where supported. A network retry loop, CPU-heavy callback, and deadlock need different fixes. Use bounded queues and explicit dropped/failed work accounting.

## Recovery report

State the failed boundary, evidence, smallest repair, validation result, and residual limitation. Avoid “reinstall everything” when a wrong home, denied capability, missing native handler, or absent event bridge explains the failure.

