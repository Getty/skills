# Decoded media, audio-health scope and portable sessions

**Read when:** diagnosing missing sound or packaging a session.

`open_session` returns a `missing` list. `inspect_session.sources[]` reports whether source audio is loaded in the pool. A loaded in-memory source and an accessible source file on disk are different facts; a session can still need relinking or packaging before it can reopen elsewhere.

The documented `session.audio_health` query checks loaded-source availability, sample-rate mismatches and clip-bound issues across playlists. It does not audit filesystem existence, signal levels, plugin behavior or routing. An all-clear result therefore does not mean the mix is audible, unclipped or portable.

Record source file paths, hashes, decoded sample rates, channel layouts and intended session sample rate. Changing the output file's rate or normalizing a conversion does not resolve every timing or routing issue inside an existing session. Inspect the actual source and clip ranges.

For portability, save the session and its associated media under an intentional package layout. Reopen from that location in a fresh process and verify `missing` is empty, source objects load, and representative clips play or bounce correctly. Do not delete original media until the copy, saved references and independent reopen have been verified and deletion is authorized.

Treat plugin binaries as executable dependencies, not inert audio data. Confirm plugin identity/version and availability where the session will run. A rendered mix can preserve the audible result when an editable session cannot carry the full processing environment; disclose that distinction instead of calling the project universally portable.

## Evidence

- [sound-mcp](https://github.com/storytold/soundcraft/blob/main/docs/mcp.md)
- [soundcraft-readme](https://github.com/storytold/soundcraft/blob/main/README.md)
- [sound-cli](https://github.com/storytold/soundcraft/blob/main/apps/soundcraft-cli/src/main.rs)
