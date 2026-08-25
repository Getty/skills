# Analytics

What Twitch reports, what it means, and which numbers deserve a decision.

## Where the numbers live

- **Creator Dashboard → Insights → Channel Analytics** — per-stream and rolling summaries.
- **Stream Summary** — per-broadcast recap, emailed and in-dashboard. Since 2026-06 it also
  surfaces a **sorted list of your best clips**, meant to be shared straight to Stories.
- **Achievements** — progress toward Affiliate/Partner and other milestones.
- **Twitch Inspector** — stream *health* (bitrate stability, dropped frames), not audience.

## The metrics, and what each is good for

| Metric | Definition | Decision it should drive |
|---|---|---|
| **Average concurrent viewers (ACCV)** | Mean viewers while live | The headline number; compare like-for-like (same category, same weekday) |
| **Peak viewers** | Max concurrent | Mostly noise on a small channel; one raid distorts it |
| **Unique viewers** | Distinct people | Reach — how many the funnel is delivering |
| **Returning viewers** | Watched a previous stream too | **The single best health metric.** Rising = the community is real |
| **Average view duration** | Time per viewer | Retention. Falling duration with rising uniques = discovery works, the stream does not |
| **Live views by source** | Where views came from | Tells you whether off-platform work is landing |
| **Follows per stream** | New follows | Conversion of the stream itself |
| **Chatters / chat messages** | Participation | A stream with viewers and no chatters has an engagement problem, not a reach problem |
| **Clips created** | By you and viewers | Leading indicator for Discovery Feed distribution |
| **Subs, gift subs, Bits, Hype Trains** | Revenue events | See `monetization.md` |
| **Ad breaks / ad revenue per hour** | Ads | Weigh against retention loss at the break |

## A review loop that actually changes behaviour

**After every stream (5 min):**
1. ACCV, unique viewers, average view duration, returning viewers, new follows.
2. One thing that worked, one that did not. Write it down.
3. Pick and publish one clip.

**Weekly (20 min):**
1. Compare this week's streams against the same weekday last month — not against your best
   day ever.
2. Which title/category/tag combinations correlate with higher unique viewers?
3. Retention: at what minute do people leave? (VOD retention view.) What happened there?
4. Off-platform: which clip/short drove channel visits?

**Monthly:**
1. Returning-viewer trend — the only number that must go up.
2. Revenue mix (subs vs Bits vs sponsorship) and its trajectory.
3. One structural experiment for next month (new slot, new format, new category), run for at
   least 4 streams before judging.

## Interpretation traps

- **Follower count is a vanity metric.** It includes everyone who ever wandered by. Returning
  viewers is the honest version.
- **A raid inflates everything.** Mark raided streams in your notes and exclude them when
  comparing.
- **Small numbers are noisy.** At 5 ACCV, one friend joining is a 20 % swing. Use medians over
  4+ streams, never single-stream deltas.
- **Twitch's numbers and third-party trackers disagree** (SullyGnome, TwitchTracker sample;
  Twitch measures). Use Twitch's for your own decisions.
