# Worked design recipes

Use these as architectural patterns and acceptance criteria. The choices are engineering recommendations derived from the supported contracts; they are not preinstalled Hermes features.

## 1. Shared text-metrics operation

Implement the deterministic handler and native registration from [tools and commands](03-tools-and-commands.md). Expose the operation to the model and as an explicit slash command. If a UI is needed, add a backend endpoint and a separate Desktop or Dashboard view.

A minimal illustrative backend API is:

```python
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()

class CountRequest(BaseModel):
    text: str = Field(max_length=20000)

@router.post("/count")
async def count_text(body: CountRequest):
    return {
        "characters": len(body.text),
        "words": len(body.text.split()),
    }
```

Declare that API file using the relevant dashboard/backend manifest contract. This is a complete route fragment with no external side effects, not a complete distributable plugin. Use one shared counting implementation in a production package to avoid divergence.

Acceptance: the same input produces the same result through tool, command, and API; the API rejects oversized input; no frontend receives another profile's data.

## 2. Telegram topic triage

Start with topic/skill configuration when domain instructions suffice. Add a plugin only if the feature needs deterministic triage, custom event handling, or auxiliary model calls. For a classifier use `ctx.llm`; for actual agent work use normal gateway dispatch or permitted injection.

Keep incoming text untrusted. A classification result can suggest an action but cannot independently grant the sender new permissions. Keep topic identity and sender scope through the entire flow.

Acceptance: a denied sender cannot trigger inference-heavy side work or the external action; two topics remain isolated; unavailable classification has a defined fallback.

## 3. Desktop monitor for gateway/cron work

Persist job status in a service or profile-scoped datastore. Serve reads through an enabled backend plugin API. Register a local Desktop pane and scope each read/result to its source connection/profile.

Use supported events only for processes that can reach the frontend. Retain polling. A gateway/cron call to `broadcast_plugin_event` alone cannot notify Desktop.

Acceptance: an event-free completion appears on the next read, switching backends never presents stale data as current, and disabling the pane releases subscriptions/timers.

## 4. Tool policy plus observability

Use request middleware for deterministic rewrites and the host's supported pre-tool/approval mechanism for enforcement. Use observer hooks for redacted outcomes and request correlation. Avoid policy in a callback whose errors fall through to execution.

Acceptance: the human sees the effective operation, a downstream failure is not hidden, and the tool never runs twice when an execution wrapper fails after completion.

## 5. Channel-native action plus business service

Keep authorization, idempotency, and operation state in one backend service. Present a Telegram callback, Slack action, or Desktop control as a thin client. Bind the proposal to actor, account, target, and expiry.

Acceptance: a copied callback token or changed resource ID cannot execute another user's proposal, duplicate delivery does not repeat the operation, and the result remains queryable after a process restart.

## 6. Portable knowledge plus native capability

Put genuinely shared skill/MCP components in a portable package. Keep Hermes lifecycle, providers, and UI integration native. Maintain independent manifests and compatibility evidence when also supporting Claude Code or Codex.

Acceptance: each host discovers only its supported components; an unsupported native feature has an explicit diagnostic or optional omission rather than a fabricated compatibility claim.

