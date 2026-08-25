# Sources

Everything in this skill that is a *fact about the world* rather than a judgement, with the
date it was verified. Re-verify anything older than a year before relying on it.

## Twitch — official

| Source | Used for | Verified |
|---|---|---|
| blog.twitch.tv, *Monetization for All* (2026-05-13) | Bits/subs/emotes/badges/Channel Points for all streamers; global rollout from 2026-05-13; Spendable Balance; $50 payout threshold; updated Affiliate criteria (4 h / 4 days / 3 ACCV / 25 followers) | 2026-08 |
| blog.twitch.tv, *Community First: Everything We Announced at TwitchCon Rotterdam 2026* (2026-05-30) | Dual Format; 2K rollout; bitrates 9 Mbps 1440p / 7.5 Mbps 1080p; server-side transcoding for Partners and many Affiliates; Auto Clips (50 %→85 %); clip captions; Stories clip recaps; Custom Power-Ups; Creator Badge Drops (+50 % gift-sub revenue); Community Train 2×; Mythic Train; GIPHY for T2/T3; Gift 'Em All; Creator Sponsorships 3× participation; **Bounty Board folded into Creator Sponsorships, open to Affiliates**; Gameplay Ads; Streamer-Led Promos 96 h/year, +80 % gift subs; Drops 36 M viewers / $11 M; SEPA fee removal; AutoMod smart detection; mod anniversaries; TwitchCon Berlin 22–23 May 2027 | 2026-08 |
| blog.twitch.tv, *Introducing Dual Format and 2k Streaming on Twitch* (2026-06-17) | Dual Format for all streamers, 2K for Partners/Affiliates; HEVC for 2K; 70 % of new viewers on mobile | 2026-08 |
| blog.twitch.tv, *New Ways to Turn Your Community's Participation into Earnings* (2026-05-19) | >⅓ of viewer spending via Hype Trains; Custom Power-Ups; Creator Badge Drops | 2026-08 |
| dev.twitch.tv/docs/product-lifecycle | API status table: Helix/EventSub/Conduits active; **PubSub deprecated**; IRC active but non-secure WebSocket decommissioned 2025-08-15; Hype Train v1 subscriptions and *Get Hype Train Events* decommissioned; Developer Rig / API v5 / WebSub decommissioned | 2026-08 |
| dev.twitch.tv/docs/eventsub, /docs/chat/irc-migration | EventSub transports, WebSocket endpoint, IRC→EventSub migration | 2026-08 |
| safety.twitch.tv, *Prohibiting Unsafe Slots, Roulette and Dice Gambling Sites* (2022-10-18) | Twitch's gambling policy | 2026-08 |

## Twitch — trade press and secondary (directional, not authoritative)

- Plus Program tiers (Level 1 = 60/40 at ≥100 points, Level 2 = 70/30 at ≥300 points, both
  over three consecutive months): consistently reported by influencermarketinghub (2025-09),
  streamscharts (2025-11), onestream (2026-01), kudos.tv and socialday (2026-07).
  **Twitch's own help pages and your Creator Dashboard are the authority.**
- Legacy 70/30 contract holders migrated into the Plus Program: reported 2026-02.
- "~95 % of channels average 0–5 viewers": widely cited trade estimate, not a Twitch figure.
- Soundtrack by Twitch shut down **2023-07-17** (routenote, amuse; Twitch retired the product).

## Germany/DACH — law and authorities

| Source | Used for | Verified |
|---|---|---|
| § 54 MStV; NLM *Zulassung/Zuweisung*; die-medienanstalten *Zulassung* | Licence-free below 20,000 simultaneous users averaged over six months; Unbedenklichkeitsbescheinigung; ZAK for nationwide; fines up to €500,000 | 2026-08 |
| § 5 DDG (gesetze-im-internet.de); § 18 MStV | Legal-notice (Impressum) duties, required content, "geschäftsmäßig" trigger | 2026-08 |
| **VG Köln, 2025-12-16, Az. 6 K 2650/22** (epd medien, 2025-12-16) | Licensed Twitch livestream = Rundfunk; age labels are a Telemedien route only; USK 16 content required a post-22:00 slot; not final, appeal to OVG Münster possible | 2026-08 |
| JMStV; KJM FAQ; mediendiskurs | Time slots: 16+ from 22:00, 18+ from 23:00, until 06:00 | 2026-08 |
| § 22 MStV; § 5a Abs. 4 UWG; § 6 DDG; die-medienanstalten *Leitfaden Werbekennzeichnung bei Online-Medien*; MA HSH (90-second Dauerwerbesendung rule) | Ad labelling duties and wording | 2026-08 |
| BGH 2021-09-09 (I ZR 90/20 u.a., "Influencer I–III") and BGH 2022-03 | Labelling required for consideration incl. free products; not every product mention is advertising | 2026-08 |
| GlüStV 2021, § 5 Abs. 3; OVG Sachsen-Anhalt (2024-08); WBS Legal (2024-08) | Online casino/poker/slots advertising blackout 06:00–21:00; prohibition order against a streamer; foreign residence no defence | 2026-08 |
| § 19 UStG as amended by JStG 2024; IHK München; Finanzamt NRW | Kleinunternehmer **€25,000 prior year / €100,000 current year** from 2025; current-year limit is hard and mid-year | 2026-08 |
| Gewerbesteuer allowance €24,500 (GewStG § 11) | Trade tax free allowance | 2026-08 |
| **GEMA**, *Ich möchte Musik auf einer Video-Plattform wie YouTube oder Twitch hochladen* | GEMA treats Twitch as the licence partner; **no additional GEMA licence currently needed** for GEMA-repertoire music on Twitch; negotiations ongoing; GVL/Leistungsschutz and Herstellungsrecht for commercial use remain the user's problem | 2026-08 — **most likely fact here to change** |
| EU AI Act Art. 50; GPAI obligations applying from 2025-08-02 | Disclosure duty for AI systems interacting with people | 2026-08 |
| RTR/KommAustria, *Informationen für Betreiber von Video-Abrufdiensten*; WKO | Austrian notification duty, two weeks before starting | 2026-08 |
| revDSG (CH, in force 2023-09-01); JSFVG (CH, in force 2025-01-01) | Swiss data protection and youth protection | 2026-08 |

## Practice knowledge, not published fact

The OBS scene structure, the run-of-show shape, the retention advice and the review loops come
from operating a real setup and from generalising it. They are engineering judgement, not
citable research — treat them as defaults to calibrate against your own numbers, exactly as
the analytics loop describes.
