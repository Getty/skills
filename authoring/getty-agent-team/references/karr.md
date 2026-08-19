# karr coordination layer

`karr` is a git-native kanban board: state lives in `refs/karr/*` inside the repo, not in
checked-in files. One board per repo. It is the coordination substrate for every project
that uses this setup, so install it unless the user says otherwise.

Full command surface: skill `kanban-issues-karr-cli`, which `karr skill install`
drops into the repo (source: [Getty/karr](https://github.com/Getty/karr)).

## Install into a repo

```bash
cd <repo>
karr init --name "<Project>"            # creates refs/karr/*
karr skill install --agent claude-code  # drops .claude/skills/karr/SKILL.md
karr board                              # verify
```

`karr init --claude-skill` does both in one step. Prefer hardlinking the canonical skill
if the machine already has one (skill `manage-skills`) — `karr skill check` /
`karr skill update` tell you whether an installed copy is current.

Statuses default to `backlog → todo → in-progress → review → done → archived`, with
`in-progress` and `review` requiring a claim. Change via `karr config set` only if the
project genuinely needs a different flow.

## Seeding the board

A fresh board with nothing on it gets ignored. Seed it from what already exists — open
TODOs in the code, the roadmap section of the README, the known-broken list — one ticket
each, priority set, so the first `karr pick` has something real to grab.

## The `.karr` file — headless agent execution

`karr-foundation` (ships with App::karr) scans configured boards, pulls, and **drains**
each board that has open work by running a headless agent until nothing actionable
remains. Execution is opt-in **per repo** via a `.karr` file:

```yaml
claude: true          # synthesize the canonical headless call
prompt: "…"           # the instruction the agent wakes up with
# command: "…"        # or override the invocation entirely
```

```bash
karr-foundation --status               # read-only overview, never runs agents
karr-foundation --dry-run --verbose    # preview
karr-foundation                        # scan, then drain
```

Config lives in `~/.config/karr-foundation/config.yml` — `dirs:` (explicit repos) and/or
`scan:` (parent dirs; any child with a `.karr` file or karr refs counts).

> **Trap:** a global `default_command` in that config **wins over every repo's `.karr`**
> and turns every discovered board into an agent board — a repo cannot opt out. Prefer
> per-repo `.karr` files, and leave boards that must not be touched (abandoned
> components, anything with a production blast radius) without agent config.

Each run is classified (progress / stall / common-error / idle): stalled tasks are
auto-blocked after `max_attempts`, API errors put the repo in exponential cooldown, a
lock file keeps concurrent runs safe.

## Repo families — the `<prefix>-coordination` skill

A family of independent repos has **no shared board**. Cross-repo work is a ticket on the
*other* repo's board — never a direct edit. That protocol belongs in a project-owned
skill, briefed into the worker and the `karr-coordinator`.

Template: `coordination-skill-template.md` (next to this file). Source of truth lives in
the family's core repo; the other repos hardlink it.

## Operational rules that go in the rules file

- **Serialize board mutations when fanning out.** Confirmed incident: 8 concurrent
  cross-repo fix agents, each ending in its own `karr move ... review`, OOM-rebooted the
  host. A single `karr handoff` is ~46MB RSS / ~18s — cheap alone, not cheap ×8. Keep
  implementation parallel, then loop the board writes sequentially.
- **No background poll loops** on the board. Check once, act on the result.
- **A board is not a public tracker.** Never mirror karr tickets into a public issue
  tracker, and never drain a public tracker into karr, without explicit instruction.
