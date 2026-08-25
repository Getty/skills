# LinkedIn Content Strategy

How to decide *what* to post, how often, and how to learn from results. For writing an
individual post see `writing-posts.md`; for the mechanics of distribution see
`algorithm-and-distribution.md`.

## 1. Strategy before posts

Work top-down, and write the answers into a small facts file the agent can reuse
(see "Facts base" below):

1. **Goal** — awareness, inbound leads, hiring, recruiter visibility, community. One primary goal.
2. **Audience** — who must read it, what they already believe, what they search for.
3. **Positioning** — the one sentence you want to be known for; the 2–3 theses you keep returning to.
4. **Pillars** — 3–5 recurring topic areas (below).
5. **Formats** — pick two you can sustain; calibrate later against data.
6. **Cadence** — realistic weekly rhythm (see §6).
7. **Loop** — a weekly review that feeds §2–§6.

## 2. Content pillars

Build around 3–5 pillars aligned with expertise and audience interest. Example for a
technical founder / engineer-consultant:

| Pillar | Share | What it looks like |
|---|---|---|
| Build-in-public / engineering story | 30% | "Look at this machine": what you built, measured, broke, fixed; screenshots of real artefacts |
| Contrarian thesis with proof | 25% | A widely repeated claim, a concrete counter-example with numbers |
| Explainers / how-to | 20% | One mechanism explained cleanly; tables and diagrams |
| Industry / product commentary | 15% | A known product or company as the hook, your analysis on top |
| Personal / career | 10% | Lessons, decisions, honest failures; keeps the account human |

Promotional posts about your own product are **not a pillar**; they are the payoff of the
story pillars (see §3).

For each pillar keep a running list: questions the audience actually asks, past posts and
their numbers, sources you can cite, follow-up angles.

## 3. Story beats advertising (the reach driver)

Observed repeatedly on personal accounts: the same author, same format, same day-of-week can
get 150 impressions for a product/audit post and 20,000 for a build-in-public post that sells
nothing. The algorithm and the readers both discount anything that reads as an ad.

- Lead with the machine, the data, the decision, the mistake. Let the product be visible
  only as the thing that produced the data.
- Product name, domain, link: **first comment**, not the body. Also no bare typed domains
  in the body (LinkedIn auto-links domain-like strings, which counts as an external link).
- Brand marks inside images are fine (pixels are not links).
- If a post's honest one-line summary is "buy/try X", rewrite it until the summary is
  "here is something true I found out".

## 4. Calibrate against your own account, not benchmarks

Published format benchmarks ("carousels get 2–3× engagement") describe accounts that
already have reach. On a small or mid-size account the ranking can invert: carousels can be
the weakest format and a single screenshot of a Markdown table the strongest.

Method:
1. Keep a per-post table: date, format, pillar, hook type, length, impressions, reactions,
   comments (the archive in `archive-and-analysis.md` does this).
2. After ≥10 posts per format, compare median impressions per format and per pillar.
3. Write an explicit **account override** section into your working notes: "on this account,
   X beats Y until Z". Re-test the losing format only when posts regularly clear a threshold
   (e.g. >1,000 impressions).
4. Treat any single viral post as a hypothesis, not a rule, until it repeats.

## 5. Reach drivers seen in the data (technical / B2B accounts)

What the top-reach posts of an archived two-year technical account had in common:

1. **A concrete number in the first sentence** (4 GB, 11,000 tokens, 42k→5k, 50%, 15 agents).
2. **A known product, company or person as the hook** (Chrome, Microsoft, AWS, a named model).
3. **First-person authenticity** — "I measured", "I was wrong", "I am not a …".
4. **A counter-intuitive thesis** the reader can argue with ("local models will never catch
   up", "TPS without error tolerance is a meaningless metric").
5. **A specific vertical** (machine tooling, hospital, telco) — the reader cannot know the
   answer, so they read.
6. **A discussion invitation at the end** — question posts get a measurable bonus.

What consistently underperformed: reposts without your own commentary; consensus posts
("AI is changing X"); meta-discourse about the discourse; abstract framework posts without a
number; anything that is recognisably an ad.

## 6. Cadence and timing

- Sustainable beats optimal: 2–5 posts/week, plus daily commenting, beats 7/week for a month
  and silence after.
- **One post per day maximum**; a second post within ~3 hours cannibalises the first. If two
  must go out the same day, space them ≥3 h.
- Weekday mornings and lunch in the audience's time zone are the usual starting point; then
  use your own data (post-level impressions by hour in the archive).
- Avoid public holidays and long weekends of the audience's country; expect a summer dip.
- Be online for the first 60–90 minutes after posting (reply to every comment; see
  `engagement-and-networking.md`).
- Scheduling: native LinkedIn scheduling exists on desktop and mobile for posts (not for
  articles); if the UI does not offer it in your region/account, post manually.

## 7. Series, clusters and bridges

- Run **recurring lines**: a thesis you attack from a new angle every few weeks. Readers
  recognise the line; each post can reference the last without repeating it.
- Every quarter, cluster the archive by theme (see the cluster-analysis template in
  `archive-and-analysis.md`): what theses you have established, which sources anchor them,
  where the gaps are (languages, verticals, formats).
- Look for **cross-cluster bridges** — a post that connects two of your lines usually
  outperforms either alone.

## 8. Re-issuing and multilingual reposting

- Posts with substance that under-performed (bad hook, wrong day, too early) are the cheapest
  content you have. After 3–6 months, re-issue: sharper stat/story hook, new image, shorter
  body, one CTA. Link the original in the first comment only if it adds proof.
- Translate your strongest posts. A German post re-issued in English (or vice versa) reaches
  a different graph; language-specific reach can differ by 10× for the same content.
- Reposting your own post ("Repost with thoughts") 3–6 months later with a new angle is
  legitimate; a bare repost is not.

## 9. Trend radar (finding angles before they are mainstream)

Sources: Google Trends (rising queries, country-filtered), Reddit (country and niche subs),
Exploding Topics, X/Bluesky trending, TikTok search suggestions, LinkedIn's own News and
Topic pages, niche Discords and newsletters.

Signals worth a post:
1. **Language shifts** — the same problem suddenly phrased differently ("burned out" →
   "overstimulated").
2. **Behaviour changes** — demand comments under other people's posts ("where is this
   from?", "link?", "does this work for me?").
3. **Community build-up** — a small niche group growing before the topic reaches LinkedIn.

Trend score before posting (0–10): ≥3 independent sources · search volume clearly rising
within 24–48 h · recognisable emotional resonance · timing (no holiday). 0–4 watch, 5–7 one
test post, 8–10 build a short series. Output format for a daily radar: exactly three picks,
each with signal strength, sources, why now, target audience, angle, hook type, risk, CTA.

Skip: exhausted trends, trends visible on only one platform, political hot takes without
substance.

## 10. Comment management as content

- Reply to every substantive comment; the reply is content and is weighted like a comment.
- Comment debates under other people's posts are post material. When you turn one into a
  post, keep the concrete example and numbers but **do not name the other party** by
  default — naming reads as piling on, especially if they partly conceded.
- Business offers that appear in comments (capacity, partnership, jobs): take to DM, do not
  negotiate publicly.
- Keep a list of open comments worth answering with draft replies; answer within the day.

## 11. Weekly review loop (20 minutes)

1. Top 3 and bottom 3 posts of the week: format, hook, pillar, first sentence — why?
2. Impressions and follower trend vs. the previous four weeks.
3. Which comment threads are still open; which could become a post.
4. Update the account-override notes (§4) and the pillar lists (§2).
5. Pick next week's 2–5 angles; draft hooks first.

## 12. Facts base (prevents invented specifics)

Keep a `profile-facts` file next to your drafts: projects with real numbers, tools, dates,
talks, roles, communities, what you actually do and do not do. Every draft pulls specifics
from it. If a needed fact is missing, the draft gets a visible placeholder
(`{{NUMBER}}`, `[INSERT REAL EXAMPLE]`) — never an invented one. This applies to numbers,
anecdotes, quotes, dates, and to claims about your own activities ("I help companies…").
