# Rust / Tauri setup

## Toolchain pinning

`rust-toolchain.toml` at repo root — rustup reads it automatically, so local and CI toolchains can't drift:

```toml
[toolchain]
channel = "stable"
components = ["rustfmt", "clippy"]
```

## Format / lint / test (the contract)

```sh
cargo fmt --all -- --check   # format:check (drop --check to fix)
cargo clippy --all-targets --all-features -- -D warnings   # lint, warnings as errors
cargo test --all-features
```

`-D warnings` in CI is what keeps the codebase warning-free; without it warnings accumulate until they're noise. If the project is a workspace, use `--workspace`.

Scaffolding new projects: `cargo new` for plain Rust; for Tauri use `pnpm create tauri-app` (or npm/cargo variants) which scaffolds frontend + `src-tauri/` together. Tauri v2 apps have a frontend stack too — apply `references/node-ts.md` to the frontend half.

## Pre-commit

The `pre-commit` framework works fine for Rust and keeps hooks in version control (`.pre-commit-config.yaml`), unlike raw git hooks:

```yaml
repos:
  - repo: local
    hooks:
      - id: fmt
        name: cargo fmt
        entry: cargo fmt --all
        language: system
        pass_filenames: false
      - id: clippy
        name: cargo clippy
        entry: cargo clippy --all-targets -- -D warnings
        language: system
        pass_filenames: false
```

Clippy on the whole workspace is slow for large projects; if it exceeds ~10s, move clippy to a pre-push hook and keep only `fmt` in pre-commit.

## CI notes

- Cache with `Swatinem/rust-cache@v2` — it handles target/ and registry caching correctly; hand-rolled cache keys for cargo are easy to get wrong.
- Tauri Linux builds need system deps: `sudo apt-get install -y libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev patchelf` (the release template includes this).

## Release

Tauri is the canonical source of dmg + msi + AppImage. See `references/release.md` and `assets/workflows/release-tauri.yml` — `tauri-apps/tauri-action` builds all three from one matrix job and attaches them to a GitHub Release. Code signing is configured via secrets (`APPLE_CERTIFICATE`, `TAURI_SIGNING_PRIVATE_KEY`, etc.) but the pipeline works unsigned — set it up, note the missing secrets, and let the user add them.
