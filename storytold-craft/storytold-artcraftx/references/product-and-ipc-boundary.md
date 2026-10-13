# ArtCraft-X automation evidence and Tauri IPC

**Read when:** routing tasks to the experimental application or inspecting integration options.

ArtCraft-X is a separate experimental generative desktop application. Do not merge its settings, executable paths or API assumptions with the main ArtCraft product or the specialized Craft editors.

The reviewed source registers native functions through Tauri's `invoke_handler` in `crates/artcraftx/src/lib.rs`. That is evidence of an internal IPC dispatch layer, not a remotely accessible HTTP/MCP server or an operator CLI. No comparable `artcraftx-cli` generation contract was verified in the reviewed material.

A meaningful integration trace follows the frontend invocation, registered command, Rust argument/result types, permission/capability checks, credential handling and any backend job calls. A function name alone does not supply a safe callable schema. Keep all parts at the same revision and distinguish experimental code from what an installed release actually contains.

If a runtime supplies authorized computer-use capabilities, GUI operation may be possible; verify that capability instead of inventing a control socket. If it does not, report the missing execution surface and limit work to a sourced integration plan or code change explicitly requested by the user.

The absence of a verified operator interface should remain a machine-readable capability status. Do not downgrade it to a vague note that a later agent can ignore while constructing fictional commands.

## Evidence

- [artcraftx-readme](https://github.com/storytold/artcraftx/blob/main/README.md)
- [artcraftx-ipc](https://github.com/storytold/artcraftx/blob/98c2a48940aa0a54604637f665ee539c122fa707/crates/artcraftx/src/lib.rs)
