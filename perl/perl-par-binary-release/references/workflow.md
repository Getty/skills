# release-binaries.yml skeleton

Replace `<name>` (binary and asset prefix), `<Dist>` and the `apt-get` packages with the
dist's own. The structure is the one karr, knarr and raider share; the optional `tag`
and the probe branch are the additions this skill prescribes.

```yaml
name: release-binaries
on:
  release:
    types: [published]
  workflow_dispatch:
    inputs:
      tag:
        description: Existing tag to build and attach assets to; empty = probe run (Actions artifacts only)
        required: false
permissions:
  contents: write
jobs:
  build:
    strategy:
      fail-fast: false
      matrix:
        include:
          - arch: x86_64
            runner: ubuntu-latest
          - arch: aarch64
            runner: ubuntu-24.04-arm
    runs-on: ${{ matrix.runner }}
    container:
      # Pinned to bookworm: older glibc (2.36), and the base image decides which
      # optional libs the bundled XS modules link. Bump only if
      # check-binary-libs.sh still passes.
      image: perl:5.40-bookworm
    # Values that reach shell go through env, never inline ${{ }} in a run: body.
    env:
      TAG: ${{ github.event.release.tag_name || inputs.tag }}
      ARCH: ${{ matrix.arch }}
    steps:
      - name: Install system build deps
        run: |
          apt-get update
          apt-get install -y build-essential git curl unzip libssl-dev zlib1g-dev
          curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
            | tee /usr/share/keyrings/githubcli-archive-keyring.gpg >/dev/null
          chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
          echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
            > /etc/apt/sources.list.d/github-cli.list
          apt-get update
          apt-get install -y gh
      - uses: actions/checkout@v5
        with:
          ref: ${{ env.TAG }}          # empty on a probe run: the dispatched ref
      - name: Fix safe.directory
        run: git config --global --add safe.directory "$GITHUB_WORKSPACE"
      - name: Install Perl deps and PAR::Packer
        env:
          TAR_OPTIONS: "--warning=no-unknown-keyword"   # cosmetic: quiets GNU tar
        run: |
          cpanm --notest --installdeps .
          cpanm --notest PAR::Packer
      - name: Compute version and asset base name
        id: v
        run: |
          v="${TAG#v}"
          v="${v:-probe}"
          echo "v=$v" >> "$GITHUB_OUTPUT"
          echo "base=<name>-$v-linux-$ARCH" >> "$GITHUB_OUTPUT"
      - name: Build binary
        env:
          <NAME>_BIN_OUT: ${{ steps.v.outputs.base }}
        run: ./scripts/build-binary.sh
      - name: Verify binary
        env:
          BASE: ${{ steps.v.outputs.base }}
        run: ./scripts/verify-binary.sh "$BASE"
      - name: Record and check runtime libs
        env:
          BASE: ${{ steps.v.outputs.base }}
        run: |
          # No pipe into tee: without pipefail its 0 would replace the check's 1.
          ./scripts/check-binary-libs.sh "$BASE"
          for lib in $(./scripts/check-binary-libs.sh --list); do
            grep -qF "\`$lib\`" README.md \
              || { printf '::error::README.md does not list runtime lib %s\n' "$lib" >&2; exit 1; }
          done
      - name: Package
        env:
          BASE: ${{ steps.v.outputs.base }}
          V: ${{ steps.v.outputs.v }}
        run: |
          mkdir -p "pkg/$BASE"
          cp "$BASE" "pkg/$BASE/<name>"
          cp LICENSE "pkg/$BASE/LICENSE"
          printf '<name> %s (linux-%s)\nRuntime libs required on target: %s\nhttps://github.com/<owner>/<repo>\n' \
            "$V" "$ARCH" "$(./scripts/check-binary-libs.sh --list)" > "pkg/$BASE/README"
          tar -C pkg -czf "$BASE.tar.gz" "$BASE"
      - name: Upload assets to the release
        if: env.TAG != ''
        env:
          GH_TOKEN: ${{ github.token }}
          BASE: ${{ steps.v.outputs.base }}
        run: |
          gh release upload "$TAG" "$BASE" "$BASE.tar.gz" \
            --clobber --repo "$GITHUB_REPOSITORY"
      - name: Keep the probe results as artifacts
        if: env.TAG == ''
        uses: actions/upload-artifact@v4
        with:
          name: ${{ steps.v.outputs.base }}
          path: |
            ${{ steps.v.outputs.base }}
            ${{ steps.v.outputs.base }}.tar.gz
  checksums:
    # One checksums file over every arch's assets; runs after both build jobs.
    needs: build
    if: github.event.release.tag_name != '' || inputs.tag != ''
    runs-on: ubuntu-latest
    env:
      TAG: ${{ github.event.release.tag_name || inputs.tag }}
    steps:
      - name: Build and upload one checksums file
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          v="${TAG#v}"
          out="<name>-$v-checksums.txt"
          mkdir dl
          # The -linux- glob matches binaries and tarballs, never the checksums
          # file or the CPAN dist tarball, so a re-run does not hash its own output.
          gh release download "$TAG" --repo "$GITHUB_REPOSITORY" \
            --pattern '<name>-*-linux-*' --dir dl
          ( cd dl && sha256sum <name>-*-linux-* ) > "$out"
          gh release upload "$TAG" "$out" --clobber --repo "$GITHUB_REPOSITORY"
```

## Extras seen in the three dists

- Alien dependency (karr): install the build-tool Alien first, then the share-built one.
  ```bash
  cpanm --notest Alien::cmake3
  ALIEN_INSTALL_TYPE=share cpanm --notest Alien::Libgit2 Git::Libgit2 Git::Native
  ```
- Recommends that the binary needs although `--installdeps` skips them (raider):
  `cpanm --notest IO::Async::SSL Mozilla::CA LWP::Protocol::https`, and make
  `build-binary.sh` refuse to build without them.
- Example config in the tarball (knarr): `cp share/example-config.yaml "pkg/$BASE/<name>.example.yaml"`.
