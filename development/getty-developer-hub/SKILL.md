---
name: getty-developer-hub
description: "Use when setting up or working in one of Getty's `<domain>-developer` hub repos — a coordination hub for a family of repos under ~/dev — when work on several repos needs one place for specs, briefs and findings, or when deciding which hub owns a repo or task."
---

# Getty's developer hubs

A hub is a repo `~/dev/<domain>-developer` that coordinates a **family of repos** and
holds **no product code**: steering, specs, plans, findings, cross-repo tools and the
karr board of campaigns that belong to no single repo. The result flows into the
product repos, nothing else does. Take the structure from the nearest sibling:
`ls -d ~/dev/*-developer`. The hubs are peers: none is the master of the others.

## Which hub

[references/hubs.md](references/hubs.md) lists every hub, the repos it coordinates and the
tools only it has. A task goes to the hub that lists the repo; another hub's request
is a card on that hub's board. Read it before dispatching across families.

## Layout

```
CLAUDE.md          purpose, the family table, what goes where, delegation, karr
docs/specs/        specs and plans
docs/briefs/       one brief (and its report) per dispatched task
docs/*.md          findings: the command, its output, the conclusion
bin/               tools that span several repos
.claude/           agents/, settings.json, skilletor.json
```

`CLAUDE.md` carries these sections, in this order: purpose; the family (a table:
repo, what, language, branch, roles in its `.claude/agents/`); what belongs where;
delegation; karr. Hub text is German; a product repo's README, CHANGELOG and comments
follow that repo's own language.

## What goes where

- **Hub:** specs, plans, run and campaign logs, briefs and reports, measurements,
  multi-repo tools.
- **Product repo:** code, tests, its docs, its skills and rules, `Changes`.
- A fix to a product repo is tracked on the hub's board when the campaign is the
  hub's; the product repo's own work stays on its own board. A commit in the product
  repo names the card as `<hub> k12`, never `#12`.

## Delegation

A task in a family repo goes from the hub to a hub agent, not to `general-purpose`.
The dispatch names the **repo, a role from that repo's `.claude/agents/`, a brief file
and a report file**. The implementer leaves a commit-ready tree; the reviewer changes
nothing. Commits, pushes, probe runs and karr moves stay with the hub session. Longer
work in one repo runs as a session of its own there (skill `claude-cross-session`).

## Rules that hold in every hub

- **Measure, then claim.** A statement counts once the command and its output are in
  `docs/`. A finding derived from code only says so.
- **Decisions belong to Getty.** Where two ways are open, deliver the finding and a
  recommendation, then ask.
- **No push, tag or release of a product repo** without Getty's word; hub commits are
  free. A change in a product repo is committed locally, on a branch if the campaign
  says so.
- Board cards are named `k12`.

## Creating a hub

1. `mkdir ~/dev/<domain>-developer && git init -b main`, then the layout above.
2. `.claude/skilletor.json` with sources `getty` and `karr`, `"targets": ["claude"]`,
   `"gitignore": true`; install `kanban-issues-karr-coordination@karr`,
   `kanban-issues-karr-ticket@karr` and the family's skills. `.claude/settings.json`
   enables `skilletor@getty` and declares the `getty` marketplace (copy a sibling's).
3. `skilletor sync`, then commit `.claude/.gitignore` and `.worktreeinclude`.
4. Remote on src.ci: `fj --host src.ci repo create -P -d "<text>" <name>` (the name
   without owner, private), then
   `git remote add origin ssh://git@src.ci/getty/<name>.git`. `fj ... -r origin`
   fails on a repo with no commit yet.
5. List the family in `CLAUDE.md`; each repo's language and branch come from the repo.
