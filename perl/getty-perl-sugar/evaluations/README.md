# Manual agent evaluations

[cases.json](cases.json) contains 12 English scenarios for evaluating an agent that
has loaded this skill. These are review cases, not executed independent-agent results.

For each case, score whether the response identifies the central failure mode,
chooses an appropriately scoped design, preserves evidence boundaries, and proposes
relevant tests. A response that claims unexecuted integrations passed, evaluates
untrusted predicate text, or treats module loading as inert fails the case.

Compare against the same agent without the skill before claiming a measured quality
improvement. Record the model, prompt, skill version, response, and rubric outcome.
The bundled functional tests validate code behavior, not agent effectiveness.
