# Owner notes

What the kit (`agent-construction-kit`) does not carry and Getty's projects use.

## Domain specialists, only for large applications

Sits on the kit's "workers by path": there one worker per part; here an application
outgrows even that and splits by **ownership of paths**, not by activity.

- One agent per surface (`…-web-controllers`, `…-cli`, `…-schema-and-migrations`,
  `…-security-and-auth`, `…-i18n`, `…-frontend`).
- One `release-manager-and-dispatcher`: routes ("who owns this path?"), gates
  (pre-commit and release-readiness checklists) and, as everywhere, is the only role
  that commits. It writes no feature code and does not push.
- The routing table lives in the dispatcher's body as a `path glob -> owner` table. A
  cross-scope task means the parent spawns two owners **in parallel**; the dispatcher
  flags, it does not spawn.

Not for a library or a small service. Three good agents beat fourteen thin ones; every
path needs an obvious owner, and ambiguity there is worse than no split.

## Writing the hazards section

The one part of the project rules no template supplies. Mine it from incident memory,
repeated review comments, `git log` reverts and the user's war stories.

1. Name the mechanism, not the moral: "live suites run against real DBs on a small
   shared box; uncontrolled runs have OOM-rebooted the host", not "never run parallel
   tests".
2. State the trap that makes the wrong thing look right (lazy driver resolution, a
   non-recursive test runner, a green suite after an illegal `@ISA` change).
3. Give the fix in one clause, with the command.
4. A project-specific discipline point ("evidence tags on every name", "originals are
   read-only") is a hazard: it goes here, not into a discipline list.

## ADR-auditor

Brief `<prefix>-adr` (the project's ADR format skill) and `<prefix>-core`. Method:
structure first (namespaces, role mesh, value objects; in a fork the upstream diff is the
decision list), then confirm the why from git history, the code and the board; archived
planning documents only confirm a rationale. ADR-worthy: a deliberate choice touching the
public API, composition seams or a cross-cutting mechanism, and **deliberate keeps**
(structure a review was tempted to change and the project chose not to). Not: local
style, naming, single-use code. Numbers monotonic per repo from `0001`, never reused. A
decision owned by another repo becomes a ticket to that repo, not an ADR here.

## Codex agents

`.codex/agents/*.toml` with a `# briefing: skills = [...]` comment, underscores in
`name`, and no `[briefing]` table (skill `briefing`).

## Settings and live check

- Never author `.claude/settings.local.json` and never commit decisions into it; it is
  per-machine permission noise.
- You cannot spawn new agents in the session that created them (agent files are read at
  startup). In a later session, the live check is behavioral: a briefed agent answers a
  question that is only in its skills without calling the `Skill` tool; if it reaches
  for `Skill`, the hook did not fire, so check the project's settings.

## Models beyond the kit's table

The kit sizes roles with `haiku`, `sonnet`, `opus` and `inherit`. `fable` (Fable 5.2) is
stronger than `opus` at twice the price: for a lane whose routine load is long-horizon
autonomous work. Sizing rules: skill `model-routing`.
