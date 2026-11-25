# Prior art in agent tooling

Checked: 2026-11-25. These are inspected implementations, not endorsements or compatibility certifications. **Getty contract proposal v0.2** is our own integration contract; its provider, the getty-bun starters, is built and tested in getty-bun's CI (phase 1); its delivery template `getty-bun-install` is planned. Compare against [contract.md](contract.md), including the per-user `<version>/<target>` store and the starter's check on every call.

## AgentPulse: private fallback and explicit executable paths

Sources: [Bash installer, commit e34101f](https://github.com/jstuart0/agentpulse/blob/e34101f471ba842ad48fafb6e24d6942a4b1ca4b/scripts/install-local.sh), [README at that commit](https://github.com/jstuart0/agentpulse/blob/e34101f471ba842ad48fafb6e24d6942a4b1ca4b/README.md).

The Bash installer pins fallback Bun 1.3.12, checks a release-asset SHA256, and stages the executable beside its destination before renaming it. A private fallback lives under `~/.agentpulse/bun`. The wrapper, installation record, and service definitions retain the selected executable path. It keeps runtime storage outside replaceable application directories.

**Partial match:** an acceptable existing Bun can satisfy a minimum version; the private fallback directory is unversioned. This does not prove exact binding or a shared immutable store across plugins. AgentPulse is an agent tooling application, not evidence of a native marketplace-plugin implementation. The detailed installer findings here are verified for Bash, not PowerShell.

**Apply:** borrow explicit path handling, integrity checks and staged publication; retain Getty's stricter version/target contract.

## GStack: installation instructions inside a skill

Source: [`pair-agent/SKILL.md`, commit afb68ac](https://github.com/garrytan/gstack/blob/afb68ac2b1876848de08a4f0ee3085ba1984e691/pair-agent/SKILL.md).

The skill checks for Bun and, if absent, downloads the official installer to a temporary file, verifies its SHA256, and runs it for pinned Bun 1.4.2. This is a concrete instruction-driven setup precedent.

**Partial match:** existing PATH Bun bypasses that pin; installation is not a private per-version shared store. The checksum covers the installer script, and the broader setup builds components. Do not reuse its version/hash or infer that its confirmation policy applies to every session.

**Apply:** keep a packaged reference the agent can follow, in v0.2 for repair and diagnosis only; installation itself belongs in a reviewed script (the starter), with runtime selection and integrity metadata explicit in Getty's own contract.

## Claude-mem: executable discovery and dependency verification

Source: [`setup-runtime.ts`, commit 4dc8e48](https://github.com/thedotmack/claude-mem/blob/4dc8e48cddee663edc3e401109f836d11f926a45/src/npx-cli/install/setup-runtime.ts).

Setup discovers Bun or invokes the standard installer. Dependency installation uses the resolved executable with argument arrays, a frozen lockfile, and ignored lifecycle scripts. It checks required package entry points/subpaths after installation.

**Partial match:** this setup path does not pin a private exact Bun release. A version-probe failure can warn and return `"unknown"`; that must not satisfy Getty's exact-version requirement.

**Apply:** verify working imports and the executable, rather than merely checking that files or `node_modules` exist. Keep Getty's own lifecycle-script policy explicit; do not assume every dependency works with scripts disabled.

## Use the evidence within its limits

The inspected examples support separate design choices: instruction-driven setup (which v0.2 replaced with starter-driven installation), private runtime placement, integrity verification, absolute executable paths, and dependency checks. No complete match for the Getty contract was verified among these implementations. Do not describe partial precedents as a shared ecosystem standard, and do not turn their sample versions into Getty's recommended runtime version.

When extending this comparison, inspect executable source at a commit, record what was actually checked, and distinguish documentation claims from observed code and executed tests. None of the projects above was installed or tested end to end for this review.
