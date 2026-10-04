# CLAUDE.md

This repo is the **source of truth** for Getty's shared skills. Consuming projects
install copies with skilletor; on this machine the checkout is their `local` source,
read directly on every `skilletor sync`.

## Editing skill files

Files here are plain files — `Edit` and `Write` are fine. A change reaches a consumer
at its next `skilletor sync` (one runs at session start); other machines see it after a
push. Edit here, never the installed copy in a consuming repo: sync overwrites it.

```bash
stat -c '%h' <group>/<skill>/SKILL.md   # 1 = plain file
```

A count above 1 means a manage-skills hardlink survived somewhere, and an edit here
changes that copy too. Say so, and clear it as skill `getty-skill-library` describes
under "Old pattern".

## Layout and rules

- `<group>/<skill-name>/SKILL.md` (+ optional `references/`, `templates/`).
- Placement, naming (`getty-` prefix semantics), grouping: skill `getty-skill-library`.
- Writing or reworking skill content: skill `skill-authoring`; shrinking or merging:
  skill `skill-compressor`. These are linked in `.claude/skills/` and load on demand.

## When skills change

- Update the group `README.md` and the root `README.md` lists — hand-maintained.
- Any skill added, renamed or moved → add or fix its path in the `skills` array of
  `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` by hand. The grouped
  layout lists each skill individually, and skilletor finds the skills through that
  array — an unlisted skill cannot be installed. Then `claude plugin validate .` (a
  root-CLAUDE.md warning is expected; don't use `--strict`).
- `bin/check-listings` verifies all listings at once; run it before committing.
- Renames ripple: consuming repos reference skills by name in `install.skills` of their
  `skilletor.json`, in `briefing.skills` and in `CLAUDE.md` files. Flag every rename in
  your summary.

## Repo conventions

- Commits follow skills `getty-git-commit-style` and `getty-git-usage` (linked in
  `.claude/skills/`). English skill content; never commit or push unasked.
- `.claude/skills/` holds relative symlinks into the groups — the repo dogfoods its own
  skills. Consumers are unaffected: skilletor skips symlinks.
