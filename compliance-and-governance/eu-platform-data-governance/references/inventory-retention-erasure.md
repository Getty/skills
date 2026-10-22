# Inventory, retention, restriction, and erasure

Sources: D1, D8, D11. Concrete control patterns below are implementation choices supporting the legal duties.

## Build a data-class map

Record purpose, subject/tenant identifiers, sensitivity, source, controller, recipients, location, access, derivations, retention rule, legal hold, disposal and evidence owner. Include these commonly missed copies:

- Uploaded original, OCR/transcript, extracted tables, chunks, embeddings, keyword indexes and summaries.
- Query/context/output, agent memory, semantic/result cache, feedback, evaluation samples and training datasets.
- Database replicas, CDC streams, search indexes, asynchronous retries, dead-letter queues and message payloads.
- Observability, APM, crash dumps, issue attachments, customer-support exports, email notifications and webhooks.
- Object versions, snapshots, backup sets, disaster-recovery replicas, downloads and vendor-controlled copies.

Map parent/child lineage so a document, tenant or subject can be corrected, restricted or erased across derived systems. Use stable opaque IDs and deletion-event propagation; do not place a person's name in every log merely to facilitate deletion.

## Design the schedule

For each class capture purpose end-event, duration/criterion, legal/contractual basis, start point, system enforcement, owner, exceptions and review trigger. There is no universal GDPR 30-day/90-day/10-year schedule. A statutory accounting requirement applies to the records it covers, not automatically to chat histories or full document attachments.

Separate retention needed for service delivery from security investigation, billing, legal claims and training. A customer retention setting must be reflected in provider copies and derived stores, or the limitations must be accurately described and assessed. Avoid indefinite default retention with a future intention to decide.

If retention is justified for claims or a legal obligation, identify the specific records and applicable country rule. Apply a scoped hold with owner, authority/reason, release trigger, access restrictions and periodic review. Do not use a generic litigation label to suspend deletion across all tenants.

## Erasure workflow

1. Identify the request/event, legal controller, verified authority, affected data and relevant deadline.
2. Determine grounds and lawful exceptions; distinguish erasure from account closure or disabling login.
3. Stop new processing/ingestion and prevent queued jobs or restored snapshots from recreating erased content.
4. Resolve lineage and delete or irreversibly anonymise covered records across active/derived stores as appropriate.
5. Send required instructions/notifications through authorised supplier/recipient processes; verify acknowledgements and actual scope.
6. Restrict retained data to its surviving purpose and record a bounded disposal date/criterion.
7. Verify with representative identifiers, authoritative stores and synthetic controls; record scope and limitations.
8. Provide an accurate outcome to the controller/person through the approved rights process.

Maintain idempotent deletion jobs, retry/failure queues, reconciliation reports and access-restricted tombstones. A tombstone can itself be personal data: minimise it, restrict purpose and set a justified lifetime. Use erasure receipts referencing object IDs/counts rather than retaining the deleted payload as proof.

## Backups and immutable storage

Do not claim backups are automatically exempt from Art 17. Design a defensible bounded approach: promptly remove active copies, restrict backup access/use, set the shortest justified backup lifecycle, ensure expiry, and reapply deletion/restriction before restored data returns to use. Document actual technical constraints, risk, timeframe and legal assessment. An immutable backup cannot become an indefinite secondary archive.

Test a restore into an isolated environment using synthetic data. Reconcile tombstones, source-authority changes and expired retention before reconnecting applications. Protect the tombstone ledger from expiring before the last relevant recoverable backup.

Crypto-erasure is only meaningful where key destruction makes all relevant copies irrecoverable, including wrapped keys, escrow, replicas and vendor copies. A shared encryption key may cover unrelated data; deleting it can cause unauthorised destruction. Obtain the correct operational authorisation and verify the key/data boundary.

## Restriction and correction

Restriction under Art 18 needs an enforceable use block, not a cosmetic UI flag. Propagate it to retrieval, exports, training and downstream processors while permitting only legally allowed operations. Correction should update the authoritative source and relevant derivatives and identify previously disclosed results that cannot simply be recalled. Coordinate recipient notification under Art 19.

Track `requested`, `scoped`, `in-progress`, `blocked`, `partially-completed`, and `completed-with-described-residue` honestly. A successful deletion API response is evidence of an accepted operation, not proof that every copy has disappeared.
