# ArtCraft is not another Craft CLI

**Read when:** routing a generation task or deciding whether a proposed automation surface is real.

Storytold ArtCraft is the generative creative desktop product, distinct from the twelve specialized Craft editors. The reviewed repository includes a frontend, native application code and Rust HTTP client bindings. That architecture does not establish a `photocraft-cli`-style `artcraft-cli` operator interface.

No comparable operator CLI or MCP command contract was verified in the reviewed sources. This is a scoped evidence statement, not a proof that no experimental adapter exists anywhere in the repository. Do not invent `artcraft-cli generate`, an MCP server switch or a public REST route to fill the gap.

The verified `artcraft_client` component is used by the Tauri desktop application. Its endpoint bindings are grouped in modules, with one endpoint per implementation file and shared wire types kept separately. A useful integration investigation starts with the actual operation's endpoint binding, request/response types and native/frontend caller at one revision.

Distinguish four surfaces: the user-facing desktop workflow; internal Tauri/native commands; Rust HTTP bindings to backend services; and development/build commands. A development launcher starts the app; it does not by itself generate an image or control a live document. An internal backend route is not automatically a stable public API.

When a supported operator interface is unavailable, state the boundary and use only an actually available authorized GUI-control or SDK integration path. Never silently substitute another provider/application while attributing the result to ArtCraft. Preserve the requested product identity in the execution record.

## Evidence

- [artcraft-readme](https://github.com/storytold/artcraft/blob/main/README.md)
- [artcraft-client](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_client/AGENTS.md)
- [artcraft-dev](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/_docs/dev_setup.md)
