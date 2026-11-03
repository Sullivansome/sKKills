---
name: kk-project-bootstrap
description: Scaffold repositories or configure reproducible tooling, hooks, CI, and initial artifact build pipelines. Use for missing or broken project setup; use kk-distribution for package/signing decisions and kk-release-delivery for promotion, rollout, and recovery.
---

# Project Bootstrap

Set up a project so that quality checks run the same way locally and in CI. Preserve working conventions and the user's requested scope. Tag-driven artifact releases are one option; service deployment can use the project's existing delivery model.

## Before changing files

Read repository instructions, inspect staged and unstaged changes, and identify existing commands, lockfiles, runtime versions, and CI provider. Add what is missing without re-scaffolding an existing project or replacing working tooling. Read only relevant stack references. Their commands and action tags are adaptation examples: verify compatibility with the installed versions and current official documentation before using them. Never copy a placeholder as a real version or invent a commit SHA.

Scale setup to the project: a documentation-only repository need not acquire a compiler or test framework. Do not create dummy passing tests or use no-tests-found overrides to manufacture a green pipeline. A new test runner needs a meaningful smoke/regression test, or an explicit statement that test coverage remains absent.

## Step 1 — Detect the stack

Check framework markers and dependencies before generic manifests. Apply every matching row, not just the first: a desktop wrapper (Wails, Electron, Tauri) and its frontend framework both apply, and the wrapper's reference owns release packaging. Generic rows (`package.json`, `go.mod`) supply the base toolchain that framework references build on. In a monorepo, detect per package/workspace.

| Marker | Stack | Reference |
|---|---|---|
| `wails.json` | Wails (Go + web frontend) | [references/wails.md](references/wails.md) |
| `electron`, `electron-builder`/`electron-forge` in deps | Electron | [references/electron.md](references/electron.md) |
| `next.config.*`, `next` in deps | Next.js | [references/nextjs.md](references/nextjs.md) |
| `@tanstack/react-start` / `@tanstack/react-router` in deps | TanStack Start / Router | [references/tanstack.md](references/tanstack.md) |
| `@tanstack/react-query` in deps | Supplemental data layer; preserve detected host framework | [references/tanstack.md](references/tanstack.md), Query-only guidance |
| `Cargo.toml`, `src-tauri/`, `@tauri-apps/cli` in deps | Rust / Tauri | [references/rust-tauri.md](references/rust-tauri.md) |
| `build.gradle(.kts)`, `settings.gradle(.kts)`, `gradle/` | Kotlin / Android (Groovy or Kotlin DSL) | [references/kotlin-android.md](references/kotlin-android.md) |
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
3. `typecheck` — check the actual source projects; avoid emit where the toolchain supports it
4. `test` — relevant automated tests, with slower integration/e2e checks separate when useful
5. `build` — proves the thing compiles

## Step 3 — Configure the toolchain

Follow the stack reference file. Universal principles:

- **Pin tool versions** (lockfile, `.tool-versions`, `rust-toolchain.toml`, exact `packageManager` field) and use locked installs. Check OS, environment, generated files, and external services too when local/CI behavior differs.
- **Fast tools beat configurable tools.** Prefer Biome over ESLint+Prettier, Ruff over flake8+black+isort, unless the project already has the slower stack — don't churn existing configs without being asked.
- **Formatting and linting are separate concerns.** The formatter owns whitespace/style; the linter owns bugs and suspicious patterns. Configure them so they don't fight (e.g. turn off stylistic lint rules the formatter handles).

## Step 4 — Pre-commit hooks

Prefer fast staged-file format/lint checks. If a tool only supports whole-project checks, use non-mutating checks against the staged snapshot or put it in pre-push/CI; never silently include unstaged hunks. Preserve an existing fast meaningful test hook. Move slow checks out of the commit path based on measured runtime.

Per-stack tooling: `lint-staged` + `husky` (Node), `pre-commit` framework (Python, or polyglot), or a plain `.git/hooks/pre-commit` script for tiny projects. The stack reference has the exact config.

Verify hooks in an isolated temporary repository with the relevant configuration and pinned tools. Exercise bad formatting, a lint failure, a filename containing spaces, and partial staging. Confirm exit codes and that unrelated/unstaged content stays out of the index. Do not create a test commit, stage a deliberate defect, or run blanket `git add` in the user's working repository.

## Step 5 — CI

Preserve the existing CI provider. For GitHub Actions, adapt [assets/workflows/ci.yml](assets/workflows/ci.yml). Run applicable Step 2 commands, respecting generation dependencies. Use ecosystem-supported dependency caching where useful.

The template deliberately fails until adapted. Replace its guard with actual applicable commands; merely deleting the guard is not a working CI configuration. Run required code generation before checks that consume generated types. Preserve an existing CI provider unless switching is requested. Use explicit read-only permissions for checks, bounded job timeouts, and job-scoped release permissions. Keep secrets away from untrusted PR code. Resolve production action references to verified full commit SHAs and use the project's tested runtime/toolchain versions.

For a desktop app, add a smoke-build job on the target platforms (macOS, Windows, Linux) so cross-platform breakage shows up before release day, not during it.

## Step 6 — Release setup, when in scope

For requested release automation, preserve the provider, trigger, and product's distribution model. Skip this step for hooks/CI-only work.

Read [references/release.md](references/release.md) for pipeline wiring and the relevant stack recipe. Use `kk-distribution` for package formats, signing, and installation trust; use `kk-release-delivery` for candidate promotion and recovery. Consult siblings only when available and needed; otherwise establish the scoped requirements directly.

Separate build and publication jobs. Every directly distributed target (downloads, install scripts, repositories/feeds you operate) must pass final-payload publisher signatures, applicable native signing/notarization, and verification before publication; missing keys or failed checks block it. Checksums and updater signatures alone are insufficient. For app stores and language registries (App Store, Play, PyPI, npm, crates.io), meet the channel's required signing and use its provenance/attestation mechanism instead of detached signatures nobody verifies.

## Step 7 — Verify, don't assume

Before declaring done, run applicable format, lint, type, test, and build commands, and exercise the hook in the isolated fixture. Validate workflow syntax and inspect trigger/permission behavior; local tools such as `act` do not reproduce every hosted runner or signing environment. Report unavailable checks separately from passes. For release workflows, dry-run supported builds and identify which hosted/signing checks remain unverified. Do not push tags or publish merely to test setup without existing authorization.

Report what was configured, which checks ran, which commands to use, and the release trigger only if release setup was included.

The detection table links the stack references. JavaScript-based stacks reuse [references/node-ts.md](references/node-ts.md). Release-specific assets and their installer contract are linked from the release reference; load them only for that work.
