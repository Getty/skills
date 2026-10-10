# Hetzner Object Storage

Reviewed: 2026-10-04. Read for S3 integrations, backup repositories, object permissions, retention and storage troubleshooting. Recheck the linked compatibility and limit tables before deployment; AWS S3 documentation explains operation semantics but does not establish Hetzner support.

## Establish endpoint, workload and access

Use the selected location's HTTPS endpoint: `fsn1.your-objectstorage.com`, `nbg1.your-objectstorage.com` or `hel1.your-objectstorage.com`. Configure the application's region and custom endpoint explicitly. Observe the account-wide base charge, hourly accumulated allowance, 64 kB minimum billable object size and current per-bucket/per-source-IP limits. API operations themselves are free; traffic resulting from them can be billable. The documented internal-traffic exemption covers `eu-central`. [Overview and limits](https://docs.hetzner.com/storage/object-storage/overview/)

The documented service uses HDD-based clusters and favors backups, archives and moderate artifact access. A bucket's data remains in one data center at its selected location; cross-location replication is not built in. There is no default object encryption at rest. Use measured latency and failure behavior when assessing demanding workloads. [General FAQ](https://docs.hetzner.com/storage/object-storage/faq/general/)

Treat `private` as an authorization setting. The documented access path remains the S3 endpoint; it does not provision a private Cloud Network interface. Therefore, provide private-only VMs with working DNS and egress, or place a backup initiator where both the application and storage are reachable. Public policies can expose objects even in a bucket originally created private. For temporary sharing, use narrowly scoped presigned URLs and treat them as bearer credentials. [Bucket access](https://docs.hetzner.com/storage/object-storage/faq/buckets-objects/)

## Set permissions before distributing credentials

S3 key pairs initially grant read/write access to every bucket in their project, including future buckets. Isolate trust groups in separate projects or use tested bucket policies that explicitly restrict keys/actions. Hetzner principals use its documented project/key identifiers; do not invent AWS account IDs or assume AWS IAM roles exist. Restricting keys can intentionally prevent Console object listing. Test allowed and denied operations using the actual application credentials. [S3 credentials](https://docs.hetzner.com/storage/object-storage/faq/s3-credentials/)

Keep application writers separate from retention administrators. Account/API control, S3 access, encryption keys and backup repository passwords have different scopes and recovery requirements. Do not include secrets in command examples, logs or generated infrastructure state outputs.

## Verify protection features independently

| Feature | Supported behavior and operating implication |
|---|---|
| Versioning | Retain prior object versions and retrieve by version ID. Account for old versions in retention and cost. [Versioning](https://docs.hetzner.com/storage/object-storage/howto-protect-objects/protect-versioning/) |
| Object Lock | Enable during bucket creation; existing unlocked buckets cannot acquire it later. Legal holds and timed retention are separate controls. [Legal hold](https://docs.hetzner.com/storage/object-storage/howto-protect-objects/protect-object-lock-legal-hold/) |
| Retention modes | Governance permits authorized bypass; compliance retention cannot end early. Select scope/duration deliberately and verify protection on an actual object version. [Retention](https://docs.hetzner.com/storage/object-storage/howto-protect-objects/protect-object-lock-retention/) |
| Lifecycle | Expire selected objects/noncurrent versions and abort incomplete multipart uploads. Check interactions with Object Lock and backup-tool retention before applying rules. [Lifecycle](https://docs.hetzner.com/storage/object-storage/howto-protect-objects/manage-lifecycle/) |
| Encryption | Supported server-side encryption is SSE-C. The client must retain and resupply the key; metadata is not encrypted by SSE-C. Losing the key loses access. Client-side backup encryption can provide a different protection boundary. [SSE-C](https://docs.hetzner.com/storage/object-storage/howto-protect-objects/encrypt-with-sse-c/) |

Do not confuse whole-object replacement semantics with deletion-resistant retention. An ordinary writable bucket is not an immutable backup merely because its API stores immutable objects. Test the backup tool's locking, pruning and restore behavior with the intended Object Lock policy; blanket retention on mutable repository metadata can break normal operation.

The compatibility table excludes features including bucket replication, notifications, website hosting and multiple AWS management features; only Standard storage is documented. CopyObject is restricted to the same bucket, SSE-C object copying is unsupported, and conditional PUT/DELETE on versioned buckets is listed as unsupported. Check the exact operation required by the client, not just an “S3 compatible” label. [Supported actions](https://docs.hetzner.com/storage/object-storage/supported-actions/)

## Exercise the integration

Use a dedicated test prefix with the actual application version and credentials. Upload representative small/large objects, exercise multipart transfers, download and compare hashes, overwrite/version as applicable, and verify restore from the intended historical version. Test both permitted and intentionally denied deletion. If testing compliance retention, use a tiny disposable object and an explicitly selected period.

Read-only inspection example after configuring a protected AWS CLI profile and setting the real bucket name:

```bash
aws --profile hetzner-s3 --region fsn1 \
  --endpoint-url https://fsn1.your-objectstorage.com \
  s3api get-bucket-versioning --bucket "$HETZNER_BUCKET"
```

Use provider-specific client guidance for supported flags and endpoint configuration. [CLI setup](https://docs.hetzner.com/storage/object-storage/getting-started/using-s3-api-tools/)

## Diagnose common failures

- **503/timeouts:** Reduce concurrency and burst size; use bounded retries with backoff and jitter. Measure whether failures follow a source-IP or bucket limit. Shared-cluster capacity can affect performance. [Performance FAQ](https://docs.hetzner.com/storage/object-storage/faq/general/)
- **HTTP 400:** Check upload inactivity and the Host header, especially behind custom domains/proxies. Preserve TLS verification and correct signed-request routing. [HTTP 400 guide](https://docs.hetzner.com/storage/object-storage/troubleshooting/http-400/)
- **Unexpected capacity growth:** List noncurrent versions and incomplete multipart uploads, not only visible current keys. [Bucket/object FAQ](https://docs.hetzner.com/storage/object-storage/faq/buckets-objects/)
- **Backup pruning fails:** Distinguish repository locks, insufficient permissions and retention protection before changing any policy. Do not apply generic object expiration to a deduplicated repository without its tool's documented model.

For cross-location recovery, copy through a controlled job, validate the copy and preserve independent retention. A destructive mirror can reproduce accidental deletion at its destination; explicitly choose whether synchronization or historical recovery is the objective.
