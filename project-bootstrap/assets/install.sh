#!/usr/bin/env sh
# install.sh — curl installer for releases published by this repo.
# Usage:  curl -fsSL https://raw.githubusercontent.com/OWNER/REPO/main/install.sh | sh
#         VERSION=v1.2.3 sh install.sh        # pin a version
#
# FILL IN these three before shipping, and keep the asset naming scheme stable
# forever — this script hard-codes it.
REPO="OWNER/REPO"
BIN="myapp"
INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/bin}"

set -eu

need() { command -v "$1" >/dev/null 2>&1 || { echo "error: $1 is required" >&2; exit 1; }; }
need curl; need uname

os="$(uname -s)"
arch="$(uname -m)"
case "$arch" in
  x86_64|amd64)  arch="x86_64" ;;
  arm64|aarch64) arch="aarch64" ;;
  *) echo "error: unsupported architecture: $arch" >&2; exit 1 ;;
esac

# Resolve version (latest release unless VERSION is set).
version="${VERSION:-}"
if [ -z "$version" ]; then
  version="$(curl -fsSL "https://api.github.com/repos/$REPO/releases/latest" \
    | grep '"tag_name"' | head -1 | cut -d '"' -f 4)"
  [ -n "$version" ] || { echo "error: could not determine latest release" >&2; exit 1; }
fi
echo "Installing $BIN $version"

# Pick the asset for this platform. Adjust names to match the release workflow.
case "$os" in
  Linux)
    # Prefer the AppImage for desktop apps; use the binary tarball for CLIs.
    asset="$BIN-$os-$arch.tar.gz" ;;
  Darwin)
    asset="$BIN-$os-$arch.tar.gz" ;;
    # For a desktop app, you might instead download the .dmg and hdiutil attach it.
  MINGW*|MSYS*|CYGWIN*)
    echo "On Windows, download the .msi from:" >&2
    echo "  https://github.com/$REPO/releases/download/$version/$BIN-$version-x86_64.msi" >&2
    exit 1 ;;
  *) echo "error: unsupported OS: $os" >&2; exit 1 ;;
esac

base="https://github.com/$REPO/releases/download/$version"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

echo "Downloading $asset..."
curl -fsSL "$base/$asset" -o "$tmp/$asset"

# Verify checksum — the release workflow must publish checksums.txt for this to work.
if curl -fsSL "$base/checksums.txt" -o "$tmp/checksums.txt" 2>/dev/null; then
  (cd "$tmp" && grep " $asset\$" checksums.txt | shasum -a 256 -c -) \
    || { echo "error: checksum verification failed" >&2; exit 1; }
else
  echo "warning: no checksums.txt in release; skipping verification" >&2
fi

mkdir -p "$INSTALL_DIR"
tar -xzf "$tmp/$asset" -C "$tmp"
install -m 755 "$tmp/$BIN" "$INSTALL_DIR/$BIN" 2>/dev/null \
  || cp "$tmp/$BIN" "$INSTALL_DIR/$BIN" && chmod 755 "$INSTALL_DIR/$BIN"

echo "Installed $BIN to $INSTALL_DIR/$BIN"
case ":$PATH:" in
  *":$INSTALL_DIR:"*) ;;
  *) echo "note: add $INSTALL_DIR to your PATH" ;;
esac
