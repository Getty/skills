# Extensions, plugins, local services, and untrusted execution

**Read when:** adding plugins, executing workflows, or embedding local services.

## Define plugin trust classes

Separate built-in reviewed plugins, user-installed trusted code, and hostile/untrusted code. A plugin API and a separate Node process do not automatically constrain filesystem/network access. Utility processes improve process ownership and fault containment but are not a complete sandbox for arbitrary malicious code.

For declarative extensions, prefer a versioned schema with a fixed set of permitted operations and resource limits. For executable extensions, design an additional isolation boundary appropriate to the threat: OS sandbox, container/VM, constrained service, or another reviewed mechanism. Do not load arbitrary user JavaScript into main or grant an extension the application's unrestricted preload bridge.

## Capability protocol

Give each plugin an identity, version, allowed operations, storage scope, network policy, time/memory/output quotas, cancellation, and revocation lifecycle. Validate every message and treat plugin output as untrusted content. Do not let a plugin request arbitrary Electron APIs by string name. Keep secrets behind narrowly scoped operations instead of distributing raw credentials.

Local HTTP services need bound interfaces, authentication, origin/CSRF policy where relevant, port-conflict handling, process supervision, and update compatibility. “Only localhost” is not equivalent to “only this renderer can call it.”

## Acceptance

Test malformed/flooded messages, path traversal attempts, resource exhaustion, plugin crash/restart, permission revocation, and incompatible versions. Verify uninstall removes active listeners/processes and handles retained data deliberately. Document residual host privileges and distinguish cooperative limits from enforced isolation. Do not claim safe hostile-code execution without evidence for the actual OS-level boundary.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E01: Electron security checklist](https://www.electronjs.org/docs/latest/tutorial/security)
- [E14: utilityProcess](https://www.electronjs.org/docs/latest/api/utility-process)
- [E15: Message ports](https://www.electronjs.org/docs/latest/tutorial/message-ports)
- [E09: Protocol API](https://www.electronjs.org/docs/latest/api/protocol)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
