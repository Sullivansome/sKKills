# Windows and Chocolatey distribution

Windows code signing and Chocolatey package publication protect different layers. Sign the software, installer, executable package scripts, and final package wrapper; verify each at the layer that consumes it.

## Authenticode

Use the product's trusted code-signing certificate or managed signing service. Sign shipped EXE/DLL code and the final MSI/EXE/MSIX installer as applicable; preserve approved third-party signatures and verify their authorized publishers. Sign PowerShell package scripts after their final edits. Select an explicit expected identity rather than an arbitrary certificate from the runner.

With the Windows SDK SignTool, choose SHA-256 file digests and RFC 3161 timestamps with SHA-256 timestamp digests. Verify with the Authenticode policy and all relevant signatures, and enforce expected publisher/identity and timestamp checks separately. For example, `signtool verify /pa /all /v installer.msi` verifies signatures but is not by itself a complete publisher allowlist or required-timestamp gate. Treat signing warnings and timestamp failures as release failures. A valid signature does not guarantee SmartScreen reputation. See [Microsoft SignTool](https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool).

Do not store PFX passwords in command files or logs. Use secure provider integration and supported credentials. Test the actual architectures, elevation behavior, reboot/exit codes, upgrade path, and uninstaller signature where the product ships executable uninstall code.

## Build the Chocolatey package

1. Select a stable package ID and explicit version; choose community versus a private feed and confirm distribution rights. Use `choco new` and the installed CLI's package schema, then populate nuspec metadata, install/uninstall behavior, and dependencies.
2. Either embed permitted signed binaries or reference immutable versioned HTTPS artifact URLs. Download installers with exact final SHA-256 checksums and architecture-specific fields. Verify the downloaded installer's Authenticode signature and expected publisher **before** executing it; checksum verification alone is insufficient.
3. Determine silent install flags and accepted exit codes from the actual installer. Do not use bypass flags to silence checksum/signature failures or remove PowerShell signatures to make scripts run. Sign scripts only after all template substitution.
4. Run `choco pack`, verify the contents and script/binary signatures, and apply a detached signature to the final `.nupkg` plus include it in the signed release manifest. Do not edit the package after signing. If using NuGet package signing, first verify that the exact Chocolatey client and feed preserve and enforce that format; NuGet capability is not evidence of Chocolatey support.
5. Test fresh install, upgrade from the previous supported version, and uninstall in a clean Windows environment using the intended client/feed. Verify the downloaded package before any package script runs, plus the downloaded installer before execution.

Chocolatey package scripts are executable inputs. If the client/feed does not enforce the selected package signature, use a trusted pre-install verifier or controlled feed-ingestion gate that checks package signatures and admits only verified immutable packages. Document the trust in that feed and test rejection at the ingress. A check inside `chocolateyInstall.ps1` cannot protect against a malicious replacement of that script itself. Do not claim that plain public `choco install` enforces your detached signature unless tested evidence establishes it.

The signed-only policy applies to both the `.nupkg` wrapper and software it installs. If the requested channel cannot meet the verification contract, keep publication blocked and provide the concrete missing integration rather than weakening the policy.

## Submit and confirm availability

Once the selected channel passes those gates and publication is authorized, push the exact signed/verified package with `choco push <package>.nupkg --source <confirmed-feed>`. Configure API access via the environment's protected mechanism. For community publication, satisfy current package review requirements and distinguish submission from moderation approval and installable availability. Re-download the accepted version to confirm bytes, signatures and install behavior. Follow [Chocolatey package creation](https://docs.chocolatey.org/en-us/create/create-packages/) and [security guidance](https://docs.chocolatey.org/en-us/information/security/) for current rules; do not infer verification guarantees from the NuGet container format.
