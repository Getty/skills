# Codex SDK and non-interactive automation

Use SDK/CLI automation for jobs owned by an external program. Choose app-server for a custom interactive client.

The current TypeScript package is `@openai/codex-sdk`. Its documented thread interface includes starting, running, continuing, and resuming local Codex threads. The SDK is server-side and has its own runtime requirements. [Codex SDK](https://learn.chatgpt.com/docs/codex-sdk)

Original conceptual example:

```typescript
import { Codex } from "@openai/codex-sdk";

const codex = new Codex();
const thread = codex.startThread();
const review = await thread.run(
  "Review the supplied release evidence and report missing checks."
);
console.log(review.finalResponse);
```

Pin the dependency and inspect current options before making this executable in a target project. This example is not a sandbox, authentication, or deployment setup.

## CLI jobs

`codex exec` supports non-interactive execution, JSONL events, and structured final output options. Normal final text and progress use distinct output streams. [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)

A bounded example is:

```sh
codex exec --sandbox read-only --json "Assess the supplied release evidence."
```

Configure credentials and policy for the job separately. Capture exit status and the documented terminal event, not only the last line of output.

## Orchestration design

Create an explicit job envelope: authorized task, input revision, workspace, identity, timeout, concurrency limit, expected artifacts, and output schema. Deduplicate jobs triggered by repeated webhook deliveries.

Use isolated workspaces for concurrent edits. Define cancellation and cleanup, and retain only necessary logs. A retry may repeat side effects; use operation IDs and inspect prior state before retrying.

Test a task with missing dependencies, failed authentication, denied permissions, malformed structured output, and interrupted execution.

A CI wrapper is an application, not a native plugin handler. It may install or invoke a plugin if the target host supports that route, but that dependency should be explicit and separately verified.
