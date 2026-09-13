---
name: kk-project-bootstrap
description: Scaffold a repository or set up reproducible development tooling, formatting, linting, type checks, hooks, CI, and initial artifact release pipelines. Covers web, desktop, mobile, and CLI stacks. Use for missing or broken project setup and build automation; use kk-release-delivery for production rollout and recovery decisions.
---

# Project Bootstrap

Set up a project so that quality checks run the same way locally and in CI. Preserve working conventions and the user's requested scope. Tag-driven artifact releases are one option; service deployment can use the project's existing delivery model.

## Before changing files

Read repository instructions, inspect staged and unstaged changes, and identify existing commands, lockfiles, runtime versions, and CI provider. Add what is missing without re-scaffolding an existing project or replacing working tooling. Read only relevant stack references. Their commands and action tags are adaptation examples: verify compatibility with the installed versions and current official documentation before using them. Never copy a placeholder as a real version or invent a commit SHA.

Scale setup to the project: a documentation-only repository need not acquire a compiler or test framework. Do not create dummy passing tests or use no-tests-found overrides to manufacture a green pipeline. A new test runner needs a meaningful smoke/regression test, or an explicit statement that test coverage remains absent.

## Step 1 — Detect the stack

Look for marker files before doing anything. Check framework markers BEFORE generic ones — a Next.js repo also has `package.json`, and an Electron repo looks like a plain Node project until you read the deps:

| Marker | Stack | Reference |
|---|---|---|
| `wails.json` | Wails (Go + web frontend) | [references/wails.md](references/wails.md) |
| `electron`, `electron-builder`/`electron-forge` in deps | Electron | [references/electron.md](references/electron.md) |
| `next.config.*`, `next` in deps | Next.js | [references/nextjs.md](references/nextjs.md) |
| `@tanstack/react-start` / `@tanstack/react-router` in deps | TanStack Start / Router | [references/tanstack.md](references/tanstack.md) |
| `@tanstack/react-query` in deps | Supplemental data layer; preserve detected host framework | [references/tanstack.md](references/tanstack.md), Query-only guidance |
| `Cargo.toml`, `src-tauri/` | Rust / Tauri | [references/rust-tauri.md](references/rust-tauri.md) |
| `build.gradle.kts`, `settings.gradle.kts`, `gradle/` | Kotlin / Android | [references/kotlin-android.md](references/kotlin-android.md) |
| `Package.swift`, `*.xcodeproj`, `*.xcworkspace` | Swift — iOS / macOS | [references/swift-apple.md](references/swift-apple.md) |
| `pyproject.toml`, `requirements.txt`, `uv.lock` | Python | [references/python.md](references/python.md) |
| `package.json` | Node / TypeScript (generic) | [references/node-ts.md](references/node-ts.md) |
| `go.mod` (no Wails marker) | Go (generic) | [references/go.md](references/go.md) |
| None (greenfield) | Ask the user, or infer from their prompt | — |

Match full dependency names, not suffixes: `react-router` and legacy `react-query` are not the scoped TanStack packages above. Query alone does not imply Start, file-based routes, or `tsr generate`. Read `go.mod` for a Wails module dependency as well as `wails.json` before treating Go as generic.

Read [references/release.md](references/release.md) only when release setup is requested or required by the agreed deliverable. Merely detecting a web, CLI, or desktop stack does not add a release task to a hooks/CI request.

## Step 2 — Establish the command contract

Every check must be runnable as a single command, identical locally and in CI. Use whatever the ecosystem already provides (package.json scripts, just/Makefile, pre-commit config) — do not invent a new task runner if one exists.

Cover these responsibilities where applicable (names may vary per stack, and a compiler can cover both typecheck and build):

1. `format` / `format:check` — auto-fix and CI-verify variants
2. `lint` — static analysis
3. `typecheck` — no emit, fast
4. `test` — relevant automated tests, with slower integration/e2e checks separate when useful
5. `build` — proves the thing compiles

Why this matters: if CI runs `eslint src/` but the local hook runs something else, drift is guaranteed. One definition, two callers (pre-commit hook and CI job).

## Step 3 — Configure the toolchain

Follow the stack reference file. Universal principles:

- **Pin tool versions** (lockfile, `.tool-versions`, `rust-toolchain.toml`, exact `packageManager` field) and use locked installs. Check OS, environment, generated files, and external services too when local/CI behavior differs.
- **Fast tools beat configurable tools.** Prefer Biome over ESLint+Prettier, Ruff over flake8+black+isort, unless the project already has the slower stack — don't churn existing configs without being asked.
- **Formatting and linting are separate concerns.** The formatter owns whitespace/style; the linter owns bugs and suspicious patterns. Configure them so they don't fight (e.g. turn off stylistic lint rules the formatter handles).

## Step 4 — Pre-commit hooks

Prefer fast staged-file format/lint checks. If a tool only supports whole-project checks, use non-mutating checks against the staged snapshot or put it in pre-push/CI; never silently include unstaged hunks. Preserve an existing fast meaningful test hook. Move slow checks out of the commit path based on measured runtime.

Per-stack tooling: `lint-staged` + `husky` (Node), `pre-commit` framework (Python, or polyglot), or a plain `.git/hooks/pre-commit` script for tiny projects. The stack reference has the exact config.

Verify hooks in an isolated temporary repository with the relevant configuration and pinned tools. Exercise bad formatting, a lint failure, a filename containing spaces, and partial staging. Confirm exit codes and that unrelated/unstaged content stays out of the index. Do not create a test commit, stage a deliberate defect, or run blanket `git add` in the user's working repository.

## Step 5 — GitHub Actions CI

Start from [assets/workflows/ci.yml](assets/workflows/ci.yml) and adapt it to the stack. Run the applicable Step 2 commands: format:check → lint → typecheck → test → build, respecting generation dependencies. Use ecosystem-supported dependency caching where it improves measured runtime.

The template deliberately fails until adapted. Replace its guard with actual applicable commands; merely deleting the guard is not a working CI configuration. Run required code generation before checks that consume generated types. Preserve an existing CI provider unless switching is requested. Use explicit read-only permissions for checks, bounded job timeouts, and job-scoped release permissions. Keep secrets away from untrusted PR code. Resolve production action references to verified full commit SHAs and use the project's tested runtime/toolchain versions.

For a desktop app, add a smoke-build job on the target platforms (macOS, Windows, Linux) so cross-platform breakage shows up before release day, not during it.

## Step 6 — Release setup, when in scope

Preserve the existing provider, trigger, and distribution model. For hooks/CI-only requests, skip this step. Web/API services may deploy on merge or through an existing platform; do not add tags, GitHub Releases, installers, or publication jobs just because the project needs CI.

When initial artifact release automation is requested, read [references/release.md](references/release.md) and the relevant stack recipe. Choose outputs for the actual product: package registry, CLI binaries, desktop installers, or mobile distribution. Tag-driven GitHub Releases are an available pattern, not a requirement. Include [assets/install.sh](assets/install.sh) only for a requested compatible CLI tarball installer; desktop formats need their own tested handling.

Use `kk-release-delivery` if available for production rollout, promotion gates, or recovery decisions. If it is unavailable, prepare those requirements directly rather than silently expanding a tooling task into a deployment.

All distributed release artifacts must be signed and verified; missing keys or failed verification block publication. Use `kk-distribution` for macOS notarization, Windows/Chocolatey, Linux package repositories, and download/update trust. A checksum, updater signature, or successful build alone does not replace the platform-native and publisher-signature requirements. Keep build jobs separate from publishing, with an aggregate gate for every requested target.

## Step 7 — Verify, don't assume

Before declaring done, run applicable format, lint, type, test, and build commands, and exercise the hook in the isolated fixture. Validate workflow syntax and inspect trigger/permission behavior; local tools such as `act` do not reproduce every hosted runner or signing environment. Report unavailable checks separately from passes. For release workflows, dry-run supported builds and identify which hosted/signing checks remain unverified. Do not push tags or publish merely to test setup without existing authorization.

Report what was configured, which checks ran, which commands to use, and the release trigger only if release setup was included.

## Reference files

Stack references (read only the detected one(s)):

- [references/node-ts.md](references/node-ts.md) — pnpm/npm, Biome or ESLint+Prettier, tsc, vitest, husky+lint-staged (base for all JS stacks)
- [references/nextjs.md](references/nextjs.md) — Next.js: eslint-config-next, next build, deploy-oriented release
- [references/tanstack.md](references/tanstack.md) — TanStack Start/Router/Query: generated route tree gotchas
- [references/electron.md](references/electron.md) — Electron: electron-builder, dmg/msi/AppImage
- [references/rust-tauri.md](references/rust-tauri.md) — rustfmt, clippy, cargo test, Tauri desktop setup
- [references/go.md](references/go.md) — generic Go toolchain, tests/build, and optional CLI distribution
- [references/wails.md](references/wails.md) — Wails frontend integration and desktop release matrix; uses the Go reference for backend tooling
- [references/python.md](references/python.md) — uv/pip, ruff, mypy, pytest, pre-commit framework
- [references/kotlin-android.md](references/kotlin-android.md) — Gradle, ktlint, detekt, Android lint, APK/AAB signing
- [references/swift-apple.md](references/swift-apple.md) — SwiftFormat, SwiftLint, xcodebuild, macOS dmg + notarization, iOS TestFlight

Shared assets:

- [references/release.md](references/release.md) — tag-driven GitHub Releases, installer matrix builds, curl install script
- [assets/workflows/ci.yml](assets/workflows/ci.yml) — CI template to adapt
- [assets/workflows/release-tauri.yml](assets/workflows/release-tauri.yml) — Tauri release template (dmg/msi/AppImage)
- [assets/install.sh](assets/install.sh) — curl-install template with OS/arch detection and checksum verification
