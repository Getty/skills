# {{$dist}} — CLAUDE.md

## Overview

{{$abstract}}

## Build System

Uses `[@Author::GETTY]` Dist::Zilla plugin bundle.

```bash
dzil test           # Build and test
prove -l t/         # Run tests directly
dzil build          # Build distribution
dzil release        # Release to CPAN
```

## License File

`LICENSE` is committed, not generated at build time. `[@Author::GETTY]` checks it
against `license`, `copyright_holder` and `copyright_year` from `dist.ini` and
aborts the build when it is missing or no longer matches:

```bash
dzil genlicense
git add LICENSE
```

The `git add` is not optional — the bundle gathers through `Git::GatherDir`, which
sees only tracked files, so an untracked LICENSE fails exactly like a missing one.
Re-run `genlicense` after changing any of the three settings.

## Project Structure

```
lib/{{$module_path}}.pm      # Main module
t/00-load.t                  # Basic load test
t/01-basic.t                 # Feature tests
cpanfile                     # Dependencies
Changes                      # Release history
LICENSE                      # dzil genlicense, committed
```

## Testing

- Tests in `t/` directory using Test::More
- Run `prove -l t/` for quick testing
- Run `dzil test` for full Dist::Zilla test

## POD Documentation

Uses `@Author::GETTY` PodWeaver. `# ABSTRACT:` required on every .pm file.
Inline `=attr`, `=method`, `=seealso` directives.

## Development Workflow

1. Make changes in `lib/` or `t/`
2. Run `prove -l t/`
3. Commit changes
4. Update `Changes` file with entries under `{{$NEXT}}`
5. Run `dzil release` when ready

---

See `~/.claude/CLAUDE.md` for global Perl workspace conventions.
