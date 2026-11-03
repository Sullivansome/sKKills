# Next.js setup

Next.js is the Node/TS stack with framework-specific defaults. Read `node-ts.md` first for the base toolchain (pnpm, typecheck, hooks) — this file only covers what Next.js changes.

## Scaffold

```bash
pnpm create next-app@latest my-app --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
```

Use `--turbopack` for dev. For an existing project, never re-scaffold — just add what's missing.

## Lint + format

- **ESLint**: `eslint-config-next` is the official config (includes React, hooks, a11y, and `@next/next` rules like no-img-element). Use the flat-config exports supported by the installed `eslint-config-next` version (for example its `core-web-vitals` entry), preserving valid existing configuration. `next lint` was deprecated in Next 15.4 and removed in Next 16; run `eslint .` directly for modern versions.
- **Biome alternative**: works but you lose the Next-specific rules. Acceptable for teams that prefer speed; keep ESLint if the user relies on `next/core-web-vitals`.
- Format with Prettier (`prettier-plugin-tailwindcss` if Tailwind) or Biome format. Never run two formatters.

## Typecheck

For installed Next versions supporting it, use `next typegen && tsc --noEmit` so a clean checkout has generated route types and `next-env.d.ts` before checking. Preserve the generated `tsconfig.json` includes. For older versions, use the documented supported generation/build path and verify from a clean fixture. See the [official CLI reference](https://nextjs.org/docs/app/api-reference/cli/next).

## Tests

Vitest + Testing Library for components (`environment: 'jsdom'`), Playwright for e2e. Don't run e2e in the pre-commit hook — CI only.

## CI

Standard Node CI (see [assets/workflows/ci.yml](../assets/workflows/ci.yml)) with `pnpm build` proving the production build compiles. If the project deploys to Vercel, CI still matters for PR checks — Vercel preview deploys don't replace lint/typecheck gates.

## Release

Next.js apps usually use a service deployment flow. Preserve the existing provider, trigger and source/version binding; tags are optional. Point the user to `release.md` for requested artifact automation, such as a desktop wrapper (Tauri/Electron around the Next app) or a CLI.
