# Versions, implementations, and compatibility

Read before installation, an upgrade, or copying an old recipe. Evidence: [G1, G4, G13, S1, S2](sources.md).

## Reviewed release boundary

The current release discovered on 2026-10-14 was **gearmand 2.1.0**, published 2026-08-31. Version 2.0.0 was published 2026-07-22. Preserve these dates with this snapshot rather than presenting the package as perpetually current.

The important 2.0 boundary includes global priority selection across functions registered on a worker connection, round-robin as the non-disableable default, FIFO rather than LIFO submission from libgearman task lists, improved epoch scheduling, and the added libgearman worker TLS API. The 2.1 boundary changes zero retry configuration and rejects `--ssl` on a server build without SSL support. Those are compatibility gates, not cosmetic release details.

## Retry migration trap

Before 2.1, zero was the unlimited setting. In 2.1, `--job-retries=0` means no requeue after the first interrupted attempt; the default unlimited setting becomes `-1`. Positive values need special care: the inspected requeue path increments an interruption counter and drops at equality with the configured positive threshold. Do not infer “initial attempt plus N additional attempts” from the option's name. Test actual assignment counts for the exact build. Requeue counts are not a durable application attempt ledger.

## Inventory record

Record all of: executable path; implementation; version; package revision; build options; backend availability; server source commit when built locally; libgearman runtime version; language binding and interpreter version; TLS implementation; deployment image digest. A PHP extension version, a Perl distribution version, and a server version are independent values.

Use `scripts/gearman_ops.py inventory` to capture installed help/version output without touching a running service. Then query the target's version read-only. Resolve `/usr/bin` versus `/usr/local/bin` collisions explicitly, especially when both Perl and C implementations install a `gearmand` name.

## Compatibility matrix to fill

For every deployed client/worker combination test foreground, background acceptance, unique-key coalescing, worker disconnect, explicit failure, progress/data packets, malformed input rejection, server restart, native TLS rejection cases, and delayed-job support when used. Test old and new workers simultaneously while queue payloads from both producer versions exist.

A packet number listed in a protocol header is not evidence the deployed server handles it. In the inspected C source, `SUBMIT_JOB_SCHED` remains an invalid-command case; do not turn that packet into a promised cron service. Likewise, the original Perl server and Python convenience server are not interchangeable durability implementations.

When documentation and source conflict, preserve the conflict in the deployment record, prefer a matching reproduction, and avoid a dangerous command until resolved.
