# Analytics

What LinkedIn reports, what it means, and which numbers should change behaviour.

## Where the numbers are

- **Post analytics** — per post: impressions, members reached, reactions, comments, reposts,
  and a demographic breakdown of who saw it (job title, company, industry, location, seniority).
- **Profile analytics** — profile views, search appearances, follower growth, and (creator
  mode) content performance over time.
- **Creator analytics** — impressions, engagement rate and top posts over 7/28/90/365 days.
- **Company page analytics** — as above plus follower demographics.
- **Official data export** — Settings → Data Privacy → Get a copy of your data. Includes
  `Shares.csv` (your posts), comments, connections, messages. **It does not include
  impressions**, which is why the archive workflow in `archive-and-analysis.md` scrapes.

## The metrics

| Metric | What it is | What it should change |
|---|---|---|
| **Impressions** | Times the post was rendered | Reach ceiling. Compare medians per format/pillar, never single posts |
| **Members reached** | Unique people | The honest reach number |
| **Engagement rate** | (reactions + comments + reposts) / impressions | Comparable across post sizes; the number to trend |
| **Comments** | | Weighted ~2× reactions by the algorithm and by usefulness to you |
| **Reposts** | | Distribution beyond your graph |
| **Demographics of viewers** | Titles, companies, industries, seniority | **The most underused number.** It tells you whether you are reaching the people you meant to |
| **Profile views** | | Conversion of post → interest |
| **Search appearances** | | Whether your headline/skills match what people search |
| **Follower growth per post** | | Which content compounds |

Dwell time and saves are ranking signals you **cannot see**. Do not promise to optimise what
you cannot measure — optimise the proxies (fold quality, first two lines, substance).

## Reading the demographics

A post with 12,000 impressions among students and job-seekers is worth less to a B2B
consultant than 900 impressions among heads of engineering at mid-size manufacturers. Check
the breakdown before celebrating or mourning a number.

## The account override

Published benchmarks describe accounts that already have reach. On a small or mid-size account
the ranking of formats can invert — carousels can be the weakest format and a plain screenshot
the strongest. The method for establishing your own ranking is in `content-strategy.md` §4:
≥10 posts per format, compare medians, write down an explicit override, re-test the loser only
when posts routinely clear a threshold.

**Reach is not capped by follower count.** A single post can reach far beyond the network via
suggested/recommended distribution — a 19,000-impression post on a mid-size account is a
normal outcome for the right content, not a fluke to explain away.

## The review loop

Per post (day 2 and day 7): impressions, engagement rate, demographic quality, follows.
Weekly: top 3 / bottom 3, and *why* — format, hook type, pillar, first sentence
(`content-strategy.md` §11).
Quarterly: cluster the archive by theme, find gaps and bridges
(`archive-and-analysis.md`).

## Traps

- **Impressions without demographics** is a vanity number.
- **One viral post is a hypothesis, not a rule.** It repeats or it does not.
- **Engagement rate rises as impressions fall** — a post shown to 200 loyal followers looks
  better by rate than one shown to 20,000 strangers. Read both numbers together.
- **Third-party analytics tools estimate.** LinkedIn's own numbers are the ones to plan with.
