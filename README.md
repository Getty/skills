# Getty/skills

**The skills that don't belong to any one project.**

Skills managed with [manage-skills](https://github.com/Getty/manage-skills) live in
whichever repo owns them — a Perl module keeps its Perl skill, a Kubernetes cluster repo
keeps its cluster skill. This repo holds the rest: knowledge that applies across many
projects and has no single home of its own.

**The rule: a skill lives here only as long as nothing else claims it.** The moment a
skill belongs to one specific project, it moves there and this repo drops the link.

```
git/     commit conventions and repo workflow
k8s/     Kubernetes concepts, tool-agnostic
perl/    house style, object systems, async, MCP, release tooling
tools/   automation frameworks
```

Each group has its own README with the full skill list:
[git](git/README.md) · [k8s](k8s/README.md) ·
[perl](perl/README.md) · [tools](tools/README.md)

## Using this repo

```bash
manage-skills sources add ~/dev/skills Getty's shared skills
manage-skills locations                        # see what's available
manage-skills link getty-perl-moo getty-git-usage
```

Once this repo is pushed, anyone can add it the same way without a local checkout:

```bash
manage-skills sources add github:Getty/skills Getty's shared skills
```

## Naming

Not every skill is prefixed `getty-`. The prefix marks a skill that **prescribes**
something — a house convention chosen over other valid options (`getty-git-usage`:
rebase, not merge), or the API of software Getty itself wrote (`getty-perl-crawl4ai`:
there's no non-Getty way to call Getty's own module). Drop the prefix when a skill is
just a **reference** — documentation of how a public tool or protocol actually behaves,
equally true for anyone using it (`kubernetes-concepts`, `perl-mcp`).

When in doubt, ask: does this tell you what Getty chose, or just what the tool does?
The pattern either way is `{lang}-{name}` (`perl-moose`) or `{tool}` for something that
doesn't need a language qualifier (`rex`), with `getty-` prepended when it prescribes.

## Adding a skill

Write it where it's used first. Only pull it in here once a second, unrelated project
needs the same knowledge — that's the signal it has outgrown a single home. Put it in the
group that matches its language or domain, creating a new one at the repo root if none
fits.
