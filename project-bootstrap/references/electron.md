# Electron setup

Electron is the Node/TS stack plus a desktop release pipeline. Read `node-ts.md` for lint/format/typecheck/hooks — this file covers Electron specifics.

## What to detect

- `electron` in dependencies, `electron-builder` or `electron-forge` config, `main` field pointing at a main-process entry
- electron-vite / electron-forge / electron-builder are the three common toolchains — keep whichever exists

Scaffold new: `pnpm create @quick-start/electron` (electron-vite) is the current sane default.

## Toolchain notes

- Same Biome/ESLint + Prettier + tsc setup as `node-ts.md`. If the project uses electron-vite there are separate tsconfigs for main/renderer/preload — `tsc --noEmit` must cover all of them (project references or a `typecheck` script chaining `tsc --noEmit -p tsconfig.node.json && tsc --noEmit -p tsconfig.web.json`).
- Security rules worth having in review if not lintable: `contextIsolation: true`, `nodeIntegration: false`, sandbox on.

## Tests

Vitest for main/renderer logic. Playwright has first-class Electron support (`_electron.launch`) for e2e — CI only.

## Release: dmg / msi / AppImage via electron-builder

`electron-builder` produces all three targets. package.json `build` config:

```json
{
  "build": {
    "appId": "com.example.app",
    "mac": { "target": "dmg", "category": "public.app-category.productivity" },
    "win": { "target": "msi" },
    "linux": { "target": "AppImage" },
    "publish": { "provider": "github" }
  }
}
```

Release workflow: tag push `v*` → matrix job (macos-14, windows-latest, ubuntu-22.04) → `pnpm exec electron-builder --publish always` with `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}`. electron-builder uploads assets to a GitHub Release matching the checked-out tag, so the workflow must check out the tag ref.

Gotchas:
- macOS builds only sign/notarize with `CSC_LINK`/`CSC_KEY_PASSWORD` + Apple notarization secrets present; unsigned builds still produce a working dmg (Gatekeeper warning on open). Wire secrets as optional and list missing ones for the user.
- Linux AppImage build needs `sudo apt-get install -y fuse libfuse2` on newer runners.
- Keep `version` in package.json in sync with the tag — electron-builder uses package.json's version for asset names.
- electron-forge instead? Use its makers (`@electron-forge/maker-dmg` etc.) + `electron-forge publish`; same matrix idea.

Curl install script: adapt `assets/install.sh` — Linux downloads the AppImage, macOS the dmg (script can `hdiutil attach` + copy .app), Windows prints the msi link.
