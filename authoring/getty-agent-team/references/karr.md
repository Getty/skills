# karr, Getty's habits

Install, board seeding, the skills and the rule `board-karr` are the kit's
(`team-board.md` of `agent-construction-kit`). What stays here is how Getty runs karr.

## The `.karr` file and `karr-foundation`

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

Config lives in `~/.config/karr-foundation/config.yml`: `dirs:` (explicit repos) and/or
`scan:` (parent dirs; any child with a `.karr` file or karr refs counts).

> **Trap:** a global `default_command` in that config **wins over every repo's `.karr`**
> and turns every discovered board into an agent board; a repo cannot opt out. Prefer
> per-repo `.karr` files, and leave boards that must not be touched (abandoned
> components, anything with a production blast radius) without agent config.

Each run is classified (progress / stall / common-error / idle): stalled tasks are
auto-blocked after `max_attempts`, API errors put the repo in exponential cooldown, a
lock file keeps concurrent runs safe.

## Board habits

- Seed a fresh board from what exists (open TODOs, the README roadmap, the known-broken
  list), one card each with a priority; an empty board gets ignored.
- Statuses stay `backlog, todo, in-progress, review, done, archived`; change them with
  `karr config set` only when the project needs a different flow.
- A board is not a public tracker: never mirror karr cards into one, never drain one
  into karr, without explicit instruction (rule `publish-gate`).
- A family has no shared board: cross-repo work is a card on the other repo's board.
