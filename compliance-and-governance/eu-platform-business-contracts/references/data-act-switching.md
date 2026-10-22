# Data Act switching and exit

## Scope and source discipline

Assess Regulation (EU) 2023/2854 Articles 2 and 23–31 for the actual service: on-demand network access to a scalable and elastic pool of shareable computing resources is the key type of activity. Hosted AI software can fall within the assessment; this chapter is not confined to infrastructure providers. Establish provider, customer, service type and exportable data. Do not confuse Chapter VI cloud switching with Chapter II connected-product data access. [B6, B7]

Original-regulation baseline: general application from 2025-09-12; the general prohibition of switching charges applies from 2027-01-12. During the applicable transitional period, any permitted charges are constrained to the statutory cost basis. Verify the current consolidated instrument and amendments before contracting. The Commission's Digital Omnibus proposal is not an enacted exemption by itself. The direct EUR-Lex body was inaccessible during this package's research; official indexed extracts and Commission guidance were available. Revalidate detailed Article 25/31 conditions against the complete official text before using them as a production legal rule. [B6, B7]

## Contract and process baseline to validate

Article 25's baseline includes a maximum notice period of two months to initiate switching, a normally maximum 30-calendar-day transition, and at least 30 calendar days for retrieval after the transition. The technical-infeasibility route can permit a longer transition, up to seven months, subject to the specific notification and justification requirements; the original text requires informing the customer within 14 working days of the request. Customer extensions are a separate branch. Do not turn the exceptional route into the default service SLA.

Capture the customer's requested destination or on-premises move, authorized recipient, data/assets scope, requested timing, known continuity risks and progress. Continue the required service, assistance and security during the relevant period. Keep retrieval and final erasure separate, with confirmation of successful migration and any lawful retention obligations reconciled. The process must handle erasure on termination without switching as its own path.

## Export design

Create an export manifest covering customer inputs/outputs, files, conversation history where relevant, agent/workflow definitions, configuration, metadata, identifiers, permissions, schemas and version information. Analyze which generated or custom assets qualify. Protect other tenants and personal data; authenticate export authority. Do not automatically export platform source code, proprietary model weights or all internal telemetry. Equally, do not label every useful field a trade secret to obstruct migration.

For software/platform services, assess open-interface and machine-readable export duties under Article 30. Functional equivalence for infrastructure is not a promise that competing AI models produce identical prose. Test whether a third party can parse and use the export without proprietary UI access. Include checksums, schema documentation, time zones, attachments and retry-safe pagination. Protect export links and expire access appropriately.

## Exceptions and commercial charges

Article 31's original custom-built-service exception is limited to specified obligations; it is not a blanket exclusion for everything called “enterprise” or “bespoke.” The time-limited non-production test/evaluation exception has its own conditions. Inform prospective customers of applicable exceptions as required. Review actual product and contract facts.

Distinguish switching charges from standard service fees and legitimate early-termination penalties, then scrutinize whether a nominally different fee actually obstructs statutory switching. Do not hide egress charges in “administration,” “API unlock” or artificial export plans. Record each fee's purpose, legal assessment and effective-date logic.

## Acceptance evidence

Run an authorized rehearsal with representative scale and recipient. Record request/notice/transition/retrieval events, throughput, completeness, access restrictions, parse success, security and erasure outcome. Preserve exceptions and failures. A download button alone does not prove the switching obligation is met. Keep statutory data-subject portability and customer contractual export as independent rights workflows.
