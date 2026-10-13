# Platform installation paths and separate CLI assets

**Read when:** locating an installed editor or diagnosing command not found.

Do not treat successful GUI installation as proof that the CLI is on PATH. The specialized app documentation generally describes a Windows CLI beside the app under Program Files, a Linux packaged CLI under `/usr/bin`, and a separate macOS CLI release ZIP rather than a binary inside the desktop `.app`. Verify the actual selected release and package.

The launcher installs applications using platform-native mechanisms where available: signed macOS app delivery, Windows installers, Linux native packages or fallback formats. Such operations may require elevation and can affect system-wide state. Confirm the intended destination and permissions before proceeding.

Linux fallback locations and sandboxed launcher paths differ from host package locations. In the documented Flatpak fallback, applications can live under the launcher's per-app data directory rather than a normal host PATH directory. A CLI inside that sandbox is not automatically invocable as a host process; inspect how the installed package is exposed.

Use absolute executable paths in agent launch descriptors. Verify OS/architecture, executable identity and actual version/catalog response. A same-named binary earlier on PATH may belong to another installation. Match the desktop and CLI release when connecting them; an incompatible pair can disagree on methods or parameters.

Do not distribute locally installed font binaries or extract private credentials while collecting installation evidence. A useful record needs package identity and binary hashes, not the user's whole application-data directory.

## Evidence

- [craft-launcher-readme](https://github.com/storytold/craft-launcher/blob/main/README.md)
