# House rules template — `.claude/rules/<prefix>-rules.md`

Auto-loaded by Claude Code on every turn, at the same priority as `CLAUDE.md`. Budget:
**~60–90 lines**. Everything in here is paid for on every single request, so it holds
only what must be true before the first tool call.

Belongs here: engineering discipline, the delegation lock, coordination, permission
gates (release, public trackers), resource discipline.

Does **not** belong here: language conventions, architecture, API details, anything a
briefed skill already carries. Reference the skill by name instead — a duplicated rule
is a rule that will drift.

---

```markdown
# <Project> House Rules

Apply to every task in this repository unless explicitly overridden. Bias: caution over
speed on non-trivial work; use judgment on trivial tasks. Loaded automatically at launch
(same priority as `CLAUDE.md`). Subagents get their discipline from the skills
force-loaded via `briefing.skills` — this file is for the orchestrating agent.

## Engineering discipline

1. **Think before coding** — State assumptions. When uncertain, ask rather than guess.
   Present alternatives when ambiguous. Push back when a simpler approach exists. Stop
   when confused; name what's unclear.
2. **Simplicity first** — Minimum code that solves the problem. Nothing speculative. No
   abstractions for single-use code.
3. **Surgical changes** — Touch only what you must. Don't "improve" adjacent code,
   comments, or formatting. Match existing style.
4. **Goal-driven execution** — Define success criteria, loop until verified.
5. **Surface conflicts, don't average them** — Contradicting patterns: pick one (more
   recent / more tested), explain why, flag the other for cleanup. Don't blend.
6. **Read before you write** — Before new code, read exports, immediate callers, shared
   utilities (<name the actual shared modules here>). "Looks orthogonal" is dangerous.
7. **Tests verify intent, not just behavior** — Tests encode WHY behavior matters. A
   test that can't fail when the logic changes is wrong. Reproduce a bug before fixing
   it; leave a regression test behind.
8. **Checkpoint after every significant step** — Summarize: done / verified / left.
   Don't continue from a state you can't describe back.
9. **Match the codebase's conventions, even if you disagree** — Conformance > taste.
   Surface a harmful convention; don't fork silently.
10. **Fail loud** — "Done" is wrong if anything was skipped silently. "Tests pass" is
    wrong if any were skipped. Surface uncertainty, don't hide it.
11. **A red test is a claim before it is a failure** — Before changing code to turn a
    test green, say out loud what the test asserts and whether your fix keeps that claim
    or replaces it. A fix that satisfies the assertion by removing the property it was
    sampling leaves a green test that proves nothing. If the claim is wrong, fix the
    claim and say so; don't quietly make the code match a wrong claim.

## Delegation

This rule depends on whether the Agent/Task tool is available to you.

- **You can spawn subagents** (orchestrating main agent): Do NOT touch behavior-relevant
  code yourself — delegate to this repo's worker (`<prefix>-worker`). Your lane:
  coordinate, inspect, plan, review diffs, run tests, manage git, edit non-behavioral
  docs. When in doubt, delegate. Why: only the `<prefix>-*` agents get their skills
  force-loaded via `briefing.skills`; you get no briefing and would touch internals with
  too little context. Specialist lanes:

  | Task | Agent |
  |---|---|
  | Implement / refactor / debug behavior-relevant code | `<prefix>-worker` (default) |
  | Write/extend tests | `<prefix>-test-writer` |
  | Pre-release audit | `<prefix>-release-checker` |

- **You cannot spawn subagents** (you ARE a `<prefix>-*` agent): The delegation lock does
  not apply to you — implement, refactor, debug, and test per these rules.

Behavior-relevant = <enumerate for this project: runtime behavior, public API, the core
mechanism, error handling, tests, performance>. Pure prose docs and changelog notes are
not.

## Coordination — karr board (always in scope)

Ticket coordination is the orchestrating agent's job, so `karr` is always in scope —
don't invoke the `kanban-issues-karr-cli` skill first, just use it. Git-native kanban; state lives in
`refs/karr/*`; this repo has its own board. Day-to-day:

- `karr list --compact` / `karr board` — open work · `karr show ID` — detail
- `karr create "Title" --priority high --tags a,b --body '…'` — new ticket
- `karr edit ID -a "note"` · `--claim NAME` · `--block "why"` — update
- `karr move ID in-progress --claim NAME` — start · `karr handoff ID --claim NAME --note "…"` — to review
- mutating commands auto-sync; `karr sync --pull|--push` for explicit exchange

<Family only:> Cross-repo handoff = create the ticket on the *other* repo's board (cd in,
or push its ref). Routing + handoff protocol: skill `<prefix>-coordination`. Full command
surface: skill `kanban-issues-karr-cli`.

**Serialize board mutations when fanning out.** Keep implementation work parallel if you
like, but collect the results and then loop `karr move`/`handoff`/`sync` sequentially —
N of them landing at once is a resource event, not a cheap command.

## Release — never without permission

`<build>` / `<test>` are fine anytime. `<release command>` and any upload/deploy are
STRICTLY forbidden without the maintainer's explicit go-ahead — even if a plan or STATUS
document lists "release" as the next step. For anything heading toward release: stop and
ask.

## Public issues — never act without instruction

<Only if the project has a public tracker.> Two trackers, two universes. **karr** is the
agent work board — internal, churned freely. **<Tracker>** carries real humans' bug
reports, outward-facing, written under the maintainer's account. **Never act on a public
issue on your own initiative — not even to read it.** No listing, viewing, commenting,
editing, closing, or creating unless the user explicitly says to handle a specific issue.
Incoming user tickets are NOT a queue the agent drains; every write is confirmed first
because it publishes under the maintainer's name.

## <Project-specific hazards>

<Everything above is boilerplate. This section is why the file is worth loading every
turn. Write down what has actually gone wrong here, with the mechanism, not the moral:
resource limits on shared hardware, a serialization requirement, a composition seam that
must never move without an ADR, an abandoned component that must not receive work.>

## <Language> specifics — reference, don't restate

Module loading, class patterns, dependency pinning, and house style live in skill
`<name>` (force-loaded for `<prefix>-*` agents). Do not duplicate that content here.
```

---

## Writing the hazards section

This is the part no template can supply and the only part worth its context cost. Mine
it from: incident memory ("the box OOM-rebooted when…"), repeated review comments,
`git log` reverts, and the user's own war stories. Three properties make one land:

1. **Name the mechanism, not the moral.** "Never run parallel live tests" is ignorable.
   "Live suites run against real DBs on a small shared box alongside k3s; uncontrolled
   runs have OOM-rebooted the host" is not.
2. **State the trap that makes the wrong thing look right.** Driver resolution being
   lazy, a test runner being non-recursive, a green suite after an illegal `@ISA`
   change — the rule exists because the naive check passes.
3. **Say what to do instead**, in one clause, with the command.
