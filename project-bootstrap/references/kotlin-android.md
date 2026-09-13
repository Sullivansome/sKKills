# Kotlin / Android setup

## What to detect

`build.gradle.kts` / `settings.gradle.kts`, `gradle/libs.versions.toml`, `AndroidManifest.xml`, or `com.android.application` plugin. Pure Kotlin (server/library) is the same minus the Android parts.

## Toolchain: Gradle plugins, not external tools

Everything runs through Gradle so local and CI can't drift. Add to the version catalog / build files:

- **ktlint** via `org.jlleitschuh.gradle.ktlint` → `./gradlew ktlintCheck` / `ktlintFormat`
- **detekt** (`io.gitlab.arturbosch.detekt`) for static analysis → `./gradlew detekt`. Start with the default config + `buildUponDefaultConfig = true`; a blank-slate custom detekt.yml is a maintenance trap.
- **Android lint** is built in: `./gradlew lint` — keep `abortOnError true`.
- **Tests**: `./gradlew testDebugUnitTest` (unit) — connected/androidTest need emulators, CI-only with `reactivecircus/android-emulator-runner` and only if the project has instrumented tests.

The command contract becomes gradle tasks: `ktlintFormat` (fix), `ktlintCheck`, `detekt`, `lint`, `testDebugUnitTest`, `assembleDebug` (build). Add an aggregate task (`checkAll`) if the user wants one command.

Also add the **Gradle wrapper validation** action in CI (`gradle/actions/wrapper-validation`) — wrapper-jar tampering is a real supply-chain attack.

## Pre-commit

Use staged-file checks supported by the pinned tools, or a staged-content-aware framework with non-mutating Gradle checks such as `./gradlew ktlintCheck`. Verify partial staging and failure exit codes in an isolated fixture. Do not call whole-worktree `ktlintFormat` from a plain commit hook or assume incremental Gradle tasks are fast enough.

Measure runtime; whole-project detekt, Android lint, builds, and tests generally belong in CI or pre-push. Keep formatter fixes as an explicit developer command rather than silently changing unstaged content.

## CI

```yaml
- uses: actions/setup-java@v4
  with: { distribution: temurin, java-version: 17 }
- uses: gradle/actions/setup-gradle@v4   # handles caching + wrapper validation
- run: ./gradlew ktlintCheck detekt lint testDebugUnitTest assembleDebug
```

Prefer `setup-gradle`'s supported dependency caching and verify its behavior with the chosen action version; measure performance instead of assuming a fixed speedup.

## Release

Tag push `v*` → build signed release artifact → GitHub Release:

- `./gradlew assembleRelease` (APK) or `bundleRelease` (AAB for Play).
- Signing via secrets: base64'd keystore + `KEYSTORE_PASSWORD`/`KEY_ALIAS`/`KEY_PASSWORD`, injected into `signingConfigs` via environment variables — never commit the keystore.
- Version: derive `versionName` from the git tag in `build.gradle.kts` (`versionName = providers.environmentVariable("VERSION").orElse("0.0.0-dev").get()` pattern) so the tag is the single source of truth.
- Attach APK/AAB to the release with `softprops/action-gh-release`. A curl install script doesn't apply to Android — if the user ships a desktop Kotlin app (Compose Desktop), use `compose.desktop` packaging (dmg/msi/deb) via `./gradlew packageDistributionForCurrentOS` in a matrix, same idea as `release.md`.
