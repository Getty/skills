---
name: linkedin
description: Use when working on anything LinkedIn — writing or editing a post, planning content strategy, optimising a profile or company page, understanding the algorithm and post limits, engagement and outreach, ads and lead generation, job search or recruiting, analytics and post archives, or the legal and cultural requirements for Germany, Austria and Switzerland.
---

# LinkedIn

Working knowledge of LinkedIn as a platform: the formats and their limits, how distribution
actually works, how to write something worth distributing, and what a commercial account must
do legally in DACH.

**Three things this skill exists to correct**, because a model without it gets them wrong:

1. **Advertising is the reach problem, not format.** On a personal account the dominant
   variable is whether a post reads as a story or as an ad — not whether it is a carousel.
   The same author can see ~150 impressions on a product post and ~20,000 on a
   build-in-public post. Reach is **not** capped by follower count.
2. **The popular link advice is contested.** Sources in 2026 disagree by a factor that spans
   "−60 % reach" to "+236 %". Do not assert either — default to links in the first comment and
   A/B it on the account. See `references/algorithm-and-distribution.md`.
3. **DACH duties have no US equivalent** — legal notice, ad labelling, GDPR joint
   controllership, employment law. See Jurisdiction below.

## Jurisdiction

Ask first: is the person, their company, or their audience in Germany, Austria or Switzerland?
If yes, read the relevant files below **before** writing posts, advising on profiles or company
pages, or planning outreach. Tone and legal duties both differ from the US default, and both
are visible in the output.

| Topic | File |
|---|---|
| Legal notice (Impressum), GDPR, ad labelling, employment law | `references/germany-legal.md` |
| Du/Sie, titles, gendering, register and tone | `references/germany-culture-and-language.md` |
| Member numbers, posting times, holidays, seasonality | `references/germany-market-and-timing.md` |
| XING, Kununu, media, events, institutions | `references/germany-ecosystem.md` |

Write in German for a DACH audience unless the target is explicitly international. None of
this is legal advice — the files state the law and the authorities' guidance.

## Reference index

| Topic | File |
|---|---|
| What to post at all: pillars, cadence, series, trend radar, facts base | `references/content-strategy.md` |
| Writing the individual post: hooks, structure, length, CTA, editing | `references/writing-posts.md` |
| Formats, character limits, media specs, mechanics | `references/post-formats-and-limits.md` |
| How distribution works, signals, what kills reach | `references/algorithm-and-distribution.md` |
| Profile fields, headline, About, Featured, settings | `references/profile-optimization.md` |
| Commenting, connections, DMs, groups, the weekly rhythm | `references/engagement-and-networking.md` |
| Images, diagrams, video, AI imagery, accessibility | `references/visuals-and-media.md` |
| Company pages and employee advocacy | `references/company-pages-and-advocacy.md` |
| Ads, targeting, Lead Gen Forms, budget reality | `references/ads-and-lead-gen.md` |
| Sales Navigator, outreach sequences, automation risk | `references/sales-navigator-and-outreach.md` |
| Job search and recruiting, both sides | `references/job-search-and-recruiting.md` |
| Metrics, demographics, the account override, review loop | `references/analytics.md` |
| Post archive: layout, schemas, scraping, cluster analysis | `references/archive-and-analysis.md` |
| Account risks, suppression, liability, platform data practices | `references/policies-and-risks.md` |
| Terms | `references/glossary.md` |
| Every dated fact with its source | `references/sources.md` |

Templates: `templates/post-draft.md` · `templates/post-analysis.md` · `templates/index-row.md`

## Core rules

- **Never invent specifics.** No fabricated numbers, anecdotes, quotes, dates, customers or
  claims about what someone does. Missing fact → a visible placeholder (`{{NUMBER}}`,
  `[INSERT REAL EXAMPLE]`) and a question. This is the one rule with no exceptions.
- **Deliver paste-ready post bodies** — no leading `>`, no blockquote, no commentary inside
  the text. Use a code fence or plain text.
- **Calibrate against the account, not benchmarks.** Published format rankings describe
  accounts that already have reach; on a small account they routinely invert. The method is in
  `references/content-strategy.md` §4.
- **Date every volatile fact.** Limits, algorithm behaviour and member numbers move; state the
  verification date or say you are unsure. `references/sources.md` holds the dates and flags
  what is contested.
- **One deliverable per request.** A finished post, not a teaser plus a full version.
- **Links and product mentions belong in the first comment**, the body stays domain-free
  (LinkedIn auto-links bare domains).

## Common workflows

**Writing a post**
`references/content-strategy.md` (which pillar, which angle) →
`references/writing-posts.md` (hook, structure, CTA) →
`references/post-formats-and-limits.md` (format and limits) →
the pre-publish checklist in `references/algorithm-and-distribution.md` →
`templates/post-draft.md` as the deliverable shape. DACH audience → Jurisdiction files first.

**Auditing a profile**
`references/profile-optimization.md` in its priority order; then
`references/germany-legal.md` if the profile is used commercially in DACH.

**Diagnosing "my reach dropped"**
`references/analytics.md` (is it reach or retention or audience quality?) →
`references/algorithm-and-distribution.md` (what kills distribution) →
`references/policies-and-risks.md` (is anything triggering suppression?). Compare medians over
≥10 posts, never single-post deltas.

**Planning outreach or a campaign**
`references/sales-navigator-and-outreach.md` and `references/ads-and-lead-gen.md`; read the
automation and GDPR warnings before recommending any tool.
