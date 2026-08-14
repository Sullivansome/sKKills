# project-bootstrap

An [agent skill](https://skills.sh) that gives AI coding agents a complete, opinionated-but-flexible development workflow setup: **scaffolding → lint/format/typecheck → pre-commit hooks → GitHub Actions CI → tag-driven releases**.

One sentence to your agent — *"set up this repo properly"* — and you get fast local checks, CI that runs the exact same commands, and a release pipeline that's one `git tag` away.

## What it sets up

| Concern | Approach |
|---|---|
| **Command contract** | `format` / `lint` / `typecheck` / `test` / `build` — same commands locally and in CI, no drift |
| **Pre-commit hooks** | Fast checks on staged files only (lint-staged, pre-commit framework, or plain git hooks). Slow stuff goes to CI or pre-push — slow hooks train people to use `--no-verify` |
| **CI** | GitHub Actions running the identical command contract, with proper dependency caching |
| **Releases** | Push `v*` tag → matrix builds → GitHub Release with installers/binaries + checksums |
| **Curl install** | `install.sh` template: OS/arch detection, latest-release resolution, checksum verification, no-sudo install |

## Supported stacks

The skill detects your stack from marker files (framework markers checked before generic ones) and loads only the relevant reference:

| Stack | Detected by | Tooling | Release |
|---|---|---|---|
| **Node / TypeScript** | `package.json` | Biome (or ESLint+Prettier), tsc, vitest, husky+lint-staged | — |
| **Next.js** | `next.config.*` | eslint-config-next / Biome, tsc | deploy-oriented |
| **TanStack** Start/Router/Query | `@tanstack/*` deps | Biome, vitest (generated route-tree gotchas covered) | deploy-oriented |
| **Electron** | `electron` deps | Node toolchain + electron-builder | **dmg / msi / AppImage** |
| **Tauri** | `Cargo.toml`, `src-tauri/` | rustfmt, clippy + frontend toolchain | **dmg / msi / AppImage** via `tauri-action` |
| **Wails** | `wails.json` | gofmt, golangci-lint + frontend toolchain | dmg / exe / AppImage (manual matrix) |
| **Python** | `pyproject.toml`, `uv.lock` | uv, ruff, mypy, pytest, pre-commit | binaries + curl installer |
| **Kotlin / Android** | `build.gradle.kts` | ktlint, detekt, Android lint (Gradle plugins) | signed APK/AAB from tag |
| **Swift — iOS / macOS** | `Package.swift`, `*.xcodeproj` | SwiftFormat, SwiftLint, xcodebuild | **notarized dmg** (macOS), TestFlight (iOS) |
| **Go** | `go.mod` | gofmt, go vet, golangci-lint | binaries + curl installer |

## Install

Using the [skills.sh](https://skills.sh) CLI (symlinks into all detected agents):

```bash
# from a GitHub repo
npx skills add Sullivansome/sKKills

# or from a local checkout (what we use for development)
npx skills add ./project-bootstrap -g -a '*' -s '*' -y
```

Works with Claude Code, Kimi Code CLI, Cursor, Codex, OpenCode, and 50+ other agents.

## Use

Just ask your agent naturally:

- *"Scaffold a new Tauri app with React and set up everything — linting, hooks, CI, releases."*
- *"Add pre-commit hooks and CI to this repo. Don't restructure my code."*
- *"Set up a release pipeline that builds a signed APK when I push a tag."*

## Repo structure

```
project-bootstrap/
├── SKILL.md                        # router: stack detection + 7-step workflow
├── references/                     # loaded per-stack (progressive disclosure)
│   ├── node-ts.md  nextjs.md  tanstack.md  electron.md
│   ├── rust-tauri.md  wails.md  python.md
│   ├── kotlin-android.md  swift-apple.md
│   └── release.md                  # tag-driven releases, installers, curl script
├── assets/
│   ├── workflows/ci.yml            # CI template (Node/Rust/Python variants)
│   ├── workflows/release-tauri.yml # dmg/msi/AppImage matrix template
│   └── install.sh                  # curl-install template with checksum verification
└── evals/evals.json                # test prompts used to evaluate the skill
```

## Principles baked in

- **Pin tool versions** — lockfiles, `rust-toolchain.toml`, `packageManager` field. Version skew is the #1 "works on my machine" cause.
- **Fast tools beat configurable tools** — Biome over ESLint+Prettier, Ruff over flake8+black — unless the project already has a working setup. Never churn existing configs uninvited.
- **Formatter and linter are separate concerns** — configured so they never fight.
- **Tags, not buttons** — pushing `v1.2.3` is the release trigger; the tag is the audit trail and the single source of truth for the version.
- **Verify, don't assume** — the skill makes the agent actually run the checks before declaring done, and dry-run what it can of the release pipeline.
