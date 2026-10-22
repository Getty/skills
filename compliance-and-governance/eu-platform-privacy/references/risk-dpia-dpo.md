# Risk assessment, DPIA, RoPA, and DPO

Sources: P1, P6, P8, P10, P13–P14.

## Keep four decisions separate

1. Determine the applicable obligation to keep records under Art 30.
2. Determine whether the processing is likely to result in high risk under Art 35.
3. Determine whether prior consultation is required under Art 36 after mitigation.
4. Determine whether a DPO must be designated under Art 37 and additional national law.

Small headcount does not answer all four questions. An AI Act classification is not a substitute for a GDPR DPIA, and a DPIA is not an AI Act conformity assessment.

## RoPA structure and exemptions

For controllers, record purposes, categories of subjects/data, recipients, third-country transfers and safeguards, envisaged erasure periods where possible, and a general description of security measures where possible, plus the required contacts. For processors, keep the separate Art 30(2) categories-of-processing record per controller; do not copy the controller template unchanged.

The original Art 30(5) under-250 exemption contains important exceptions for non-occasional processing, processing likely to risk rights/freedoms, and Art 9/10 data. Ongoing account/service processing is ordinarily not occasional. Proposals to change thresholds do not establish an exemption. Retrieve the operative consolidated Art 30 and any amendment before relying on a numerical threshold. Even where legally exempt, a proportionate inventory supports fulfilment of other duties; label it as an operational control.

## DPIA screening

Use actual nature, scope, context, purposes, and risks. Check Art 35(3), the competent authority's Art 35(4) mandatory list, and any applicable Art 35(5) list. The common supervisory criteria include systematic evaluation/scoring, consequential automated decisions, systematic monitoring, sensitive/highly personal data, large-scale processing, matching datasets, vulnerable subjects, innovative uses, and preventing exercise of rights or access to services.

Multiple criteria are a useful risk indicator, not a mechanical statutory test. A single serious criterion may justify a DPIA; absence from an authority's list is not automatic clearance. Document a reasoned negative screen and the change triggers that would invalidate it.

AI-platform examples requiring careful screening include large-scale prompt training, employee productivity scores, inferred health/political traits, identity matching across services, automated denial of important services, and minors' behavioural profiling. Ordinary text completion is not automatically high risk solely because it uses an LLM; the data/use context decides.

## Perform the DPIA before exposure

Describe processing and legitimate interests where relevant; assess necessity and proportionality; assess risks to people; document measures to address risks and demonstrate compliance. Consult the DPO where designated and seek affected persons' views where appropriate under Art 35(9), recording justified omissions.

Evaluate harms such as discrimination, loss of confidentiality, financial loss, reputational injury, stalking, loss of employment opportunities, manipulation and inability to exercise rights. Score severity and likelihood transparently with an explained scale. A risk score is a prioritisation device, not legal permission.

For each risk capture a threat/causal path, affected population, existing safeguards, proposed control, owner, verification evidence, residual risk and decision. Compare less intrusive alternatives: smaller datasets, scoped retrieval instead of training, local inference, no content logging, meaningful human review, or an optional feature.

If residual high risk remains without measures sufficient to mitigate it, assess Art 36 prior consultation **before** processing begins. A management acceptance signature does not replace that consultation. Reassess when risks change; keep earlier versions and reasons.

## DPO decision

Art 37 core tests cover public authorities/bodies subject to its judicial exception, core activities requiring large-scale regular/systematic monitoring, and core activities involving large-scale Art 9/10 processing. Analyse core activities and scale; buying an AI API does not resolve the test.

**German overlay:** BDSG §38 adds designation when normally at least 20 persons are constantly engaged in automated personal-data processing. It also supplies triggers independent of that number, including processing subject to a DPIA and certain business-purpose transmission/market-opinion research. Count relevant people according to the statutory test, not only IT staff or full-time-equivalent developers. Verify current law and actual employment/processing facts.

Other member states may have different additional rules. Do not reuse the German headcount test as EU law.

Where a DPO is required, verify expertise, resources, independence, access to management, early involvement, conflict-of-interest review, published contact details and authority notification under Arts 37–39. Do not appoint the person who decides purposes and means without a conflict assessment. The accountable controller remains responsible; an AI agent cannot simply be declared the DPO to satisfy designation duties.

## Evidence packet

Include scope/version, data flow, current legal text, authority list, role/basis decisions, screen or DPIA, DPO advice, decision owner, implemented controls, tests and review triggers. Keep sensitive risk detail access-restricted. Report the specific unresolved release consequence and what evidence or decision will resolve it.
