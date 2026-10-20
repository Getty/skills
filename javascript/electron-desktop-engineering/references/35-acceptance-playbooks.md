# Acceptance playbooks and agent delivery requirements

**Read when:** finishing an implementation, reviewing an application, or delegating work to another agent.

## Read and act selectively

Start with `SKILL.md`, inventory the repository, then load the smallest relevant set of references. Security-sensitive bridge work requires preload, IPC, and threat-model chapters. Packaging work requires tooling, resource layout, signing, and updater chapters as applicable. React integration does not exempt any process boundary from this review.

## Scenario: secure desktop shell

Verify isolated/sandboxed renderer, narrow bridge, denied unknown sender/frame/URL, rejected malformed payload, denied navigation/window creation/permissions, correct CSP/assets, and listener cleanup. Pure policy tests are necessary but not sufficient; exercise the real packaged runtime.

## Scenario: document application

Open via native dialog, parse bounded content, edit, save conflict-aware data, cancel/close safely, recover after interrupted write, and migrate prior schemas. Test two windows, external file changes, offline state, and disk failure. Confirm no generic arbitrary path capability escaped to React.

## Scenario: release

Build cleanly, inspect included files, validate native architecture/ABI, apply/read back fuses, sign/verify, install, launch, and update from the previous release. Test bad feed/artifact, interrupted update, incompatible migration, and rollback recovery on every claimed target.

## Delivery contract

Provide changed files, decisions, threat/compatibility notes, exact commands and results, artifact stage tested, and unresolved risks. Never state “fully secure,” “cross-platform tested,” “signed,” or “update verified” unless the relevant evidence exists. The supplied README is optional human guidance; the skill and references contain the operative instructions. Install the whole directory, including examples, tests, scripts, and assets.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E01: Electron security checklist](https://www.electronjs.org/docs/latest/tutorial/security)
- [E07: IPC tutorial](https://www.electronjs.org/docs/latest/tutorial/ipc)
- [E26: Playwright Electron support](https://playwright.dev/docs/api/class-electron)
- [E19: Code signing](https://www.electronjs.org/docs/latest/tutorial/code-signing)
- [E20: Application updates](https://www.electronjs.org/docs/latest/tutorial/updates)
- [S01: Agent Skills specification](https://agentskills.io/specification)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
