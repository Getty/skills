# Moderation and Safety

Twitch's tools, plus the operating practices that make them work. In DACH, none of this
replaces the legal duties in `germany-youth-protection.md` and
`germany-legal.md` — Twitch's tools are the platform's rules, not the law.

## The tools

| Tool | What it does | Set up |
|---|---|---|
| **AutoMod** | Holds messages for review by category (discrimination, sexual content, hostility, profanity) at levels 0–4. Since 2026 it uses **smart detection** — a context-aware model that improves as moderators act; no configuration needed on your side (Twitch, 2026-05-30) | Creator Dashboard → Moderation |
| **Blocked terms** | Exact/phrase blocklist, supports wildcards | Same place; add slurs in *your* language, AutoMod is not equally strong in all of them |
| **Shield Mode** | One click applies an aggressive preset (followers-only with age limits, no links, AutoMod max, etc.) | Configure the preset *before* you need it |
| **Ban Evasion Detection** | Flags likely alt accounts of banned users; can hold or restrict their messages | Enable at "likely evader" for a growing channel |
| **Suspicious User Controls** | Monitor/restrict users flagged manually or automatically | Use "restrict" rather than ban for ambiguous cases |
| **Warnings** | Formal warning a user must acknowledge before chatting again | Better than a silent timeout for first offences |
| **Mod View** | Single-pane moderation UI with logs, actions, AutoMod queue | Have mods use this, not the normal chat |
| **Unban requests** | Structured appeals instead of DMs | Turn on; it keeps appeals out of your inbox |
| **Followers-only chat** | See `community-and-chat.md` | The best single default |

## Hate raids and coordinated attacks

Have this ready *before* it happens, because it happens fast:

1. **Shield Mode preset** configured and bound to a hotkey / Stream Deck button.
2. Mods briefed: enable Shield Mode first, ask questions later. No mod should hesitate.
3. Emote-only or sub-only as the second step.
4. **Do not read the attack out loud.** Do not engage. Do not screenshot it to social media
   while live.
5. Afterwards: report the accounts, keep the logs, and check Ban Evasion settings.

## Your own compliance surface

Things that get channels struck, in rough order of frequency:

- **Music.** Recorded music in the stream or VOD → DMCA strikes and muted VODs. See
  `germany-music-and-copyright.md`; the short version is that "royalty-free" and
  "I bought the song" are not licences to broadcast.
- **Miscategorisation** — streaming content that does not match the category.
- **Mature content without Content Classification Labels.**
- **Showing someone else's content** (movies, full VODs, react content) without rights.
- **Gambling** — Twitch prohibits streaming certain unlicensed slots/roulette/dice sites
  (policy since 2022-10). In Germany there is a *separate and stricter* legal layer, see
  `germany-advertising-and-gambling.md`.
- **Leaked personal data** — yours (screen capture) or a viewer's (reading out a name,
  address, order confirmation on stream).

## The three-strike reality

Twitch enforcement escalates: warning → timed suspension → indefinite suspension. Appeals
exist but are slow. **The channel is not an asset you own** — export your VOD archive, keep
your community reachable somewhere you control (Discord, newsletter), and never let Twitch be
the single point of failure for a business.

## Moderating in a language you do not speak

If your chat is multilingual, you need mods in each language. AutoMod's coverage and your
blocked-terms list are only as good as the language they were written for.
