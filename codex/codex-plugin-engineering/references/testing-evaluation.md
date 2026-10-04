# Validation and behavioral evaluation

Evaluate the package's actual contract. Static validation, tool tests, and agent behavior establish different things.

## Validation layers

| Layer | Evidence |
|---|---|
| Files | Parse manifests/config; resolve referenced resources inside package |
| Skill | Correct frontmatter, meaningful description, complete linked references |
| Tool | Input/output schemas, authorization, errors, limits, side effects |
| Hook | Actual event matching, supported response handling, failure behavior |
| Installation | Correct catalog source, installed content, enabled state |
| Host | Claimed client/environment supports the required capability |
| Workflow | User reaches the intended result with appropriate authorization |

The official test flow covers direct/paraphrased requests, follow-ups, negative cases, authentication, metadata refresh, and installed skills/tools together. [Connect and test](https://developers.openai.com/plugins/deploy/connect-chatgpt)

## Original evaluation set

| Prompt or condition | What to measure |
|---|---|
| “Review release R-17 using its evidence.” | Correct skill and record |
| “Are we ready to ship R-17?” | Equivalent intent reaches the same workflow |
| “Which checks are still missing?” | Reuses the correct release context |
| “Explain what a semantic version is.” | Avoids unnecessary plugin activation |
| Two plausible matching releases | Resolves ambiguity without guessing |
| Record belongs to another tenant | Backend denial without data leakage |
| Tool times out after a possible write | Reconciles state before retrying |
| Connection revoked between read and write | Stops the write with a useful explanation |
| No UI renderer | Produces a useful structured/text result |

Do not feed the expected tool name into every prompt. Selection quality should be tested with realistic wording.

## Acceptance criteria

Define a small set of essential cases and an explicit threshold for each. For a sensitive mutation, one unauthorized success is a defect even if most cases pass. For retrieval, measure correct source selection and useful evidence, not just fluent prose.

For release comparisons, retain prompts, input fixtures, model/runtime versions, selected tools, arguments, final outputs, and observed effects with secrets removed.

## Report honestly

State which tests actually ran and what environment they used. “JSON parses” does not mean “loads in Codex”; “loads in Codex” does not mean “works in the IDE”; “hook fired” does not mean “all execution paths are protected.”

Broaden testing only to resolve a concrete risk or a required release gate.
