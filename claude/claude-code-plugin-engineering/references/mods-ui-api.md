# Mod UI, state, and service API

## Render for the surface that exists

Use `ui.render` and `$.ui.resolve(e)` to produce supported elements. Match the intended component and, for a pane, its own request ID. Check `e.surface` and measured dimensions. A replacement of a shared render site can hide another mod's output unless the downstream tree is preserved. [Interface guide](https://code.claude.com/docs/en/plugins/mods/interface).

Design a functional text fallback for hosts that run the handlers but do not render mod UI. Keep the primary action available as a command if the user may operate from headless or IDE sessions.

For a dashboard or status mod:

- Collect data outside the render callback; render a bounded snapshot.
- Show an observation timestamp and distinguish unavailable from empty data.
- Keep state changes explicit and redraw only affected sites.
- Use stable identifiers for controls; test keyboard and narrow-window behavior.
- Retain the host's actual result and permission information when restyling rows.

The current API supports panes, bands, controls, and many transcript/render sites, but not rewriting the permission prompt. Verify element support per terminal/Desktop surface; arbitrary HTML or a browser DOM is not implied. [Rendering inventory](https://code.claude.com/docs/en/plugins/mods/reference#render-sites).

## Choose state by lifetime

| State | Use |
|---|---|
| Module variables | Cheap transient observations that may reset on reload |
| `$.state` | Reactive values that should survive module reload in the session |
| `$.store` | Plugin data shared across sessions on the machine |
| External store | Durable multi-user records, transactions, and strong concurrency |

`$.state` requires typed declarations; a store `get` followed by `set` is not an atomic increment. Distinct keys avoid some collisions but do not provide transactions. [State and concurrent saves](https://code.claude.com/docs/en/plugins/mods/interface#keep-state).

## Reach services through the supported API

The mod API includes namespaces for files, processes, HTTP, MCP, models, prompts, commands, tools, agents, session data, timers, and state. The module has no direct Node filesystem/network APIs. Use `$.process.run` with an argument array and inspect its result; use `$.http.fetch`'s documented return object rather than assuming a native Fetch `Response`. [Mods API](https://code.claude.com/docs/en/plugins/mods/api#reach-files-processes-and-the-network).

Use `$.model.complete` for a separate bounded request and `$.model.fork` when the current conversation is required. Validate the returned status rather than assuming every model call returns text. These calls use the session's credentials and consume model usage. Assign a token, latency, and frequency budget.

## Background work and messaging

Use `$.clock` timers for ongoing work and account for reload cleanup. A UI log/status can update without starting a model turn. `$.prompt.submit` schedules a turn; awaiting it while a turn is still running can create a dependency cycle. Prefer attributed submissions, and do not use `asUser` to misrepresent remote or plugin-generated input. [Background work](https://code.claude.com/docs/en/plugins/mods/api#run-work-in-the-background).

For inter-session messages, validate the intended target and inspect delivery status. A display name is not authentication. Bound polling, deduplicate events, and prevent two sessions from triggering each other indefinitely. Use service-side controls for message authorization that must survive host or plugin changes.
