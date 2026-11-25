---
name: getty-bun-integration
description: Use when an agent plugin or tool must run TypeScript on Getty's shared per-user Bun runtime (getty-bun) — declaring the Bun version in package.json, writing the setup adapter for Claude Code or Codex, or reviewing such an integration.
---

# Getty Bun Integration

Build integrations against **Getty contract proposal v0.1**. Treat this skill as an engineering specification and reusable references. It does not install Bun, supply a runtime manager, or establish that a `getty-bun` executable exists.

## Inspect the actual integration

1. Inspect the consumer repository, existing provider, package manifests, release process, and target agent client. Follow repository instructions and preserve unrelated work.
2. Identify the execution environment: native Windows, macOS, Linux, WSL distribution, remote host, or container. Record the client version and distribution surface.
3. Read [the contract](references/contract.md). If an implementation exists, inspect its API and map it to this contract. Report mismatches; do not invent commands or silently migrate a live store.
4. Establish authorization from the session. Continue authorized setup and reversible engineering work. Prepare concrete changes before required host trust/review; do not bypass it.

## Preserve the invariants

- Declare one exact runtime requirement in the consumer's real `package.json`: `gettyBun.contractVersion` and `gettyBun.bunVersion`. These are Getty metadata, not built-in Bun behavior.
- Share one verified installation per exact **version and target within one execution environment**. Use immutable versioned slots outside consumer plugin caches. Keep the executable named `bun` or `bun.exe`.
- Bind execution to a resolved absolute executable. Do not use PATH discovery, shell startup files, a mutable `current` link, or `bun upgrade` as the runtime contract.
- Keep initial setup possible before external Bun or Node exists. A host instruction adapter points the ordinary agent to setup instructions; context injection does not complete installation.
- Recheck readiness at actual execution boundaries. Gate this consumer's dependent work while keeping the agent's setup tools usable.
- Hold a verified OS-backed mutex throughout shared installation mutations. Use `.installing` for PID, process name, process start identity, and attempt diagnostics. Never remove a suspected stale lock based only on process metadata.
- Provision dependencies explicitly from shipped `package.json` and `bun.lock`. Run ordinary TypeScript entry points with the selected executable and `--no-install`.
- Stage and verify new versions alongside old ones, then rebind only the consumers being updated. Retain still-referenced runtimes and the last working binding.

## Implement in order

### 1. Declare ownership and supported targets

Use [contract.md](references/contract.md) and [paths-platforms.md](references/paths-platforms.md). Put the runtime pin in the consumer package, integrity data in the provider, and machine bindings in local state. Verify the release's actual artifacts and OS/CPU/ABI requirements; agent-client support does not prove Bun or dependency support.

Merge [package.fragment.json](assets/package.fragment.json) deliberately; its version is illustrative. Validate the Getty object using [requirement.schema.json](assets/requirement.schema.json). Preserve unrelated fields and select a version actually tested by the consumer.

### 2. Package setup instructions and host adapters

Read [setup-and-installation.md](references/setup-and-installation.md). Adapt [setup-skill-template.md](assets/setup-skill-template.md) into a real consumer setup skill; replace every template token with inspected implementation details.

- Claude Code: read [claude-code.md](references/claude-code.md) for native instruction injection and classic-hook limits.
- Codex: read [codex.md](references/codex.md) for onboarding, hook support, trust, and distribution constraints.
- Hermes or another host: apply the common contract and inspect current official interfaces. This skill ships no verified Hermes-specific hook adapter.

Use the smallest adapter that already executes on the target. A missing-runtime check must not require that runtime. Treat host API examples as source-checked until exercised in the actual client.

### 3. Implement transactional provisioning

Read [installation-locking.md](references/installation-locking.md) before writing installer or recovery code. Keep the real lock owner alive through publication; confine external workers to unique staging directories. Make verification, publication, and binding updates inspectable. A prompt's completion message is not an installation receipt.

### 4. Package dependencies and execute

Read [dependencies-and-execution.md](references/dependencies-and-execution.md). Resolve the consumer package independently of the user's working project. Check that a shipped lockfile exists before frozen installation. Separate application output from setup logs, use argument arrays where available, and test spaces in paths and missing imports.

### 5. Handle updates and retention

Read [updates-and-retention.md](references/updates-and-retention.md). Treat runtime and consumer updates separately. Preserve rollback. Do not add automatic garbage collection until consumer references and active executions can be accounted for reliably.

### 6. Verify and deliver

Use [verification.md](references/verification.md) and [integration-review-template.md](assets/integration-review-template.md). Run the cases needed to substantiate claimed host/platform support. Separate source inspection, schema validation, scenario reasoning, and actual runtime tests.

Deliver concrete changes, exact runtime requirements, supported/tested targets, setup entry point, update behavior, and remaining gaps. Never describe the provider as installed or cross-platform tested merely because this skill exists.

## Research and rationale

Read [prior-art.md](references/prior-art.md) for OpenClaw, mise, pnpm, and metadata compatibility. Read [prior-art-plugins.md](references/prior-art-plugins.md) for inspected AgentPulse, GStack, and Claude-mem implementations. Use [sources.md](references/sources.md) when APIs or platform claims need refreshing.

Attribute external facts. Mark Getty paths, fields, locking policy, and lifecycle rules as our proposal. Treat partial precedents as partial; do not claim another project implements the complete Getty contract.
