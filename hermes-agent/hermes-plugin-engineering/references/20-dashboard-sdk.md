# Web Dashboard extensions

Use the [Dashboard extension guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/extending-the-dashboard) for the browser administration interface. Native Desktop ESM is a different contract.

A Dashboard UI component normally lives in `plugins/<name>/dashboard/`, with `manifest.json`, a prebuilt JavaScript bundle, and optional CSS/API file. The bundle uses `window.__HERMES_PLUGIN_SDK__` and registers through `window.__HERMES_PLUGINS__`. This is not `@hermes/plugin-sdk` loaded from a native Desktop disk directory.

## Choose the contribution

Use a theme for appearance only. Use a tab/route for a standalone management screen. Use a documented shell or page slot to augment an existing surface. Replacing a built-in page is more tightly coupled; justify it and test upgrades.

Keep manifest name, registration name, declared entry path, and backend namespace consistent. Bundle the format required by this frontend. Do not assume the Dashboard will compile TypeScript/JSX or resolve a disk plugin's bare imports.

## Shared backend

The optional `plugin_api.py` exports FastAPI routes mounted below `/api/plugins/<name>`. Native Desktop may use the same backend namespace while providing a different renderer. Sharing business/data access code is useful; sharing UI module assumptions is not.

Design one backend model with explicit read/write operations. Validate authorized profile/account/resource context on the server. Avoid leaking another profile through global caches or unscoped persistent paths.

Use declared route files and the relevant enablement/restart behavior. A frontend rescan finding the manifest does not establish that Python routes were imported.

## Diagnostic sequence

Check manifest discovery first, then bundle/CSS fetch, registry registration, component render, backend route availability, and requested operation. Use browser console/network evidence to distinguish a missing bundle from a rejected API call.

Run actual tests for:

- A standalone route and any contributed slot.
- Missing API, disconnected backend, and authentication failure.
- Refresh and rescan without duplicate registrations.
- Profile/connection change during an in-flight read.
- Long content, empty data, and unsafe-looking HTML in returned text.
- Backend write denial even if the UI control is visible.

Maintain separate frontend support entries for Dashboard and Desktop. If only one is tested, say so and keep the other optional.

