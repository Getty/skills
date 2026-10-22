# Service operations and evidence

## SLA semantics

Define each metric precisely: measured surface, region, calculation period, numerator/denominator, exclusions, planned maintenance, dependency failures, minimum request volume and clock source. A status page showing uptime is not evidence that every tenant's contractual metric was met. Distinguish availability, latency, support acknowledgement, mitigation and full recovery.

Record whether the platform promises model availability, comparable capability or merely access to a managed catalog. Model fallback can restore HTTP success while violating the promised processing region, confidentiality, latency or capability. Connect contractual policy to routing and failover tests.

## Recovery and continuity

Define RTO and RPO per service and data class. Verify backups are recoverable and that access-control/erasure state is restored alongside content. Have a clear procedure for an upstream provider shutdown, billing outage, credential compromise or accidental region change. Maintain emergency contacts outside the platform's own identity dependency.

## Incident communication

Map statutory reporting, processor-to-controller notification and contractual customer communication separately. Contracts may require faster notification than the statutory outer deadline. Record when the relevant awareness event occurred, who owns each clock and which facts are confirmed. Coordinate with cybersecurity and privacy; do not wait for complete root-cause analysis before assessing time-sensitive duties.

Prepare the exact customer notice, affected cohort, recipient authorization and evidence. Execute only through approved authority or established policy. An internal ticket must not silently be treated as customer notification.

## Customer-specific controls

Maintain a machine-readable policy derived from the approved contract: allowed regions/providers, retention classes, training permission, admin access, customer-managed keys, export rights, monitoring constraints and support entitlements. Test policy propagation across web/API requests, async tasks, retries, caches and emergency operations. Detect unrecognized tenant policy versions rather than using permissive defaults.

## Evidence register

For each promise, record clause/document version, required behavior, control ID, owner, test or observation, evidence location, last verification, limitations and next trigger. Use separate statuses for designed, implemented, tested and accepted. Keep audits scoped to relevant time and systems. Restrict customer audit exports so they do not disclose unrelated tenants or secrets.

## Renewal and termination

At renewal, compare contract changes, actual usage, incident patterns, vendor changes and evidence expiry. At termination, verify notice receipt, service continuity, access revocation sequencing, export, retained records, key destruction and deletion confirmation. Avoid deleting data before the legally or contractually required retrieval window. Finance and identity deprovisioning must not race the export workflow.
