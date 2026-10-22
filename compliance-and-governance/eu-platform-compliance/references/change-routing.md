# Change routing

## Select reviewers from behaviour

Review actual system behaviour and data destinations, not just filenames. A documentation change can alter legally relevant marketing claims or intended purpose. A dependency patch can add telemetry. A prompt change can turn document summarisation into employee ranking.

| Change | Reopen at least | Concrete evidence to collect |
| --- | --- | --- |
| Add external model fallback | Data governance, privacy, AI role, contracts | Full egress route, subprocessors, retention/training settings, transfers, customer notices |
| Enable customer-uploaded RAG | Privacy, IP, data lifecycle, security | Rights/purpose, source ACL propagation, deletion lineage, cross-tenant retrieval tests |
| Add public share links | Content/DSA, privacy, IP, youth | Default visibility, enumeration resistance, indexing, revocation, report/action path |
| Add business workspaces | B2B, privacy, security, employment | DPA roles, tenant/admin boundaries, support access, employee monitoring defaults |
| Sell consumer subscriptions | B2C, accessibility, billing, marketing | Checkout, complete price, withdrawal, cancellation, confirmation, invoices |
| Change price or renewals | B2C/B2B contracts, billing | Legal basis for change, notice, old/new terms, renewal and cancellation behaviour |
| Fine-tune or distribute a model | AI Act, IP, privacy, cyber | Provider-role analysis, model licence, data provenance, evaluations, release history |
| Ship desktop client/agent | CRA/cyber, privacy, tracking, consumer | Software supply chain, local permissions, update plan, terminal storage, telemetry |
| Connect action tools | Security, privacy, contracts, assurance | Least privilege, confirmation rules, egress, side effects, trace redaction, revocation |
| Rank applicants or employees | AI Act, privacy, employment/AGG | Intended purpose, profiling, human decision process, bias/fundamental-rights assessment |
| Offer service in another state | Jurisdiction adapter and each affected domain | Targeting, language, national law, tax, local authority allocation |
| Change logging or retention | Privacy/data governance, cyber, tax if records | Purpose-specific periods, redaction, access, backup restore and holds |

## Parallel specialist review

Give each reviewer the same profile revision, feature/commit, countries, expected output schema and unresolved facts. Assign ownership of a specific question. Avoid a separate full platform audit by each specialist. Require source identifiers and evidence locations so the integration pass can resolve conflicts.

If reviewers disagree about roles, scope or dates, preserve both reasons and identify the exact source or missing fact that resolves the disagreement. Do not average conclusions or choose the least demanding answer.

## Dependency-aware implementation

Sequence changes that depend on each other. Example: decide lawful processing and vendor allocation before enabling production egress; implement deletion identifiers before introducing vector stores; establish subscription state semantics before adding withdrawal and cancellation buttons; settle output permissions before enabling public download.

Run tests using synthetic fixtures and realistic permissions. Verify rejected and revoked states, not only the happy path. Repeat only checks affected by the change or necessary to resolve remaining risk. Read the assurance skill for explicit evidence selection and release gates.

## Report shape

Lead with the product consequence and affected release. State decisions made, controls verified, unresolved blockers, remaining followups, source versions and the next reopening event. An unaffected domain can retain prior evidence if its assumptions and implementation are still valid; record that determination instead of rerunning everything.
