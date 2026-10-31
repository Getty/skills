# Script skeletons

Three scripts under `scripts/`, each `#!/usr/bin/env bash` with `set -euo pipefail`.
Fill the `<...>` slots from the dist; comment every `-M`, `-a` and `-X` line with the
failure it prevents.

## build-binary.sh

```bash
OUT="${<NAME>_BIN_OUT:-./<name>}"
[ -f bin/<name> ] || { echo "ERROR: run from the checkout root" >&2; exit 1; }

# Preconditions that pp itself would not notice (examples):
#   an Alien must be a share build, or dist_dir points at host paths the target lacks
install_type=$(perl -MAlien::Foo -e 'print Alien::Foo->install_type')
[ "$install_type" = share ] || { echo "ERROR: Alien::Foo is '$install_type', need 'share'" >&2; exit 1; }

# Optional modules: -M on an absent module aborts pp.
optional=()
for m in Cpanel::JSON::XS JSON::XS; do
  perl -Ilib -M"$m" -e1 >/dev/null 2>&1 && optional+=(-M "$m")
done

# Share trees, packed where File::ShareDir looks in an installed dist.
DEP_SHARE=$(perl -MFile::ShareDir=dist_dir -e 'print dist_dir("<Dep-Dist>")')

# The loaded set (computed variant): load the namespace for real, then print every
# module that came from its own file. A module that fails to load is reported and left
# out; a tiny set means the loading went wrong.
mapfile -t loaded < <(perl -Ilib - <<'PERL'
use strict; use warnings; use File::Find ();
my %mods = ( '<Top::Module>' => 1 );
for my $dir ( grep { !ref } @INC ) {
  next unless -d "$dir/<Top>";
  File::Find::find( { no_chdir => 1, wanted => sub {
    return unless /\.pm\z/;
    ( my $m = substr $_, length($dir) + 1 ) =~ s{/}{::}g;
    $m =~ s/\.pm\z//;
    $mods{$m} = 1;
  } }, "$dir/<Top>" );
}
for my $m ( sort keys %mods ) {
  eval "require $m; 1" or warn "build-binary: not bundled: $m (" . ( split /\n/, $@ )[0] . ")\n";
}
# ... run the lazy loads the request path triggers here ...
for my $file ( sort keys %INC ) {
  next unless $file =~ m{\A[\w/]+\.pm\z};
  next unless defined $INC{$file} && !ref $INC{$file} && $INC{$file} =~ m{/\Q$file\E\z};
  ( my $m = $file ) =~ s{/}{::}g;
  $m =~ s/\.pm\z//;
  print "$m\n";
}
PERL
)
[ "${#loaded[@]}" -gt <N> ] || { echo "ERROR: loaded set suspiciously small (${#loaded[@]})" >&2; exit 1; }
mods=(); for m in "${loaded[@]}"; do mods+=(-M "$m"); done

PAR_VERBATIM=1 pp -o "$OUT" \
  -I lib \
  "${mods[@]}" \
  -M '<Dist>::**' \
  "${optional[@]}" \
  -X <Module-That-Links-A-Target-Lib> \
  -a "share;lib/auto/share/dist/<Dist-Name>" \
  -a "$DEP_SHARE;lib/auto/share/dist/<Dep-Dist>" \
  bin/<name>

chmod +x "$OUT"
echo "Built $OUT ($(du -h "$OUT" | cut -f1))"
```

The explicit-list variant (shared namespace) replaces the computed set with:

```bash
pm_to_mod() { sed -e 's#\.pm$##' -e 's#/#::#g'; }
mods=()
while IFS= read -r m; do mods+=(-M "$m"); done \
  < <(cd lib && find <Top> -name '*.pm' | sort | pm_to_mod)
```

Installed dependency modules can come from the dist's `.packlist`
(`$INC/auto/<Dist>/.packlist`), filtered with `grep -v` for the siblings to leave out.

## verify-binary.sh

```bash
BIN=$(realpath "${1:?usage: verify-binary.sh <binary>}")
[ -x "$BIN" ] || { echo "FAIL: not an executable: $BIN" >&2; exit 1; }
root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
work=$(mktemp -d); cache=$(mktemp -d)
trap 'rm -rf "$work" "$cache"' EXIT
mkdir -p "$work/home" "$work/cwd"; cd "$work/cwd"

fail() { echo "FAIL: $*" >&2; exit 1; }
tmo=${<NAME>_VERIFY_TIMEOUT:-120}

# The binary under a wiped environment and a fresh extraction cache.
bin() { env -i PATH=/usr/local/bin:/usr/bin:/bin HOME="$work/home" \
          PAR_GLOBAL_TEMP="$cache" timeout "$tmo" "$BIN" "$@"; }
# The reference: the same CLI from the checkout.
ref() { perl -I"$root/lib" "$root/bin/<name>" "$@"; }

# same_as_perl ARGS...: stdout and exit code match the checkout's perl run.
same_as_perl() {
  local want got rc_want=0 rc_got=0
  want=$(ref "$@" 2>/dev/null) || rc_want=$?
  got=$(bin "$@" 2>/dev/null)  || rc_got=$?
  [ "$rc_want" = "$rc_got" ] || fail "exit code for '$*': binary $rc_got, perl $rc_want"
  [ "$want" = "$got" ]       || fail "output for '$*' differs from perl -Ilib"
}

want_version=$(sed -n "s/^our \$VERSION = '\(.*\)';/\1/p" "$root/lib/<Module>.pm")
bin --version | grep -qF "$want_version" || fail "--version is not $want_version"
echo "startup (--version, fresh cache): OK"

for sub in <subcommands>; do bin "$sub" --help >/dev/null || fail "subcommand $sub"; done
echo "subcommands: OK"

same_as_perl <args that succeed>
same_as_perl <args that fail>          # error paths too
echo "output equals perl -Ilib: OK"

# Shipped files, byte for byte.
for f in $(cd "$root/share" && find . -type f); do
  cmp -s "$root/share/$f" <(bin <show-or-install-that-file>) || fail "share/$f"
done

# Packed module set: every module in the archive loads with @INC = archive lib/.
unzip -qq -o "$BIN" -d "$work/archive" 2>/dev/null || [ -d "$work/archive/lib" ] \
  || fail "cannot unpack the PAR archive"
# ... PLIB="$work/archive/lib" perl -e 'BEGIN { @INC = ($ENV{PLIB}) } ... require each ...'

echo "verify: OK"
```

Where the CLI talks HTTP, serve a fake upstream from core-only Perl
(`IO::Socket::INET` on `127.0.0.1`, port 0, one forked process per connection) and
point the binary at it; where it touches a repository or database, work in a
`mktemp -d` copy.

## check-binary-libs.sh

```bash
RUNTIME_LIBS=(libssl libcrypto)          # what a target must install; the README names the same
BASE_LIBS=(libc libm libpthread libdl librt libgcc_s ld-linux-.* linux-vdso libperl)

if [ "${1:-}" = "--list" ]; then echo "${RUNTIME_LIBS[*]}"; exit 0; fi

BIN=$(realpath "${1:?usage: check-binary-libs.sh <binary> | --list}")
[ -f "$BIN" ] || { echo "FAIL: no such file: $BIN" >&2; exit 1; }
allowed=$(IFS='|'; echo "${RUNTIME_LIBS[*]}|${BASE_LIBS[*]}")
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT

rc=0
unzip -qq -o "$BIN" -d "$work/par" || rc=$?       # exit 1 = warning (bytes before the zip)
[ "$rc" -le 1 ] || { echo "FAIL: cannot unpack the PAR archive (unzip exit $rc)" >&2; exit 1; }

objects=("$BIN")
while IFS= read -r -d '' f; do objects+=("$f"); done \
  < <(find "$work/par" -type f \( -name '*.so' -o -name '*.so.*' \) -print0 | sort -z)
[ "${#objects[@]}" -ge 2 ] || { echo "FAIL: no shared objects inside $BIN" >&2; exit 1; }

: > "$work/needs"
for obj in "${objects[@]}"; do
  { ldd "$obj" 2>/dev/null || true; } \
    | awk -v obj="${obj#"$work/par/"}" '$1 ~ /\.so/ {
        lib = $1; sub(/.*\//, "", lib); sub(/\.so.*/, "", lib); print lib "\t" obj }' \
    | sort -u >> "$work/needs"
done

echo "Shared libs the binary needs on the target (${#objects[@]} objects checked):"
cut -f1 "$work/needs" | sort -u | sed 's/^/  /'

undocumented=$(cut -f1 "$work/needs" | sort -u | grep -vxE "$allowed" || true)
if [ -n "$undocumented" ]; then
  for lib in $undocumented; do
    printf '::error::undocumented runtime lib %s, needed by: %s\n' "$lib" \
      "$(awk -F'\t' -v l="$lib" '$1 == l {print $2}' "$work/needs" | sort -u | paste -sd' ')" >&2
  done
  echo "FAIL: libs outside the documented runtime set (${RUNTIME_LIBS[*]})" >&2
  exit 1
fi
echo "runtime-libs check: only the documented libs are needed"
```
