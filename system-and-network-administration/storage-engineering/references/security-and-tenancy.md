# Storage security, tenancy and data lifecycle

Evidence reviewed: 2026-10-21. Apply these controls to the actual threat model and operation; do not manufacture compliance claims.

## Contents

- Separate security planes
- Control identity and network access
- Protect keys and recoverability
- Isolate tenants and resources
- Govern retention and deletion
- Verify security operationally
- Primary references

## Separate security planes

Map application access, storage data access, storage administration, backup administration, key management and infrastructure control separately. One compromised production credential should not automatically administer every historical recovery copy.

| Plane | Examples | Design concern |
| --- | --- | --- |
| Application | User permissions, object references, signed downloads | Prevent cross-tenant access even when IDs are guessable |
| Data | File share rights, bucket policies, block-device access | Grant the necessary operations and data scope only |
| Administration | Delete pools, change replicas, edit lifecycle, force failover | Stronger credentials and explicit operational ownership |
| Backup | Append backups, prune history, restore data | Separate ingest from destructive retention management where supported |
| Keys | KMS, encryption keys, recovery secrets, certificates | Key availability and rotation can determine data availability |
| Infrastructure | VM consoles, disks, hypervisor, root, cloud account | Bypasses at other layers must be considered |

Encryption, integrity, authorization, availability and recoverability are distinct. Replication cannot restore deleted keys. Encryption does not stop an authorized malicious application from overwriting plaintext through its ordinary interface.

## Control identity and network access

Prefer short-lived credentials and workload identities where supported. For simpler providers, scope static access keys narrowly, rotate them deliberately, and avoid embedding secrets in images, shell history, command-line process listings or repository configuration.

For NFS/SMB, verify identity mapping and the selected authentication/security mode. A private IP network is not proof that UID-based trust or an unencrypted share is sufficient. For iSCSI/NVMe-oF and other block transports, restrict which initiators can reach which targets and distinguish authentication from encryption.

For object APIs, separate bucket policy, identity policy, ACL and public-access controls according to the provider. Do not apply AWS-specific policy syntax or key scope assumptions to an endpoint that does not support them.

A presigned URL grants bearer access under the signing principal's permissions. Keep it out of public logs, referer trails and analytics. Use a lifetime appropriate to the operation, validate the uploaded result, and understand that short-lived underlying credentials may expire sooner than the requested URL lifetime.

Avoid treating CORS, obscure object names, a mounted-directory permission bit, or a CDN URL as independent authorization. Evaluate the entire access path, including cached private content and backup restores.

## Protect keys and recoverability

Distinguish:

- Encryption at rest inside the storage service.
- Host/volume encryption such as an encrypted block layer.
- File- or application-level encryption.
- Client-side object encryption.
- Encryption in transit.
- Integrity checks and authenticated encryption.

Record who possesses keys, how the service accesses them, which metadata remains visible, and whether restores in another account/site can decrypt the data. TLS protects a transport hop; a TLS-terminating gateway sees plaintext. Server-side encryption does not necessarily exclude the service operator from decryption.

Test recovery from key rotation, lost node credentials, unavailable KMS/secret service, expired certificate and lost administrative account. Keep bootstrap secrets outside a circular dependency: the only credentials to unlock storage must not exist only on that locked storage.

For backups, include encryption keys or the supported recovery material under an independently protected process. Re-encryption, key deletion and cryptographic erasure can be irreversible; verify the exact key scope and every retained copy before acting.

## Isolate tenants and resources

Use the strongest practical boundary for the risk: application-enforced namespaces, distinct credentials/buckets/shares, filesystem quotas, separate volumes, pools, nodes, accounts or providers.

A prefix is an organizational convention until policy enforces it. A Kubernetes namespace does not automatically isolate all shared storage paths, CSI credentials or network endpoints. Root access on a host can be stronger than per-file permissions.

Account for noisy neighbors and exhaustion: quotas for bytes, object count, inodes, snapshots/versions, bandwidth, API operations, open handles and metadata. Reserve capacity for recovery, logs and administrators; a tenant who fills every available byte can cause an availability failure without escaping authorization.

Protect sensitive filenames, object keys, access logs, metadata and backup indexes. Encryption of payload bytes alone may leave these exposed. Deduplication can introduce information leakage or cross-tenant coupling in some designs; evaluate its isolation scope rather than assuming it is purely a capacity feature.

## Govern retention and deletion

Build retention from the data lifecycle:

1. Define live data, historical versions, audit records and recovery copies.
2. Choose expiry rules for each and account for legal/business requirements supplied by the user.
3. Assign authority to change retention, bypass governance controls or delete keys.
4. Verify what delete means: hide latest name, create a delete marker, unlink, tombstone, discard, purge a version, or physically sanitize.
5. Confirm replicas, snapshots, caches and backups follow the intended policy.
6. Verify restore and deletion through evidence appropriate to the storage medium.

WORM/Object Lock may protect selected versions while allowing new versions or delete markers. Retention capabilities, bypass permissions and irreversible compliance modes are provider-specific. Do not equate “versioning enabled” with immutable backup.

File unlink and block discard/TRIM are not universal secure erasure guarantees. Flash translation layers, remapped sectors, copy-on-write snapshots, replicas and archives can retain data outside a simple overwrite. Use a medium-appropriate sanitization procedure and current organizational guidance; NIST SP 800-88 Rev. 2 is a primary reference for planning sanitization.

Distinguish cryptographic erasure from deleting a file containing one copy of a key. The claim depends on all relevant key copies, key hierarchy, encryption design and unencrypted remnants.

## Verify security operationally

Use controlled tests with disposable data and the intended identities:

- A reader cannot write or enumerate another tenant's data.
- An uploader cannot alter already-published objects unless intended.
- Production write credentials cannot erase every backup generation.
- A restore operator can recover needed keys and catalog state.
- Expired credentials and revoked rights are handled predictably.
- Private content is not publicly cached.
- Logs capture administrative changes without leaking secrets or signed URLs.
- Quota or policy failure produces a clear application error rather than silent data loss.

Do not remove security controls to resolve a storage incident until their causal role is established and the user has authorized the risk-bearing change.

## Primary references

- [AWS S3 security best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html).
- [Presigned URL capabilities and expiration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html).
- [AWS Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html).
- [NIST SP 800-88 Rev. 2](https://csrc.nist.gov/pubs/sp/800/88/r2/final): media sanitization framework.
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/): use version-matched platform guidance when implementing.
