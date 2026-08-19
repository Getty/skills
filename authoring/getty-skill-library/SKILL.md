---
name: getty-skill-library
description: Use when adding, naming, moving or renaming a skill in Getty's projects, linking one into a repo with manage-skills, or before editing a hardlinked SKILL.md.
---

# Getty's Skill Library

How skills are owned, named, shared, and edited across Getty's
projects. The shared library is [Getty/skills](https://github.com/Getty/skills);
the transport is
[manage-skills](https://github.com/Getty/manage-skills) — one source file per
skill, hardlinks everywhere else.

## Where a skill lives

**A skill lives in the repo that owns its subject.** A Perl module keeps its
module skill, a cluster repo keeps its cluster skill. The shared library holds
only what has no single home:

- Knowledge a *second, unrelated* project needs → promote it to the
  library as `<group>/<name>/` and hardlink it back. Write it where
  it is used first; promotion is triggered by the second consumer, never by
  anticipation.
- Skills that run only user-level (never linked into a project, e.g.
  `getty-agent-team`) also live in the library — it is their home repo.
- The moment a shared skill turns out to belong to one project, it moves
  there and the library drops it.

Groups are one directory level under `skills/`, each with a `README.md`
listing its skills; the root `README.md` lists the groups (the directory
listing is the authority — this skill deliberately doesn't enumerate them).
Create a new group only when no existing one fits — a domain name, never a
`misc` drawer. "Didn't know where to put it" means a new group is due, not
that the nearest group absorbs it.

## Naming

Pattern: `{lang}-{name}` (`perl-mcp`) or `{tool}` (`rex`), kebab-case.
Prepend `getty-` when the skill **prescribes** — a house choice among valid
options (`getty-git-usage`: rebase, not merge) or the API of Getty's own
software. Drop the prefix when it is **reference** — equally true for anyone
using the tool (`kubernetes-concepts`, `perl-mcp`). The test: does it tell you
what Getty chose, or just what the tool does?

Skill names are flat and global across all sources — check for collisions
before naming (`manage-skills list`). Renaming a skill means chasing every
`briefing.skills` entry and `CLAUDE.md` reference in every consuming repo;
name it right the first time.

## Editing a shared skill — keep the inode

Skill files are hardlinked across projects: every copy is the same inode.
`Edit` and `Write` replace the file and detach it — every other project
silently keeps the old content. **Edit hardlinked skill files only with an
in-place truncating write:**

```bash
cat > <group>/<skill>/SKILL.md <<'SKILL'
…full new content…
SKILL
stat -c '%i %h' <group>/<skill>/SKILL.md   # inode AND link count must match pre-edit
```

`cp new old` is equally safe; `sed -i` renames on GNU — unsafe. This applies
in the library *and* in any project holding a linked copy. `git mv` and plain
`mv` keep the inode — renames are safe. A brand-new file has no links yet;
`Write` is fine until the first link exists.

Detached anyway? `manage-skills sync` relinks copies whose content still
matches their source; a diverged copy is reported and kept (`--force`
overwrites — only when you know the divergence is accidental).

## Wiring a project

```bash
manage-skills sources add <checkout>/<group> <label>   # once per group
manage-skills link <skill> [<skill>…]    # hardlink into ./.claude/skills/
manage-skills check                      # verify inode integrity
manage-skills sync                       # repair stale links
```

Register library groups individually (group-level dirs); `manage-skills
locations` shows what resolves. Remote consumers use
`manage-skills sources add github:Getty/skills` — grouped layouts are
detected there.

## Distribution duties (library repo)

Three routes ship the same files: manage-skills source, Claude Code plugin,
Codex plugin. When skills or groups are added, renamed, or moved:

1. Update the group `README.md` and the root `README.md` skill lists — they
   are hand-maintained and drift silently.
2. Regenerate the plugin manifests: `manage-skills package` (writes
   `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`); validate
   with `claude plugin validate .`.
3. The marketplace entry lives in `Getty/marketplace`, not here.

## Related

- `skill-authoring` — how to write the skill's content.
- `skill-compressor` — shrinking or merging existing skills.
