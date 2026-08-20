# CLAUDE.md

This repo is the **source of truth** for Getty's shared skills. Roughly 50 projects
hardlink against these files — every copy out there is the same inode as
the file here.

## Editing skill files — keep the inode

`Edit` and `Write` replace the file and detach its inode: every project keeps the old
content, silently. This holds for every file a skill directory ships —
`references/*.md` are hardlinked exactly like `SKILL.md`. **Edit any existing skill
file only with an in-place truncating write, and verify:**

```bash
cat > <group>/<skill>/SKILL.md <<'SKILL'
…full new content…
SKILL
stat -c '%i %h' <group>/<skill>/SKILL.md   # inode AND link count must equal pre-edit values
```

Record the `stat` output *before* editing, compare after. `cp new old` is equally safe;
`git mv`/`mv` keep inodes (renames are fine); `sed -i` renames on GNU — unsafe.
Brand-new files have no links yet — `Write` is fine there. If a link count ever drops,
say so and repair with `manage-skills sync` before doing anything else.

## Layout and rules

- `<group>/<skill-name>/SKILL.md` (+ optional `references/`, `templates/`).
- Placement, naming (`getty-` prefix semantics), grouping: skill `getty-skill-library`.
- Writing or reworking skill content: skill `skill-authoring`; shrinking or merging:
  skill `skill-compressor`. These are linked in `.claude/skills/` and load on demand.

## When skills change

- Update the group `README.md` and the root `README.md` lists — hand-maintained.
- Any skill added, renamed or moved → add or fix its path in the `skills` array of
  `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` by hand. The grouped
  layout lists each skill individually, `manage-skills package` refuses to touch an
  existing manifest, and its `--force` would replace the hand-written `description`
  with a placeholder. Then `claude plugin validate .` (a root-CLAUDE.md warning is
  expected; don't use `--strict`).
- Renames ripple: consuming repos reference skills by name in `briefing.skills` and
  `CLAUDE.md` files. Flag every rename in your summary.

## Repo conventions

- Commits follow skills `getty-git-commit-style` and `getty-git-usage` (linked in
  `.claude/skills/`). English skill content; never commit or push unasked.
- `.claude/skills/` holds relative symlinks into `skills/` — the repo dogfoods its own
  skills. Consumers are unaffected: source detection prefers `skills/`.
