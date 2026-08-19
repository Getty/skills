![claude](../assets/claude.png)

# Claude skills

Working with Claude itself: spawning another instance of it, and deciding which
model any given piece of work should run on. Both are reference skills — nothing
here is specific to one project.

## [claude-headless](claude-headless/SKILL.md)

`claude -p` runs one non-interactive turn-loop and exits, and calling it from
inside a running session works without any environment cleanup. What bites is
everything around that: a child does **not** inherit the parent's model (it reads
the saved user default), print mode cannot ask for permission so an unapproved tool
call is simply denied, and settings resolve against the **child's** cwd rather than
the parent's session.

Covers pinning the model by exact ID and verifying it from `modelUsage`, the JSON
output fields worth reading, the three ways to decide permissions before launch,
what the child inherits and how `cd` is the main lever on that, plus guard rails —
`--max-turns`, `--max-budget-usd`, resuming by `session_id`, and the fact that
background commands a child starts get killed seconds after its final result.

**Load when** running Claude Code headless, or when a nested run hangs, denies a
tool, or picks the wrong model.

## [model-routing](model-routing/SKILL.md)

Route work by the **hardest single dimension it routinely hits** — never by size,
volume, or average difficulty. A 2000-record extraction is fast-tier work; a
three-line auth diff is strong-tier work.

Gives the four-tier ladder with a cache of current model IDs and prices, the six
dimensions that decide the tier (spec clarity, judgment depth, cost of error,
verifiability, context breadth, novelty), and the effort dial as the second knob —
a strong model at low effort keeps its judgment, a dropped tier does not. Then the
patterns that make work route cheap: the sandwich (strong writes the spec, fast
executes, strong verifies), separating generation from verification, and sizing
agent roles so a lane that spans two tiers becomes two lanes.

**Load when** choosing a model for a subagent, headless run or workflow stage, or
setting an agent's `model:` field.
