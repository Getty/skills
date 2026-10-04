# Compatibility and evidence record

Create a task-local record before committing to version-sensitive behavior. This template is an analysis artifact, not plugin metadata.

```yaml
checked_on: "YYYY-MM-DD"
target:
  client: "Codex CLI | desktop Codex | IDE | Codex Cloud | ChatGPT Work"
  client_version: "observed value"
  runtime_version: "observed value"
  os: "observed platform"
  orchestration: "local | cloud | unknown"
  execution: "local | remote | hosted"
package:
  format: "portable-agent-plugins | codex-compatibility"
  revision: "reviewed revision"
  distribution: "local | repo | workspace | public"
capabilities:
  required: []
  optional: []
evidence:
  local: []
  official_urls: []
  runtime_tests: []
unverified: []
```

## Evidence order

Inspect the available executable help and schemas to establish what that installation exposes. Read relevant code when available and necessary. Then open current official pages for product semantics, limitations, and publication rules.

Use documentation excerpts to locate the full page; do not base an implementation on search snippets alone. Follow redirects to canonical current pages. If a claim is disputed, record both the source version and observed behavior.

When the task concerns a release newer than the installed runtime, do not silently use local absence as proof the feature does not exist. Conversely, new web documentation does not upgrade the local installation.

## Classify findings

| Label | Meaning |
|---|---|
| Documented | Current primary source explicitly supports the claim |
| Locally verified | A named test succeeded on the recorded environment |
| Implementation detail | Source-code behavior without a stable product promise |
| Experimental/draft | Explicit opt-in or evolving protocol |
| Design proposal | Suggested architecture, not a built-in feature |
| Unknown | Evidence is insufficient |

Version-sensitive refresh targets include plugin support by host, hooks and unsupported fields, MCP protocol/auth, configuration precedence, public submission rules, and app-server methods.

Do not record usable credentials, complete personal configuration, or raw sensitive transcripts in compatibility reports. Record only the values needed to reproduce the behavior.

A capability can be documented but untested. Keep those statuses separate in the final handoff.
