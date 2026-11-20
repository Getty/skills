# Diagnostic shortcuts

Read this when a request rests on a common storage belief — "it is mounted", "copies mean
HA", "share one ext4 volume", "RWO", "S3 is eventually consistent", "the snapshot is the
backup", "a second data center", "attach the disk to a new VM", "self-hosted is cheaper" —
to find what to check before accepting it.

- **“It is mounted, so it is a normal disk.”** Identify the implementation and
  operation-level contract; load filesystem/object semantics.
- **“Two/three copies means HA.”** Inspect data placement, voters, quorum thresholds,
  fencing, endpoint ownership, and spare capacity.
- **“We can mount one ext4/XFS/NTFS volume on several servers.”** Stop independent
  writers unless the complete filesystem/application coordination model supports them.
- **“RWO means exactly one pod.”** Distinguish node-based access from supported
  ReadWriteOncePod enforcement; inspect actual CSI capabilities.
- **“S3 means eventual consistency/no rename.”** Resolve provider and bucket type. AWS
  general-purpose, directory, table, and vector buckets have different contracts.
- **“A snapshot is our backup.”** Identify shared failure domains, app consistency,
  independent retention, and an actual restore path.
- **“A second data center solves disasters.”** Determine which copy is current, who can
  promote it, which side may write during a partition, and how failback avoids
  divergence.
- **“A new VM can attach the disk immediately.”** Verify location constraints, old-writer
  exclusion, control-plane reachability, mount recovery, credentials, and application
  startup.
- **“Self-hosted storage is cheaper.”** Include replicas, traffic, idle headroom,
  operators, recovery time, replacements, upgrades, and tested backups.
