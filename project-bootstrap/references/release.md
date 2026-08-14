# Release flow

## The trigger: tags, not buttons

Pushing a tag `v1.2.3` triggers the release workflow. Reasons: the tag is the audit trail, anyone with push access can release without dashboard access, and the version in the tag is a single source of truth. Use `on: push: tags: ["v*"]`.

Keep the version in the manifest (`tauri.conf.json`, `package.json`, `Cargo.toml`) in sync with the tag — either bump it in a release commit before tagging, or have the workflow inject the tag version into the manifest at build time (tauri-action supports `--args` / version overrides; electron-builder reads package.json).

## Desktop apps: dmg / msi / AppImage

The full per-stack release recipes live in the stack references — this file holds the shared principles:

- **Tauri** → `references/rust-tauri.md` + `assets/workflows/release-tauri.yml` (tauri-action, the smoothest path)
- **Electron** → `references/electron.md` (electron-builder `--publish always` on a tag-checked-out matrix)
- **Wails** → `references/wails.md` (no helper action; manual matrix + create-dmg / NSIS / linuxdeploy)
- **macOS Swift app** → `references/swift-apple.md` (archive → Developer ID export → notarytool → create-dmg)

### Tauri

Use `assets/workflows/release-tauri.yml`. `tauri-apps/tauri-action@v0` on a 3-OS matrix produces:

- **macOS**: `.dmg` (+ `.app.tar.gz` for auto-updater)
- **Windows**: `.msi` (+ `.exe` NSIS if configured in tauri.conf.json)
- **Linux**: `.AppImage` + `.deb`

It creates a draft GitHub Release and uploads everything. Gotchas that bite everyone:

- Linux runner needs `libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev patchelf` — without these the build fails 15 minutes in.
- For Apple Silicon + Intel builds, add `macos-13` (Intel) and `macos-14` (ARM) matrix entries with `tauri build --target` as needed; a single macos-latest only covers one arch.
- Signing: works unsigned. `TAURI_SIGNING_PRIVATE_KEY`/`TAURI_SIGNING_PRIVATE_KEY_PASSWORD` secrets enable the updater signature; Apple notarization needs `APPLE_CERTIFICATE`, `APPLE_CERTIFICATE_PASSWORD`, `APPLE_SIGNING_IDENTITY`, `APPLE_ID`, `APPLE_PASSWORD`, `APPLE_TEAM_ID`. Set up the workflow so these are optional, and list the missing ones for the user at the end.

### Electron

`electron-builder` with a matrix job; publish via `softprops/action-gh-release` or electron-builder's own `publish: onTagOrDraft`:

```yaml
- run: pnpm build && pnpm exec electron-builder --publish always
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

electron-builder's `publish` needs the tag checked out — guard with `if: startsWith(github.ref, 'refs/tags/v')`. Targets in package.json `build`: `mac.target: dmg`, `win.target: msi` (or nsis), `linux.target: AppImage`.

## CLI tools: binary matrix

Cross-compile per target in a matrix (`cargo build --release --target <triple>`, `go build`, PyInstaller, `pkg`/`bun build --compile`), upload `myapp-<os>-<arch>.tar.gz` plus a `checksums.txt` to the release. The curl script depends on a **stable asset naming scheme** — decide it here and keep it forever, because the install script hard-codes it.

## Curl install script

Use `assets/install.sh` as the template and fill in REPO/BIN/asset names. Requirements it handles:

- OS/arch detection (`uname -s/-m`) → asset name
- Latest release resolution via the GitHub API, or `VERSION=v1.2.3` env override
- Checksum verification against the release's `checksums.txt` — never pipe unsigned bytes into `~/.local/bin` without this
- Install to `~/.local/bin` (no sudo) with PATH hint if needed

For desktop apps the curl story is weaker: Linux can download the AppImage directly; macOS can download and `hdiutil attach` the dmg; Windows users should just get the msi link — print it rather than attempting install. Serve the script from the repo (`https://raw.githubusercontent.com/OWNER/REPO/main/install.sh`) or a release asset.

## First release checklist to hand the user

1. `git tag v0.1.0 && git push --tags`
2. Watch the workflow; the draft release appears under Releases
3. Test: `curl -fsSL <raw-url>/install.sh | sh` on a clean machine
4. Publish the draft release
