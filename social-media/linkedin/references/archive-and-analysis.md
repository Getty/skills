# Archiving Your LinkedIn Posts and Analysing Them

LinkedIn is not your database: post analytics are only visible for a limited window, the
feed hides old posts, posts can be removed, and the official export does not include
impressions. Keep your own archive with metrics, and analyse it.

## 1. Folder layout

```
posts/
  README.md            structure, schema, lifecycle
  index.md             one table row per archived post, newest first
  _manifest.json       master tracker: id, metrics snapshot, status, dir
  drafts/              YYYY-MM-DD_slug.md  (not yet published)
  YYYY/                one folder per published post
    YYYY-MM-DD_slug/
      post.md          frontmatter + full body (live text, not the draft)
      comments.yaml    comment tree as data
      media/           01.jpg … or document.pdf for carousels
  analysis/            one analysis file per post (optional, see §6)
```

## 2. Lifecycle

```
DRAFT      posts/drafts/YYYY-MM-DD_slug.md       (date = planned/created)
POSTED     published manually on LinkedIn
SCRAPE     on "it's posted": fetch the live post — real permalink, final text, images,
           metrics, comments
ARCHIVE    posts/YYYY/YYYY-MM-DD_slug/ (date derived from the activity ID, §4),
           add manifest entry + index row, DELETE the draft (git history keeps it)
```

Rules:
- **The live post is the source of truth**, not the draft. Authors edit while posting.
- The archive slug may differ from the draft slug (thematic, kebab-case, 5–7 words, from the
  core thesis, not the first line).
- Metrics are a snapshot: store `scraped_at`. Re-scrape when the comment count changes,
  otherwise the archive drifts.
- Never hand-create folders in the year directories; they contain only scraped, published posts.

## 3. Schemas

`post.md` frontmatter:

```yaml
---
activity_id: "7486839560308596736"
urn: "urn:li:activity:7486839560308596736"
date: 2026-07-25T17:47:29Z            # derived from the ID
permalink: https://www.linkedin.com/posts/<handle>_<slug>-activity-<id>-<hash>
internal_url: https://www.linkedin.com/feed/update/urn:li:activity:<id>/
author: <name>
type: original                        # original | repost
language: de                          # ISO 639-1
reactions: 5
comments: 1
impressions: 280
media: [media/01.jpg]
source: linkedin
scraped_at: 2026-07-27
# optional: reshare_of, original_of (multilingual twins), note
---
<full body; images inline as ![](media/01.jpg)>
```

`comments.yaml`: a tree of `author, headline, is_author, time, body, replies[]`.

`_manifest.json`: `{ "profile": ..., "posts": [ { "id", "impressions", "reactions",
"comments", "status": "pending|done|skip", "dir", "note" } ] }` — `status` makes a long
scrape resumable.

Draft file format: see `templates/post-draft.md`.

## 4. Deriving the timestamp from the activity ID

LinkedIn activity IDs are 64-bit snowflakes; the top 41 bits are milliseconds since epoch:

```bash
node -e 'const id=7486839560308596736n; console.log(new Date(Number(id>>22n)).toISOString())'
python3 -c 'import datetime;print(datetime.datetime.utcfromtimestamp((7486839560308596736>>22)/1000))'
```

Use this for the archive folder date (the visible "3 wk ago" is useless).

## 5. Getting the data out

### Official export (no impressions)
Settings → Data privacy → *Get a copy of your data*. The basic export ships Profile,
Connections, Positions, Skills, Endorsements, Invitations, Events, messages and similar CSVs;
the full export adds `Shares.csv`, `Comments.csv`, `Reactions.csv` and article HTML. Good for
connections and message history; **no post metrics**.

### Logged-in browser scrape (impressions, comments, real permalink)
Use a browser-automation tool with a persistent, logged-in profile (Chrome DevTools MCP,
Playwright, a Chrome extension). Only scrape your own posts.

Useful URLs:
- `https://www.linkedin.com/feed/update/urn:li:activity:<ID>/` — single post
- `https://www.linkedin.com/in/<handle>/recent-activity/all/` — all your posts with
  impressions ("N impressions" entry point), reactions and comments per card; the activity
  ID is in each card's `data-urn`
- `…/recent-activity/shares/` — only your shares (newest first; quickest way to get the
  latest ID)

Per post: expand "…more"/"see more", load all comments and replies (click every
"load more"/"previous replies"), then read the post text container, image URLs (filter out
avatars, company logos, article thumbnails), the author, whether it is a reshare, the
comments, and the **real permalink** (search `<code>`/`<script>` blocks for the
`/posts/<handle>_…-activity-<id>-<hash>` pattern).

Pitfalls learned the hard way:
- The activity list **recycles DOM nodes**. Jumping to the page bottom skips whole days (in
  one test 18 of 32 known posts were missed). Scroll in ~700 px steps and harvest after
  each step into an accumulator object kept on `window` across script calls (`localStorage`
  and init scripts do not survive context switches). Stop when the oldest loaded post is
  older than your target window (derive its date from the ID).
- Document/carousel posts often do not render slides as `<img>`. Archive text and comments
  anyway and mark `note: carousel-media-missing`; do not invent media.
- Reshares: keep your own commentary as body; if there is none, `type: repost` with a short
  reference body.
- A post that answers "This post can't be displayed" was deleted; keep the archive entry,
  set `note: no-longer-available (<date>)`.
- Comment timestamps that only contain the connection degree ("• 1st") are not times.
- Login lost (redirect to `/login`, title without "Feed"): stop and report which IDs remain.

Rate: one post every few seconds with human-like pauses; the account is yours and the
volume is small, but automation still violates LinkedIn's User Agreement in the strict
reading — keep it to your own content and low volume.

### Analytics pages
`https://www.linkedin.com/analytics/creator/…` (post analytics, audience demographics,
top posts) — screenshot or copy periodically; they are not exported.

## 6. Post analysis (one file per post)

Template in `templates/post-analysis.md`. Sections that proved useful:

1. Original post (short summary, core thesis)
2. Topic extraction (primary / secondary / tertiary)
3. External evidence (source, date, key finding, URL) — verified, dated
4. Comparable posts by other authors (author, platform, engagement, URL)
5. Sources you can build on
6. Learnings and possible follow-up posts (why did it reach or not?)
7. Follow-up tasks (checklist)

## 7. Cluster analysis (per theme, quarterly)

For each theme you keep returning to: the theses you have established with the posts that
carry them; the external source situation (what anchors each thesis); reach by language and
format; open gaps (languages, verticals, formats); bridges to other clusters. Keep one file
per cluster plus a short index.

## 8. Top-reach overview

A single table of every post above a threshold (e.g. ≥1,000 impressions) with date, title,
impressions, reactions, comments, file — then a short "what these have in common" section
and a "what did not reach and why" section. This is the file the content strategy
(`content-strategy.md` §4–§5) is calibrated from.
