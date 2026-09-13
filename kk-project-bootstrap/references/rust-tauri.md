# Rust / Tauri setup

## Toolchain pinning

`rust-toolchain.toml` at repo root — rustup reads it automatically, so local and CI toolchains can't drift:

```toml
[toolchain]
channel = "REPLACE_WITH_TESTED_EXACT_RUST_VERSION"
components = ["rustfmt", "clippy"]
```

Replace the version placeholder with an exact version verified against the project before writing this file. A floating `stable` channel is not a reproducibility pin. CI should use this file rather than install a separate floating toolchain.

## Format / lint / test (the contract)

```sh
cargo fmt --all -- --check   # format:check (drop --check to fix)
cargo clippy --locked --all-targets -- -D warnings   # lint, warnings as errors
cargo test --locked
cargo build --locked
```

Use `--locked` when the repository commits Cargo.lock. Test the supported feature combinations explicitly; do not assume all features can be enabled together.

`-D warnings` in CI is what keeps the codebase warning-free; without it warnings accumulate until they're noise. If the project is a workspace, use `--workspace`.

Scaffolding new projects: `cargo new` for plain Rust; for Tauri use `pnpm create tauri-app` (or npm/cargo variants) which scaffolds frontend + `src-tauri/` together. Tauri v2 apps have a frontend stack too — apply [references/node-ts.md](node-ts.md) to the frontend half.

## Pre-commit

The `pre-commit` framework works fine for Rust and keeps hooks in version control (`.pre-commit-config.yaml`), unlike raw git hooks:

```yaml
repos:
  - repo: local
    hooks:
      - id: fmt
        name: cargo fmt
        entry: cargo fmt --all -- --check
        language: system
        pass_filenames: false
      - id: clippy
        name: cargo clippy
        entry: cargo clippy --locked --all-targets -- -D warnings
        language: system
        pass_filenames: false
```

These are non-mutating whole-project checks; verify the framework's staged-snapshot behavior in a fixture. Measure runtime and move clippy or formatting to pre-push/CI when too slow. Do not substitute a mutating whole-worktree formatter in a plain hook.

## CI notes

- Cache with `Swatinem/rust-cache@v2` — it handles target/ and registry caching correctly; hand-rolled cache keys for cargo are easy to get wrong.
- Tauri Linux builds need system deps: `sudo apt-get install -y libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev patchelf` (the release template includes this).

## Release

Tauri can build dmg + msi + AppImage candidates in a platform matrix. See [references/release.md](release.md) and [assets/workflows/release-tauri.yml](../assets/workflows/release-tauri.yml). Distributed builds require native OS signing/notarization, separate updater signatures when used, and verified detached signatures for final release payloads. Missing credentials block release. The workflow template has no public upload path and must be adapted with signing and verification before use; consult kk-distribution if available.
