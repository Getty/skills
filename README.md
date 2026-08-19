# Getty/skills

**The skills that don't belong to any one project.**

Skills managed with [manage-skills](https://github.com/Getty/manage-skills) live in
whichever repo owns them — a Perl module keeps its Perl skill, a Kubernetes cluster repo
keeps its cluster skill. This repo holds the rest: knowledge that applies across many
projects and has no single home of its own.

**The rule: a skill lives here only as long as nothing else claims it.** The moment a
skill belongs to one specific project, it moves there and this repo drops the link.

```
authoring/    skills about skills — authoring, compressing, library rules, agent teams
claude/       working with Claude itself — headless spawning, model routing
development/  engineering practice — debugging discipline, workflows independent of language
git/          commit conventions and repo workflow
perl/         house style, object systems, async, MCP, release tooling
software/     project scaffolding, cross-language
system-and-network-administration/
              machines, networks, containers, Kubernetes, admin automation
```

Each group has its own README with the full skill list:
[authoring](authoring/README.md) · [claude](claude/README.md) ·
[development](development/README.md) · [git](git/README.md) · [perl](perl/README.md) ·
[software](software/README.md) ·
[system-and-network-administration](system-and-network-administration/README.md)

## Using this repo

Without a local checkout:

```bash
manage-skills sources add github:Getty/skills Getty's shared skills
manage-skills locations                        # see what's available
manage-skills link getty-perl-moo getty-git-usage
```

With a local checkout, register the groups you want:

```bash
manage-skills sources add ~/dev/skills/perl Cross-project Perl practices
manage-skills sources add ~/dev/skills/git  Git conventions
```

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
