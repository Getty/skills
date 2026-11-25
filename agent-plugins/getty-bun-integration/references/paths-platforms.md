# Paths and platform selection

Status: Getty contract proposal v0.1. Use [contract.md](contract.md) for ownership and canonical fields.

## Resolve once, then use absolute paths

Derive the root from the OS user identity/home/profile exposed to the bootstrap adapter. Validate that it is absolute, belongs to the intended user, and is writable before provision.

| Environment | Proposed default executable |
| --- | --- |
| macOS/Linux | `<actual-user-home>/.getty/runtimes/bun/<version>/<target>/bin/bun` |
| Native Windows | `<actual-user-profile>\.getty\runtimes\bun\<version>\<target>\bin\bun.exe` |
| WSL | The Linux layout in that distribution's user home, with a Linux target. |
| Remote/container | The root of the user/environment actually executing the tool. |

Tildes and angle-bracket names are explanatory notation. Persist resolved absolute paths in local bindings; APIs need not expand a literal tilde. Never hardcode another machine's home path. If an alternative root is needed, make it one deliberate persisted provider setting shared by consumers; arbitrary per-call overrides must not silently split the store or locks.

This reduces dependence on shell startup and PATH; identifying the current user/environment remains necessary. For a home shared between incompatible execution contexts, configure separate local roots first.

## Select a real release artifact

Inspect the **chosen exact release**, not just current documentation or the agent client's platform list. Review:

- OS, architecture of the process that executes Bun, and deliberate emulation mode.
- Linux libc/ABI differences and minimum OS/kernel requirements.
- CPU instruction requirements and any official baseline variant.
- Actual asset, archive layout, checksum, and expected executable.
- Constraints from native application dependencies.

Use official [Bun installation documentation](https://bun.sh/docs/installation) and [release assets](https://github.com/oven-sh/bun/releases). Do not manufacture an asset URL or infer support from a plausible name. Artifact coverage can differ between releases.

Prefer verified native artifacts. Treat emulation as an explicit tested target and keep bindings separate. Do not reuse Windows executables in WSL or assume host runtimes exist in containers.

## Keep three paths separate

1. **Runtime executable:** shared store plus exact requirement.
2. **Consumer package:** current installed plugin/package location.
3. **User project:** explicit application input or chosen working directory.

Resolve imports against the consumer package and dependencies. Pass project paths as arguments where supported. Changing directory must not select another Bun, manifest, or unrelated dependency tree.

Prefer executable-plus-argument arrays. Quote for the actual shell when shell syntax is unavoidable; POSIX escaping is not PowerShell escaping. Test spaces, Unicode, and separators. Validate versions/targets before constructing paths.

## Host lifecycle

Claude Code uses versioned plugin cache locations; its plugin data has a separate lifecycle and may be removed on uninstall. Keep provider storage outside both. Resolve the current consumer root from host metadata rather than an old cached path. Source: [Claude Code loading](https://code.claude.com/docs/en/plugins/loading).

Apply the same lifecycle analysis to other hosts using their documentation. A moved package invalidates its package-root binding even when the shared runtime remains valid.
