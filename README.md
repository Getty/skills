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
| [claude](claude/README.md) | 3 | Working with Claude itself — headless spawning, talking across running sessions, routing work across model tiers |
| [codex](codex/README.md) | 2 | Working with the Codex CLI — non-interactive runs, and reaching threads that already exist |
| [development](development/README.md) | 1 | Engineering practice independent of language — debugging discipline |
| [git](git/README.md) | 2 | How repositories are used, and how commit messages are written |
| [perl](perl/README.md) | 11 | House style, object systems including Mojo::Base, typing, async, MCP, XS and Alien, release tooling |
| [social-media](social-media/README.md) | 2 | LinkedIn and Twitch — platform mechanics, content practice, and the DACH legal duties that have no US equivalent |
| [software](software/README.md) | 1 | Project scaffolding across languages |
| [system-and-network-administration](system-and-network-administration/README.md) | 8 | Machines, networks, containers, Kubernetes, admin automation |

Each group README describes every skill in it: what it covers, and when to load it.

## Every skill

### [authoring](authoring/README.md)

| Skill | What it is |
|---|---|
| [getty-agent-team](authoring/getty-agent-team/SKILL.md) | A whole multi-agent setup for a project: subagents, briefing-preloaded skills, karr wiring |
| [getty-skill-library](authoring/getty-skill-library/SKILL.md) | Where a skill lives, what it is named, and how the hardlinks stay intact |
| [skill-authoring](authoring/skill-authoring/SKILL.md) | Writing a SKILL.md that fires from its description and then gets followed |
| [skill-compressor](authoring/skill-compressor/SKILL.md) | Shrinking or merging skills without losing the rules that drive behaviour |
| [skill-mining](authoring/skill-mining/SKILL.md) | Deriving skill content from a codebase instead of inventing conventions |

### [claude](claude/README.md)

| Skill | What it is |
|---|---|
| [claude-cross-session](claude/claude-cross-session/SKILL.md) | One Claude session starting, watching and messaging another |
| [claude-headless](claude/claude-headless/SKILL.md) | Driving Claude Code as a subprocess: `-p`, JSON, permissions, the multi-turn channel |
| [model-routing](claude/model-routing/SKILL.md) | Choosing a model tier by the hardest dimension the work routinely hits |

### [codex](codex/README.md)

| Skill | What it is |
|---|---|
| [codex-cross-session](codex/codex-cross-session/SKILL.md) | Reaching an existing Codex thread: the queue, the daemon, `--remote` |
| [codex-headless](codex/codex-headless/SKILL.md) | `codex exec` non-interactively: JSONL events, sandboxes, resuming a thread |

### [development](development/README.md)

| Skill | What it is |
|---|---|
| [feedback-loop-debugging](development/feedback-loop-debugging/SKILL.md) | A six-phase discipline for hard bugs, built on a fast pass/fail signal |

### [git](git/README.md)

| Skill | What it is |
|---|---|
| [getty-git-commit-style](git/getty-git-commit-style/SKILL.md) | Imperative summary, one body line per change, and how changelog entries read |
| [getty-git-usage](git/getty-git-usage/SKILL.md) | Linear history: rebase over merge, and `--force-with-lease` after it |

### [perl](perl/README.md)

| Skill | What it is |
|---|---|
| [getty-perl-core](perl/getty-perl-core/SKILL.md) | The base layer: module loading, object-system choice, errors, subroutine shape |
| [getty-perl-distribution](perl/getty-perl-distribution/SKILL.md) | Creating a CPAN distribution, or bringing an existing one to house standard |
| [getty-perl-moo](perl/getty-perl-moo/SKILL.md) | Moo classes and roles — roles for reuse, inheritance only for a stable is-a |
| [getty-perl-moose](perl/getty-perl-moose/SKILL.md) | The same shape in Moose, plus `make_immutable` on every class |
| [getty-perl-typing](perl/getty-perl-typing/SKILL.md) | Whether a project needs a type system at all, and which one is cheap here |
| [perl-alien](perl/perl-alien/SKILL.md) | `Alien::Build`: providing a C library or tool through CPAN |
| [perl-io-async-future](perl/perl-io-async-future/SKILL.md) | PEVANS-style async Perl, and its unforgiving lifetime rules |
| [perl-mcp](perl/perl-mcp/SKILL.md) | Building an MCP server in Perl with `MCP::Server` |
| [perl-mojo](perl/perl-mojo/SKILL.md) | `Mojo::Base` as an object system, plus the `Mojo::*` toolkit around it |
| [perl-release-dist-ini](perl/perl-release-dist-ini/SKILL.md) | Dist::Zilla for any distribution, independent of the author bundle |
| [perl-xs](perl/perl-xs/SKILL.md) | The Perl/C boundary, and why an `.xs` file is C behind a preprocessor |

### [social-media](social-media/README.md)

| Skill | What it is |
|---|---|
| [linkedin](social-media/linkedin/SKILL.md) | Formats, how distribution actually works, and the DACH legal duties |
| [twitch](social-media/twitch/SKILL.md) | Channel operation end to end: encoder, growth, chat, monetization, moderation |

### [software](software/README.md)

| Skill | What it is |
|---|---|
| [getty-create-software](software/getty-create-software/SKILL.md) | Scaffolding a new project from the signals that reveal its type |

### [system-and-network-administration](system-and-network-administration/README.md)

| Skill | What it is |
|---|---|
| [docker](system-and-network-administration/docker/SKILL.md) | Docker and Compose as one workflow — the decisions and the traps |
| [docker-engine-api](system-and-network-administration/docker-engine-api/SKILL.md) | Speaking the Engine API over the socket instead of shelling out to `docker` |
| [docker-registry](system-and-network-administration/docker-registry/SKILL.md) | `registry:2` as two products in one binary, and the pull-through trap |
| [kubernetes-cilium-concepts](system-and-network-administration/kubernetes-cilium-concepts/SKILL.md) | Cilium replacing CNI, kube-proxy, policy, encryption and ingress at once |
| [kubernetes-concepts](system-and-network-administration/kubernetes-concepts/SKILL.md) | Control plane, resource hierarchy, and how ownership and selectors tie it together |
| [kubernetes-gpu](system-and-network-administration/kubernetes-gpu/SKILL.md) | The four layers that must line up before a pod can use a GPU |
| [kubernetes-rke2](system-and-network-administration/kubernetes-rke2/SKILL.md) | RKE2 and K3s as one topic, with the differences named where they exist |
| [rex](system-and-network-administration/rex/SKILL.md) | Perl automation from a `Rexfile`, and the OpenSSH connection trap |

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

A skill has to be listed in four places — its group README, the group table and the
skill table above, and both plugin manifests. `bin/check-listings` holds them against
the directories and names what is missing; it exits non-zero, so it fits a hook or CI.

Every file here is hardlinked into the projects that use it — one inode, many repos.
Editing a `SKILL.md` with a tool that replaces the file detaches it, and every consumer
silently keeps the old content. `getty-skill-library` has the rules for editing safely;
`manage-skills check` is what proves they held.

## Licence

[Artistic License 2.0](LICENSE) — the Perl licence, because that is where most of this
came from.
