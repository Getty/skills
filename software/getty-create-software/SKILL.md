---
name: getty-create-software
description: "Use when creating a new project or module — 'create', 'new', 'scaffold', 'init' plus a name, for a Perl dist, Node app, Python package, Go binary, or a bare .gitignore."
---

# Create Software

Scaffold a new project to Getty's conventions: detect the type, create the
structure, `.gitignore`, and build config, init git. Language-specific depth
lives in dedicated skills — this one routes and covers the common ground.

## Detect the type

| Signal | Type | Action |
|---|---|---|
| `Foo::Bar` / `Foo-Bar` name, or `dist.ini` present | Perl/Dist::Zilla | Load skill `getty-perl-distribution` — it owns the full scaffold |
| `package.json` present or Node named | Node.js | `.gitignore` (nodejs), then `npm init` |
| `pyproject.toml`/`setup.py` present or Python named | Python | `.gitignore` (python), venv, `pyproject.toml` skeleton |
| `go.mod` present or Go named | Go | `.gitignore` (go), `cmd/<name>/main.go`, `go mod init` |
| Unclear | Generic | `.gitignore` (generic) only |

A name that fits two types (`Data::Cache` in a Python context) → ask, never
guess.

## Every project gets

- `.gitignore` from `templates/gitignore/<type>.gitignore` — plus the
  `claude.gitignore` block when the repo will carry a `.claude/` directory.
  Merge into an existing `.gitignore`, never overwrite custom patterns.
- `git init` + first commit (skill `getty-git-commit-style`) — only if not
  already inside a repo.
- A `README.md` stub naming what the thing is (one paragraph beats a
  template essay).

## Ask before proceeding when

- The project type is ambiguous.
- An existing `.gitignore` would lose custom patterns.
- Author/license metadata is needed and not derivable (`~/.gitconfig`,
  sibling projects) — never fabricate names, emails, or channels.

## Related

- `getty-perl-distribution` — the complete CPAN scaffold; this skill only
  routes to it.
- `getty-git-usage`, `getty-git-commit-style` — repo and commit conventions
  for the first commit.
