# Content Types on Twitch

What form the stream takes, and what each form demands. Choose deliberately — the format
sets the production load, the moderation load and the discovery path.

| Type | Discovery | Production load | Moderation load | Notes |
|---|---|---|---|---|
| Gaming | Category browse; huge categories are invisible, small ones are searchable | Low | Medium | Category choice is a strategy decision, not a description |
| Software & Game Development | Small, high-intent category | Low | Low | Screen-leak risk is the real hazard (tokens, `.env`, customer data) |
| Just Chatting | Largest and most crowded category | Low | High | Needs a topic; "just chatting" without a subject is invisible |
| IRL / travel | Mobile-first, high incident risk | High | High | Legal exposure in DACH: filming people in public, see `germany-advertising-and-gambling.md` for ads and `germany-youth-protection.md` |
| Music / DJ | Rights-heavy | Medium | Medium | Read `germany-music-and-copyright.md` before the first note |
| Art / making | Strong VOD/Clip afterlife | Medium | Low | Timelapse exports well to other platforms |
| Talk show / co-stream | Guests via Stream Together / Guest Star (up to 5 guests, no third-party software) | Medium | Medium | Guests' behaviour is your compliance problem |
| Esports / watch parties | Rights-dependent | Medium | High | Co-streaming rights must be granted by the event; assume no unless stated |
| Charity | Twitch charity tooling | Medium | Medium | Donations to you are taxable in DE even when "for charity" unless routed properly — see `germany-taxes-and-business.md` |

## Coding streams specifically

- **Leak surface is the thing to solve first.** Use a separate OS user or VM for streaming;
  keep secrets out of the captured window; blur or hide terminal panes that hold tokens; use
  a scene that shows only the editor when you touch credentials.
- Narrate decisions, not keystrokes. The watchable part is *why*, not the typing.
- Long silences kill retention harder than in gaming. Have a second scene (camera + talk) for
  thinking-out-loud stretches.
- Category: "Software and Game Development" · Tags: language, framework, "Deutsch" if you
  stream in German — a German-language niche category is one of the few places a small
  channel is genuinely discoverable.

## Subathons and marathons

High revenue per hour, high risk: sleep deprivation, moderation gaps, and — in DACH —
a real chance of crossing thresholds that matter (viewer counts, taxable income).
Plan mod shifts before the first hour, not during hour 40.
