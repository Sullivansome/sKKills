# Node / TypeScript setup

## Package manager

Detect via lockfile: `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, else npm. Prefer pnpm for new projects. Pin the exact tested version in the `packageManager` field in package.json; do not use an `x.x` placeholder. Install that same version in CI. If using Corepack, verify it is installed and configured; newer Node releases do not necessarily bundle it.

## Format + lint: Biome (default) or ESLint + Prettier

**For a new project, consider Biome** (`@biomejs/biome`) for integrated formatting and linting. Keep a working toolchain and check required framework rules before choosing:

```bash
pnpm add -D -E @biomejs/biome
pnpm biome init
```

**Use ESLint + Prettier instead when** the project already has them, needs a specific ESLint plugin Biome lacks (e.g. some framework rules), or the user asks. If so: `eslint`, `@typescript-eslint/parser`, `@typescript-eslint/eslint-plugin`, `prettier`, `eslint-config-prettier` (disables stylistic rules that fight Prettier — this is the piece people forget). Use flat config (`eslint.config.js`), not `.eslintrc`.

## Typecheck

Inspect the actual `tsconfig` files before choosing the command. For a single project that includes the application sources, use `tsc --noEmit -p tsconfig.json`. A solution-style root with `files: []` and `references` can return success without checking any application code when invoked with plain `tsc --noEmit`.

For project references, preserve the project's supported `tsc -b` workflow and its configured emit behavior, or run `tsc --noEmit -p <config>` for each independent application/tooling config. If projects consume generated declarations from one another, build those dependencies in the required order. See the [TypeScript project-reference documentation](https://www.typescriptlang.org/docs/handbook/project-references.html).

Keep a typecheck command separate from a bundler-only build: esbuild/Vite can strip types without checking them. In an isolated fixture, introduce a type error in each source project and verify that the chosen command fails, then restore valid code and verify success.

## Tests

`vitest` for new projects (fast, ESM-native, jest-compatible API). Keep the existing runner if one is configured.

## package.json scripts (the contract)

This example assumes a single source-bearing `tsconfig.json`; replace `typecheck` with the project-aware command above for a solution-style root.

```json
{
  "scripts": {
    "format": "biome format --write .",
    "format:check": "biome format .",
    "lint": "biome lint .",
    "typecheck": "tsc --noEmit -p tsconfig.json",
    "test": "vitest run",
    "build": "...",
    "prepare": "husky"
  }
}
```

## Pre-commit: husky + lint-staged

```bash
pnpm add -D -E husky lint-staged
pnpm exec husky init
```

`.husky/pre-commit`:
```sh
pnpm exec lint-staged
```

`lint-staged` config in package.json (runs on staged files only — this is what keeps commits fast):

```json
{
  "lint-staged": {
    "*.{ts,tsx,js,jsx,json,css,md}": ["biome format --write --no-errors-on-unmatched"],
    "*.{ts,tsx,js,jsx}": ["biome lint --no-errors-on-unmatched"]
  }
}
```

If typecheck is fast enough (<5s on this repo), add a second hook `.husky/pre-push` running `pnpm typecheck` — it's whole-project so it can't be lint-staged, and pre-push keeps commits snappy.

## CI notes

- `pnpm/action-setup@v6` + `actions/setup-node@v7` with `cache: pnpm`, then `pnpm install --frozen-lockfile`.
- For Electron apps, see [electron.md](electron.md) — electron-builder produces dmg/NSIS/AppImage candidates from a matrix job.
