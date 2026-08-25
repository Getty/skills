---
name: twitch
description: Use when working on anything Twitch or live-streaming — setting up or auditing a channel, OBS and encoder settings, growth and discovery, stream structure and overlays, chat and community features, monetization and payouts, moderation and safety, the Twitch API/EventSub and bots, or the legal duties of a streamer in Germany, Austria or Switzerland.
---

# Twitch

Working knowledge of Twitch as a platform: what exists, what changed recently, what the
numbers actually are, and what a streamer is legally required to do in DACH.

**Two things this skill exists to prevent**, because a model without it gets both wrong:

1. **Stale monetization facts.** In May–June 2026 Twitch opened subs, Bits, emotes, badges and
   Channel Points to *all* streamers and lowered the Affiliate bar. Almost every guide
   online predates that. Never answer monetization questions from memory —
   read `references/monetization.md`.
2. **US-default legal answers for German streamers.** A regular livestream is *Rundfunk* under
   German law, with a licence threshold, broadcast-grade youth-protection time slots, and ad
   labelling duties that have no US equivalent. See Jurisdiction below.

## Jurisdiction

Ask first: is the streamer, their company, or their audience in Germany, Austria or
Switzerland? If yes, read the relevant files below **before** advising on licensing,
advertising, taxes, music, data protection or minors. Do not answer from general knowledge —
these rules have no US equivalent and getting them wrong is expensive for the streamer.

| Topic | File |
|---|---|
| Broadcasting licence (MStV), legal notice / Impressum (§5 DDG, §18 MStV), GDPR on stream | `references/germany-legal.md` |
| Youth protection, age ratings, broadcast time slots (JMStV) | `references/germany-youth-protection.md` |
| Ad labelling, sponsorships, gambling (§22 MStV, UWG, GlüStV) | `references/germany-advertising-and-gambling.md` |
| Gewerbe, VAT/Kleinunternehmer, donations, W-8BEN, payouts | `references/germany-taxes-and-business.md` |
| Music rights, GEMA, GVL, DMCA | `references/germany-music-and-copyright.md` |
| Market size, scene, events, viewing habits, Du/Sie | `references/germany-market-and-culture.md` |

Austria and Switzerland differ from Germany on most of these; each file says where. None of it
is legal advice — the files state the law and the authorities' guidance, and flag where a
Steuerberater, Rechtsanwalt or Landesmedienanstalt has to be asked.

## Reference index

| Topic | File |
|---|---|
| Account, identity, metadata, roles, first stream | `references/channel-setup.md` |
| Encoder, bitrate, Enhanced Broadcasting, Dual Format, scenes, network | `references/broadcasting-and-obs.md` |
| Discovery Feed, clips, categories, tags, raids, the growth funnel | `references/discovery-and-growth.md` |
| Overlays, run of show, segments, failure drills | `references/stream-design-and-run-of-show.md` |
| Chat modes, Channel Points, Power-Ups, emotes, mods, guests | `references/community-and-chat.md` |
| Subs, Bits, Hype Trains, sponsorships, Drops, splits, payouts | `references/monetization.md` |
| AutoMod, Shield Mode, hate raids, policy strikes | `references/moderation-and-safety.md` |
| Helix, EventSub, PubSub deprecation, bots, tooling | `references/developer-and-tools.md` |
| Formats: gaming, coding, IRL, music, talk, subathons | `references/content-types.md` |
| Metrics, what they mean, the review loop | `references/analytics.md` |
| Terms | `references/glossary.md` |
| Every dated fact with its source | `references/sources.md` |

Templates: `templates/obs-scene-collection.md` · `templates/run-of-show.md` ·
`templates/stream-checklist.md`

## Core rules

- **Date every volatile fact.** Thresholds, splits, bitrates and feature availability move.
  State the verification date and the source, or say you are unsure. `references/sources.md`
  carries the dates.
- **Never invent numbers.** No made-up viewer counts, revenue figures, dates, or "typical"
  results. Use a placeholder and ask.
- **Distinguish platform policy from law.** A Twitch Content Classification Label is not a
  German youth-protection measure; Twitch's gambling policy is not the GlüStV; DMCA is not
  GEMA. Conflating them is the most common serious error.
- **Calibrate against the streamer's own data**, not published benchmarks. Twitch analytics
  from four comparable streams beat any blog's median.
- **Growth advice must name the funnel stage.** "Get more viewers" is not actionable; "your
  reach is fine and your retention is broken" is.

## Common workflows

**Auditing an existing channel**
1. Metadata: title, category, tags, CCL, schedule — `references/channel-setup.md`
2. Stream health: Twitch Inspector, bitrate, transcoding — `references/broadcasting-and-obs.md`
3. Funnel: which stage is broken — `references/discovery-and-growth.md` + `references/analytics.md`
4. Money left on the table: participation features not turned on — `references/monetization.md`
5. DACH: legal-notice, labelling, youth-protection slots — Jurisdiction files above

**Setting up a new channel**
`references/channel-setup.md` → `references/broadcasting-and-obs.md` →
`templates/obs-scene-collection.md` → `templates/stream-checklist.md` → Jurisdiction files
before the first monetized stream.

**Building a bot or integration**
`references/developer-and-tools.md` first — it lists what is deprecated. Do not start on
PubSub. If chat data leaves the machine, read the data-protection section of
`references/germany-legal.md`.
