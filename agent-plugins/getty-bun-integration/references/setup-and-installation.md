# Setup and transactional installation

Status: Getty contract proposal v0.1. This is an implementation procedure, not a shipped installer. Follow [contract.md](contract.md), [paths-platforms.md](paths-platforms.md), and [installation-locking.md](installation-locking.md).

## Instructions and execution

Package a setup skill/reference with the consumer. A host-native adapter may inject conditional guidance pointing to it without requiring missing Bun. The ordinary agent follows those instructions using available tools and existing session authorization.

Context injection does not execute commands, prove completion, or order matching hooks. Keep readiness checks at each consumer execution boundary. Gate unavailable consumer functionality while keeping the agent's shell/read/edit tools usable for setup.

Keep recurring hooks short. Do not repeatedly install from session startup. Supply a clear setup entry point, deduplicate hints, and stop automatic retries after interruption or failure. A completion message is not an observed installation result.

## Bootstrap without external Bun

Inspect available capabilities. The first install may use a small POSIX-shell or PowerShell coordinator with download, hash, archive, and OS-locking facilities. Check these prerequisites; neither Node, Python, nor Bun may be silently assumed.

A Markdown reference can direct setup, but **one real coordinating process** must own the mutex across download, validation, and publication. Several independent shell calls with a dead PID in `.installing` are not one protected installation. Put the transactional part into a reviewed script or equivalent host operation and run it as one operation.

Use an existing provider's inspected implementation. If none exists, implement it within an authorized provider-building task or identify the missing component. Do not present a template as an installer or invent `getty-bun ensure` commands.

## Provision one runtime key

1. Parse the real consumer manifest and validate the Getty requirement.
2. Resolve root and target from trusted provider metadata. Check bootstrap capabilities, filesystem assumptions, space, and write access.
3. Acquire the permanent version/target mutex. Re-read readiness after acquisition; another installer may have completed.
4. Reuse a valid slot and reconcile orphan status under the mutex. Do not overwrite a corrupt published slot while consumers may run; use coordinated repair.
5. Create a unique private stage on the final slot's filesystem. Publish `.installing` under the mutex. Restrict workers to their stage.
6. Fetch the exact reviewed asset; verify its archive checksum before executing content. Reject traversal, links, duplicate executable entries, or unexpected archive layout.
7. Construct the staged final layout. Check executable permissions/type, run a bounded `--version` probe, compare the exact requirement, and run a minimal runtime smoke check. Record binary digest and receipt.
8. Publish the complete stage to an **absent** final slot while holding the mutex, using an operation whose atomicity is established for that local filesystem. A cross-filesystem copy/move is not such a primitive.
9. Clear this attempt's status safely and release the mutex. Keep the permanent lock file/control directory. Handle uncertain orphan workers as specified in the locking reference.
10. Provision consumer dependencies under separate consumer coordination; publish its binding only after all checks pass.

A crash after runtime publication but before marker cleanup should trigger validation and cleanup by the next owner, not blind reinstallation. Bound lock/network waits and preserve prior working bindings on failure.

## Official installer limitations

Official Bun installers accept a release and `BUN_INSTALL`; inspect current source before wrapping them. The Unix installer may edit shell startup files, so a private directory alone does not establish no PATH changes. The inspected Windows script exposes `-NoPathUpdate`, `-NoRegisterInstallation`, and `-NoCompletions`. Sources: [Unix installer](https://bun.com/install), [Windows installer](https://bun.sh/install.ps1).

Prefer controlled download/verification/extraction from provider-owned release metadata, or a demonstrably equivalent invocation into unique staging. Running an unpinned mutable installer script is not verification of the resulting runtime. Send installer logs to stderr or a dedicated log channel when stdout carries a host protocol.

## Authorization

Honor existing authorization for setup; do not repeatedly request the same permission. If a real boundary remains—required access, native hook review, or an unapproved system change—finish concrete reviewable work first and identify that step. Do not modify global shell configuration, replace system Bun, or add unrelated system packages as incidental effects of this private-store design.
