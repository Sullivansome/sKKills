# Initial release automation

Use this reference to wire an agreed artifact/distribution contract into the project's build system. `kk-distribution` owns package formats, signing and consumer trust; `kk-release-delivery` owns candidate promotion and recovery. Use them when available and needed, or establish those requirements directly. Pipeline setup alone does not authorize publication.

## Preserve the trigger and version contract

Keep the existing provider and trigger, including manual dispatch or platform-managed delivery. For a requested tag workflow, `on: push: tags: ["v*"]` is one GitHub Actions pattern. Only that mode requires creating/pushing a tag; setup verification does not.

Bind the selected source revision to the artifact version. Keep package/application manifests consistent before building and signing, using the installed tool's supported version mechanism. In tag mode, compare against the tag; in dispatch mode, validate the selected ref/version. Do not introduce a tag requirement into another trigger's workflow.

## Build candidates and gate publication

Use the detected stack's build recipe:

- [Rust/Tauri](rust-tauri.md) and [the Tauri scaffold](../assets/workflows/release-tauri.yml).
- [Electron](electron.md), [Wails](wails.md), or [Swift/Apple](swift-apple.md) for desktop candidates.
- [Go](go.md), [Python](python.md), or [Node/TypeScript](node-ts.md) for CLI/package outputs; [Kotlin/Android](kotlin-android.md) for mobile builds.

Adapt the matrix to requested platforms, architectures and outputs. Verify runner/toolchain support before selecting images. For Tauri on macOS, account explicitly for Intel and Apple Silicon; aggregate checksums from the final matrix outputs when an installer requires a shared manifest. The Tauri scaffold remains blocked until project-specific signing and verification are implemented.

Build without publishing. Keep signing credentials away from untrusted PR jobs and grant publication permissions only to a separate job gated on every requested target. For directly distributed payloads, require verified final-payload publisher signatures, applicable native signatures/notarization and install/update evidence. Checksums or updater signatures alone do not meet that gate. App stores and language registries instead require their own signing (Apple distribution signing, Play upload key, Maven Central PGP) and supported provenance such as PyPI Trusted Publishing attestations or npm provenance; do not block those channels on detached signatures that no client checks. Missing credentials or failed verification block publication; only an explicit user scope change narrows the release targets.

## Optional CLI installer

Use [assets/install.sh](../assets/install.sh) only for requested CLI tarballs. Each archive must contain exactly one regular nonempty file named as BIN at its root. The installer requests `<BIN>-<OS>-<arch>.tar.gz` with `uname -s` casing and normalized architectures: `myapp-Linux-x86_64.tar.gz`, `myapp-Linux-aarch64.tar.gz`, `myapp-Darwin-x86_64.tar.gz`, `myapp-Darwin-aarch64.tar.gz`. Publish exactly those names for every supported target (a universal macOS binary is published under both Darwin names), or change the installer's `asset=` line and its tests together. Go-style names such as `linux-amd64` do not match. Desktop formats require a separate verified installation path.

Configure REPO, BIN, asset names and an independently trusted public key. Authenticate the script before execution; never pipe an unverified download into a shell. Its contract is:

- Select an explicit `VERSION` or resolve the latest GitHub release using Python 3's JSON parser. Only latest discovery requires `python3`; an explicit `VERSION` avoids that dependency. Latest discovery is not authenticated freshness.
- Verify detached artifact and `checksums.txt` signatures with the pinned publisher key.
- Require exactly one signed `# version <selected-version>` line and one matching, valid SHA-256 row; missing, duplicate or mismatched entries fail installation.
- Install to `~/.local/bin` without sudo, preserving an existing installation on verification failure.

## Verify the configured workflow

Run applicable checks/builds, validate workflow syntax, and inspect trigger/version binding, permission boundaries and the aggregate publication gate. Test hooks/installers in isolated fixtures. Verify selected local artifacts or authenticated draft assets before publication; anonymous `/releases/latest` cannot select a draft.

Report configured automation and actual checks separately from hosted/signing steps that remain unrun. Execute a release only when it is within the requested scope; pass candidate identity and verification evidence to promotion, then verify the explicit published version.
