# Backup and Restore

Evidence checked: 2026-10-21. Use this reference to design recovery from deletion, corruption, compromise, or loss of the primary storage system. Judge success by restoring the required application state in time.

## Contents

- [Classify the recovery artifact](#classify-the-recovery-artifact)
- [Choose a consistent capture method](#choose-a-consistent-capture-method)
- [Design independence and retention](#design-independence-and-retention)
- [Protect the whole recovery set](#protect-the-whole-recovery-set)
- [Build a restore workflow](#build-a-restore-workflow)
- [Verify without confusing checks](#verify-without-confusing-checks)
- [Size retention and recovery](#size-retention-and-recovery)
- [Primary references](#primary-references)

## Classify the recovery artifact

| Artifact or method | What it provides | Essential qualification |
| --- | --- | --- |
| Replica | Another current copy | Usually carries legitimate deletes and bad application writes forward |
| Snapshot | A point-in-time view of one storage boundary | Often depends on the original pool, account, and metadata |
| Clone | A writable derived copy | May share blocks or dependencies with its origin |
| File-level backup | Selected files, potentially versions and metadata | Capture open-file consistency, ACLs, links, sparse data, and exclusions deliberately |
| Image/block backup | Volume or machine recovery image | May need application coordination and recovery drivers/configuration |
| Logical database export | Portable logical objects or records | May omit roles, extensions, server settings, or other objects unless requested |
| Physical database backup + logs | Engine-native restore and point-in-time recovery | Requires a compatible engine and a complete valid recovery chain |
| Full / differential / incremental | Different capture/change strategies | Explain which bases and intermediate data are required for restore |
| Synthetic full / deduplicated snapshot | Logical full state assembled from shared stored chunks | Deleting a needed chunk or catalog can affect many recovery points |
| Continuous data protection | Frequent or continuous retained change history | Define retention, consistency points, and maximum recoverable lag |
| Offline/removable/tape archive | Physical or logical separation from online faults | Retrieval, media handling, catalog, key survival, and restore hardware govern usability |

A backup is a recovery capability, not a file extension. A snapshot exported into an independent, recoverable repository can form a backup. A directory called “backup” on the same unprotected pool does not create independence. Explain the exact shared and independent failure domains.

## Choose a consistent capture method

Distinguish **file-consistent**, **crash-consistent**, **application-consistent**, and **transactionally coordinated across applications**. Storage snapshots usually provide only the semantics their capture mechanism supports. An atomic volume snapshot can still capture a database needing crash recovery; snapshots of several volumes taken at different times may not form a valid database image.

Use a supported application backup protocol, quiescence hook, filesystem freeze, or consistency group as appropriate. Bound freeze duration and ensure failures unfreeze the workload. Do not copy a live database data directory with an ordinary file copier unless its engine documents that procedure. A successful copy command is not evidence of a valid recovery point.

Windows VSS is an example of coordination among backup requesters, application writers, and snapshot providers. Its value depends on the relevant application writer and provider participating correctly. Check writer results, not only whether a shadow copy exists. [Microsoft VSS overview](https://learn.microsoft.com/en-us/windows-server/storage/file-server/volume-shadow-copy-service)

PostgreSQL illustrates the distinction between logical exports and physical PITR: a valid physical base backup plus the required continuous WAL sequence can support recovery to a chosen point, whereas a logical dump is not a WAL-replay base. Retain the correct timeline history and validate archive completeness. [PostgreSQL continuous archiving and PITR](https://www.postgresql.org/docs/current/continuous-archiving.html)

## Design independence and retention

Choose independent failure domains for device, host, site, provider/account, identity, and encryption-key management. The familiar “3-2-1” family of rules is a planning mnemonic; it does not prove recoverability. Write down which incident each copy survives and who can erase or decrypt it.

Compare these controls:

- **Versioning:** retain prior versions, subject to lifecycle and deletion permissions.
- **Retention lock / WORM:** prevent selected modification or deletion for a defined period according to the service's mode and API semantics.
- **Append-only repository access:** reduce what a compromised backup client can remove, if the repository and protocol enforce the restriction.
- **Offline or disconnected copy:** remove ordinary online access during the disconnected period.
- **Separate administrative authority:** prevent one production credential from destroying every copy and its keys.

Do not treat these as interchangeable. An immutable object with a deleted decryption key is unusable. A protected version can remain recoverable even while an application sees a later corrupt version or a delete marker. Amazon S3 Object Lock applies to specific object versions, depends on versioning, and allows newer versions to be created; governance and compliance controls have different permissions and retention behavior. Verify the exact provider's implementation rather than transferring AWS guarantees to every S3-compatible endpoint. [Amazon S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)

Align retention with detection delay. If corruption is discovered after the oldest clean version expires, fast daily backups do not solve the incident. Define legal/business retention independently from engineering availability. Avoid changing irreversible lock policies as part of an exploratory test.

## Protect the whole recovery set

Inventory payload, indexes/catalogs, manifests, chunk maps, configuration, application versions, schemas, identities/ACL mappings, secrets, encryption keys, certificates, DNS, infrastructure definitions, and image/artifact repositories. Record any sequence needed to recover the identity or key services themselves. Keep access instructions outside the failed system's only copy.

For Kubernetes, treat cluster-state backup and persistent-volume backup as separate scopes unless the tool explicitly coordinates both. An etcd snapshot stores Kubernetes API state; it is not a copy of arbitrary application volume contents. Conversely, restored volume bytes do not recreate all workload manifests, storage identities, secrets, and routing. Follow the actual control-plane restoration procedure; etcd documents restore-specific identity and revision considerations. [etcd disaster recovery](https://etcd.io/docs/v3.6/op-guide/recovery/)

For a filesystem built on object chunks plus a metadata database, recover both consistently. An object bucket containing every chunk may be insufficient to reconstruct filenames and references if the metadata is gone. Include garbage-collection and retention rules in this coordination.

## Build a restore workflow

1. Define the incident, recovery objective, target environment, and authoritative recovery point.
2. Establish clean administrative access and retrieve keys through an independent path.
3. Restore the catalog/control metadata or rebuild it using the documented method.
4. Retrieve the full required data chain and verify transport/integrity results.
5. Restore ownership, permissions, configuration, and application dependencies.
6. Replay logs or complete application recovery to the intended boundary.
7. Validate application invariants and representative end-to-end requests.
8. Expose traffic only after confirming write ownership and recovery completeness.
9. Re-establish backups for the new authoritative environment and retain incident evidence.

Choose a restore target that cannot accidentally send production emails, execute queued jobs, or accept real writes during validation. When restoring after compromise, decide which credentials and artifacts require replacement before reconnecting the service.

## Verify without confusing checks

Use several checks with different purposes:

| Check | What it can show | What remains unproven |
| --- | --- | --- |
| Job success and object count | A scheduled capture and transfer completed | Semantic completeness and successful recovery |
| Repository metadata validation | Index/catalog relationships are coherent | Every stored payload byte remains readable |
| Payload verification | Checked data matches expected checksums | The application was consistent at capture time |
| File/sample restore | Selected retrieval paths work | Whole-system restore time and omitted dependencies |
| Full isolated application recovery | The selected recovery set can run | Future versions, larger datasets, and other incident types |
| Timed disaster exercise | Actual critical-path behavior under a chosen failure | All possible failures or an unchanging future RTO |

For example, restic's default repository check and a check that reads stored data have different coverage and I/O costs. Budget payload verification explicitly and record whether sampling eventually covers the full repository. [restic repository verification](https://restic.readthedocs.io/en/stable/045_working_with_repos.html)

Test at least a recent point, an older retained point, and a recovery involving lost production credentials. Validate application data counts, cross-store references, migrations, and representative user operations. Record measured elapsed times, missing prerequisites, and the fixes applied to the runbook.

## Size retention and recovery

Model retained logical versions separately from physically deduplicated chunks. Use measured change rates, retention tiers, compression, and lifecycle behavior. Account for immutable data that cannot yet be pruned and for temporary space needed during compaction or restore.

Size restore throughput using the source read limit, retrieval delay, request limits, network/egress, decryption/decompression, destination writes, and application replay. A 100 TB backup with sufficient capacity but insufficient transfer bandwidth cannot meet a short RTO. Consider local recovery copies, warmed replicas, or staged restoration when the business objective requires them; retain an independent backup for historical recovery even then.

## Primary references

- [PostgreSQL PITR](https://www.postgresql.org/docs/current/continuous-archiving.html): physical backup and log-chain recovery.
- [Microsoft VSS](https://learn.microsoft.com/en-us/windows-server/storage/file-server/volume-shadow-copy-service): coordinated application snapshots.
- [Amazon S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html): version-specific retention semantics.
- [restic repository checks](https://restic.readthedocs.io/en/stable/045_working_with_repos.html): metadata versus payload verification.
- [etcd disaster recovery](https://etcd.io/docs/v3.6/op-guide/recovery/): control-plane restore considerations.
