# Update approval, checksums and quiescent handoff

**Read when:** updating editors used by active agents.

Record the installed versions and active workloads before updating. Save documents, complete/cancel jobs through their supported interfaces, and close relevant processes intentionally. The launcher avoids replacing running applications, but an agent should not rely on a forced replacement or kill to make an update proceed.

Download verification and source authenticity are separate concepts. Compare artifacts against the official release's published checksums/signatures as available; a hash only proves correspondence with the expected bytes, not that an arbitrary hash source is trustworthy. Preserve the exact release/tag/asset identity in the evidence record.

Keep the previous working version or a rollback path according to the user's environment. Replacing a binary can change CLI grammar, MCP tool schemas, native-file versions or renderer behavior. After an update, capture catalogs again and run the app's bounded acceptance recipe on a copy before resuming production work.

Do not equate `main` source review with released functionality. A repository commit, release tag, downloaded binary and running desktop may all differ. Version-aware skills should carry those identities separately and refuse unsupported assumptions.

Installation, elevation, self-update and editor launch are user-environment mutations. Obtain the relevant authorization and do not silently enable recurring updates merely because a newer release exists.

## Evidence

- [craft-launcher-readme](https://github.com/storytold/craft-launcher/blob/main/README.md)
- [launcher-xtask](https://github.com/storytold/craft-launcher/blob/1aaf7b27be2dba970d1a77f96aef6aad52352730/xtask/src/main.rs)
