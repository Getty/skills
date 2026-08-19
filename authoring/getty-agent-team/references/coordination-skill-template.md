# Template — `<prefix>-coordination` SKILL.md

Copy the block below into `.claude/skills/<prefix>-coordination/SKILL.md`, replace the
placeholders, delete what doesn't apply. It is a project-owned skill: the source of truth
lives in the family's core repo and the other repos hardlink it (skill `manage-skills`).

Brief it into the worker and the `karr-coordinator`. Do not brief it into single-repo
projects — they have no cross-repo protocol to follow.

---

---
name: <prefix>-coordination
description: "Cross-repo workflow for the <family> family. Which repo owns what. How to hand off work via karr tickets pushed to other repos' remotes."
user-invocable: false
allowed-tools: Read, Bash, Glob
model: sonnet
---

# <Family> Cross-Repo Coordination

The <family> family is **many independent repos**, each its own git repo. There is no
central workspace. Coordination happens via `karr` tickets pushed to repo remotes, picked
up by the receiving repo's agent on its next `karr sync --pull`.

## Repo ownership

| Concern | Owning repo |
|---------|-------------|
| <core abstraction, shared API, test infrastructure> | `<core repo>` |
| <variant-specific behavior> | `<variant repo>` |
| <build / release tooling> | `<tooling repo>` |
| This coordination skill | `<core repo>` (source of truth, hardlinked) |

## Decision rule when a ticket arrives

```
ticket is about <core concern>          → keep in <core>
ticket is about <variant concern>       → push to <variant>
ticket is about release tooling         → push to <tooling>
ticket needs change in both             → split into two tickets, link via tags or set-refs
```

## Cross-repo handoff via karr

There is **no shared board**. Each repo has its own `refs/karr/*`. Cross-repo handoff =
create a ticket in another repo's remote and let its agent pick it up.

### Posting a ticket to another repo

```bash
# Option 1: the other repo is checked out locally (fast, no network)
( cd <path/to/other-repo> \
  && karr create "<title>" --priority high \
       --body "Originated from <this repo> ticket #N. <why it matters there>" \
  && karr sync --push )

# Option 2: remote-only (other repo not checked out)
git push <other-repo-remote> refs/karr/tasks/<new-id>/data
```

### Loop prevention

1. **Always read existing tickets first** — `karr list` shows open work including prior
   cross-repo notes. If a ticket already covers it, comment via `karr edit` instead of
   creating a new one.
2. **Tag cross-repo tickets** with `from:<source-repo>` and the originating ticket id, so
   the receiving agent can see the chain.
3. **Use `karr set-refs` for shared plan documents** several repos must read, so nobody
   files a ticket just to publish a plan.
4. **One agent claims the chain end-to-end** when feasible — fewer hops, less drift.

### Handoff back

```bash
karr handoff <id> --claim "$(karr agentname)" \
  --note "Done. Commit <sha> in <repo>." \
  --timestamp
```

Then note the resolution on the originating ticket:

```bash
( cd <path/to/origin-repo> \
  && karr edit <origin-id> -a "Resolved downstream in <repo> ticket #N (commit <sha>)" )
```

## Shared plan storage via set-refs

For plans several repos must consult but which shouldn't be a ticket:

```bash
karr set-refs <family>/plan/<topic>.md - <<'EOF'
# <topic> plan
...
EOF

# elsewhere:
karr get-refs <family>/plan/<topic>.md
```

Pushes via `karr sync --push`; other repos see it after `karr sync --pull`.

## What NOT to do

- ❌ Edit code in another repo from this repo's agent. Cross-repo work = ticket, not a
  direct push.
- ❌ Create a ticket without first checking whether one already exists.
- ❌ Hold a claim across a long cross-repo wait — release it and let the originating
  agent pick it up when downstream is done.
- ❌ Treat the parent directory as a workspace root. Each repo is independent.
