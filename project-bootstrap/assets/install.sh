#!/usr/bin/env sh
# CLI tarball installer template. Fill in REPO and BIN before distribution.
# Each tarball must contain exactly one regular nonempty file named BIN at its root.
# Publish a sha256 checksums.txt alongside artifacts; verification is mandatory.
# Usage: VERSION=v1.2.3 sh install.sh
# A checksum from the same release detects corruption, not publisher compromise.
set -eu

REPO="OWNER/REPO"
BIN="myapp"
INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/bin}"

die() { echo "error: $*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || die "$1 is required"; }
[ "$REPO" != "OWNER/REPO" ] || die "configure REPO and BIN before distribution"
case "$BIN" in ''|.*|*[!a-zA-Z0-9_-]*) die "invalid binary name" ;; esac
for tool in curl uname awk tar mktemp cp chmod mv; do need "$tool"; done
if command -v sha256sum >/dev/null 2>&1; then
  checksum_tool=sha256sum
elif command -v shasum >/dev/null 2>&1; then
  checksum_tool=shasum
else
  die "sha256sum or shasum is required"
fi

os="$(uname -s)"
arch="$(uname -m)"
case "$arch" in
  x86_64|amd64) arch=x86_64 ;;
  arm64|aarch64) arch=aarch64 ;;
  *) die "unsupported architecture: $arch" ;;
esac
case "$os" in
  Linux|Darwin) ;;
  MINGW*|MSYS*|CYGWIN*) die "download the Windows installer from https://github.com/$REPO/releases" ;;
  *) die "unsupported OS: $os" ;;
esac

fetch() { curl --proto '=https' --tlsv1.2 -fsSL "$1" -o "$2"; }
tmp="$(mktemp -d)"
install_tmp=""
cleanup() {
  rm -rf "$tmp"
  if [ -n "$install_tmp" ]; then rm -f "$install_tmp"; fi
}
trap cleanup 0
trap 'exit 1' HUP INT TERM

version="${VERSION:-}"
if [ -z "$version" ]; then
  fetch "https://api.github.com/repos/$REPO/releases/latest" "$tmp/release.json"
  version="$(awk -F '"' '/"tag_name"[[:space:]]*:/ {print $4; exit}' "$tmp/release.json")"
fi
case "$version" in ''|.*|*[!a-zA-Z0-9._-]*) die "invalid or missing release version" ;; esac
asset="$BIN-$os-$arch.tar.gz"
base="https://github.com/$REPO/releases/download/$version"
echo "Downloading $BIN $version ($os/$arch)..."
fetch "$base/$asset" "$tmp/$asset"
fetch "$base/checksums.txt" "$tmp/checksums.txt" || die "checksums.txt is required"

# Parse an exact filename, rejecting missing/duplicate/malformed entries.
expected="$(awk -v asset="$asset" '
  { name=$2; sub(/^\*/, "", name) }
  name == asset {
    count++
    if (NF != 2 || length($1) != 64 || $1 ~ /[^0-9a-fA-F]/) bad=1
    digest=tolower($1)
  }
  END { if (count != 1 || bad) exit 1; print digest }
' "$tmp/checksums.txt")" || die "expected exactly one valid checksum for $asset"
if [ "$checksum_tool" = sha256sum ]; then
  actual="$(sha256sum "$tmp/$asset")"
else
  actual="$(shasum -a 256 "$tmp/$asset")"
fi
actual="${actual%% *}"
[ "$actual" = "$expected" ] || die "checksum verification failed"

# Stream only the selected regular member to a file we own. Never extract paths.
tar -tzf "$tmp/$asset" > "$tmp/members" || die "invalid tarball"
[ "$(cat "$tmp/members")" = "$BIN" ] || die "tarball must contain only $BIN at archive root"
[ "$(awk 'END {print NR}' "$tmp/members")" = 1 ] || die "duplicate archive members"
tar -tvzf "$tmp/$asset" > "$tmp/member-types" || die "invalid tarball metadata"
case "$(cat "$tmp/member-types")" in -*) ;; *) die "binary must be a regular file" ;; esac
tar -xzOf "$tmp/$asset" "$BIN" > "$tmp/binary" || die "could not read binary"
[ -s "$tmp/binary" ] || die "binary is empty"

mkdir -p "$INSTALL_DIR"
[ ! -d "$INSTALL_DIR/$BIN" ] || die "destination is a directory"
install_tmp="$(mktemp "$INSTALL_DIR/.$BIN.XXXXXX")"
cp "$tmp/binary" "$install_tmp"
chmod 755 "$install_tmp"
mv -f "$install_tmp" "$INSTALL_DIR/$BIN"
install_tmp=""
echo "Installed $BIN to $INSTALL_DIR/$BIN"
case ":$PATH:" in
  *":$INSTALL_DIR:"*) ;;
  *) echo "note: add $INSTALL_DIR to your PATH" ;;
esac
