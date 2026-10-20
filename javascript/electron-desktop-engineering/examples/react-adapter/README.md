# React adapter sketch

Include `desktop.d.ts` in the renderer TypeScript project. `use-preferences.ts` subscribes with cleanup, handles an absent bridge, and ignores obsolete revisions. It was syntax-transpiled, not installed-React typechecked or browser-tested. The type-only import has no runtime output; the actual bridge is supplied by the secure-shell preload. Keep React out of main/preload unless a separately justified tool requires it.
