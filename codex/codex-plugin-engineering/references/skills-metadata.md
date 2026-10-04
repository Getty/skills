# Skills and skill metadata

Use a skill to express a repeatable workflow. Put deterministic computation in scripts only when needed, and keep live authorization in tools.

A skill requires `SKILL.md` with `name` and `description`. Its description is the discovery contract; supporting resources load when selected. `agents/openai.yaml` adds OpenAI metadata, invocation policy, and tool dependencies. Standalone local discovery differs from bundled plugin installation. [Build skills](https://learn.chatgpt.com/docs/build-skills)

## Original workflow example

```markdown
---
name: release-review
description: Review a proposed software release using supplied changes, checks, and rollout notes; report missing evidence and unresolved risks.
---

1. Identify the release scope and the evidence supplied.
2. Read only the relevant release checklist and supporting records.
3. Separate confirmed results, assumptions, and unverified claims.
4. Check rollback instructions against the proposed changes.
5. Return a release assessment with evidence links and unresolved items.
6. Do not publish, deploy, or invent missing test results.
```

Add supporting files such as `references/release-checklist.md`. Link each resource from the workflow and say when to read it.

## Original metadata example

```yaml
interface:
  display_name: "Release Review"
  short_description: "Assess release evidence and readiness"
  default_prompt: "Use $release-review to assess this release."
policy:
  allow_implicit_invocation: true
```

For a real MCP dependency, add a `dependencies.tools` entry using the documented server identifier, transport, and endpoint. Declaring it does not implement authorization or manufacture a missing connection. [Plugin skill integration](https://developers.openai.com/plugins/build/skills)

Keep skill metadata's snake_case fields separate from plugin listing metadata's camelCase fields. Treat implicit activation as a discovery preference, not permission to execute every step.

## Authoring and evaluation

Front-load precise task language. A release-review skill should not activate for a generic explanation of semantic versioning unless that behavior is intended.

Supply one direct request, one paraphrase, one follow-up, and one negative request. Check whether the selected workflow reads the right files and asks only for missing information that matters. Measure unnecessary activation as well as successful activation.

Avoid duplicating broad repository policy into every skill. Refer to the user's available instructions and tools without assuming specific personal paths, organizations, or accounts.
