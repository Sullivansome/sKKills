# Detached signatures and installer bootstrap

Use the approved production signing identity and its supported signing service. The example below matches the bundled bootstrap CLI installer's OpenSSL RSA/SHA-256 verifier. It is not a substitute for Apple or Windows native signing, timestamps, notarization, or package-manager trust. Other signing schemes need a matching, explicitly trusted verifier.

## Produce final release signatures

Finish all byte-changing native signing, packaging, notarization and stapling first. Build an inventory and manifest binding product, version, OS/architecture, filename, and SHA-256 digest. For compatibility with the bundled installer, use exactly one `# version v1.2.3` line and checksum rows `<sha256>  <filename>`; product/platform are encoded in its fixed asset names. Other signed context can use comment lines.

For each final payload, including direct installers, archives, package wrappers, and distributed bootstrap scripts, the protected signing job can use an existing RSA key file:

```sh
openssl dgst -sha256 -sign "$DISTRIBUTION_SIGNING_KEY_FILE" \
  -out "$artifact.sig" "$artifact"
openssl dgst -sha256 -verify "$TRUSTED_PUBLISHER_PUBLIC_KEY_FILE" \
  -signature "$artifact.sig" "$artifact"
```

Run signing and verification for every inventory item and then for `checksums.txt`. Configure the job to stop on any command failure; a final successful command must not hide an earlier failure. If the identity lives in a hardware or managed service, use that provider's supported mechanism instead of exporting its key. Signatures and the public verification key are publishable; private keys are not. Do not generate production keys merely to fill these variables.

Verify identity, complete inventory, version context, and each platform's acceptance gates before making any artifact public. The signature file authenticates bytes; the manifest binds those bytes to a particular release. Both are required by the installer contract.

## Authenticate the bootstrap before execution

An embedded public key cannot authenticate the script containing it. Provision the script or its verification key through an independently trusted path. After downloading a version-pinned script and its signature to local files, verify before execution:

```sh
openssl dgst -sha256 -verify "$TRUSTED_PUBLISHER_PUBLIC_KEY_FILE" \
  -signature install.sh.sig install.sh && VERSION=v1.2.3 sh install.sh
```

The public key file must be the intended publisher's previously trusted key. Never trust a newly downloaded key just because it sits beside the script, and never execute a downloaded installer to ask it whether it is authentic. Protect verified files from replacement between verification and execution. Latest-release discovery does not establish freshness; use an explicit supported version or a tested signed-update policy.

Test with ephemeral test identities: the expected key succeeds; missing signatures, byte changes, a different key, and a mismatched signed version fail before installation. Keep these local mechanics results separate from real certificate, hosted pipeline, and clean-OS installation evidence.
