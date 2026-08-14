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

Prefer `xcodebuild` over `xcpretty`-wrapped pipelines unless the user wants pretty logs; if logs are unreadable, use `xcbeautify`.

## Pre-commit

Plain git hook (installed via a `scripts/install-hooks.sh` checked into the repo — git hooks aren't cloned) running SwiftFormat + SwiftLint on staged files only:

```sh
git diff --cached --name-only --diff-filter=d -- '*.swift' | while read f; do
  swiftformat "$f"; swiftlint lint --quiet "$f"
done
git add -u   # re-stage formatter fixes
```

Keep it to format+lint; `xcodebuild` anything is far too slow for a hook.

## CI

Runs on macOS runners — the expensive part. Minimize macOS minutes:

- `runs-on: macos-14` (ARM, cheaper/faster than intel), `actions/checkout@v4`
- Select Xcode: `sudo xcode-select -s /Applications/Xcode_16.app` (runner images list available versions — pin one)
- Cache DerivedData/SPM only if builds are slow; wrong cache keys cost more than they save. `runs-on: macos-14` builds are usually fast enough without.
- Steps: `swiftformat --lint .` → `swiftlint lint --strict` → `xcodebuild ... test`

## Release

**macOS app → dmg** (this is where dmg comes from in this stack):

Tag push `v*` → macos runner →

1. `xcodebuild archive -scheme MyApp -archivePath build/MyApp.xcarchive`
2. `xcodebuild -exportArchive -exportOptionsPlist ExportOptions.plist -exportPath build/` (Developer ID export for distribution outside the App Store)
3. Notarize: `xcrun notarytool submit build/MyApp.app.zip --keychain-profile ... --wait` then `xcrun stapler staple`
4. Package dmg: `create-dmg` (brew) or `hdiutil`
5. Upload to GitHub Release with `softprops/action-gh-release`

Secrets: base64'd signing certificate (`BUILD_CERTIFICATE_BASE64`), its password, Apple ID / app-specific password / team ID (or API key p8) for notarytool, stored via a keychain-setup step. Notarization is NOT optional for Developer ID distribution — un-notarized apps get Gatekeeper-blocked. If secrets are absent, produce an unsigned dmg but tell the user exactly what to add.

**iOS app → App Store/TestFlight**: no GitHub-Release artifact; the flow is `xcodebuild archive` + upload via `xcrun altool`/App Store Connect API key, or fastlane (`fastlane beta`) if the project already uses it. Keep fastlane if present, don't introduce it if not.

Version sync: set `MARKETING_VERSION` from the tag via `xcodebuild MARKETING_VERSION=1.2.3 CURRENT_PROJECT_VERSION=<build#>` overrides so the tag stays the source of truth.
