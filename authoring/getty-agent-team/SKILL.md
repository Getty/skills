---
name: getty-agent-team
description: "Use when one of Getty's repos needs subagents or an agent team — setting one up, wiring briefing or karr, or when .claude/agents is missing or drifted. Getty's preset: load it before the skill of the plugin agent-construction-kit."
---

# Agent team, Getty's preset

Getty's answers to the questions of the public plugin `agent-construction-kit`: which
board, who commits, which sources, bundles and skills per role. The procedure itself
(analysis, agents, rules, settings, board, verification) lives in the kit; this skill
holds only what is Getty's own.

**This skill is user-level only.** Its home is the shared library
([Getty/skills](https://github.com/Getty/skills), group `authoring/`); it runs
user-level and changes the target project. Never install or copy it into a project —
a project's `.claude/` never mentions `getty-agent-team`.

## Prerequisite

The plugin `agent-construction-kit` must be installed and enabled, from whichever
marketplace: this session then lists the skill `agent-construction-kit:agent-construction-kit`.

Not listed: ask the user to run these two slash commands (Claude cannot run them),
then continue in a new session:

```
/plugin marketplace add Getty/marketplace
/plugin install agent-construction-kit@getty
```

Without the plugin, do not rebuild its procedure from memory.

## Procedure

Load the skill `agent-construction-kit:agent-construction-kit` and follow it with the
answer sheet below; ask the user only what the sheet leaves open. Verification is the
kit's `ack-team check`.

## Answer sheet

- board: karr
- committer: release-manager
- publish_gate: on
- outside_input: on
- sources: getty=Getty/skills, karr=Getty/karr
- bundles: getty-house
- bundles when "dist.ini exists": getty-cpan-dist
- provider: minimax, openai, kimi, ollama, fireworks
- headless: off
- headless when family: on
- headless when hub: on

| roles | skills | when |
|---|---|---|
| worker | + `getty-perl-core`, `getty-perl-pod` | "dist.ini exists" |
| test-writer | + `getty-perl-core` | "dist.ini exists" |
| reviewer | + `getty-perl-core` | "dist.ini exists" |
| release-manager | + `getty-git-commit-style`, `getty-git-usage` | |
| release-manager | + `getty-perl-release-author-getty`, `perl-release-dist-ini` | "dist.ini exists" |
| doc-writer | + `getty-perl-pod` | "dist.ini exists" |
| coordinator | + `kanban-issues-karr-ticket` | |

Project-specific stack skills (`getty-perl-moo`, `getty-perl-moose`,
`perl-io-async-future`, ...) are added per project when the analysis shows the code
uses them.

`outside_input: on` is the house rule `publish-gate`: public trackers are not a queue;
single entries come in as cards the user writes.

The `getty-cpan-dist` bundle already ships `getty-perl-pod` and
`getty-perl-release-author-getty`; the rows add them to the roles, the bundle installs
them. The kit keeps `<prefix>-core`, the coordinator's `<family>-coordination` and the
karr card skills on top.

## CPAN specifics

- A brand-new distribution has no `dist.ini` yet, so the `"dist.ini exists"` lines would
  not apply. Tell the kit "this will be a CPAN distribution", or create `dist.ini` first
  (skill `getty-perl-distribution`).
- Commit style, `Changes` mechanics and release knowledge go into the release-manager
  alone (rows above); workers and writers leave a commit-ready tree.
- The doc-format skill is `getty-perl-pod` (`@Author::GETTY` POD commands, `# ABSTRACT`),
  not `getty-perl-release-author-getty`, which is release knowledge.
- The release-manager never pushes to a remote, tags or releases (`dzil release`) unless
  the project rules allow it (the kit's drive copy, the karr board to `origin`).

**Goes into the release-manager's body** (release audit, report and do not release):

1. `cpanfile`: every dependency declared, none declared that is not used (POD blocks
   excluded from the grep); Getty-authored dependencies pinned to their latest *released*
   CPAN version (`cpanm --info`), never to the unreleased `$VERSION` in the sibling repo.
2. `dist.ini`: version strategy consistent with `[@Author::GETTY]`; `copyright_year`
   current; `$VERSION` present in every module under `lib/`, the same literal.
3. `dzil build` clean, no missing files, no warnings.
4. `Changes` has an unreleased `{{$NEXT}}` section covering the user-visible changes
   since the last tag.

**The "pins ahead of CPAN" exception.** A coordinated family release stages pins ahead
of what CPAN knows, and an auditor not told "fixes" that every time. Record the
exception in the project's `<prefix>-core` (or `<prefix>-hazards`) skill, and name that
skill in the release-manager's body.

## Karr and the board

`.karr` agent execution, `karr-foundation` and the board habits:
[references/karr.md](references/karr.md). The karr install, skills and rule are the
kit's ("The board").

## Owner notes

[references/owner-notes.md](references/owner-notes.md), read when:

- the project is a large application that outgrows one worker (domain specialists);
- you write the hazards section of a project rules file;
- you write an ADR-auditor or a Codex agent, edit settings, or need the live check of a
  briefed agent.

## Sharing a role across repos

When the same agent or rule file is wanted in several repos, ship it through skilletor
(`agent:<name>@<source>`, `rule:<name>@<source>`; skill `skilletor`). Put an agent and
every skill in its `briefing.skills` into one bundle: a user-level agent never sees
project skills, and sync warns `briefing skills not installed` when they drift apart.
Installed copies (`.claude/agents/.local.*`) are build artifacts; change the source.

## Briefing, as it works now

The `briefing` plugin denies the spawn of an agent that names an unknown skill
(PreToolUse) and injects the skills when the subagent starts (SubagentStart); it does
not rewrite the prompt. Codex agents are `.codex/agents/*.toml` with a
`# briefing: skills = [...]` comment; skill `briefing` has the details.

## Bringing an existing setup in line

`ack-team check` reports what is missing (unresolved skills, `allowed-tools`, a top-level
`skills:` key, undeclared marketplaces, the hook). Audit by hand, and report before
editing, what it does not see:

- agent bodies that restate skill content: migrate to `briefing.skills`;
- a project rules file that duplicates a skill, lacks the house-rules bundle in
  `install.bundles` (`getty-house` or `getty-cpan-dist`), or still carries its own
  discipline list, delegation lock, karr block or release/public-issue gate: cut to what
  differs goes into the hazards or the lane table (the kit's rules file has no
  deviations section), project-specific discipline points go to hazards. If the house
  rules are missing, run `skilletor sync` and publish nothing until they load. The shared
  rules are `engineering-discipline`, `agent-delegation`, `publish-gate`, `board-karr`
  (older names: `getty-agent-delegation`, `getty-publish-gate`, `karr-coordination`);
- a read-only `<prefix>-release-checker`: replace with `<prefix>-release-manager`.
  An existing `karr-coordinator` is not drift (the kit names new ones
  `<family>-coordinator`);
- workers or writers briefed with commit-style, changelog or release skills, or told to
  commit: strip both, the release-manager owns them;
- doc-writers briefed with a whole release skill just for the doc format: brief the
  doc-format skill instead;
- `kanban-issues-karr-cli` in a working role: replace with `kanban-issues-karr-ticket`;
  in the coordinator: `kanban-issues-karr-coordination` plus `-ticket`;
- shared skills copied by hand or still hardlinked instead of installed (skill
  `getty-skill-library`, "Old pattern").
