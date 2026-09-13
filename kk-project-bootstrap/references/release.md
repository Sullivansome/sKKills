# Release flow

All distributable artifacts must be signed and verified before publication. For macOS, Windows/Chocolatey, Linux repositories, and direct-download trust use `kk-distribution` when available. Otherwise implement the same native and detached signature gates directly; checksums alone do not meet this collection's policy. Signing failures never fall back to unsigned publication.

## The trigger: tags, not buttons

Pushing a tag `v1.2.3` triggers the release workflow. Reasons: the tag is the audit trail, anyone with push access can release without dashboard access, and the version in the tag is a single source of truth. For versioned artifacts, use `on: push: tags: ["v*"]` when consistent with the requested workflow. Preserve established service deployment triggers. Preparing the pipeline does not authorize pushing a tag or publishing a release.

Keep the version in the manifest (`tauri.conf.json`, `package.json`, `Cargo.toml`) in sync with the tag — either bump it in a release commit before tagging, or have the workflow inject the tag version into the manifest before build and signing (verify the installed tool's supported version mechanism; electron-builder reads package.json).

## Desktop apps: dmg / msi / AppImage

The full per-stack release recipes live in the stack references — this file holds the shared principles:

- **Tauri** → [references/rust-tauri.md](rust-tauri.md) + [assets/workflows/release-tauri.yml](../assets/workflows/release-tauri.yml) (tauri-action, the smoothest path)
- **Electron** → [references/electron.md](electron.md) (electron-builder candidates, then separately gated publication)
- **Wails** → [references/wails.md](wails.md) (no helper action; manual matrix + create-dmg / NSIS / linuxdeploy)
- **macOS Swift app** → [references/swift-apple.md](swift-apple.md) (archive → Developer ID export → notarytool → create-dmg)

### Tauri

Use [assets/workflows/release-tauri.yml](../assets/workflows/release-tauri.yml). `tauri-apps/tauri-action@v0` on a 3-OS matrix produces:

- **macOS**: `.dmg` (+ `.app.tar.gz` for auto-updater)
- **Windows**: `.msi` (+ `.exe` NSIS if configured in tauri.conf.json)
- **Linux**: `.AppImage` + `.deb`

The template has no public upload path and deliberately stops until application-specific signing and verification are configured. Adapt these details:

- The Tauri template does not generate a shared checksums manifest. If an installer depends on one, add an aggregation step after matrix completion that hashes the exact final assets, and test the installer's format-specific path.

- Linux runner needs `libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev patchelf` — without these the build fails 15 minutes in.
- For Apple Silicon + Intel builds, add supported `macos-15-intel` (Intel) and `macos-15` (ARM) matrix entries with `tauri build --target` as needed; a single macos-latest only covers one arch. Verify current runner support before generating workflows; macos-13 is retired.
- Signing is mandatory for distributed builds. Tauri updater signatures do not replace Apple Developer ID/notarization, Windows Authenticode, or Linux artifact/package signatures. Configure the applicable identities and verify actual outputs; missing credentials or verification failures block publication. The template builds candidates only and deliberately requires project-specific signing/verification before it can be enabled.

### Electron

`electron-builder` with a matrix job; prepare signed candidates before publishing through a separately gated job:

```yaml
- run: pnpm build && pnpm exec electron-builder --publish never
# Sign/notarize and verify every final artifact before a separate gated publication job.
```

The separate publisher must require all target verification jobs to succeed and confirm the intended version/ref. A tag condition alone is not a signature gate. Targets in package.json `build`: `mac.target: dmg`, `win.target: msi` (or nsis), `linux.target: AppImage`.

## CLI tools: binary matrix

Cross-compile per target in a matrix (`cargo build --release --target <triple>`, `go build`, PyInstaller, `pkg`/`bun build --compile`), upload `myapp-<os>-<arch>.tar.gz` plus detached publisher signatures for every final payload and a signed `checksums.txt` to the release. Each CLI tarball for the bundled installer must contain exactly one regular nonempty file named as BIN at archive root. The curl script depends on a **stable asset naming scheme** — decide it here and keep it forever, because the install script hard-codes it.

## Curl install script

Use [assets/install.sh](../assets/install.sh) as the template and fill in REPO/BIN/asset names and an independently trusted public key. Authenticate the script before executing it; do not pipe an unverified download into a shell. The default template refuses an unconfigured key. Requirements it handles:

- OS/arch detection (`uname -s/-m`) → asset name
- Latest release resolution via the GitHub API, or `VERSION=v1.2.3` env override
- Required checksum verification against exactly one matching entry in the release's `checksums.txt`; missing, duplicate, malformed, or mismatched checksums stop installation. A checksum detects corruption but does not authenticate the publisher when the same release hosts both files. Verify the mandatory detached artifact and manifest signatures with the pinned publisher key. The manifest must include exactly one `# version <selected-version>` line; missing or mismatched signed context blocks installation. Explicit VERSION selection pins a version; latest discovery is not an authenticated freshness policy.
- Install to `~/.local/bin` (no sudo) with PATH hint if needed

For desktop apps the curl story is weaker: Linux can download the AppImage directly; macOS can download and `hdiutil attach` the dmg; Windows users should just get the msi link — print it rather than attempting install. Serve the script from the repo (`https://raw.githubusercontent.com/OWNER/REPO/main/install.sh`) or a release asset.

## First release verification

1. Run applicable checks on the candidate and verify its version matches the intended tag. Use explicit read-only CI permissions and job-scoped `contents: write` for GitHub release uploads; resolve production action refs to verified SHAs.
2. When authorized, create and push only the intended tag: `git tag v0.1.0` then `git push origin v0.1.0`. Do not use `git push --tags`.
3. Verify all requested platforms pass native signing/notarization, detached signatures, expected-identity checks and signed-manifest completeness before uploading any release assets. Inspect workflow results and test selected artifacts. A draft release is not available through anonymous `/releases/latest`; use authenticated draft downloads or selected local artifacts before publication.
4. Publish only within the requested authorization, then test the explicit published version on a clean machine. Verify signatures/checksums and the actual install/update path.
5. Record which hosted platform/signing checks ran, which remain unavailable, and the recovery path for a faulty release. For service rollout or stateful changes, use the available kk-release-delivery guidance.
