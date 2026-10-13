# Generation job records, costs and retry safety

**Read when:** planning or integrating remote generation through ArtCraft.

Before sending a generation request, establish the actual provider/model/capability list for the authenticated installation, requested output type, required source assets and any cost or quota implications. Model availability and service behavior are live account/server properties; do not freeze a marketing list into executable truth.

Get explicit approval for uploading private material, using paid capacity or publishing results. A request to inspect a project does not authorize those effects. Keep credentials in the supported secret/session mechanism, not prompt files, skill assets, command-line examples or logs.

Use a controller job record containing the operation intent, source hashes, sanitized parameters, request identifier, returned job identifier, actual server status, output handles, warnings and accepted budget. Controller labels such as pending/running/complete/failed are bookkeeping categories, not asserted upstream enum names; map them only after reading the real response types.

A timeout can occur after a paid job was accepted. Inspect the server's job/query contract before resubmitting. Do not assume idempotency keys, cancellation or refunds exist unless the actual API provides them. Store enough returned identity to recover without duplicating the request.

Once a result is available, download/save only to an authorized location and verify file type, dimensions/duration and content against the brief. A successful generation response is not evidence that the result is suitable, safe to publish, or free of third-party rights concerns. Keep the selected result and its provenance distinct from discarded candidates.

## Evidence

- [artcraft-readme](https://github.com/storytold/artcraft/blob/main/README.md)
- [artcraft-client](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_client/AGENTS.md)
