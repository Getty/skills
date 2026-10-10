# Garbage collection without corrupting live content

> Read when: disk reclamation is required or scheduling registry maintenance.

Distribution's mark-and-sweep GC identifies content referenced by manifests and removes unreferenced blobs. Concurrent writes can invalidate the mark set. Run GC only under the selected release's safe procedure: stop writers or put **every** serving replica into verified read-only mode, then run the matching binary/config against the intended storage.

## Maintenance sequence

1. Verify backups and the exact registry image/config/storage target. Finish or pause CI pushes and cache writers.
2. Enter the maintenance window; disable writes across the entire deployment and prove a test write is rejected.
3. Run the supported `garbage-collect --dry-run` command with the exact configuration and storage access. Review candidates and retained release dependencies.
4. Only after explicit approval, perform the real GC. Keep logs and measure reclaimed bytes.
5. Verify representative retained digests, all required platforms, and attached artifacts; then restore writes and test a controlled push.

Commands are deliberately not embedded in a blind scheduled deletion script. A typical invocation uses the registry binary's `garbage-collect` subcommand; inspect `--help` for the exact image release and options before executing. Using a different binary or incomplete config can select the wrong backend.

## Dangerous assumptions

`--delete-untagged` is not synonymous with safe cleanup of “unused images.” Tagless objects can be referenced through multi-platform indexes or artifact relationships; behavior and bug fixes are version-dependent. Test the full artifact graph on a restored copy before enabling aggressive options.

A dry run is evidence at one moment, not a lock against concurrent writes. Disabling pushes at one proxy does not cover a second endpoint or a cache that writes fetched blobs. A storage snapshot alone does not make simultaneous GC safe.

## Stop conditions

Stop if storage ownership is uncertain, any writer remains active, inventory is incomplete, retained manifests reference missing content, or the release's GC/referrer behavior is untested. Restore/read-only investigation is safer than deleting low-level files to recover a few gigabytes.

## Primary sources

- [Distribution garbage collection](https://distribution.github.io/distribution/about/garbage-collection/)
- [Distribution configuration](https://distribution.github.io/distribution/about/configuration/)
- [OCI Distribution specification 1.1.1](https://raw.githubusercontent.com/opencontainers/distribution-spec/v1.1.1/spec.md)
- [Distribution releases](https://github.com/distribution/distribution/releases)
