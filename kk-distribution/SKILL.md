---
name: kk-distribution
description: Package, sign, verify, and publish desktop or CLI software for macOS, Windows including Chocolatey, and Linux package repositories or direct downloads. Use for distribution channels, code signing, notarization, installer/update trust, and package publication; use kk-release-delivery for service rollout or production recovery.
---

# Signed Software Distribution

Deliver installable software whose publisher and exact bytes can be verified on the user's machine. This personal collection requires **every distributed release payload to be signed**. Missing keys, unsupported verification, failed notarization, or an unsigned payload block publication; a checksum or an unsigned fallback is insufficient.

## Define the distribution matrix

Inspect the application's stack, existing packaging/update mechanism, version, architectures, minimum OS requirements, and requested channels. Identify artifact names, package IDs, publisher identity, signing method, verification mechanism, publication destination, and upgrade/uninstall behavior for each target. Preserve established tools and identifiers.

Read only the relevant platform references:

For final payload signatures and the bootstrap installer's exact verification contract, use [references/detached-signatures.md](references/detached-signatures.md).

| Target | Distribution and trust | Reference |
|---|---|---|
| macOS | Developer ID code/installer signatures, notarization, direct DMG/PKG/archive; optional Homebrew tap | [references/macos.md](references/macos.md) |
| Windows | Authenticode executable/installer/script signatures and timestamps; Chocolatey package and feed verification | [references/windows-chocolatey.md](references/windows-chocolatey.md) |
| Linux | Signed APT metadata, signed RPM packages/repository metadata, authenticated direct archives/AppImages | [references/linux.md](references/linux.md) |

`kk-project-bootstrap` can set up build machinery; this skill owns distribution formats, signing, package channels, and install/update trust. `kk-release-delivery` owns broader promotion/recovery coordination. Use siblings only if available; their absence does not permit skipping signing.

## Establish trusted identities before release

Record expected Apple Team ID, Windows publisher and allowed certificate identities, Linux signing key fingerprints, and the public verification material clients will trust. Inventory third-party executable components and their authorized signers. Verify certificate validity, timestamp service, signing permissions, key access, and revocation/rotation procedures without printing secrets.

Use the existing secure signing provider, protected key store, or hardware-backed service. Limit signing and publication credentials to protected release jobs; untrusted PR builds must not receive them. Never generate a new production identity, buy a certificate, expose a key, or weaken client trust just to complete a pipeline. A locally generated test key proves mechanics only.

The public key or allowed signing identity must come from an independently trusted installation/bootstrap path. Downloading a key alongside its artifact from the same untrusted location does not establish publisher identity. Pin an intended release or provide a signed update policy; signatures alone do not prevent replay of an older vulnerable version.

## Sign in the correct order

1. Build and test the requested OS/architecture candidates using locked inputs. Enumerate every file intended for distribution, including installers, executable helpers, update metadata, package wrappers, scripts, and direct archives.
2. Sign nested executable code and required scripts with platform-native signatures. Verify their expected identities; packaging must not invalidate them.
3. Assemble final installers/containers, then apply their native signatures and timestamps where supported. Perform notarization/stapling as applicable. Do not confuse an updater signature with an OS code signature.
4. After all byte-changing operations, produce digests and detached publisher signatures for final distributable payloads and a signed release manifest binding product, version, platform/architecture, filenames, and digests. Formats without native signatures still require authenticated detached signatures. Signature sidecars themselves do not require recursively signing more sidecars.
5. Verify signatures, identity, native OS acceptance, manifest completeness, and digest agreement on the exact files intended for publication. Every requested matrix entry must pass. Do not publish one platform early while another remains unsigned or failed unless the user explicitly narrows the release targets.

A signature's presence is not evidence of validity. Fail on an unexpected signer, missing timestamp where required, unsigned nested code, changed bytes after signing, missing inventory entry, or a verifier that was skipped. Keep unverified intermediate builds private and ineligible for release.

## Verify the consumer path

Test fresh install, upgrade from a supported older version, uninstall, architecture selection, and updater behavior in appropriate clean machines/VMs. Download the final candidate through the planned channel and verify it before running any installer or package script. An install script cannot authenticate itself after it has already started executing; do not recommend piping unverified network scripts into a shell.

For channels that do not enforce a supported signature format automatically, add and test a trusted verification step before package execution, or report that the channel cannot yet meet the signing requirement. Merely attaching a signature or publishing through HTTPS is not equivalent to client verification.

Exercise negative cases: absent signatures, corrupt/replaced payload, unexpected signer, stale version, missing timestamp/notarization, and modified package scripts. A valid trusted candidate must still install; refusing everything is not a useful verification path.

## Publish and report accurately

Prepare all signed and verified outputs before any missing publication approval. Reuse existing authorization; publishing a package or pushing a release is permitted only for the requested targets and version. Keep package API keys in the appropriate secret store and out of committed commands/logs.

Promote immutable verified artifacts; publish package/repository metadata that references those exact bytes. Track channel-specific acceptance, moderation, indexing, and mirrors independently. A successful `choco push` or artifact upload is not proof that users can install the approved version.

Record artifact/version, channel, signing identity, native and detached verification results, install/upgrade checks, and actual state: prepared, signed, verified, submitted, available. List missing credentials or platform access as blockers to the affected release, without claiming that this skill itself signs or publishes an unspecified app.
