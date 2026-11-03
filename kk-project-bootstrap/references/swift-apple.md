# Swift — iOS / macOS app setup

## What to detect

`Package.swift` (SwiftPM), `*.xcodeproj` / `*.xcworkspace`, `.swift` sources. iOS app: `Info.plist` with `UIApplicationSceneManifest` / SwiftUI `App` targeting iOS. macOS app: AppKit/SwiftUI macOS target. The CI and release flows differ between the two — determine which (or both) early.

## Toolchain

No package manager for linters — use Homebrew-installed tools (document in README) or mint/mise to pin versions. Pinning matters: SwiftLint rule sets change between versions and a surprise upgrade fails CI.

- **SwiftFormat** (`nicklockwood/SwiftFormat`) — formatter: `swiftformat .` (fix) / `swiftformat --lint .` (CI check). Config in `.swiftformat`.
- **SwiftLint** — linter: `swiftlint lint --strict` in CI (strict = warnings fail). Config `.swiftlint.yml`; start minimal — `opt_in_rules` only where the team wants them, or the first run buries the project in violations.
- **Type check** is the compiler: `xcodebuild build` / `swift build` covers it.

`.swiftformat` and `.swiftlint.yml` must both exclude generated/vendored dirs (`DerivedData`, `.build`, `Pods`, generated protobuf/mocks).

## Build + test (the contract)

- SwiftPM: `swift build`, `swift test`
- Xcode project: pin the scheme and destination so local == CI:

```sh
xcodebuild -scheme MyApp -destination 'platform=macOS' test          # macOS
xcodebuild -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 16' test  # iOS
```

Prefer `xcodebuild` over `xcpretty`-wrapped pipelines unless the user wants pretty logs; if logs are unreadable, use `xcbeautify` with shell `pipefail` so a failed build cannot be masked.

## Pre-commit

Use the project's staged-content-aware hook framework. For a project using `pre-commit`, local non-mutating hooks can check staged Swift files while the framework handles unstaged changes:

```yaml
repos:
  - repo: local
    hooks:
      - id: swiftformat
        name: SwiftFormat check
        entry: swiftformat --lint
        language: system
        types: [swift]
      - id: swiftlint
        name: SwiftLint check
        entry: swiftlint lint --strict
        language: system
        types: [swift]
```

Verify filename argument handling against the pinned tool versions. Do not use `git add -u`, unquoted filename loops, or a formatter that silently includes unstaged hunks. Test failure propagation, filenames with spaces, and partial staging in an isolated fixture. Keep project-wide builds out of the commit hook.

## CI

Runs on macOS runners — the expensive part. Minimize macOS minutes:

- `runs-on: macos-15` (ARM; verify the supported runner and required architecture), `actions/checkout@v7`
- Select an exact Xcode version listed in the chosen runner image and compatible with the project; do not assume an example application path exists
- Cache DerivedData/SPM only if builds are slow; wrong cache keys cost more than they save. Supported macOS runner builds are usually fast enough without.
- Steps: `swiftformat --lint .` → `swiftlint lint --strict` → `xcodebuild ... test`

## Release

**macOS app → dmg** (this is where dmg comes from in this stack):

Preserve the agreed trigger and selected source/version from [release.md](release.md); tag push `v*` is one option. On the macOS runner, adapt these paths and the export options to the actual archive product:

1. `xcodebuild archive -scheme MyApp -archivePath build/MyApp.xcarchive`
2. `xcodebuild -exportArchive -archivePath build/MyApp.xcarchive -exportOptionsPlist ExportOptions.plist -exportPath build/export` (Developer ID export for distribution outside the App Store).
3. Create the notarization submission: `ditto -c -k --keepParent build/export/MyApp.app build/MyApp.app.zip`.
4. Submit with `xcrun notarytool submit build/MyApp.app.zip --keychain-profile "$NOTARY_PROFILE" --wait`. Check the returned status/log; continue only when accepted. Staple the exported app with `xcrun stapler staple build/export/MyApp.app` and validate with `xcrun stapler validate build/export/MyApp.app`. ZIP files cannot be stapled.
5. Package the stapled app into the final DMG, sign with Developer ID Application, notarize/staple as applicable, then verify identities, tickets and clean-machine acceptance. If distributing a ZIP too, recreate it from the stapled app before producing detached signatures for its final bytes. See [Apple's custom notarization workflow](https://developer.apple.com/documentation/security/customizing-the-notarization-workflow).
6. Sign the final payload and release manifest after all byte changes. Upload only after every requested platform has passed its signing/verification gates.

Secrets: base64'd signing certificate (`BUILD_CERTIFICATE_BASE64`), its password, Apple ID / app-specific password / team ID (or API key p8) for notarytool, stored via a keychain-setup step. Notarization is NOT optional for Developer ID distribution — un-notarized apps get Gatekeeper-blocked. If credentials or notarization are unavailable, block distribution and report the missing capability. Never publish an unsigned fallback.

**iOS app → App Store/TestFlight**: no GitHub-Release artifact; the flow is `xcodebuild archive` + upload via `xcrun altool`/App Store Connect API key, or fastlane (`fastlane beta`) if the project already uses it. Keep fastlane if present, don't introduce it if not.

Version sync: validate the selected release version and build number, then pass `MARKETING_VERSION` and `CURRENT_PROJECT_VERSION` overrides to the archive command or update the project's established version settings before archiving. Compare against the tag only for tag-triggered releases; manual dispatch or platform-managed delivery uses its selected revision/version. Verify the archived version before export/upload.
