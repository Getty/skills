# JavaScript skills

Engineering knowledge for the JavaScript/TypeScript ecosystem, where the frameworks
move faster than any single skill could track. Both skills below share one design:
a small `SKILL.md` that holds the operating sequence, a "load by task" table and the
non-negotiable boundaries, and a numbered `references/` directory of which an agent
loads two to four chapters — never the whole package. Neither asserts an unverified
"latest" version; each starts by establishing what the project actually resolves and
keeps source review, syntax checks and executed tests apart in what it reports.

The two are companions: `react-ecosystem-engineering` covers the renderer,
`electron-desktop-engineering` the privileged side around it, and the React skill hands
over to the Electron one at the preload boundary.

Install the **whole directory** of either skill — the references, `assets/`, `scripts/`
and `examples/` are operative, not decoration.

## [electron-desktop-engineering](electron-desktop-engineering/SKILL.md)

Building, securing, reviewing, debugging, packaging and maintaining Electron desktop
applications. The skill assumes a compromised renderer is possible and keeps the
defaults that make that survivable: `contextIsolation`, `sandbox`, no
`nodeIntegration`, and a preload that exposes narrow domain methods
(`preferences.setTheme(theme)`) instead of raw IPC. The main process validates sender,
frame, payload and authorization on every call.

Thirty-six reference chapters run from process architecture, preload and IPC contracts
through CSP and navigation, sessions and permissions, storage, credentials, native
addons and utility processes, to the per-OS platform notes, Forge / electron-builder /
electron-vite, fuses, signing and notarization, update rollouts and recovery. It
distinguishes pure, runtime, packaged, signed, installed and update evidence, and
ships a constrained example shell, threat-model and release-gate templates, a
read-only project inventory script and policy tests.

**Load when** working on an Electron app — architecture, IPC, security review,
packaging, signing or updates — or when a React renderer needs platform access.

## [react-ecosystem-engineering](react-ecosystem-engineering/SKILL.md)

Building, reviewing, debugging, migrating and testing React applications and the
library ecosystem around them. It inspects the repository before prescribing a stack
and keeps an existing coherent one unless evidence says otherwise. The invariants:
rendering stays pure, identity stable, resources explicitly owned; values are derived,
not mirrored in effects; URL state, server cache, form drafts and client stores stay
distinct; types are not authorization, so external boundaries get runtime validation.

Fifty-odd chapters cover hooks, the compiler and concurrency, SSR and RSC, routing,
query caches, forms and schemas, headless primitives and accessibility, tables,
charts, editors, drag and drop, realtime and local-first, auth, testing and
debugging, plus an ecosystem catalog and stack recipes for dependency decisions. React
Flow has its own deep track — nodes, handles, layout, validation, persistence, history,
collaboration, performance — under the rule that a diagram editor is not a workflow
executor.

**Load when** writing or reviewing React, choosing between libraries, building a
React Flow editor, or migrating legacy React code. For Electron-specific privileged
work, load `electron-desktop-engineering` alongside it.
