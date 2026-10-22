---
name: eu-platform-regulatory-watch
description: "Use when checking whether EU or national law affecting an AI platform has changed — a new amendment, proposal or Omnibus, regulator guidance, a standard's citation, an applicability date, changed vendor terms, refreshing a legal source register, review_sources.py."
---

# EU Platform Regulatory Watch

Maintain a versioned legal source and change-impact register for the actual platform. Read current primary sources when a decision depends on changing law. Research snapshot of the collection: 2026-10-22. A static skill cannot make itself current without retrieval and review.

## Source review workflow

1. Read the platform profile, countries, roles, features and obligation register. Limit the watch scope to applicable and plausibly triggered regimes, plus material upcoming changes.
2. Use [source-map.md](references/source-map.md) to locate official EU/national legislation, authorities, courts and standards records. Follow a proposal to its final published act before treating it as enacted.
3. Retrieve the current operative text, amendments, commencement/transitional provisions and relevant official guidance. Record issuer, URL, document identifier/version, exact provision, dates, access mode and limits.
4. Separate a textual change from a legal change, and a legal change from a platform impact. Read the substantive provision and affected cohort; do not decide from a page hash or news summary alone.
5. Match the change to existing control IDs, code/configuration, contracts, user journeys and owners. Preserve previous versions and reasoning.
6. Produce a concrete change packet with action, deadline basis, acceptance evidence and accountable owner. Update affected specialist decisions and source references together.
7. Escalate an unresolved material conflict with the exact unavailable text or question. Continue unaffected work; do not invent a newer rule or fallback to an obsolete one silently.

## Keep legal statuses distinct

Use `enacted_law`, `proposal`, `draft_guidance`, `final_guidance`, `standard`, `case_law` or `contract`. Also record whether an enacted provision is applicable now, future or transitional for the specific population. An official Commission page can describe a proposal; 'official' does not mean 'already law'.

Do not confuse publication, entry into force, application, national transposition, commencement of a specific section, phase-in, deadline, review date and a consultation closing date. Treat standards publication, harmonisation and Official Journal citation as separate events. Identify court level, procedural status and binding scope.

## Optional offline review helper

```bash
python3 scripts/review_sources.py /project/compliance/source-register.json --as-of YYYY-MM-DD --horizon-days 30
```

Python 3.10+, standard library only. The helper checks declared dates/status, duplicates, review gaps and supplied hash differences. It makes no network requests and does not discover or interpret legal changes. Exit 0 means metadata checks passed; 2 means review attention is required; 1 means invalid input. A due-soon item is a review task, not automatically a release blocker.

Start from [source-register.template.json](assets/source-register.template.json). It contains snapshot examples and intentionally needs adoption for the actual platform. Do not label its illustrative owner or review dates as assigned tasks or statutory deadlines.

## Practical refresh rules

Refresh before a material launch/market change, use of an exemption, a deadline-sensitive decision, an authority submission, or reliance on changed provider terms. Set a risk-based internal cadence for other sources. Near an application date, verify transition population and implementation status, not just the date.

The user must request or authorise an actual recurring automation. Do not install a scheduler, subscribe an email address or send updates merely because this skill describes a watch process. Use read-only research first; prepare communication for the authorised sender.

## Outputs

Return current confirmed changes, proposals/drafts to watch, no-effect decisions with reasons, unresolved verification gaps, and concrete implementation tasks. Cite primary sources and label your inference about platform impact. Avoid 'all laws checked' claims or a global compliance status.

## Reference map

- [source-map.md](references/source-map.md): primary-source routes by regime.
- [legal-status-and-time.md](references/legal-status-and-time.md): status/date taxonomy and cohorts.
- [verification-and-conflicts.md](references/verification-and-conflicts.md): retrieval limitations and source conflicts.
- [change-impact-workflow.md](references/change-impact-workflow.md): translate amendments into platform tasks.
- [snapshot-2026-10-22.md](references/snapshot-2026-10-22.md): concrete current traps and live followups.
- [monitoring-integration.md](references/monitoring-integration.md): safe operational design and helper contract.
- [change-impact.md](assets/change-impact.md): reviewable change packet.
- [country-adapter-review.md](assets/country-adapter-review.md): national implementation review.

Coordinate with `eu-platform-compliance` for scope and `eu-platform-agent-assurance` for evidence. Reopen specialist skills for substantive interpretation; this skill does not replace them.
