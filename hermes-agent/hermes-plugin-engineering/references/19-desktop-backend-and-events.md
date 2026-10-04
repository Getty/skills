# Desktop backend, remote hosts, and events

Separate local UI installation from backend execution. Native Desktop plugins are app-level on the machine running Desktop, even when the selected agent is remote.

The [local root reconciler](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/apps/desktop/electron/desktop-plugins-root.ts) materializes unified local package components into the Desktop plugin root. It does not read a remote gateway's filesystem. Native Windows Desktop and a WSL Python backend therefore need deliberate host-specific placement; that is an inference from the local-root contract, not a special WSL plugin API.

## Unified package

A combined package can contain:

| File | Purpose |
| --- | --- |
| `plugin.yaml` and optional Python entry point | Agent plugin metadata/runtime |
| `desktop/plugin.js` | Local native renderer contribution |
| `dashboard/manifest.json` | Backend API declaration, optionally Dashboard UI |
| `dashboard/plugin_api.py` | FastAPI router exposed under the plugin namespace |

The [Desktop guide](https://hermes-agent.nousresearch.com/docs/developer-guide/desktop-plugin-sdk) explains this composition. Backend `plugins.enabled/disabled`, Desktop enable choices, and any capability grants remain separate. Restart the relevant backend after route import/enable changes when required; a frontend hot reload does not reload Python routes.

## Backend API

Export a FastAPI `router` from the declared API file. Validate bodies, object ownership, paths, deadlines, and side effects on the backend. UI visibility is not authorization.

`ctx.rest('/status')` resolves inside `/api/plugins/<id>/status` on the current connection/profile. The [REST/socket implementation](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/apps/desktop/src/api/plugins.ts) enforces plugin-path rules and connection handling. Keep any data-fetch result associated with the connection/profile it came from; a later user switch must not retarget an old action.

Do not treat a remote persisted file path as a local filename. Use the SDK's authenticated gateway download operation when available and preserve the captured source scope.

## Event bridge

The supported Python bridge is:

```python
from hermes_cli.plugin_events import broadcast_plugin_event

broadcast_plugin_event("text-metrics", "scan.finished", {"document_id": "example"})
```

Listen through `ctx.onEvent('plugin.text-metrics.scan.finished', listener)`. This is an illustrative event, not proof of a completed scan.

The [event implementation](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/plugin_events.py) validates identifiers and dictionary payloads, but delivery is process-specific:

| Calling runtime | Desktop delivery |
| --- | --- |
| `hermes serve` / supported Desktop backend | Connected clients receive the event |
| Isolated Desktop turn child | Host relay can forward it |
| Stdio TUI | Its terminal client is the destination |
| `hermes gateway run`, headless chat, standalone cron | Logged no-op for Desktop delivery |

For work originating elsewhere, persist results in a service/datastore reachable by the Desktop backend or use an explicit authenticated bridge. Do not pretend a Python module global is a cross-process bus.

## Socket fallback

At this snapshot, `ctx.socket` is a no-op on OAuth remote connections. Keep polling or another documented supported event path. Treat notification events as cache invalidation hints; retain a read endpoint for initial load, reconnection, missed events, and authoritative state.

