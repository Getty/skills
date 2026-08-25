# Developer APIs, Bots and Tools

For building against Twitch. Status verified 2026-08 against `dev.twitch.tv/docs/product-lifecycle`.

## Current API surface

| Product | Status (2026-08) | Notes |
|---|---|---|
| **Twitch API (Helix)** | Active | The REST API. `https://api.twitch.tv/helix/…` |
| **EventSub** | Active | The event system. Transport-agnostic |
| **EventSub: WebSockets** | Active | `wss://eventsub.wss.twitch.tv/ws` — the right default for a single-channel bot; no public endpoint needed |
| **EventSub: Webhooks** | Active | For servers with a public HTTPS endpoint; requires signature verification |
| **EventSub: Conduits** | Active | For scale — one subscription set fanned out to multiple shards |
| **Chat (IRC)** | Active | Still supported. **Non-secure WebSocket connections were decommissioned 2025-08-15** — use TLS |
| **Extensions** | Active | Overlay/panel/component apps |
| **Twitch CLI** | Active | `twitch api`, `twitch event trigger` — mock events locally |
| **Embedding** (chat, video, clips) | Active | |
| **Drops**, **Insights & Analytics**, **Game Engine Plugins**, **Mobile Deep Links** | Active | |
| **PubSub** | **Deprecated** | Legacy. Migrate to EventSub — Twitch publishes a *Legacy PubSub to EventSub Migration Guide* |
| Twitch Developer Rig, Enhanced Experiences, API v5, WebSub webhooks | Decommissioned | Do not build on these; guides that mention them are stale |

Also decommissioned 2025: the *Get Hype Train Events* endpoint and **v1** of the Hype Train
EventSub subscription types — use the current version.

## Choosing a transport

```
Single channel, your own machine, no public URL   → EventSub over WebSocket
Server with a domain, many channels               → EventSub over Webhooks
Thousands of channels / horizontal scale          → EventSub over Conduits
Only need to read and send chat messages          → IRC (TLS) or the Chat API
```

**Do not start a new project on PubSub or on IRC-only event parsing.** Chat-adjacent events
(subs, cheers, raids, channel-point redemptions, Hype Trains, follows, moderation actions)
belong to EventSub.

## Auth

- **App access token** (client credentials) for public data.
- **User access token** (authorization code flow) for anything channel-specific; scopes are
  granular (`channel:read:subscriptions`, `moderator:manage:banned_users`, …).
- Tokens expire. Implement refresh from the start; a bot that dies at 3 a.m. because nobody
  wrote refresh handling is the classic failure.
- Run the bot under a **separate Twitch account**, moderator on your channel.

## Bots and tooling ecosystem

| Need | Common choices |
|---|---|
| Ready-made chat bot | Nightbot, StreamElements, Fossabot, Moobot |
| Alerts/overlays | StreamElements, Streamlabs, OBS browser sources |
| Own bot (libraries) | twitch4j (JVM), TwitchLib (.NET), twitchAPI (Python), tmi.js / @twurple (Node) |
| Local automation | OBS WebSocket 5.x + your own script; Advanced Scene Switcher |
| Hardware control | Stream Deck (plugins for Twitch, OBS) |
| Stream health | Twitch Inspector |

## Building a bot responsibly (DACH note)

Chat messages are **personal data**. If you pipe chat into anything that stores or processes
it — a database, an analytics tool, an LLM — you need a legal basis and you should
**pseudonymise usernames before they leave your machine**. If an AI system interacts with
viewers, EU **AI Act Art. 50** transparency duties apply (obligations phased in from
2025-08-02 for GPAI, with further steps through 2026–2027): people must be able to tell they
are talking to a machine. Say so in a panel and in chat. See `germany-legal.md`.
