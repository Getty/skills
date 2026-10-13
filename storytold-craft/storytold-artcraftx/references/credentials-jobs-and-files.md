# Credential and file boundaries in a generative desktop adapter

**Read when:** designing a narrowly scoped automation path.

The registered native surface includes credential-related operations, making it especially important not to expose arbitrary invocation to a model. Discover the exact supported credential mechanism and keep secrets out of skill data, command lines and shared logs. Do not inspect or copy a user's cookies/credential stores merely to discover available generation features.

Trace what content crosses the local/native/backend boundary before submitting a task. Source images, audio, documents and prompts can be private even when the final generated result is intended for publication. Obtain approval for the specific upload and any resulting charge/quota usage.

For an adapter, allowlist validated operations and input types, restrict file reads/writes to an approved workspace, bound downloads and record result paths. An application's internal Tauri permission system is not automatically preserved by an external wrapper that directly calls internal functions; explicitly maintain the boundary.

Handle asynchronous jobs using real returned identifiers and statuses. Do not invent polling paths, cancellation verbs, idempotency fields or retention promises. A native/frontend restart is not proof that a backend job stopped. Inspect the documented status mechanism before retrying a potentially paid operation.

Save results under new names and verify actual media characteristics before handing them to another Craft editor. Include a clear unsupported/not-tested status when the required execution path was not available.

## Evidence

- [artcraftx-readme](https://github.com/storytold/artcraftx/blob/main/README.md)
- [artcraftx-ipc](https://github.com/storytold/artcraftx/blob/98c2a48940aa0a54604637f665ee539c122fa707/crates/artcraftx/src/lib.rs)
