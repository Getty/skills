# Post Formats and Limits

Hard numbers first, then what each format is actually for. Limits verified 2026-08 against
current published specs (`sources.md`); LinkedIn changes them without announcement — if a
limit matters, test it in the composer.

## Character limits

| Field | Limit |
|---|---|
| Feed post (text, image, video, document) | **3,000** characters |
| Text visible before the "…see more" fold | ~**200–210** desktop, ~**140** mobile |
| Comment | **1,250** characters |
| Profile headline | **220** characters |
| About / summary | **2,600** characters |
| Experience entry description | 2,000 characters |
| Article (LinkedIn publishing) | ~110,000 characters |
| Poll question | 140 characters · options 30 characters each |
| Connection request note | 300 characters (200 for some non-Premium surfaces) |
| InMail subject / body | 200 / 1,900 characters |

**The fold is the only limit that changes behaviour.** Everything after ~140 mobile characters
requires a click, and that click is a ranking signal. Write the first two lines as if they
were the whole post.

## Formats and what they are for

| Format | Best for | Notes |
|---|---|---|
| **Text-only** | A thesis, a story, a strong opinion | Reaches further than its reputation suggests. On accounts whose reach comes from substance rather than production value, text-only regularly beats carousels |
| **Single image** | One artefact: a screenshot, a diagram, a table, a photo of the real thing | The workhorse. A screenshot of a real terminal, dashboard or table outperforms a designed graphic surprisingly often |
| **Multi-image** | Before/after, a small series | Weaker than a single strong image |
| **Document ("carousel")** | A stepwise explainer, a checklist, a teardown | High effort. Verify it earns its cost on *your* account before making it the default |
| **Video** | Demos, face-to-camera arguments | Native upload only; add captions — most views are muted. Vertical performs better in-feed |
| **Poll** | Cheap engagement, genuine audience research | Overuse reads as farming; the results are the content, so plan the follow-up post |
| **Article** | Long-form for search and reference | Little feed distribution; use as a durable asset you link to later |
| **Newsletter** | Recurring long-form with subscriber notifications | Strong owned-audience play once you post regularly |
| **Repost with your own take** | Amplify with commentary | A bare repost carries almost no distribution — add a thesis |

## Media specs

| Asset | Spec |
|---|---|
| Single image | 1200×1200 (1:1) or 1080×1350 (4:5) — portrait occupies more feed height |
| Document/carousel | PDF, 4:5 or 1:1, **4–12 pages** is the working range; max 300 pages / 100 MB |
| Video | MP4, up to 10 minutes for good measure (limit is higher), 4:5 or 9:16; **captions mandatory in practice** |
| Link preview image | 1200×627 |
| Profile photo | 400×400 minimum |
| Profile background | 1584×396 |
| Company page logo / cover | 300×300 / 1128×191 |

## Mechanics worth knowing

- **Editing a post after publishing** is possible, but it historically dampens distribution.
  Publish clean; if a typo is not material, leave it.
- **The first comment is your own** — put links, sources and product mentions there. See
  `algorithm-and-distribution.md` for why, and for the caveat that link penalties are
  contested.
- **Line breaks**: LinkedIn collapses some empty lines depending on where you paste from. The
  Braille blank (U+2800) on an otherwise empty line survives everywhere — see
  `../templates/post-draft.md`.
- **Hashtags**: 3–5 maximum, at the end, and only ones people actually follow. Their value has
  declined; they no longer drive meaningful reach on their own.
- **Mentions** notify the mentioned party. Tagging people who do not engage is a negative
  signal, not a neutral one.
- **Scheduling** is native on desktop and mobile for posts (not articles).
- **One post per day maximum.** A second post within ~3 hours cannibalises the first.
