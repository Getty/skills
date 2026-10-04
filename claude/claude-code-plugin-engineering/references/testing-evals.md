# Testing, native mod tests, and behavioral evals

## Match each check to a claim

| Layer | Useful evidence | Limit |
|---|---|---|
| Package | JSON/YAML parses, paths resolve, native validation passes | No behavior has run |
| Pure contract | Fixtures verify parsing, decisions, transforms and errors | Host loading/order is untested |
| Native mod test | Middleware responds correctly to controlled events | Effects are stubbed |
| Host integration | The installed component receives an event and produces the expected effect | One host/version/permission state |
| Behavior | Representative tasks succeed with acceptable time/cost | Model outputs vary; compare baselines |

Use the smallest checks resolving the actual risk. A new paragraph in a skill rarely needs a full model eval suite; an authorization interceptor needs meaningful negative and failure cases.

## Validate the package first

```bash
claude plugin validate ./change-companion --strict
```

Native validation reports structural problems and can inspect mod registrations without executing the mod. Its documented exits distinguish success (`0`), validation failure or strict warnings (`1`), and unexpected failure (`2`). Do not substitute generic JSON parsing for it. Conversely, validation is not exhaustive runtime proof: for example, the separate `.lsp.json` file has a validation blind spot. [Validator](https://code.claude.com/docs/en/plugins/cli-reference#plugin-validate), [component-specific validation](https://code.claude.com/docs/en/plugins/components).

Check all referenced files, executable requirements, schema versions, and relative paths. For scripts, separately test stdout protocol purity, nonzero exits, timeout, cancellation, empty input, and malformed data. The [command-hook fixture](hooks-command-contracts.md) is an original small example of this separation.

## Use the native mod test kit for middleware

The current kit discovers `.test.ts` files in a plugin, loads each test with a fresh module, and runs without a real session, sign-in, network, or tool effects. Put an actual assertion in every test. Register all stubs before the first event call. Engine events return their event result; API stubs usually return `{ value: ... }`. `session.start` does not fire automatically. [Native test contract](https://code.claude.com/docs/en/plugins/mods/test).

Original `tests/read-meter.test.ts` for [the read-meter module](mods-runtime.md):

```typescript
import { expect, test } from 'claude-code/testing';

test('records success and denial without changing their results', async ($, on) => {
  on('tool.call', (_api, event) =>
    event.file_path === 'denied.md'
      ? { deny: 'fixture denial' }
      : { result: 'fixture content' }
  );

  const ok = await $.tool.call({ tool: 'Read', file_path: 'allowed.md' });
  const denied = await $.tool.call({ tool: 'Read', file_path: 'denied.md' });
  const summary = await $.command.run({ command: 'read-meter-summary', args: '' });

  expect(ok).toEqual({ result: 'fixture content' });
  expect(denied).toEqual({ deny: 'fixture denial' });
  expect(summary.text).toBe('Completed reads: 1; denied or failed reads: 1');
});
```

Run it with `claude plugin test ./read-meter` on a compatible build. This test invokes the command event directly; it does not prove the command was registered in a real session. To test registration, stub `command.register` and `session.start`, explicitly fire `$.session.start`, and assert the registration payload. Use the kit's mock clock for timers and its UI tree testing for interaction; visually inspect the actual host for layout. A successful custom JavaScript mock is still not a native kit run.

## Assess model-driven behavior when needed

Plugin evals require v2.1.269 or later. They use real account/provider model calls; installed Git must meet the documented minimum. The suite format is `evals/<case>/prompt.md` plus graders and optional case configuration, not another skill tool's `evals.json` format. `claude plugin eval init --bare first-case` scaffolds placeholders without running a model. [Eval requirements and format](https://code.claude.com/docs/en/plugin-evals).

Write cases around user outcomes: a task that should trigger the skill, an adjacent task that should not, missing configuration, and an unavailable required service. Grade the result and, where meaningful, whether the intended component actually participated. Do not reward tool usage that contributes no value.

For a bounded local pilot after authorizing its model usage:

```bash
claude plugin eval . --case first-case --runs 1 --ablation none --no-publish
```

One run finds obvious mistakes; it does not estimate reliability. Use repeated runs and the no-plugin baseline to measure contribution once the case is useful. Retain `--no-publish` unless publishing the report is explicitly intended: eligible accounts can publish reports by default. Distinguish model latency, hook/tool latency, tokens, cost estimates, and outcome quality instead of compressing everything into one pass rate. [Eval operation and reports](https://code.claude.com/docs/en/plugin-evals#run-evals-in-ci).

## Report what actually ran

Include the host version, surface, plugin source/version, test command, fixture assumptions, observed result, and remaining runtime checks. If `claude` is unavailable, say that native validation, mod tests, and real loading were not executed. Do not install or authenticate a host just to make a knowledge-only deliverable appear tested.
