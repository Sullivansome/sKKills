# Next.js setup

Next.js is the Node/TS stack with framework-specific defaults. Read `node-ts.md` first for the base toolchain (pnpm, typecheck, hooks) — this file only covers what Next.js changes.

## Scaffold

```bash
pnpm create next-app@latest my-app --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
```

Use `--turbopack` for dev. For an existing project, never re-scaffold — just add what's missing.

## Lint + format

- **ESLint**: `eslint-config-next` is the official config (includes React, hooks, a11y, and `@next/next` rules like no-img-element). With ESLint flat config: `import next from 'eslint-config-next'` — or keep the generated `.eslintrc.json` if that's what the scaffold produced. Note: `next lint` is deprecated/removed in Next 15+; run `eslint .` directly as the lint script.
- **Biome alternative**: works but you lose the Next-specific rules. Acceptable for teams that prefer speed; keep ESLint if the user relies on `next/core-web-vitals`.
- Format with Prettier (`prettier-plugin-tailwindcss` if Tailwind) or Biome format. Never run two formatters.

## Typecheck

`next build` typechecks by default, but it's slow for a quick check — keep a dedicated `tsc --noEmit` script using the generated `tsconfig.json` (which includes `next-env.d.ts` and the bundler moduleResolution). Add `next-env.d.ts` to the typecheck include if it's gitignored.

## Tests

Vitest + Testing Library for components (`environment: 'jsdom'`), Playwright for e2e. Don't run e2e in the pre-commit hook — CI only.

## CI

Standard Node CI (see `assets/workflows/ci.yml`) with `pnpm build` proving the production build compiles. If the project deploys to Vercel, CI still matters for PR checks — Vercel preview deploys don't replace lint/typecheck gates.

## Release

Next.js apps deploy rather than ship installers — the release flow is usually Vercel/self-host deploy on merge to main, with tags for versioning. Point the user to `release.md` only if they also ship a desktop wrapper (Tauri/Electron around the Next app) or a CLI.
