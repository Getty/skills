# House rules template — `.claude/rules/<prefix>-rules.md`

Auto-loaded by Claude Code on every turn, at the same priority as `CLAUDE.md`, next to the
shared house rules skilletor installs from Getty/skills:

| Bundle | Rules |
|---|---|
| `getty-house` | `engineering-discipline`, `getty-agent-delegation`, `getty-publish-gate`, `karr-coordination` |
| `getty-cpan-dist` | `getty-house` + `getty-cpan-release` |

```bash
skilletor install bundle:getty-cpan-dist@getty --project   # a CPAN distribution
skilletor install bundle:getty-house@getty --project       # anything else
```

The project file holds only what is true here. Budget: **~30–50 lines**; everything in it
is paid for on every request.

Belongs here: what the repo is and what to read first, the lane table, what counts as
behavior-relevant, release mechanics beyond the shared gate, deviations from the shared
rules, hazards.

Does **not** belong here: anything a shared rule already says (discipline, the lock, the
publish gate, karr usage, CPAN lag), language conventions, architecture, API details,
anything a briefed skill carries. A restated rule is a rule that will drift — change the
shared rule in Getty/skills instead.

---

```markdown
# <Project> House Rules

The shared house rules come from skilletor — bundle `<getty-house|getty-cpan-dist>@getty`:
engineering discipline, the delegation lock, the publish gate, karr coordination<, CPAN
release>. They load as `.claude/rules/.local.*.md`; if they are missing, run
`skilletor sync` and publish nothing until they load. This file adds what is true only
here, and wins where it differs.

## What this repo is

<One to three lines.> Read first: <the modules every change must read — the seams, the
shared utilities>.

## Agent team

| Task | Agent |
|---|---|
| Implement / refactor / debug behavior-relevant code | `<prefix>-worker` (default) |
| Write/extend tests | `<prefix>-test-writer` |
| Commits, changelog, card → done, pre-release audit | `<prefix>-release-manager` |
| Read-only research, audit, gap analysis | `<prefix>-worker` ("read-only, change nothing") |

Behavior-relevant = <enumerate for this project: runtime behavior, public API, the core
mechanism, error handling, tests, performance>. Pure prose docs and changelog notes are not.

<Family only:> Cross-repo routing: skill `<prefix>-coordination`.

## Release

<Only what the shared rules do not say: the build/test commands for a non-CPAN project,
what the release is here (a tag that triggers CI, an image, a HACS release), coupled
releases, extra gated actions. Omit the section for a plain CPAN distribution.>

## Deviations from the house rules

<Only if any: a shared rule that does not apply here or applies differently — public PRs
gated too, direct cross-repo edits allowed, no new cards for side findings. Omit otherwise.>

## Hazards

<Why this file is worth loading every turn. Write down what has actually gone wrong here,
with the mechanism, not the moral: resource limits on shared hardware, a serialization
requirement, a composition seam that must never move without an ADR, an abandoned
component that must not receive work.>

## <Language> specifics — reference, don't restate

<One line naming the skills that carry the conventions (force-loaded for `<prefix>-*`
agents).>
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

A project-specific discipline point ("evidence tags on every name", "originals are
read-only") is a hazard: it goes here, not into a numbered discipline list.
