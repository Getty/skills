# Development workflow

Use this procedure for a new plugin or a substantial extension.

## 1. Write a compact design brief

Record the intended users, task, inputs, outputs, supported clients, execution environment, distribution route, data sources, side effects, and success criteria. Mark unresolved choices.

Example objective: “Given a release ID, retrieve evidence and produce a review; applying changes is a separate authorized operation.”

Reject undefined goals such as “control everything in Codex” until they are decomposed into actual capabilities.

## 2. Choose and scaffold the package

Select the format in [package formats](package-formats.md). Create one focused skill and only the components needed for its first workflow.

Use existing project tooling and dependency conventions. Do not introduce a backend, frontend, or hook when existing tools plus instructions already complete the task.

## 3. Implement the vertical workflow

If tools are required, implement and directly exercise them before relying on model selection. The official flow recommends component testing followed by testing the installed package. [Plugin testing](https://developers.openai.com/plugins/deploy/connect-chatgpt)

Give each component observable inputs and outcomes. Keep selection text separate from implementation logic. Add a single end-to-end scenario with representative but non-sensitive data.

## 4. Install into the intended development source

Use a local or dedicated development marketplace. Confirm the installed version/path and test from the installed package, not merely from the authoring directory.

Use a fresh conversation after package installation as required by the host. Do not claim that every live process hot-reloads all component types.

## 5. Add complexity deliberately

Add authentication, writes, UI, hooks, or events one at a time. For each addition, record the new failure modes and the host capability it requires.

## 6. Finish the implementation

Remove scaffold placeholders, unresolved example endpoints, dead references, unused assets, and accidental credential files. Verify the package with [testing and evaluation](testing-evaluation.md), then prepare [distribution and release](distribution-release.md).

Keep a small reproducible fixture with the implementation. Avoid a large mock suite that mirrors code while missing installation, permissions, or client behavior.
