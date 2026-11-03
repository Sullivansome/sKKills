# Electron setup

Electron is the Node/TS stack plus a desktop release pipeline. Read `node-ts.md` for lint/format/typecheck/hooks — this file covers Electron specifics.

## What to detect

- `electron` in dependencies, `electron-builder` or `electron-forge` config, `main` field pointing at a main-process entry
- electron-vite / electron-forge / electron-builder are the three common toolchains — keep whichever exists

For a new electron-vite project, verify its current official scaffolding command (for example `pnpm create @quick-start/electron`). Preserve the user's chosen toolchain.

## Toolchain notes

- Same Biome/ESLint + Prettier + tsc setup as `node-ts.md`. If the project uses electron-vite, inspect the tsconfigs covering main/renderer/preload. Use the supported `tsc -b` reference build or a `typecheck` script targeting each independent config (for example `tsc --noEmit -p tsconfig.node.json && tsc --noEmit -p tsconfig.web.json`). Plain `tsc --noEmit` at a references-only root does not check those projects.
- Security rules worth having in review if not lintable: `contextIsolation: true`, `nodeIntegration: false`, sandbox on.

## Tests

Vitest for main/renderer logic. Playwright exposes experimental Electron automation through `_electron.launch`; verify support for the installed Electron/Playwright versions and use it for appropriate integration/e2e checks.

## Release: dmg / NSIS exe / AppImage via electron-builder

`electron-builder` produces all three targets. package.json `build` config:

```json
{
  "build": {
    "appId": "com.example.app",
    "mac": { "target": "dmg", "category": "public.app-category.productivity" },
    "win": { "target": "nsis" },
    "linux": { "target": "AppImage" },
    "publish": { "provider": "github" }
  }
}
```

Release workflow: the authorized trigger selects a version/commit, then matrix jobs build with `pnpm exec electron-builder --publish never`. Require native signatures/notarization, updater signatures where applicable, detached payload signatures, and verification for every target before a separate publication job receives GitHub write credentials. Confirm the selected version/ref; no partial or unsigned release upload is allowed.

Gotchas:
- Windows target: electron-updater auto-updates only the NSIS target. Use `msi` only when the product needs MSI deployment (e.g. enterprise/GPO) and does not rely on electron-updater; otherwise keep `nsis`.
- macOS distribution requires configured Developer ID signing and notarization; Windows requires the chosen Authenticode signing provider and timestamps. Enforce identity/verification checks. Missing access blocks publication; report the required setup rather than publishing unsigned artifacts.
- Linux AppImage build needs `sudo apt-get install -y fuse libfuse2` on newer runners.
- Keep `version` in package.json consistent with the selected release version; compare it to the tag only for tag-triggered releases. electron-builder uses package.json's version for asset names.
- electron-forge instead? Use its makers (`@electron-forge/maker-dmg` etc.) + `electron-forge publish`; same matrix idea.

Curl install script: the bundled [assets/install.sh](../assets/install.sh) handles CLI tarballs only. If an AppImage or dmg installer is requested, implement a separate verified format-specific path and publish matching signed checksums and detached payload signatures; do not feed desktop artifacts to tar extraction. Windows can link to the selected installer.
