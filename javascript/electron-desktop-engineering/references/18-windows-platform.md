# Windows integration, packaging, and operational edge cases

**Read when:** targeting Windows or diagnosing installed behavior.

## Target contract

Record minimum supported Windows version from the selected Electron release, architectures, installation scope, distribution format, signing, update mechanism, and enterprise constraints. Do not infer current OS support from an old tutorial. Distinguish per-user and machine-wide installation, store distribution, and conventional desktop installers.

## Platform review

Test installation paths, spaces/Unicode, file locking, antivirus interference, long paths where relevant, and permissions under a standard non-admin user. Avoid requiring elevation for ordinary user data or routine operation. Keep app data out of protected installation directories. Define single-instance behavior and file/protocol association ownership.

Signing and reputation are related but not identical: signing is not a guarantee of immediate absence of every OS warning. Verify current certificate/provider and distribution requirements. For updates, align updater with installer format and installed layout rather than assuming any Windows package can use the same feed.

## Desktop behavior

Check multi-monitor DPI, titlebar controls, taskbar identity, shortcuts, notifications, and sleep/resume. Persist user work continuously enough that logout/shutdown does not depend on a final asynchronous callback always finishing. Native modules/helper executables need matching architecture and packaged-path tests.

## Acceptance

Install, launch, update, repair where supported, uninstall, and reinstall as a normal user. Test locked files during update, interrupted download, network/proxy restrictions, and rollback/data compatibility. Verify signed installed artifacts, not just the unpacked development directory. Keep Windows Store-specific guidance separate from classic desktop packaging; entitlements, identity, and update ownership differ by channel.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E19: Code signing](https://www.electronjs.org/docs/latest/tutorial/code-signing)
- [E21: autoUpdater API](https://www.electronjs.org/docs/latest/api/auto-updater)
- [E28: App API](https://www.electronjs.org/docs/latest/api/app)
- [E40: Windows Store guide](https://www.electronjs.org/docs/latest/tutorial/windows-store-guide)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
