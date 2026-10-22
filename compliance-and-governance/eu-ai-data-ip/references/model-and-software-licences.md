# Model and software licences

## Inspect the exact components

List application dependencies, inference engine, tokenizer, weights, adapters, datasets, model cards, evaluation tools, icons/fonts and distribution packages. Each can have a different licence or owner. The licence of a repository's code does not necessarily cover downloaded weights or training data.

For each licence, inspect actual text/version and grants, restrictions, notices, source obligations, patent clauses, attribution, permitted users/territories, commercial hosting, redistribution, modification, downstream terms and termination. Do not label custom model terms 'open source' merely because weights are downloadable.

## Uses to distinguish

Self-hosted inference; serving a hosted API; distributing an appliance/client; shipping weights; publishing adapters; fine-tuning; continued pretraining; distilling another model's outputs; using synthetic data for training; and supplying source to a customer can require different rights. A paid enterprise API may have different terms from the public API or consumer product.

Network-copyleft and distributed-copyleft requirements depend on the actual licence and how components are combined or modified. Do not assume all SaaS avoids source obligations or that every dependency forces the entire platform open. Use a component-level decision with legal review for ambiguity.

## Supplier onboarding and changes

Capture contractual entity, product, effective terms, negotiated overrides, model/version, hosting mode, data-processing terms, safety/use restrictions and output claims. Subscribe/check for changes only within authorised workflows; preserve the terms governing historical releases.

Set an approval boundary on unreviewed licence changes, download URL substitutions and new distribution modes. A package update can change licensing as well as behaviour. Maintain licence/notice inventory with SBOM where helpful, but do not treat an SBOM as a completed licence analysis.

## Test and evidence

Inspect the actual shipped artefact for required notices, offered source and included components. Check whether container layers or model caches accidentally redistribute assets licensed only for internal use. Reconcile declared dependencies with build outputs. Use hashes for identity and provenance, not as evidence of the legal validity of a licence.

Cross-check AI Act open-source exceptions separately in `eu-ai-act`; those conditions are not identical to software licence labels. For model-provider obligations, record copyright policy and training summary where applicable without implying those documents clear the underlying rights.

Sources: the actual licences and negotiated contracts are primary for the asset; applicable UrhG software provisions §§69a ff, AI Act Article 53, and official licensor texts must be consulted per component. No vendor-specific commercial permission is assumed by this skill.
