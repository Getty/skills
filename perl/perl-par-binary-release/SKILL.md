---
name: perl-par-binary-release
description: "Use when a Perl dist should ship a standalone PAR::Packer (pp) binary in its GitHub release: release-binaries workflow, build/verify scripts, runtime-lib check."
---

# Shipping a PAR::Packer binary with a Perl release

A dist's GitHub release carries one `pp` binary per platform, so users run the CLI
without Perl. Four files make the recipe: a workflow `release-binaries.yml` and the
scripts `scripts/build-binary.sh`, `scripts/verify-binary.sh` and
`scripts/check-binary-libs.sh`. karr, knarr (`langertha-knarr`) and raider
(`langertha-raider`) ship this way; start from the closest one's files and keep the
shape.

Skeletons: [references/workflow.md](references/workflow.md) (the YAML) and
[references/scripts.md](references/scripts.md) (the three scripts). Read them when
writing the files; this page holds the decisions.

**Verification is the centre.** `pp` exits 0 on a binary that dies at runtime: a module
loaded by name is not found by the scanner, a share tree is not packed, an XS module
links a lib the target lacks. Each of those passes `--help`. The build is done when
`verify-binary.sh` and `check-binary-libs.sh` pass, not when `pp` returns.

## Workflow

- Triggers: `release: types: [published]` and `workflow_dispatch` with an optional
  `tag` input. `permissions: contents: write`.
- With a tag (from the release or the input) the run builds that tag and attaches the
  assets to its release, so a failed release build is redone after a fix on main by
  dispatching the tag. Without a tag the run is a probe: it builds and checks the chosen
  ref on every platform and keeps the results as Actions artifacts only, leaving every
  release untouched. Gate the release upload on `env.TAG != ''` and the artifact upload
  on `env.TAG == ''`.
- Matrix `x86_64` on `ubuntu-latest` and `aarch64` on `ubuntu-24.04-arm`,
  `fail-fast: false`.
- Container `perl:5.40-bookworm`, pinned to the bookworm tag, for two reasons: bookworm's
  older glibc (2.36) runs on newer glibc, and the base image decides which optional libs
  the bundled XS modules link. The trixie-based `perl:5.40` carries `-dev` packages such
  as `libthai-dev`, so `Unicode::LineBreak` links `libthai.so.0` and the binary dies at
  startup on every target without it. Bump the tag when `check-binary-libs.sh` still
  passes.
- Step order: system deps (`gh` included), checkout with `ref: ${{ env.TAG }}`,
  `git config --global --add safe.directory "$GITHUB_WORKSPACE"`, Perl deps
  (`cpanm --notest --installdeps .`, then `cpanm --notest PAR::Packer`), compute version
  and asset base name, build, verify, lib check, package, upload.
- Asset base name: `<name>-<version>-<os>-<arch>`, with `v="${TAG#v}"`.
- **Tag values reach shell only through `env`.** Set
  `TAG: ${{ github.event.release.tag_name || inputs.tag }}` at job level and write
  `"$TAG"` in `run:` bodies. Keep `${{ }}` out of `run:` bodies, so a crafted tag name
  cannot inject shell. Step outputs travel the same way, as `env:` entries
  (`BASE: ${{ steps.v.outputs.base }}`).
- Run the lib check as a plain command: the default shell has no `pipefail`, and a
  `tee` after it would replace the check's exit 1 with 0.
- A dist with an Alien dependency sets `ALIEN_INSTALL_TYPE=share` inline on the one
  `cpanm` call that builds that Alien (karr: `Alien::Libgit2`). Build-tool Aliens
  (`Alien::cmake3`) stay `system` and are installed first.

## build-binary.sh

`set -euo pipefail`, run from the checkout root, output path from `<NAME>_BIN_OUT`
(default `./<name>`). The `pp` call:

```bash
PAR_VERBATIM=1 pp -o "$OUT" -I lib "${mods[@]}" \
  -a "$SHARE_DIR;lib/auto/share/dist/<Dist-Name>" bin/<name>
```

- **`PAR_VERBATIM=1`** switches off pp's POD-stripping filter, which corrupts files with
  POD interleaved with code (`=attr`/`=method` blocks) until a module "did not return a
  true value".
- **`-I lib`** puts the checkout's `lib/` first on `@INC`, so the dist resolves although
  it is not installed in the CI container, and wins over an older installed copy.
- **The loaded set becomes `-M` options.** pp's scanner reads source. Whatever the code
  loads by name (`Module::Runtime`, `use_module`, `Module::Pluggable`, `require $class`,
  Moose meta roles, JSON/loop/reactor backends, `YAML::PP` schemas, XS boot requires)
  is invisible to it. Choose the variant by how much loads by name (table below) and add
  a `-M 'Pkg::**'` glob for each namespace whose members load on some path only.
- **Guard optional modules**: `-M` on a module that is not installed aborts pp, so add
  it with `perl -Ilib -M"$m" -e1 && opts+=(-M "$m")`.
- **Share directories via `-a "<src>;lib/auto/share/dist/<Dist-Name>"`.** That is where
  an installed dist's share lands below an `@INC` dir (`$PAR_TEMP/inc/lib` at runtime),
  so `File::ShareDir::dist_dir` finds it. pp packs no share tree by itself and exits 0
  for an `-a` path that is not there. Pack the dist's own `share/` and the share tree of
  each dependency that reads one (an Alien's `dist_dir`, Langertha's OpenAPI specs).
- **`-X <Module>`** leaves out an optional module that links a lib the target may lack
  (`Term::ReadLine::Gnu`, the Brotli codecs, `Net::LibIDN`); the code falls back.
- Guards at the top refuse to build when a precondition is missing: Alien not a `share`
  build, a required module not installed, not at the checkout root.
- Each `-M`/`-a`/`-X` line carries a comment naming the runtime failure it prevents;
  that is what the next maintainer lacks.

### Picking the variant

| Situation | Variant | Seen in |
|---|---|---|
| Small dist: dependencies named in `use` lines plus a few by-name loads | Hand-written `-M` list, `-M 'Dist::**'` globs for the dist's own namespaces | karr |
| Large framework underneath, most of it loading by name | Computed set: load every module of the namespace for real, run the lazy paths, print the `%INC` entries that come from their own file, pass them as `-M`; fail the build when the set is suspiciously small | knarr |
| The namespace is shared with sibling dists, or an older release left stale files in it | Name modules one by one from file lists (`find lib`, the installed dist's `.packlist`) | raider |

A `'Foo::**'` glob searches all of `@INC`, so the explicit list is the choice wherever
siblings share the namespace.

## verify-binary.sh

Takes the binary path, runs from a throwaway cwd, and treats the binary as a user's
machine would:

- **Fresh `PAR_GLOBAL_TEMP="$(mktemp -d)"`**, so the first start (extraction) is the one
  under test and a stale cache cannot hide a missing module.
- **A wiped environment**:
  `env -i PATH=/usr/local/bin:/usr/bin:/bin HOME="$work/home" PAR_GLOBAL_TEMP="$cache" "$BIN" ...`
  (or `unset PERL5LIB PERLLIB PERL5OPT` plus every `*_API_KEY`). No `PERL5LIB` for the
  binary to lean on, no credentials, no network; where the CLI talks HTTP, a fake
  upstream on 127.0.0.1.
- **Compare with the source tree.** The reference comes from `perl -Ilib bin/<name> ...`
  in the checkout; the binary gives the same stdout and the same exit code, on success
  and on error paths. Compare the version (`--version` against `$VERSION` in `lib/`),
  shipped files byte for byte (`cmp` each `share/` file against what the binary serves
  or installs), and the packed module set (unzip the binary, require every packed module
  with `@INC` limited to the archive's `lib/`).
- **Reach every path that loads by name**: `--help` of every subcommand class, one real
  round trip per backend (a database, libgit2, an HTTP request), the lazy loads of the
  request path. A missing module can hang instead of dying, so bound each run with
  `timeout`.
- `fail()` prints the cause and the tail of the logs; one `OK` line per stage and a final
  `verify: OK`.

## check-binary-libs.sh

A packed binary is portable when everything in it needs only the libs the README names.

- Unpack the binary (a zip behind the ELF head; `unzip` exits 1 for "extra bytes", 2 and
  up is a failure) and run `ldd` on the loader and on every `.so` inside.
- Compare lib names against two arrays: `RUNTIME_LIBS` (what a target installs, e.g.
  `libssl libcrypto`) and `BASE_LIBS` (`libc libm libpthread libdl librt libgcc_s
  ld-linux-.* linux-vdso libperl`). Names only, so the check runs in the build container
  where every lib is present; `libfoo.so.0 => not found` counts like a resolved one.
- `check-binary-libs.sh --list` prints `RUNTIME_LIBS`, the one place the set lives. The
  workflow writes it into each tarball's README and greps `README.md` for every listed
  lib in backticks, so docs and binary change together.
- A violation prints `::error::undocumented runtime lib <lib>, needed by: <objects>` and
  exits 1. The remedy is a base image that does not link it, an `-X`, or, when it should
  ship, an entry in `RUNTIME_LIBS` and the README.

## Packaging and checksums

- Per arch: the raw binary and `<base>.tar.gz` holding `<base>/<name>`, `LICENSE`, an
  example config where the dist has one, and a README with version, platform, runtime
  libs (`check-binary-libs.sh --list`) and the repository URL. Upload both with
  `gh release upload "$TAG" "$BASE" "$BASE.tar.gz" --clobber --repo "$GITHUB_REPOSITORY"`.
- Checksums: one `<name>-<version>-checksums.txt` from a final `checksums` job
  (`needs: build`) that downloads the release's `<name>-*-linux-*` assets and runs
  `sha256sum` over them. The glob matches binaries and tarballs, never the checksums
  file or the CPAN dist tarball, so a re-run does not hash its own output.
- `GH_TOKEN: ${{ github.token }}` as `env:` on every step that calls `gh`.
- `release: published` fires for a release made with a personal token; a release created
  by a workflow's `GITHUB_TOKEN` starts no workflow. Create the release the way the
  dist's release tool does (`dzil release` through the GitHub plugin), or dispatch the
  workflow with the tag.

## Done when

- `verify-binary.sh` and `check-binary-libs.sh` pass on both architectures, in the
  container, from a fresh cache.
- Every runtime lib `--list` prints appears in `README.md`.
- A probe run (dispatch without a tag) ends green with Actions artifacts and no release
  change.
