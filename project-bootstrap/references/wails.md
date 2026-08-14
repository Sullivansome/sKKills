# Wails setup (Go + web frontend desktop app)

Wails apps are two stacks in one repo: a Go backend and a JS frontend (usually in `frontend/`). Both halves get the full treatment — the Node/TS toolchain from `node-ts.md` for `frontend/`, and the Go toolchain below for the root.

## What to detect

`wails.json` at the root, `go.mod` with `github.com/wailsapp/wails` dep. Scaffold new: `wails init -n myapp -t react-ts` (templates for react/vue/svelte/vanilla, TS variants).

## Go toolchain (the contract)

```sh
gofmt -l .                  # format:check (gofmt -w . to fix) — or goimports
go vet ./...
golangci-lint run           # lint aggregator
go test ./...
```

`golangci-lint` is the standard linter — one binary wrapping dozens of linters. Add a minimal `.golangci.yml` (enable `govet`, `staticcheck`, `errcheck`, `gofmt`/`goimports`) rather than running a pile of separate tools. Pin its version in CI (`golangci/golangci-lint-action` handles install + caching).

## Frontend toolchain

`frontend/` is a Vite + TS app — apply `node-ts.md` there (biome/eslint, tsc --noEmit, vitest). Wails generates TypeScript bindings in `frontend/wailsjs/` from Go methods — **exclude `wailsjs/` from lint/format** (it's generated) but keep it typechecked.

## Pre-commit

The `pre-commit` framework handles both halves (see `rust-tauri.md` for the pattern): hooks for `gofmt`/`golangci-lint run` (system hooks, `pass_filenames: false` for the linter) plus lint-staged inside `frontend/` or a system hook calling `pnpm --dir frontend exec lint-staged`.

## CI

Two jobs (or one job with both setups): Go job with `actions/setup-go@v5` (cache on) running fmt/vet/lint/test; frontend job running the Node contract in `frontend/`. Add a `wails build` smoke step — it catches frontend/backend binding breakage.

## Release: dmg / msi(-ish) / AppImage

Wails has no equivalent of tauri-action — you orchestrate the matrix yourself:

- **macOS**: `wails build -platform darwin/universal` produces `.app`; wrap in dmg with `create-dmg` (brew). Signing/notarization via `codesign` + `notarytool` with Apple secrets, optional.
- **Windows**: `wails build -platform windows/amd64` → `.exe`. There's no native msi maker; ship the exe, or add NSIS (`makensis`) for an installer. Wails v3 is improving this — check the version.
- **Linux**: `wails build -platform linux/amd64` → binary; AppImage via `linuxdeploy` + appimagetool (needs the `.desktop` file and icon; Wails generates them in `build/`).

Upload all artifacts with `softprops/action-gh-release@v2` on tag push, with a stable naming scheme (`myapp-x.y.z-darwin-universal.dmg`, `...-windows-amd64.exe`, `...-linux-amd64.AppImage`) plus `checksums.txt` so `assets/install.sh` can verify downloads. The curl script works well for the AppImage and macOS dmg.
