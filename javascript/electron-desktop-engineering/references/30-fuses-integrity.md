# Electron fuses, ASAR integrity, and production hardening

**Read when:** reducing packaged attack surface or reconciling tests with production configuration.

## Fuse decision record

Inspect supported fuse names and semantics for the selected Electron release and `@electron/fuses` version. Evaluate RunAsNode, Node options/inspect behaviors, cookie encryption where applicable, embedded ASAR integrity, and loading only from the expected ASAR according to current platform support. Do not copy a universal boolean array without understanding which tooling/features it disables.

Apply fuse settings before final signing. Verify the actual packaged binary after the packaging step, not only a source configuration. ASAR integrity depends on supported packaging/runtime integration and does not automatically cover all unpacked resources. Keep the trusted asset path immutable and review native/helper files separately.

## Testing conflict

Some Electron automation launchers rely on behaviors intentionally removed by production hardening, including RunAsNode-related launch paths. Use a documented test artifact where necessary and separately verify the production artifact's fuses and launch behavior. Never silently ship permissive fuses because they make one test harness easier to use.

## Failure and recovery

A wrong fuse can prevent startup, debugging, or tooling. Keep a reproducible build path and a rollback artifact. Restrict debugging capabilities in production according to threat model rather than relying on UI-hidden DevTools alone. Fuses reduce attack surface; they do not validate IPC, sanitize HTML, authorize files, or secure a compromised update authority.

## Acceptance

Read back fuse states, verify signatures after all transformations, and launch the final artifact. Test an intentionally modified archive/resource according to the actual integrity scope. Record which platforms and resources the check covers and what remains outside it. Do not claim tamper resistance solely because `asar: true` or an integrity-related option appears in configuration.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E12: Fuses](https://www.electronjs.org/docs/latest/tutorial/fuses)
- [E35: ASAR integrity](https://www.electronjs.org/docs/latest/tutorial/asar-integrity)
- [E17: ASAR archives](https://www.electronjs.org/docs/latest/tutorial/asar-archives)
- [E26: Playwright Electron support](https://playwright.dev/docs/api/class-electron)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
