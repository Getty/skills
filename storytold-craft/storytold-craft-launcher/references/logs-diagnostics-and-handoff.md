# Launcher diagnostics and post-install verification

**Read when:** investigating failed installs or handing control to an editor skill.

The launcher writes logs in platform application-data locations rather than necessarily beside its executable. The documented locations include Linux user data, macOS Application Support, Windows LocalAppData and a portable-data variant. Locate the active profile before assuming a missing log means the launcher never ran.

Collect the relevant bounded log interval, selected product, release/asset, OS/architecture, install format, destination and error. Redact account/credential material and unrelated private paths before sharing. Do not upload a whole home directory or application-data tree for diagnosis.

Separate download failure, checksum/signature failure, elevation/installer failure, application launch failure and CLI-discovery failure. Their recovery procedures differ. A GUI opening successfully does not establish that an MCP server can initialize or that an editor can save/export under the agent's account.

After installation, run the editor's metadata probe, inspect the tool/command catalog and execute a bounded sample only with the intended authority. Verify a native save/reopen and requested output format where the downstream workflow depends on them. Hand off the actual binary path and evidence to the product-specific skill.

Report the exact completion level: package installed, GUI launched, CLI discovered, MCP initialized, sample operation verified. Do not compress those into an unsupported statement that the whole suite is ready.

## Evidence

- [craft-launcher-readme](https://github.com/storytold/craft-launcher/blob/main/README.md)
