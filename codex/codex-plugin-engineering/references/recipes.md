# Design recipes

These are original architectural suggestions. Each requires verification against the selected host and sources before implementation.

## 1. Documentation workflow

**Need:** Reuse a research procedure over trusted technical documentation.

**Shape:** Skill plus references; optional documentation MCP when current information is needed.

Define source order, query scope, output format, and uncertainty handling. The official OpenAI Docs MCP is available at `https://developers.openai.com/mcp`. [Docs MCP](https://developers.openai.com/learn/docs-mcp)

Test a direct question, an ambiguous topic, absent documentation, and an outdated local reference. Avoid hard-coding model names into unrelated tasks.

## 2. Business system with controlled changes

**Need:** Search records, prepare a change, and apply an authorized update.

**Shape:** Skill + authenticated MCP server.

Use stable IDs, revision checks, explicit mutations, and structured receipts. Keep account/tenant validation in the server. A UI is optional; add it if comparing or editing a proposal materially helps.

Test permission revocation between read and write.

## 3. Project-specific execution checks

**Need:** Inspect a supported tool operation before it executes.

**Shape:** Narrow hook plus backend/host enforcement where needed.

Capture the actual event and use the documented response. Avoid pretending to parse arbitrary shell semantics. Keep the feature useful when another execution path is outside hook coverage.

Test denial, timeout, unsupported fields, and a nonmatching operation.

## 4. Review dashboard for Codex work

**Need:** Own a UI for threads, progress, approval, and cancellation.

**Shape:** App-server client with explicit user identity and session ownership.

Use generated schemas, correlated requests, and supported notifications. A native plugin can add domain tools, but the dashboard itself remains an external application.

Test disconnect/reconnect during a long-running operation.

## 5. Incoming-message automation

**Need:** React to a message or external state change.

**Shape:** Supported MCP Events host, or an application-operated messaging bridge plus SDK/app-server.

Define which user authorized which trigger and response. Keep inbound content separate from authority. Include deduplication, queue limits, and loop prevention.

Test cancellation and revoked sender/resource access.

## Selection rule

Choose the fewest moving parts that meet the required input, output, authority, and host constraints. Do not add a server just for a checklist, a hook just for reusable prose, or a custom client just to install a tool.
