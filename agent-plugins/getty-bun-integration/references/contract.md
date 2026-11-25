# Getty integration contract

Status: **proposal v0.1**, checked 2026-11-25. These are Getty design decisions. This skill contains no implemented provider, download service, CLI, or runtime.

## Responsibilities

| Component | Owns |
| --- | --- |
| Getty runtime provider | Approved release/target metadata, private shared slots, integrity verification, provisioning locks, receipts, retention policy. |
| Consumer plugin/tool | Exact Bun requirement, package manifest and lockfile, application sources, dependency setup, host adapter, smoke tests, bindings. |
| Agent host | Instruction/skill/hook surfaces, workspace trust, execution tools, activation/review behavior. |
| Setup agent | Following the packaged procedure with available tools and session authorization, inspecting outcomes, reporting failures. |

Call the provider component `getty-bun`; keep its managed executable named `bun` or `bun.exe`. Do not assume a command named `getty-bun` exists. Inspect the actual provider API before writing call sites. If the task includes building the provider, implement and test that API explicitly rather than presenting invented commands as available.

## Canonical consumer requirement

Place this custom object in the consumer's real `package.json`:

```json
{
  "gettyBun": {
    "contractVersion": 1,
    "bunVersion": "1.4.5"
  }
}
```

The version is illustrative, not a recommendation or Getty compatibility certification. Replace it with the version tested by the consumer. v0.1 accepts only stable `major.minor.patch`, without a leading `v`, ranges, tags, prereleases, or build suffixes. Future contracts may support other release identities explicitly.

[The schema](../assets/requirement.schema.json) validates the `gettyBun` object, not the entire manifest. Reject unknown contract versions and malformed requirements before provisioning. Bun does not enforce custom Getty fields; the integration must read and check them.

Keep ordinary requirements in `dependencies`/`devDependencies` and a shipped `bun.lock`. Do not infer the runtime pin from an arbitrary executable, `engines`, or a lockfile format. Optional toolchain metadata may mirror the exact pin but must not introduce a second runtime provisioner; see [prior-art.md](prior-art.md).

## Shared immutable runtime slots

Define `runtimeRoot` once for the current user and execution environment. The proposed default is the actual user home/profile plus `.getty/runtimes`.

| Item | Path relative to `runtimeRoot` |
| --- | --- |
| Runtime slot | `bun/<version>/<target>/` |
| Executable | `bun/<version>/<target>/bin/bun` or `bin/bun.exe` |
| Verified receipt | `bun/<version>/<target>/receipt.json` |
| Permanent mutex | `bun/.locks/<version>/<target>/.install.lock` |
| Attempt status | `bun/.locks/<version>/<target>/.installing` |
| Attempt stage | `bun/.staging/<unique-attempt-id>/` |

The runtime key is the exact version plus the provider-verified release target, including the selected OS/architecture/ABI/CPU artifact identity where relevant. Validate targets against trusted metadata before using them as path components; never accept arbitrary path fragments.

All projects and consumers in that environment requesting the same key reuse one slot. Different versions coexist. Installed executables and receipts remain immutable during ordinary operation. Update by installing a new key, then rebinding a consumer. Repairing a corrupt published key requires coordinated quiescence; do not overwrite a possibly running binary.

Keep the store outside consumer caches and data that clients may erase on plugin upgrade/uninstall. Consumers must not delete shared runtimes on removal. Sharing is per user/execution environment, not indiscriminate across Windows, WSL, containers, remote hosts, or network-mounted homes.

## Provider integrity record

Maintain reviewed metadata for each allowed key: official release identity, exact asset URL/name, expected archive SHA256, required archive member, supported OS/ABI/CPU conditions, and any expected binary hash/revision used by the implementation. Acquire integrity metadata through a documented trusted update path; a checksum from the same untrusted location as an archive is not an independent trust anchor.

Write `receipt.json` only after successful verification. Record contract version, exact Bun version, target, asset identity, archive hash, resulting binary hash, verification timestamp, and relative executable path. A receipt records a verified operation; it does not alone prove that today's file exists, runs, or matches today's consumer.

## Consumer binding

Record machine-local state for the installed consumer release: consumer/content identity, package root, manifest digest, lockfile digest, runtime key, resolved absolute executable, receipt identity, and dependency installation/smoke-test result. Store it where the host permits consumer state; regenerate after a cache move. Do not commit user-specific absolute paths into portable manifests.

Publish the binding only after runtime and dependencies pass. At execution, compare it with the current requirement and environment, recheck the actual executable, and revalidate changed content. Reject a mismatch instead of silently selecting another Bun.

Coordinate concurrent setup of the same consumer release so dependency installation and binding publication serialize. The runtime-key mutex does not protect a separate `node_modules` tree.

## Portability boundary

Distribute the same TS/JS application source across supported targets without compiling a custom executable for each OS. A compatible Bun binary, suitable dependency artifacts, and a working bootstrap are still required. Shell commands, filesystem conventions, native add-ons, and host APIs remain platform-sensitive. Verify these boundaries rather than promising universal execution from a file extension.
