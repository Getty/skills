# Hub register

Which hub coordinates which repos. Hand-maintained: a new hub, or a repo that changes
hub, is edited here first (`~/dev/skills`), then `skilletor sync` in the hubs.

| Hub | Coordinates | Hub-only tools |
|---|---|---|
| `perl-developer` | the Perl fleet under `~/dev`: `dbio-dev/*`, `p5-*`, `langertha*`, `kubernetes-*`, `rex-*`, `karr` | `bin/fleet` (inventory, dependencies, release order, board status for **all** repos), `bin/fleet-housecheck`, `bin/claude-uptodate`, `bin/smoke` |
| `sunriser-developer` | `sunriser`, `sunriserx`, `sunriser4`, `sunriser2`, `sunriser-homeassistant`, `sunriser-mobile` | none |
| `windows-developer` | a campaign, not a family: the plugins of the `getty` marketplace on Windows; findings live there, fixes land in the plugin repos | none |
| `agent-developer` | the agent repos: `agent-irc`, `briefing`, `ruler`, `loadguard`, `skilletor`, `manage-skills`, `marketplace` (the fleet's `marketplace` corner), plus `agent-construction-kit` and `our-codex`; the move to the shared Bun runtime | none |

Every hub installs the skill `getty-fleet` from the source `developer-fleet`
(`ssh://git@src.ci/getty/developer-fleet.git`); the `fleet` tool it describes is
`~/dev/perl-developer/bin/fleet`. A skill shared by all hubs lives in that repo, never in
one hub.

## Which hub gets a task

1. A task about **one repo** goes to the hub that lists the repo. `bin/fleet --json repo
   <name>` shows a repo's corner when the table is unclear.
2. A task that spans **several families** (a campaign) belongs to the hub named for it,
   or to the hub where it starts; the other hubs get a card on their own board, not a
   copy of the work.
3. A repo has **one home hub**. The fleet inventory lists every repo, including those
   another hub owns; that makes `perl-developer` the place to look things up, not the
   place to dispatch from.
4. A repo no hub lists: ask Getty, then add a row.

## Cross-hub requests

A hub never edits another hub's files or dispatches into its repos. It leaves a card on
the owning hub's board (`k12`, `kanban-issues-karr-coordination`) with the repo, the
finding and what it needs; the owner picks it up. An exception only on Getty's word.
