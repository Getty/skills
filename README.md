![skills](assets/github.png)

# Getty/skills

**The skills that don't belong to any one project.**

Skills managed with [manage-skills](https://github.com/Getty/manage-skills) live in
whichever repo owns them — a Perl module keeps its Perl skill, a Kubernetes cluster repo
keeps its cluster skill. This repo holds the rest: knowledge that applies across many
projects and has no single home of its own.

**The rule: a skill lives here only as long as nothing else claims it.** The moment a
skill belongs to one specific project, it moves there and this repo drops the link.

## The groups

| Group | Skills | What it holds |
|---|---|---|
| [authoring](authoring/README.md) | 5 | Skills about skills — writing them, mining them out of existing code, compressing them, the library's own rules, and the agent team that consumes them |
| [claude](claude/README.md) | 2 | Working with Claude itself — headless spawning, routing work across model tiers |
| [development](development/README.md) | 1 | Engineering practice independent of language — debugging discipline |
| [git](git/README.md) | 2 | How repositories are used, and how commit messages are written |
| [perl](perl/README.md) | 11 | House style, object systems, typing, async, MCP, release tooling |
| [software](software/README.md) | 1 | Project scaffolding across languages |
| [system-and-network-administration](system-and-network-administration/README.md) | 7 | Machines, networks, containers, Kubernetes, admin automation |

Each group README describes every skill in it: what it covers, and when to load it.

## Using this repo

Without a local checkout:

```bash
manage-skills sources add github:Getty/skills Getty's shared skills
manage-skills locations                        # see what's available
manage-skills link getty-perl-moo getty-git-usage
```

With a local checkout, register the groups you want:

```bash
manage-skills sources add <checkout>/perl Cross-project Perl practices
manage-skills sources add <checkout>/git  Git conventions
```

The same files also ship as a plugin for Claude Code (`.claude-plugin/`) and for
Codex (`.codex-plugin/`) — three distribution routes, one source of truth.

## Naming

`getty-` prefixed skills **prescribe** — a house convention chosen over other valid
options, or the API of Getty's own software. Unprefixed skills are **reference** —
documentation of how a public tool or protocol behaves, equally true for anyone.
The full naming and placement rules are themselves a skill:
[getty-skill-library](authoring/getty-skill-library/SKILL.md).

## Adding a skill

Write it where it's used first. Only pull it in here once a second, unrelated project
needs the same knowledge — that's the signal it has outgrown a single home. The
workbench for that is the [authoring group](authoring/README.md): `skill-authoring`
for the content, `getty-skill-library` for placement, naming, and the hardlink editing
discipline.

Every file here is hardlinked into the projects that use it — one inode, many repos.
Editing a `SKILL.md` with a tool that replaces the file detaches it, and every consumer
silently keeps the old content. `getty-skill-library` has the rules for editing safely;
`manage-skills check` is what proves they held.

## Licence

[Artistic License 2.0](LICENSE) — the Perl licence, because that is where most of this
came from.
