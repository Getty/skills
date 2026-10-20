# Code editors, language tools, and terminal components

**Read when:** integrating Monaco, CodeMirror, xterm.js, or a code-execution interface.

## Scope and discovery gate

Monaco, CodeMirror, and xterm.js are specialized editor/terminal ecosystems; their catalog links are discovery pointers, not reviewed API contracts in this package. Fetch the installed-version documentation before choosing a React wrapper, worker configuration, language service, addon, or stylesheet. Distinguish a maintained core project from a third-party wrapper that may lag its peer dependencies.

## Integration design

Assign ownership of the editor model separately from the visible view. Decide whether switching files retains models, undo history, selection, diagnostics, and language-server sessions. Dispose unused models, workers, listeners, and addon resources; keeping every file ever opened can become a memory leak. Lazy-load heavy language features and restrict worker origins according to deployment/CSP requirements.

A terminal UI is not a secure command executor. It displays terminal output and emits input; the backend/PTTY or Electron-owned service remains responsible for authorization, process limits, working directory, environment, cancellation, and audit policy. Treat links and escape-sequence effects as a separate review surface. Never expose a general shell bridge to an untrusted renderer just to make a terminal widget work.

## Acceptance

Open/close many files, reconnect the language service, switch themes, resize hidden panes, use IME, and test large/minified files. Test hostile-looking terminal output and links without executing embedded commands. Verify clipboard behavior, keyboard shortcuts that conflict with browser/OS commands, screen-reader mode, and worker loading in the packaged build. Document whether code is merely edited, statically analyzed, or actually executed; each requires different trust and resource controls.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R04: Effects decision guide](https://react.dev/learn/you-might-not-need-an-effect)
- [R74: Vite](https://vite.dev/guide/)
- [E01: Electron security checklist](https://www.electronjs.org/docs/latest/tutorial/security)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
