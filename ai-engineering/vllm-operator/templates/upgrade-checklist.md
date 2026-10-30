# Upgrade checklist

Before: save the running manifest/config; review release/security notes;
pin the image digest and model revision separately; have rollback artifacts ready.

Compare: CLI flags/defaults, engines/MRV2, kernel/quantization matrix, template
and parser, generation defaults, API/stream/usage fields, metric names/units,
cache/connector layout, administrative surface, dependencies, and GPU architecture.

Test: startup/readiness, correct short answer, long inputs/outputs, tools/JSON,
reasoning/TTFA, stream fragmentation, timeout/cancellation, tenant-cache isolation,
OOM/overload behavior, store failure, and new configuration limits.

Measure: identical warmup/cache state, realistic length mix, single request,
saturation/arrivals/bursts, errors and SLO goodput, CPU/RAM/VRAM/disk, quality.

Approve: document observed benefits and regressions; use a canary or maintenance
window; drain the old instance; test rollback. With only one GPU, do not promise
uninterrupted simultaneous operation of old and new instances.

After: update the source/compatibility matrix and runbook; invalidate/delete
old sensitive KV/cache artifacts in a controlled way; check retention and costs.
