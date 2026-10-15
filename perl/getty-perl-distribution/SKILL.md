---
name: getty-perl-distribution
description: Use when creating a Perl CPAN distribution or bringing an existing one in line with [@Author::GETTY] — dist.ini, cpanfile, Changes, lib/, t/, CI scaffolding.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Perl Distribution

Create or polish a Perl distribution matching Getty's workspace conventions.

## Inputs to resolve before writing

| What | Resolution order |
|---|---|
| `dist`      | dash-form (`WWW-Foo`) — from user arg or from the checkout dir name (`p5-www-foo` → `WWW-Foo`) |
| `module`    | colon-form (`WWW::Foo`) — derived from `dist` by `s/-/::/g`; `module_path` is its path form (`WWW/Foo`) |
| `abstract`  | one-line `# ABSTRACT:` from the first non-empty existing `lib/**/*.pm`, else ask |
| `copyright_year` | current year |
| `irc`       | optional. Only a real channel: an `irc =` line from a sibling `p5-*` `dist.ini` in the same topic cluster, else ask the user — never make one up |

`author`, `copyright_holder` and `license` are fixed — see *dist.ini header*.

## Sibling reference

Before writing, read **one** existing sibling dist that is closest in topic
(e.g. for a new `WWW-*` HTTP client, read an existing `WWW-*` client dist —
same shape, same layout). Match its layout exactly:

- `dist.ini`
- `cpanfile` (split `on test` / `on develop` if the sibling does)
- `Changes` (`{{$NEXT}}` marker with the initial bullet list; the release turns it into `0.001`)
- `README.md` (Synopsis → Description → one example per public method → License)
- `.gitignore` (copy sibling's, substituting the dist name in the build-dir ignore line)
- `LICENSE` — **never** from the sibling (most predate the check and have none):
  generated and committed, see *After writing*
- `t/00-load.t` using `Test::LoadAllModules` OR `use_ok` — match what the sibling uses
- Any additional `t/NN-*.t` the author convention calls for (often `10-*`, `20-*` topical tests)
- `.github/workflows/ci.yml` — the sibling's, else the fallback template (*CI workflow*)

Do NOT diverge from the sibling's style even if it feels outdated. Workspace
consistency beats "modern best practice."

## Test file conventions

- **Every `.t` opens with a shebang:** `#!/usr/bin/env perl`, then `use strict; use warnings; use Test::More;`
- **Close with `done_testing;`** — never `plan tests => N`.
- **Ship a load test** that `use_ok`s every module of the distribution, either via `Test::LoadAllModules` or an explicit `qw( ... )` list — match the sibling.

```perl
#!/usr/bin/env perl
use strict;
use warnings;
use Test::More;

for (qw(
  WWW::Foo
  WWW::Foo::Client
)) {
  use_ok($_);
}

done_testing;
```

## dist.ini header

Open every `dist.ini` with the metadata block, aligned on `=`:

```
name    = WWW-Foo
author  = Torsten Raudssus <getty@cpan.org>
license = Perl_5
copyright_holder = Torsten Raudssus <torsten@raudssus.de> L<https://raudssus.de/>
copyright_year   = 2026
```

- `author` carries the **cpan.org** address — that is what links the release to
  the PAUSE account across the CPAN subsystems. `copyright_holder` carries the
  everyday address plus the homepage link. Never swap the two, never fabricate
  either — older dists show other forms; new ones use exactly these lines.
- Copyright year in `dist.ini` and `Changes` must match.
- Every module under `lib/` and executable under `bin/` carries its own
  `our $VERSION`; a new dist starts at `'0.001'` (rules: `getty-perl-core`).

Then the plugin bundle. For Getty's own CPAN work that is `[@Author::GETTY]` —
its options are documented in `getty-perl-release-author-getty`.

## CI workflow

Every dist gets a `.github/workflows/ci.yml`. The Dist::Zilla CI mechanics live
ONCE in a shared composite action in the bundle repo; the per-dist workflow
carries only its matrix and any system-library install:

```yaml
- uses: Getty/p5-dist-zilla-pluginbundle-author-getty/.github/actions/dzil-test@main
```

The action runs `dzil authordeps` + `dzil listdeps --author` + `dzil test`. The
`--author` flag installs develop-phase author-test deps (e.g. `Test::Pod`, which
`[PodSyntaxTests]` registers). **Never fake `Test::Pod` into the cpanfile's
`on test`** — that is exactly the bug this setup removes.

- Pure-Perl dist: use the fallback template `templates/github-ci.yml` as-is.
- Alien / XS dist: add the `apt-get`/`brew` system-library step(s) before the
  action, and a `share-build` job passing `install-type: share`. Copy the
  layout from an existing Alien dist of the same shape.

## Templates

Fallbacks for when no suitable sibling exists, in `templates/`: `dist.ini`,
`cpanfile`, `Changes`, `README.md`, `claude-md.md`, `lib_Module.pm`,
`t_00-load.t`, `t_01-basic.t`, `github-ci.yml`. Substitute the `{{$name}}`
placeholders (leave `{{$NEXT}}` literal — it is Dist::Zilla's marker), then
rename: `lib_Module.pm` → `lib/<Path>/<Name>.pm`, `t_*.t` →
`t/*.t`, `claude-md.md` → `CLAUDE.md`, `github-ci.yml` →
`.github/workflows/ci.yml`. The names keep them inert in an installed skill — a
file named `CLAUDE.md` there would load as instructions.

## After writing

Write the licence file and track it. `[@Author::GETTY]` aborts the build without
a committed `LICENSE`, and the `git add` is not optional — the bundle gathers
through `Git::GatherDir`, which only sees tracked files:

```bash
dzil genlicense
git add LICENSE
```

Then run `dzil test` inside the dist directory and surface the output. Do NOT
`dzil release` unless the user explicitly asks.

## Related

- `getty-create-software` — parent orchestrator; loads this skill for Perl projects.
- `perl-release-dist-ini` — loaded when *editing* an existing `dist.ini`.
- `getty-perl-release-author-getty` — loaded when *releasing*.
- `getty-perl-core` — Getty's house Perl style rules, cpanfile pinning, `$VERSION`.
