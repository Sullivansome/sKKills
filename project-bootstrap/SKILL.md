---
name: project-bootstrap
description: Set up a complete development workflow for a new or existing project — scaffolding, pre-commit hooks, linting, formatting, type checking, GitHub Actions CI, and release pipelines (desktop installers dmg/msi/AppImage, GitHub Releases, curl install scripts). Covers Node/TypeScript, Next.js, TanStack (Start/Router/Query), React, Electron, Tauri, Wails (Go), Python, Kotlin/Android, and Swift (iOS/macOS). Use this whenever the user starts a new project or repo, asks to set up or fix linting/formatting/hooks/type checking, wants a CI workflow, asks about releasing/publishing builds, desktop installers (dmg, msi, AppImage), Android APK/AAB or Apple notarization/TestFlight release flows, or wants an install script — even if they don't use the word "scaffold" or "bootstrap".
---

# Project Bootstrap

Set up a project so that quality checks run the same way locally and in CI, and releases are one tag push away. The goal is boring reliability: `git commit` runs fast local checks, every push runs the full suite in CI, and pushing a `v*` tag publishes installers.

## Step 1 — Detect the stack

Look for marker files before doing anything. Check framework markers BEFORE generic ones — a Next.js repo also has `package.json`, and an Electron repo looks like a plain Node project until you read the deps:

| Marker | Stack | Reference |
|---|---|---|
| `wails.json` | Wails (Go + web frontend) | `references/wails.md` |
| `electron`, `electron-builder`/`electron-forge` in deps | Electron | `references/electron.md` |
| `next.config.*`, `next` in deps | Next.js | `references/nextjs.md` |
| `@tanstack/react-start` / `react-router` / `react-query` in deps | TanStack | `references/tanstack.md` |
| `Cargo.toml`, `src-tauri/` | Rust / Tauri | `references/rust-tauri.md` |
| `build.gradle.kts`, `settings.gradle.kts`, `gradle/` | Kotlin / Android | `references/kotlin-android.md` |
| `Package.swift`, `*.xcodeproj`, `*.xcworkspace` | Swift — iOS / macOS | `references/swift-apple.md` |
| `pyproject.toml`, `requirements.txt`, `uv.lock` | Python | `references/python.md` |
| `package.json` | Node / TypeScript (generic) | `references/node-ts.md` |
| `go.mod` (no wails.json) | Go (generic) | Go section of `references/wails.md` |
| None (greenfield) | Ask the user, or infer from their prompt | — |

If it's a desktop app (dmg/msi/AppImage mentioned, or Electron/Tauri/Wails detected) or ships release artifacts (Android APK/AAB, macOS dmg, CLI binaries), the release flow matters — read `references/release.md` in addition to the stack reference.

## Step 2 — Establish the command contract

Every check must be runnable as a single command, identical locally and in CI. Use whatever the ecosystem already provides (package.json scripts, just/Makefile, pre-commit config) — do not invent a new task runner if one exists.

The contract is always these five commands (names may vary per stack):

1. `format` / `format:check` — auto-fix and CI-verify variants
2. `lint` — static analysis
3. `typecheck` — no emit, fast
4. `test` — unit tests
5. `build` — proves the thing compiles

Why this matters: if CI runs `eslint src/` but the local hook runs something else, drift is guaranteed. One definition, two callers (pre-commit hook and CI job).

## Step 3 — Configure the toolchain

Follow the stack reference file. Universal principles:

- **Pin tool versions** (lockfile, `.tool-versions`, `rust-toolchain.toml`, `packageManager` field). "Works on my machine" failures are almost always version skew.
- **Fast tools beat configurable tools.** Prefer Biome over ESLint+Prettier, Ruff over flake8+black+isort, unless the project already has the slower stack — don't churn existing configs without being asked.
- **Formatting and linting are separate concerns.** The formatter owns whitespace/style; the linter owns bugs and suspicious patterns. Configure them so they don't fight (e.g. turn off stylistic lint rules the formatter handles).

## Step 4 — Pre-commit hooks

Hooks run on staged files only, and only the fast checks (format + lint, maybe typecheck if <5s). Tests belong in CI, not in the commit path — slow hooks train developers to use `--no-verify`, which defeats the entire setup.

Per-stack tooling: `lint-staged` + `husky` (Node), `pre-commit` framework (Python, or polyglot), or a plain `.git/hooks/pre-commit` script for tiny projects. The stack reference has the exact config.

After installing, verify by staging a deliberately badly-formatted file and committing — the hook should fix or reject it.

## Step 5 — GitHub Actions CI

Start from `assets/workflows/ci.yml` and adapt it to the stack. The CI job must run the exact same commands from Step 2, in this order: format:check → lint → typecheck → test → build. Cache dependencies (pnpm/cargo/pip) or every run wastes 1–3 minutes.

For a desktop app, add a smoke-build job on the target platforms (macOS, Windows, Linux) so cross-platform breakage shows up before release day, not during it.

## Step 6 — Release flow

Read `references/release.md`. The short version:

- **Tag-driven**: pushing `v1.2.3` triggers the release workflow. No manual artifact uploads.
- **Desktop apps**: matrix build on macOS/Windows/Linux producing dmg, msi, AppImage, attached to a GitHub Release (`tauri-action` for Tauri, `electron-builder` + `softprops/action-gh-release` for Electron).
- **CLI tools**: cross-compile binaries per OS/arch, publish as release assets.
- **Curl install script**: `assets/install.sh` is the template — it detects OS/arch, picks the right release asset, verifies the checksum, and installs. Host it in the repo so `curl -fsSL .../install.sh | sh` works.

## Step 7 — Verify, don't assume

Before declaring done, actually run: the format check, the linter, the typechecker, the tests, and a commit that exercises the hook. For release workflows, dry-run what you can (`tauri build` locally, `electron-builder --dir`, `act` if available) and clearly tell the user that the full pipeline only proves itself on the first real tag push.

Report back a short summary: what was installed, which commands to run, and what happens on tag push.

## Reference files

Stack references (read only the detected one(s)):

- `references/node-ts.md` — pnpm/npm, Biome or ESLint+Prettier, tsc, vitest, husky+lint-staged (base for all JS stacks)
- `references/nextjs.md` — Next.js: eslint-config-next, next build, deploy-oriented release
- `references/tanstack.md` — TanStack Start/Router/Query: generated route tree gotchas
- `references/electron.md` — Electron: electron-builder, dmg/msi/AppImage
- `references/rust-tauri.md` — rustfmt, clippy, cargo test, Tauri desktop setup
- `references/wails.md` — Go (gofmt/golangci-lint) + frontend half, manual release matrix
- `references/python.md` — uv/pip, ruff, mypy, pytest, pre-commit framework
- `references/kotlin-android.md` — Gradle, ktlint, detekt, Android lint, APK/AAB signing
- `references/swift-apple.md` — SwiftFormat, SwiftLint, xcodebuild, macOS dmg + notarization, iOS TestFlight

Shared assets:

- `references/release.md` — tag-driven GitHub Releases, installer matrix builds, curl install script
- `assets/workflows/ci.yml` — CI template to adapt
- `assets/workflows/release-tauri.yml` — Tauri release template (dmg/msi/AppImage)
- `assets/install.sh` — curl-install template with OS/arch detection and checksum verification
