# REST, WebSocket, and authentication

Choose REST for bounded snapshots/actions and WebSocket for event-driven clients. Verify the explicit configured base URL before attaching a token.

| Need | Surface | Limit |
| --- | --- | --- |
| Availability | `GET /api/` | Trailing slash matters |
| Configuration | `GET /api/config` | Contains sensitive location/system data |
| Loaded states | `GET /api/states` or `/api/states/<entity_id>` | Not a registry export |
| Discover actions | `GET /api/services` | Historical “services” name persists |
| Execute action | `POST /api/services/<domain>/<service>` | Validate target and physical effect |

Writing a state only changes HA's representation; it does not command hardware. Discover actions and use response-data options only where supported. [REST API](https://contributors.home-assistant.io/core/internals/rest-api/).

## Credentials

Bearer access tokens are used for these APIs. OAuth refresh flows and long-lived tokens have different lifecycles. Tokens inherit account permissions; they are not automatically entity-scoped. Use a dedicated account where useful, test actual access, revoke unused tokens, and keep secrets out of command history, source control, and logs. [Authentication](https://contributors.home-assistant.io/core/internals/auth-api/).

If native permissions cannot express a narrow workflow, use a mediated allowlist and identify it as additional architecture. Do not give an administrative token to a model merely to read temperature.

## WebSocket clients

Connect to `/api/websocket`, complete `auth_required` → `auth` → `auth_ok`, and use increasing command IDs. Match results separately from subscription events and check unsuccessful results. The official JavaScript client handles common authentication/reconnect needs. [WebSocket API](https://contributors.home-assistant.io/core/internals/websocket-api/).

After reconnect, reconcile a fresh snapshot because intermediate events may be missing. Never blindly replay non-idempotent actions after a timeout. Bound subscriptions and refresh rate, and never log authentication frames.

## Bundled read-only helper

`scripts/ha_readonly_snapshot.py` uses the Python standard library and only GETs configuration, states, and services. It refuses redirects and outputs version/domain/availability/action counts, discarding attributes and location.

```bash
python3 scripts/ha_readonly_snapshot.py --offline-states /path/to/states.json
```

For live use, provide `HA_BASE_URL` and `HA_TOKEN` securely, then run `python3 scripts/ha_readonly_snapshot.py --live`. `--include-entities` adds IDs/state values, which can disclose occupancy/activity. Review before sharing. TLS verification stays enabled. Explicit local HTTP is allowed but sends the token unencrypted; use HTTPS on untrusted links. The helper does not infer authorization or establish a tunnel.

Verify command feedback separately from HTTP success: some devices queue or optimistically acknowledge actions. Use `home-assistant-automations` for Assist/MCP authority boundaries.
