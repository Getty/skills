# Country and sector adapters for data governance

Use the GDPR core without pretending every country has identical retention, secrecy or contractual rules. Source each local requirement from the applicable official statute/authority and record its actual scope.

## Adapter fields

For each relevant country record the entities and establishments, applicable national law, data classes, sector, role, local source/version, retention trigger/period, access restrictions, supervisory contact, customer disclosures, legal owner and uncertainty. Resolve conflicts with documented legal analysis; choosing the longest retention in every country can violate storage limitation elsewhere.

## German starting points

Use the current German accounting/tax rules for the **particular** invoice, book, correspondence or other retained document; coordinate with the commercial/tax workflow rather than hardcoding a universal period here. Distinguish the underlying billing record from prompts, chat history and unrelated attachments. Consider pending proceedings/holds only for relevant records and with a responsible owner.

For employee content, add BDSG §26 and collective/employee-representation requirements where applicable. For professional or sector secrecy, establish whether the supplier/support/AI access is permitted and what contracts/safeguards are necessary. A GDPR processor contract is not an automatic answer to professional secrecy.

For ordinary German private-sector processing, confirm the competent authority; do not use the BfDI as a universal contact. Public-sector or regulated customers may impose additional lawful requirements through their sector rules and contracts.

## Other European markets

Verify national accounting/claims retention, employment, professional confidentiality, health/financial/public-sector restrictions and regulator guidance in each relevant member state. Do not copy German DPO/headcount/retention rules into an Austrian, French or Dutch adapter. EEA territorial treatment does not eliminate these national differences.

The UK and Switzerland require distinct local-law and transfer analysis even where a current adequacy decision facilitates an EEA export. For multinational routes, a valid EEA export mechanism does not automatically satisfy the recipient country's onward-transfer law.

## Additional regimes

Screen Data Act cloud switching/export obligations and contracts separately from GDPR portability. GDPR access/portability concerns people and specified conditions; a business customer's service-exit dataset and interoperability needs can be broader or different. Also route copyright/database rights and contractual confidentiality when data is acquired, transformed or reused.

When a local rule is unknown, retain a concrete issue with the affected class and required source. Implement shared isolation, lineage and deletion capability meanwhile. Do not silently treat the absence of an adapter as legal approval for a market launch.
