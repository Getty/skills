# Layered rights and provenance

## The record follows the operation

An asset can simultaneously contain copyright works, database material, third-party personal data and a customer's confidential information. Buying a subscription may grant access without permitting bulk extraction, redistribution, model training or use by another legal entity. A customer's permission reaches only the rights that customer can grant.

For each operation record: actor; asset; jurisdiction; access mechanism; licence/exception; permitted purpose; recipient; duration; attribution/notice duties; redistribution/sub-licensing limits; revocation/update rule; and uncertainty. Record licence text/version and acquisition context, preferably using a reference/hash rather than unnecessarily duplicating full proprietary material.

## Source categories

| Source | Evidence needed | Frequent mistake |
| --- | --- | --- |
| Customer upload | Contractual rights, actual intended use, source ACLs and privacy purpose | Assuming an uploader can authorise global model training |
| Licensed knowledge base | Contract/product/version, allowed extraction/reuse and user population | Treating paid access as a blanket corpus licence |
| Public website | Lawful access, relevant terms, rights reservations and specific operation | Equating accessible with public domain |
| Government material | Actual public-domain/reuse status and third-party inclusions | Assuming every government webpage/image is unrestricted |
| Open dataset | Dataset and component licences, provenance and personal-data assessment | Trusting a repository-level licence for every item |
| Model weights | Exact model licence, upstream lineage and restrictions | Using the code licence as the weights licence |
| Generated content | Inputs, human contributions, vendor terms and third-party risk | Promising exclusive copyright in every output |

## Track lineage

Assign stable IDs to source asset, collection job, transformed text, chunks, embeddings, index version, training/evaluation datasets, model version and exported output where appropriate. The necessary granularity depends on purpose and risk. Do not turn provenance into unlimited surveillance of every customer interaction.

Preserve a way to find affected downstream assets if rights change or a complaint proves valid. For training, record which dataset snapshot affected which model. Do not pretend simple record deletion equals machine unlearning; choose tested retraining, exclusion, distribution restriction or other justified remedies with an accountable owner.

## Release decision

Select `permitted_for_defined_use`, `permitted_with_conditions`, `unknown`, `restricted` or `rejected`. State precisely which operation the decision covers. Reopen for new use, new recipient, new model, publication, jurisdiction, licence change or credible claim.

Primary anchors: DSM Directive 2019/790, Database Directive 96/9/EC, German UrhG and GeschGehG. Privacy, secrecy, contract and IP analysis remain separate and cumulative where relevant.
