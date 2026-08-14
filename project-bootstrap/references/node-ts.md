# Node / TypeScript setup

## Package manager

Detect via lockfile: `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, else npm. Prefer pnpm for new projects. Pin it via the `packageManager` field in package.json (`"packageManager": "pnpm@9.x.x"`) so corepack enforces it for everyone including CI.

## Format + lint: Biome (default) or ESLint + Prettier

**Default to Biome** (`@biomejs/biome`) — one dependency, one config file, ~20x faster than ESLint+Prettier, and formatter/linter can't fight each other because they're the same tool:

```bash
pnpm add -D -E @biomejs/biome
pnpm biome init
```

**Use ESLint + Prettier instead when** the project already has them, needs a specific ESLint plugin Biome lacks (e.g. some framework rules), or the user asks. If so: `eslint`, `@typescript-eslint/parser`, `@typescript-eslint/eslint-plugin`, `prettier`, `eslint-config-prettier` (disables stylistic rules that fight Prettier — this is the piece people forget). Use flat config (`eslint.config.js`), not `.eslintrc`.

## Typecheck

`tsc --noEmit` as a dedicated script. It must be separate from the build — bundlers like esbuild/vite strip types without checking them, so "the build passed" says nothing about type safety.

## Tests

`vitest` for new projects (fast, ESM-native, jest-compatible API). Keep the existing runner if one is configured.

## package.json scripts (the contract)

```json
{
  "scripts": {
    "format": "biome format --write .",
    "format:check": "biome format .",
    "lint": "biome lint .",
    "typecheck": "tsc --noEmit",
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

- `pnpm/action-setup@v4` + `actions/setup-node@v4` with `cache: pnpm`, then `pnpm install --frozen-lockfile`.
- For Electron apps, see `references/release.md` — electron-builder produces dmg/msi/AppImage from a matrix job.
