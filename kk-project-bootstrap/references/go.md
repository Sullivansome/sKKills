# Generic Go setup

Use this reference for a Go library, CLI, or service. A `go.mod` file does not imply a frontend or desktop application. Read Wails guidance only if its configuration or module dependency is present.

## Toolchain and command contract

Inspect `go.mod`, toolchain directives, `go.sum`, workspace files, existing task scripts, and CI. Preserve the project's tested Go version and supported platforms; verify compatibility before changing a version or linter schema. Keep library, CLI, and service build requirements distinct.

Run the existing command contract or establish these responsibilities:

```sh
# format:check — gofmt alone prints differences without failing the gate.
unformatted=$(gofmt -l .) || exit 1
if [ -n "$unformatted" ]; then
  printf '%s\n' "$unformatted"
  exit 1
fi
```

- Format fixes: `gofmt -w .` as an explicit developer command.
- Static checks: `go vet ./...` plus the existing linter if configured.
- Behavior: `go test ./...`; add `-race` for relevant concurrency checks on supported targets.
- Build: `go build ./...`, with additional commands for the actual shipped executable when needed.

Keep generated/vendor exclusions consistent with project conventions. Reuse the existing linter. If adding golangci-lint, pin a tested version and use its matching schema: v2 separates `formatters` from `linters`. Consult the [official migration guide](https://golangci-lint.run/docs/product/migration-guide/) when changing major versions.

## Hooks and CI

Prefer staged-file non-mutating checks or a staged-content-aware hook framework. Move slower whole-project vet, lint, race checks, tests, and builds to pre-push or CI. Verify partial staging and failure propagation in isolation; do not auto-stage the working tree.

Use the same commands and tested toolchain in CI. Use supported dependency caching, explicit read-only permissions, and real failure-producing gates. Do not add Node, Vite, `frontend/`, generated Wails bindings, or platform installer jobs to a generic Go repository.

## Distribution, only when requested

For a library, preserve module/import-path and supported-version conventions. For a service, preserve its deployment platform. For a CLI, build and test the actual supported OS/architecture artifacts and stable asset names. Read [release.md](release.md) only for requested artifact release setup; the bundled tarball installer expects exactly one root-level executable and detached payload/manifest signatures verified with a trusted publisher key, as well as a matching checksum manifest.
