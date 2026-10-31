---
name: perl-par-binary-release
description: "Use when a Perl dist should ship standalone PAR::Packer (pp) binaries in its GitHub release: release-binaries workflow, build/verify/smoke scripts, runtime-lib check."
---

# Shipping a PAR::Packer binary with a Perl release

A dist's GitHub release carries one `pp` binary per platform (Linux x86_64, Linux
aarch64, macOS arm64), so users run the CLI without Perl. The recipe is a workflow
`release-binaries.yml` plus `scripts/`: `build-binary.sh`, `loaded-modules.pl`,
`verify-binary.sh`, `check-binary-libs.sh` and `smoke-binary.sh`. Start from the closest
sibling dist's files and keep the shape.

Skeletons: [references/workflow.md](references/workflow.md) (the YAML and the README
text for users) and [references/scripts.md](references/scripts.md) (the scripts). Read
them when writing the files; this page holds the decisions.

**Verification is the centre.** `pp` exits 0 on a binary that dies at runtime: a module
loaded by name is not found by the scanner, a share tree is not packed, an XS module
links a lib the target lacks. Each of those passes `--help`. The build is done when
`verify-binary.sh`, `check-binary-libs.sh` and the smoke jobs pass, not when `pp` returns.

## Workflow

Three jobs, `build`, then `smoke`, then `release`.

- Triggers: `release: types: [published]` and `workflow_dispatch` with an optional
  `tag` input. `permissions: contents: write`.
- **The tag decides.** With a tag (from the release or the input) every job, build and
  smoke alike, checks out that tag (`ref: ${{ env.TAG }}`), so fixtures and `$VERSION`
  come from the release; a failed release build is redone by dispatching the tag after
  a fix. Without a tag the run is a probe: it builds and checks the chosen ref and keeps
  the results as Actions artifacts only, leaving every release untouched. Only the
  `release` job (`if` tag set) touches the release. The version step reads `$VERSION`
  from `lib/` (dzil-built dists may carry no literal `our $VERSION` in the repo), stops
  when it cannot (`[ -n "$want" ] || fail`), and stops when the tag does not match it.
- Hygiene: a `concurrency` group per tag with `cancel-in-progress: false` (two runs for
  one tag queue instead of racing on `--clobber`); `timeout-minutes` on every job (build
  30, smoke 30, release 15; a slow package mirror took 11 minutes once).
- **Tag values reach shell only through `env`.** Set
  `TAG: ${{ github.event.release.tag_name || inputs.tag }}` at job level and write
  `"$TAG"` in `run:` bodies, so a crafted tag name cannot inject shell. Step outputs
  travel the same way, as `env:` entries.
- Run the lib check as a plain command: the default shell has no `pipefail`, and a
  `tee` after it would replace the check's exit 1 with 0.
- **The build image sets the glibc floor.** Linux builds run in a pinned old-glibc image
  (`perl:5.40-bullseye`, glibc 2.31): the packed XS modules need the build image's glibc
  or newer, and the image decides which optional libs they link (a `-dev` package in a
  newer image can make `Unicode::LineBreak` link `libthai`). The lib check compares the
  floor against a constant (`GLIBC_MAX`), and the README names the same version.
- macOS builds on `macos-14` (arm64) with Perl from `shogo82148/actions-setup-perl@v1`.
  The scripts stay bash-3.2 compatible (`while read` loops, no `mapfile`) and `tar` is
  bsdtar there.
- A dist with an Alien dependency sets `ALIEN_INSTALL_TYPE=share` inline on the one
  `cpanm` call that builds that Alien. Build-tool Aliens (`Alien::cmake3`) stay `system`
  and are installed first.

## build-binary.sh and loaded-modules.pl

`set -euo pipefail`, run from the checkout root, output path from `<NAME>_BIN_OUT`.

```bash
PAR_VERBATIM=1 pp -o "$OUT" -I lib "${mods[@]}" -M 'Dist::**' bin/<name>
```

- **`PAR_VERBATIM=1`** switches off pp's POD-stripping filter, which corrupts files with
  POD interleaved with code until a module "did not return a true value".
- **`-I lib`** puts the checkout's `lib/` first on `@INC`, so the dist resolves although
  it is not installed in the CI container.
- **One computed module set for build and verify.** `scripts/loaded-modules.pl` loads the
  dist's namespace for real, runs every command path (help, version, each subcommand, the
  error paths) and prints the `%INC` entries that come from their own file. Build turns
  each line into `-M`; verify requires each inside the binary. One source, so the two
  cannot drift. pp's scanner reads source and misses whatever loads by name
  (`Module::Runtime`, `require $class`, backend choosers like `Locale::TextDomain`,
  `Module::Pluggable`, Moose meta roles, JSON/loop backends, `YAML::PP` schemas); the
  script lists such backends explicitly. The build fails when the set is suspiciously
  small.
- A `-M 'Pkg::**'` glob covers a namespace whose members load on some path only. It
  searches all of `@INC`, so name modules one by one (from `find lib` or the installed
  dist's `.packlist`) when sibling dists share the namespace or an older release left
  stale files in it.
- **Guard optional modules**: `-M` on a module that is not installed aborts pp, so add
  it with `perl -Ilib -M"$m" -e1 && opts+=(-M "$m")`.
- **Share directories via `-a "<src>;lib/auto/share/dist/<Dist-Name>"`**, where an
  installed dist's share lands below an `@INC` dir, so `File::ShareDir::dist_dir` finds
  it. pp packs no share tree by itself and exits 0 for an `-a` path that is not there.
  Pack the dist's own `share/` and each dependency's share tree that is read.
- **`-X <Module>`** leaves out an optional module that links a lib the target may lack
  (`Term::ReadLine::Gnu`, Brotli codecs, `Net::LibIDN`); the code falls back.
- Guards at the top refuse to build when a precondition is missing: Alien not a `share`
  build, a runtime dependency not installed, not at the checkout root.
- Each `-M`/`-a`/`-X` line carries a comment naming the runtime failure it prevents.

## verify-binary.sh

Takes the binary path, runs from a throwaway cwd, treats the binary as a user's machine
would, and runs where it was built.

- **Fresh `PAR_GLOBAL_TEMP="$(mktemp -d)"`**, so the first start (extraction) is the one
  under test; then a second start on the same cache.
- **A wiped environment** (`env -i PATH=... HOME="$work/home" PAR_GLOBAL_TEMP=...`): no
  `PERL5LIB` to lean on, no credentials, no network; where the CLI talks HTTP, a fake
  upstream on 127.0.0.1.
- **Compare with the source tree.** `perl -Ilib bin/<name> ...` is the reference: same
  stdout and exit code on success and error paths, and a reference that printed nothing
  fails the case. Compare `--version` with `$VERSION`, shipped files byte for byte
  (`cmp`), and every module of the computed set inside the unzipped archive. Verify
  outside the build's `@INC`: the host's modules mask a missing one, so the check reads
  the archive's `lib/`, never the host.
- **Reach every path that loads by name**: `--help` per subcommand, one real round trip
  per backend. Bound each run with `timeout` (macOS: a `perl -e 'alarm shift; exec @ARGV'`
  fallback), since a missing module can hang.
- `fail()` prints the cause; one `OK` line per stage and a final `verify: OK`.

## check-binary-libs.sh

A packed binary is portable when everything in it needs only the libs the README names.

- Unpack the binary (a zip behind the ELF head; `unzip` exit 1 is a warning, 2 and up a
  failure) and run `ldd` (Darwin: `otool -L`, with the system dylibs as `BASE_LIBS`) on
  the loader and every shared object inside. Compare names against `RUNTIME_LIBS` (what
  a target installs) and `BASE_LIBS` (`libc libm libpthread libdl librt libgcc_s
  ld-linux-.* linux-vdso libperl`); `libfoo.so.0 => not found` counts like a resolved one.
- **Runtime libs the loader needs come from the system.** The `pp` loader executable
  links libperl, which needs `libcrypt.so.1` before PAR extracts anything, so `pp -l`
  cannot pack it. List such libs in `RUNTIME_LIBS`, the one place the set lives
  (`check-binary-libs.sh --list`), name them in the README with the package that carries
  them (RHEL, Rocky, Alma, Fedora, Amazon Linux, Arch: `libxcrypt-compat`), and let CI
  grep `README.md` for every listed lib in backticks.
- A violation prints `::error::undocumented runtime lib <lib>, needed by: <objects>` and
  exits 1. The remedy is a base image that does not link it, an `-X`, or an entry in
  `RUNTIME_LIBS` and the README.
- The glibc check takes the highest `GLIBC_x.y` among the objects' undefined symbols
  (`objdump -T`) and compares it with `GLIBC_MAX`.

## smoke-binary.sh and the smoke job

Smoke what users download, on machines that never built it.

- Cells: `almalinux:9`, `ubuntu:22.04`, `debian:bullseye-slim` (x86_64), `almalinux:9`
  (aarch64), `macos-14`, `macos-15`. No setup-perl, no build container; the script runs
  under `env -i` and the cell asserts the build Perl is absent (`/usr/local/lib/perl5`
  on Linux, the hosted-toolcache perl on macOS).
- **Linux cells start the clean image with `docker run`** on the runner host, checkout
  and artifacts mounted. A clean image has no git, and `actions/checkout` without git
  fetches the REST archive, which honours `export-ignore`, so scripts and test fixtures
  go missing. The `dnf` cells install the runtime lib with a three-try retry loop.
- With the tarball the script unpacks it: one directory named like the tarball, holding
  the binary (executable as extracted, `cmp`-identical to the bare asset), `LICENSE` and
  `README`; the checks (version, a fixture converted byte-identically, an error path)
  then run against the extracted binary.

## Packaging, checksums, users

- Per platform: the raw binary and `<base>.tar.gz` holding `<base>/<name>`, `LICENSE`
  and a README (version, platform, runtime libs, glibc floor, quarantine hint on macOS,
  repository URL); `<base>` is `<name>-<version>-<os>-<arch>`. Build jobs upload both as
  Actions artifacts in every mode.
- The `release` job (`needs: [build, smoke]`) downloads all artifacts and writes one
  `<name>-<version>-checksums.txt` (`sha256sum` over every asset), then runs
  `gh release upload "$TAG" dl/<name>-* "$out" --clobber`. It runs on the plain runner,
  where `gh` exists; `GH_TOKEN: ${{ github.token }}` goes in its `env:`.
- `release: published` fires for a release made with a personal token; a release created
  by a workflow's `GITHUB_TOKEN` starts no workflow. Create the release the way the
  dist's release tool does (`dzil release`), or dispatch the workflow with the tag.
- **The dist README tells users** (text in `references/workflow.md`): the bare asset
  arrives without the executable bit (HTTP downloads carry no mode, `upload-artifact`
  drops it too), so `install -m 755` or `chmod +x`; the checksum check
  `grep " <asset>\$" <checksums> | sha256sum -c` (macOS: `shasum -a 256 -c`) works
  without `--ignore-missing`; the macOS binary is unsigned, so after a browser download
  `xattr -d com.apple.quarantine <name>` (a `curl` download sets no flag).

## Done when

- `verify-binary.sh` and `check-binary-libs.sh` pass on every build platform, from a
  fresh cache, and every smoke cell passes on the tarball.
- Every runtime lib `--list` prints appears in `README.md`.
- A probe run (dispatch without a tag) ends green with Actions artifacts and no release
  change; a tag dispatch ends with assets and one checksums file on the release.
