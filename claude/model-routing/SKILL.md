---
name: model-routing
description: Use when choosing which Claude model runs work — opus/sonnet/haiku/fable for a subagent, headless run or Workflow stage, or assigning the model field to agent roles.
---

# Model Routing

Route work by the **hardest single dimension it routinely hits — never by
size, volume, or average difficulty.** A 2000-record extraction is fast-tier
work; a three-line auth diff is strong-tier work.

## The ladder

Four tiers. The mapping below is a cache (2026-08) — when it smells stale,
`claude --help` and the models API are the authority; the *tier logic* does
not change when the names do.

| Tier | Model | $/MTok in/out | Note |
|---|---|---|---|
| Frontier | Fable 5 (`claude-fable-5`) | 10 / 50 | Hardest, longest-horizon work; thinking always on |
| Strong | Opus 5 (`claude-opus-5`) | 5 / 25 | Default for judgment-heavy work |
| Mid | Sonnet 5 (`claude-sonnet-5`) | 3 / 15 | Default for well-scoped engineering |
| Fast | Haiku 4.5 (`claude-haiku-4-5`) | 1 / 5 | 200K context (others: 1M) — bulk jobs must fit or chunk |

**Effort is the second dial.** On current models `low`–`max` effort shifts
cost and depth *within* a tier; a strong model at low effort is still a
strong model — dropping effort keeps judgment quality on mechanical stretches,
dropping tier does not. Tune effort before switching tiers when the work is
the same kind but lighter.

## The dimensions

Score work on whichever of these is worst; that dimension picks the tier.

| Dimension | Pushes down (fast/mid) | Pushes up (strong/frontier) |
|---|---|---|
| Spec clarity | Exact pattern/rubric given, decisions closed | Open-ended, the task includes deciding what "right" means |
| Judgment depth | One obviously correct output | Many plausible outputs, subtle differences matter |
| Cost of error | Cheap, visible, reversible | Security, data loss, irreversible, silently wrong |
| Verifiability | Tests/schema/grep will catch mistakes | No external check; the model's answer is the check |
| Context breadth | One file, one record at a time | Cross-file/cross-system synthesis, long-horizon state |
| Novelty | Seen-a-thousand-times shape | Genuinely new problem, no template |

Tier anchors: **fast** — specified transforms at volume (extraction,
formatting, renames with a given pattern, commit messages for explained
changes, classification with a rubric). **Mid** — scoped implementation,
tests for specified behavior, debugging with a reproducer, medium synthesis.
**Strong** — architecture, security review, debugging without a reproducer,
ambiguous specs, verification of high-stakes work. **Frontier** — the
long-horizon autonomous end of strong-tier work, when a failed strong-tier
attempt shows the ceiling.

## Splitting tasks so they route cheap

Cut work so the judgment is small and the volume is cheap:

- **Sandwich:** strong model writes the spec (closing every decision) → fast
  model executes the volume → strong model verifies. Most tokens run cheap.
- **Generation and verification are separate routes.** Cheap generation is
  fine exactly when verification is strong — up-tier the checker, not the
  typist. Never down-tier verification of high-stakes work because the diff
  is small.
- **A split is wrong if the cheap side inherits open decisions.** If the
  executor must choose (naming, ordering, edge-case behavior), either close
  the choice in the spec or move that piece up-tier.
- **Escalate, don't retry sideways:** on failure or "unsure", go one tier up
  and pass the failed attempt along as context. Instruct subordinates to
  surface uncertainty — a cheap model saying "unsure" routes correctly; a
  cheap model guessing routes a defect downstream.

## Sizing agent roles (for agent builders)

An agent definition is static — its model must carry the **hardest task the
lane routinely sees**, not the median:

- Worker/implementer lanes: mid, strong when the codebase is subtle or specs
  arrive open. Reviewer, security, release-checker lanes: strong — their
  entire job is the judgment dimension. Formatter/extractor/board-keeping
  lanes: fast.
- **A role whose load spans tiers is two roles.** Don't buy a strong model
  for a lane that is 90% mechanical — split the mechanical part into its own
  fast-tier agent and keep the judgment lane small. This is the same sandwich,
  frozen into the team.
- Give cheap lanes an explicit escalation path ("if unsure, report back —
  never guess") so uncertainty flows to a strong-tier lane instead of into
  the work.
- Where the choice lands: `model:` in `.claude/agents/*.md` frontmatter, the
  Agent tool's `model` parameter, `opts.model` per Workflow stage, `--model`
  on a headless run (skill `claude-headless`). Default everywhere: **omit and
  inherit the session model** — override only when the rubric gives you a
  reason.

## Anti-patterns

| Mistake | Why it's wrong |
|---|---|
| Routing by size ("big task → big model") | Volume is a cost argument *for* the fast tier; difficulty is what buys tiers |
| "Small diff → small model" | Cost of error and judgment depth don't scale with line count |
| Everything on frontier "to be safe" | Pays 10× for work a rubric fully specifies; spend it on the judgment slice |
| Everything cheap "to save cost" | Rework and silent defects cost more than the tier difference |
| One do-everything agent on a strong model | Freeze the sandwich into roles instead — see sizing above |
| Forgetting the effort dial | Same-tier low effort often beats a tier drop for lighter work of the same kind |
