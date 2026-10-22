# Vendor procurement

## Identify all providers

Inventory foundation-model APIs, embeddings, rerankers, moderation, speech/image services, cloud, observability, support, payments, email, analytics and customer connectors. Map billing entity, contracting entity, actual service operator and subcontractors; these can differ. For each, obtain the agreement, product-specific terms, DPA, subprocessor list, retention and training settings, location commitments and support access model.

## Establish roles and controls

Determine GDPR controller/processor roles per operation from facts. An AVV/DPA label does not override independent vendor purposes. Article 28 contractual requirements, subprocessor arrangements, transfers and international-access assessments belong with privacy/data governance; this skill owns procurement completeness and consistency. Do not activate a provider whose required contract or legal basis is unresolved. [B5]

Translate settings into enforceable controls: allowed providers/models/regions, no-training state, retention mode, failover allowlist, audit access, key ownership and incident contacts. Check background jobs and administrative tools as well as main inference. Make a rejected provider stay rejected during retry and failover.

## Evidence quality

Verify certificate issuer, scope, validity, legal entity, services, regions and exclusions. An ISO certificate for an unrelated subsidiary or a SOC report for only a data center does not prove the AI service meets every contractual requirement. Security assessments and model evaluations answer different questions. Obtain product-specific evidence rather than inferring guarantees from a marketing page.

Record what was actually verified: executed contract, current terms, documented configuration, observed test or vendor assertion. A vendor statement is evidence of an assertion, not an observed technical control. Record unavailable evidence and decide whether to require it, constrain use or select another provider.

## Subprocessor and terms changes

Track notification channels and dates. Route a new subprocessor or processing purpose to the responsible review. Honor the actual authorization/objection regime in the DPA; do not universally assume individual written approval is required for every subcontractor. Reassess downstream notice promises and termination options. Maintain a decision log if a vendor rejects requested restrictions.

## Approval package

Use an explicit scope: approved for synthetic development, approved for non-confidential production, approved for specified personal-data categories, or blocked/pending. Never make a vendor globally “GDPR approved.” Include allowed country, purpose, service version, data sensitivity, settings, residual risk owner and re-review trigger.

## Exit before adoption

Test a representative export and restoration before a provider becomes critical. Record data schema, volumes, rate limits, migration assistance, charges, timeline, encryption and deletion semantics. For a processor, confirm what happens at termination under the contract; for an in-scope Data Act service, assess statutory switching duties separately. Never leave the only copy of the contract and exit procedure inside the service being terminated.
