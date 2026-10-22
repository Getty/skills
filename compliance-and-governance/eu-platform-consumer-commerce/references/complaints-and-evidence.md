# Complaints and evidence

## Consumer support as a product control

Provide an accessible route that accepts a complaint without requiring a live AI conversation. Let customers reach a human for contested charges, legal declarations, unresolved identity problems and rights requests. Classify requests by operative facts, preserving the original message: billing dispute, withdrawal, cancellation, digital-product remedy, privacy request, safety incident or accessibility issue. More than one route may apply.

Configure time limits from the relevant legal regime and contract, rather than one global “30 days” SLA. A support ticket does not reset a legal receipt time. Ensure the bot cannot falsely state that an accepted cancellation failed because a retention discount was declined.

## ADR and obsolete templates

The former EU ODR platform was discontinued on 2025-07-20 following Regulation (EU) 2024/3228. Do not reproduce an obsolete mandatory-link paragraph from old ecommerce templates. The Commission's replacement consumer-redress pages are information resources, not evidence that the old ODR obligation still exists. [C16]

Independently assess Germany's VSBG §§ 36 and 37. Section 36 covers general information about willingness or obligation to participate in consumer ADR, with a specific exemption for § 36(1) no. 1 tied to ten or fewer persons at the previous year end. It does not make every ADR information duty disappear. Section 37 addresses information after a dispute cannot be resolved. Verify any legal or contractual duty to participate and the actual competent ADR body's contact information. [C17]

## Evidence objects

Keep a contract evidence record containing offer identifier, customer class and evidence, market, accepted text versions, applicable notices, affirmative actions, formation and confirmation events, billing events, legal declarations and remedy outcome. Minimize personal content in engineering logs; link to a controlled case store rather than duplicating complaints into CI artifacts.

Keep evidence immutable enough to reconstruct events, yet subject to a documented retention/deletion policy. A legal hold requires purpose, authority, scope, owner and review date. “Could be useful in a dispute” does not justify perpetual retention of all chat content. Coordinate access rights and accounting retention with privacy and billing.

## Monitoring after release

Recommended signals include receipt delivery failure, cancellations still being billed, mismatched contract versions, excessive unmatched declarations, broken locale links, price rendering differences and repeat complaints after model updates. These are operational indicators, not proof that a law has been violated. Investigate with a reproducible sample and route findings to the accountable owner.

For a serious defect, identify all affected contract cohorts and necessary remediation. Prepare notices and refund batches for authorized review; preserve existing authority where a policy already permits execution. Do not send legal admissions, regulator communications or mass customer messages without the responsible authorization.

## Review output

State what was actually inspected: screen, route, API, document version and date. State what remains untested. Give a specific finding such as “the mobile DE withdrawal confirmation cannot be activated with keyboard focus in build X,” not “accessibility may be an issue.” End with owner, patch, evidence required and applicable deadline.
