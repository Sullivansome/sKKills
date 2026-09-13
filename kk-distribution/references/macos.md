# macOS distribution

Choose direct Developer ID distribution versus the Mac App Store before selecting signing identities and entitlements. This reference focuses on direct distribution; store distribution needs its own supported signing/submission path. Do not ship ad-hoc or development signatures as production Developer ID signatures.

## Native signing and notarization

Use Developer ID Application for executable code and DMG signing; use Developer ID Installer for installer packages. Sign nested code inside out using the appropriate hardened-runtime settings, entitlements, and secure timestamp. Do not use blanket deep signing as a substitute for enumerating nested frameworks, helpers and extensions. Verify the expected Team ID and designated requirements, not merely that a signature exists.

Package the app with the stack's supported tools. Validate code, notarize the supported submission with `xcrun notarytool`, inspect the returned status/log, and staple the ticket to supported app/DMG/PKG targets. ZIP files do not accept stapled tickets; follow Apple's archive workflow and sign the final archive bytes separately. Check the result on a clean Mac. [Apple notarization](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution), [packaging](https://developer.apple.com/documentation/xcode/packaging-mac-software-for-distribution), and [custom workflow](https://developer.apple.com/documentation/security/customizing-the-notarization-workflow) describe the platform mechanics.

Typical verification building blocks, adapted to the actual product:

```sh
codesign --verify --deep --strict --verbose=2 MyApp.app
spctl --assess --type execute --verbose=4 MyApp.app
pkgutil --check-signature MyApp.pkg
xcrun stapler validate MyApp.dmg
```

Use only applicable commands and supplement them with identity and notarization-status checks. An accepted notarization submission does not by itself prove that the app's entitlements, update flow, or every shipping container is correct. For a CLI binary, sign its Mach-O code and notarize an appropriate supported container; do not assume the raw executable supports stapling.

## Channels and updates

For direct downloads, finish native signing/stapling before generating final hashes, detached signatures, and the signed release manifest. Publish each selected architecture or a tested universal build. Verify quarantine/Gatekeeper behavior, installer permissions, first launch, supported upgrades, and removal.

If Homebrew is requested, choose a cask for a suitable application/installer or a formula for a CLI. Keep URL, version and digest tied to the final signed payload; test via a maintained tap and the current Homebrew guidance. Do not add quarantine-removal or signature-bypass instructions. Homebrew checksum matching alone does not verify a detached publisher signature; test the actual native/trusted verification path and report any gap before calling the channel compliant.

For Sparkle, Tauri, or another updater, use that updater's required signing keys and client verification in addition to OS signing. Include update metadata and helper code in the inventory. Stage rollout only after a valid signed upgrade and rejection of tampered updates have been exercised.

Missing Developer ID identity, notarization access, timestamp verification, or a required updater key blocks distribution. Keep the candidate private and report the exact missing capability; do not publish an unsigned DMG as a workaround.
