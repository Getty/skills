# Control and test catalogue

These are proposed engineering tests. A specialist applicability decision supplies their legal/contractual basis and scope. Passing them is not a universal compliance claim.

| Surface | Acceptance case | Failure/adversarial case | Evidence |
| --- | --- | --- | --- |
| Tenant/RAG access | Authorised requester retrieves permitted source | Revoked user, guessed ID, shared cache, reranker or cross-project path leaks text | Synthetic identities, permissions snapshot, request/result assertions |
| Egress and fallback | Only approved vendor/region receives relevant data | Primary outage silently falls back to unreviewed provider | Controlled outage, network destinations, effective configuration |
| Consent | Optional SDK remains inactive before valid choice and after refusal | Server-side relay, retry or browser storage bypasses choice | Browser/network/storage traces with redacted data |
| Withdrawal/cancellation | Each applicable customer right completes with correct state/evidence | Cancellation mislabeled withdrawal, authentication loop or missing confirmation | End-to-end state timeline and customer-visible confirmation |
| Deletion | Primary/derived copies are handled under approved schedule | Restored backup reintroduces deleted data, vector index or attachment remains | Synthetic subject lineage, restore drill and suppression test |
| Retention | Each record class expires/holds under its own purpose | Global retention keeps raw chats for invoice duration | Schema/TTL/hold review plus expiry execution |
| AI identity | Disclosure appears clearly on first relevant interaction | Voice/widget/white-label bypass lacks required information | Journey recordings and accessible announcement observations |
| Generated content | Chosen marking/disclosure survives supported paths as designed | Export/transcoding strips required information without mitigation | Format matrix, metadata checks, limitations record |
| Human oversight | Reviewer can understand/intervene with time and authority | UI nudges rubber-stamping, critical explanation hidden, override ineffective | Scenario test and task outcome evidence |
| Agent actions | Action stays within actor's purpose and approved permissions | Prompt injection from a document causes disclosure/payment/admin mutation | Synthetic attack fixture, denied tool call, audit trace |
| Accessibility | Critical journeys work with keyboard and assistive technologies | Modal focus trap, unlabeled chat controls, inaccessible error/verification | Manual test protocol plus relevant automated findings |
| Billing | Tax/price/invoice/renewal state matches reviewed rules | B2B self-label, wrong location, rounding or refund breaks records | Synthetic invoices, calculations and reconciliation |
| Public sharing | Intentional visibility, safe revocation and report route | Public search indexing or enumeration exposes private work | Share lifecycle, unauthenticated requests and revoked-link checks |
| Logs | Necessary metadata captures incident facts | Secrets, health data or full prompts appear in debug/error tooling | Synthetic sensitive markers and log inspection |
| Legal/config drift | Material provider/policy/source changes open review | Text hash changed only by cookie banner; substantive change missed | Semantic diff and disposition history |

## Avoid implementation-mirroring tests

Testing that a `consent=true` flag is set does not show that nonessential requests were blocked. Testing that a delete endpoint returns 200 does not show that derived data was handled. Testing that a policy file contains 'GDPR' proves nothing about processing. Test observable invariants at the relevant integration boundaries.

Use meaningful negative cases and role permutations. Do not broaden every small change into a full audit; select tests according to the actual behaviour and remaining risk. Treat machine results, manual usability tests and legal interpretation as different evidence types.

Keep fixtures lawful, minimised and reproducible. Redact diagnostics before sharing. Do not access another customer's data to prove an isolation defect when a synthetic controlled reproduction is possible.
