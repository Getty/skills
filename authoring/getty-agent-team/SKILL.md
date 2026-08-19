---
name: getty-agent-team
description: "Use when a repo needs subagents — setting one up, wiring briefing, adding karr, or when .claude/agents is missing or drifted from the house pattern."
---

# Setup: agent team, skill base, house rules

Installs the setup used across this machine's projects (`dbio`, `langertha`,
`p5-app-karr`, `goldmine`, `hi-proto`, …). Nothing here is language-specific — the
Perl repos are just where it grew up.

**This skill is user-level only.** Its home is the shared library
(`~/dev/skills/authoring/`); it runs user-level, changes the target project, and is
done. Never hardlink or copy it into a project — the hardlink discipline below applies
to the *briefed* skills the agents need at runtime, not to this one. A project's
`.claude/` never mentions `getty-agent-team`.

## The architecture in four sentences

1. **Skills are the knowledge base.** Conventions, architecture, tooling. One source of
   truth per skill, shared across repos via hardlink (skill `manage-skills`).
2. **Agents are roles, not knowledge.** An agent file is a role sentence + a
   `briefing.skills` list + whatever is genuinely repo-specific and lives in no skill.
3. **`briefing` (plugin) force-loads those skills** into the subagent's context *before*
   its first turn, and **hard-fails the spawn** if a name doesn't resolve. No
   "MANDATORY: load X first" pleading, no silent skips.
4. **`.claude/rules/<prefix>-rules.md` carries discipline + the delegation lock** — it is
   auto-loaded for the orchestrating main agent, which gets no briefing and therefore
   must delegate instead of touching internals itself.

`karr` sits underneath as the coordination layer: a git-native board per repo, tickets
as the only legal cross-repo channel.

Bundled references — read the one you need, not all four:

| File | Holds |
|---|---|
| `references/agents.md` | role catalogue, frontmatter contract, agent templates |
| `references/rules-template.md` | the house-rules file, with the delegation lock |
| `references/karr.md` | karr install, `.karr`, `karr-foundation`, board discipline |
| `references/coordination-skill-template.md` | the `<prefix>-coordination` skill (families only) |

## Step 0 — prerequisites

```bash
grep -q '"briefing"' ~/.claude/plugins/known_marketplaces.json && echo "briefing marketplace: ok"
ls ~/.claude/plugins/cache/briefing/briefing >/dev/null 2>&1 && echo "briefing installed: ok"
command -v karr >/dev/null && echo "karr: ok"
```

If `briefing` is missing, ask the user to run these two slash commands (Claude cannot
run them):

```
/plugin marketplace add Getty/briefing
/plugin install briefing@briefing
```

Without briefing the whole setup degrades to prompt-stuffing — do not proceed by
inlining skill bodies into agent files as a workaround.

## Step 1 — discover the project

Before writing anything, establish:

| Question | How |
|---|---|
| Build / test / lint commands | `dist.ini`, `Makefile`, `justfile`, `package.json`, `Cargo.toml`, `pyproject.toml`, CI config |
| Recursive test gotchas | do subdirs under `t/` / `tests/` exist that the naive runner skips? |
| Single repo or family? | sibling repos with a shared prefix → family, needs cross-repo routing |
| Existing skills to brief from | `.claude/skills/`, `~/.claude/skills/`, and the sources `manage-skills locations` lists |
| Existing conventions worth encoding | `CLAUDE.md`, `CONTEXT.md`, `docs/adr/`, the code itself |
| Release path | CPAN / npm / container / deploy-only — determines whether a release role is needed |

**Prefix**: everything is named `<prefix>-<role>` where `<prefix>` is the project or
family name in kebab-case (`dbio`, `langertha`, `karr`). Family repos suffix the worker:
`dbio-worker-postgresql`. `karr-coordinator` is the one role that keeps its own name.

## Step 2 — settle the skill base first

`briefing` hard-fails on an unresolvable name, so every skill an agent lists must exist
before the agent file does. For each skill an agent needs:

- **Already shared** (the library `~/dev/skills`, or another project that owns it) →
  hardlink it in, never copy: `manage-skills link <name>`, or
  `ln <source>/SKILL.md .claude/skills/<name>/SKILL.md`. Rules and repair: skills
  `getty-skill-library` and `manage-skills`. **Never `Edit`/`Write` a hardlinked
  SKILL.md** — that breaks the inode chain; use `cat > path <<'EOF'`.
- **Project-owned and missing** → write it (skill `skill-authoring`). The two that most
  projects end up needing:
  - `<prefix>-core` — architecture, vocabulary, the invariants an implementer must know.
  - `<prefix>-coordination` — only for a repo *family*: who owns what, how tickets are
    routed. Template: `references/coordination-skill-template.md`.
- **Genuinely repo-specific and tiny** → put it in the agent body instead of inventing a
  skill for three lines.

Verify every name resolves before moving on:

```bash
for s in <skill> <skill> …; do
  ls .claude/skills/$s/SKILL.md ~/.claude/skills/$s/SKILL.md 2>/dev/null | head -1 \
    || echo "MISSING: $s"
done
```

## Step 3 — write the agents

Role catalogue, frontmatter contract, model/tool choices and full templates:
`references/agents.md`.

Minimum viable team: **worker** (always) + **release-checker** if the project ships
anything + **karr-coordinator** if it's a family. Add test-writer, doc-writer and
adr-auditor when the project has enough surface to warrant a lane.

Two rules that decide whether this setup works or rots:

- **Never restate skill content in the agent body.** The skills are already in context.
  The body says who the agent is, what its lane is, and what is true about *this repo*
  and written down nowhere else.
- **Every agent body ends the conventions paragraph with**: *"The conventions above are
  non-negotiable — apply silently, do not restate."*

## Step 4 — house rules

Write `.claude/rules/<prefix>-rules.md` from `references/rules-template.md`. Keep it
under ~90 lines; it is loaded on every single turn. It carries engineering discipline,
the **delegation lock** (the part that makes the main agent delegate), coordination, and
the release-permission rule. It does **not** carry language conventions — those are
skills, referenced by name.

## Step 5 — settings

`.claude/settings.json` (committed, project-wide):

```json
{
  "enabledPlugins": {
    "briefing@briefing": true
  }
}
```

Add `superpowers@claude-plugins-official` / `caveman@caveman` only if the user already
uses them in sibling repos. `.claude/settings.local.json` is per-machine permission
noise — never author it, never commit decisions into it.

## Step 6 — CLAUDE.md pointer

The repo's `CLAUDE.md` gets a short delegation table naming the agents and a line saying
where the rules and skills live. It must not duplicate rule or skill content — a
duplicated rule is a rule that will drift.

```markdown
## Delegation

Delegate behavior-relevant code to the right agent instead of touching it yourself —
principle and lane are in `.claude/rules/<prefix>-rules.md`.

| Task | Agent |
|---|---|
| Implement / refactor / debug behavior-relevant code | `<prefix>-worker` (default) |
| Write/extend tests | `<prefix>-test-writer` |
| Pre-release audit | `<prefix>-release-checker` |

The agents carry their skills via `briefing.skills` (see `.claude/agents/`); the main
agent delegates rather than loading them. Skill sources live under `.claude/skills/`.
```

## Step 7 — karr coordination (optional, default yes)

`karr init`, the `.karr` agent-execution file, the board conventions, cross-repo handoff
and the `karr-foundation` drain loop: `references/karr.md`.

Two hard-won operational rules go with it, and belong in the rules file of any repo that
fans work out:

- **Serialize karr mutations when fanning out.** Parallel implementation is fine;
  N concurrent `karr move`/`handoff`/`sync` calls landing together have OOM-rebooted a
  host. Collect results, then loop the board writes sequentially.
- **Public trackers are not a queue.** If the project has a public issue tracker
  (Codeberg/GitHub), agents never read, comment on or close an issue on their own
  initiative — only on explicit instruction, because every write publishes under the
  maintainer's name.

## Step 8 — verify

```bash
ls .claude/agents/ .claude/rules/ .claude/skills/ 2>/dev/null
python3 - <<'EOF'
import glob, re, os, sys
missing = []
for f in glob.glob('.claude/agents/*.md'):
    fm = open(f).read().split('---')[1]
    if 'briefing:' not in fm: print(f'{f}: no briefing block'); continue
    for name in re.findall(r'^\s*-\s*([\w:-]+)\s*$', fm.split('briefing:')[1], re.M):
        if not any(os.path.exists(p) for p in (
            f'.claude/skills/{name}/SKILL.md',
            os.path.expanduser(f'~/.claude/skills/{name}/SKILL.md'))):
            missing.append((f, name))
for f, n in missing: print(f'UNRESOLVED {n} in {f}')
print('all skills resolve' if not missing else 'FIX THESE — briefing will deny the spawn')
EOF
```

The plugin-namespaced form (`plugin:skill`) and plugin caches also resolve — the check
above only knows the two common locations, so treat its output as a first pass.

**You cannot spawn the new agents in the session that created them.** Claude Code reads
`.claude/agents/` at startup, so a fresh agent file is `not found` until the next
session. Drive the hook directly instead — it proves both halves without a restart:

```bash
HOOK=$(ls -d ~/.claude/plugins/cache/briefing/briefing/*/hooks/briefing-preload | tail -1)
printf '%s' '{"session_id":"t","cwd":"'"$PWD"'","tool_name":"Agent","tool_input":
{"subagent_type":"<prefix>-worker","description":"x","prompt":"MARKER"}}' \
  | tr -d '\n' | "$HOOK" | python3 -m json.tool | head -20
```

Expect an `updatedInput.prompt` many KB long, containing each briefed skill's body and
still carrying `MARKER`. Then repeat with a throwaway agent file listing a skill that
does not exist: the hook must answer `"permissionDecision": "deny"` naming the unknown
skill. Anything else means the setup is silently unbriefed. Delete the throwaway after.

Once a later session has the agents, the live check is behavioral: a briefed agent
answers a question that is only in its skills without calling the `Skill` tool. If it
reaches for `Skill`, the hook did not fire — check `enabledPlugins` in *this* project.

## Bringing an existing setup in line

Same steps, but audit first and report before editing: agents whose bodies restate skill
content (migrate to `briefing.skills`), agents still using the plain top-level `skills:`
key (**briefing deliberately ignores it — it only reads `briefing.skills`**), a rules file
that duplicates a skill, a missing delegation lock, skills copied instead of hardlinked
(skill `manage-skills-drift-triage`).
