# Channel Setup

Everything that exists before the first frame goes out. Verified 2026-08; monetization
program details move fastest — re-check `monetization.md` sources before quoting numbers.

## Account and security

- **2FA is mandatory for monetization.** Twitch requires two-factor authentication before a
  channel can enable subs/Bits payouts. Set it up on day one, not on payout day.
- Use a dedicated email for the channel; recovery of a hijacked streaming account is slow.
- A **separate Twitch account for your bot** (if you run one) keeps the bot's OAuth scopes
  away from your main account. See `developer-and-tools.md`.

## Channel identity

| Element | Where | Notes |
|---|---|---|
| Username | Settings → Profile | Cannot be changed often (60-day cooldown); pick the name you will use everywhere else |
| Display name | Settings → Profile | Capitalisation only — same string as username |
| Profile picture | Settings → Profile | Readable at 30 px; it appears in the sidebar at thumbnail size |
| Profile banner | Settings → Profile | 1200×480; safe area centred — mobile crops the edges |
| Offline banner (video player) | Settings → Channel | 1920×1080; what non-followers see most often |
| Panels | Channel page → Edit Panels | Markdown-ish; each panel = image + link + text |
| Channel trailer | Settings → Channel | Plays for non-followers; 30–60 s beats 3 minutes |

**Panels worth having:** who you are (2 sentences) · schedule · specs/setup · rules ·
socials · support/donations · sponsors/affiliate disclosures (see
`germany-advertising-and-gambling.md` if you are in DACH).

## Stream metadata (set before every stream)

- **Title** — the single strongest discovery lever you control on-platform. Front-load the
  specific thing ("Rewriting the parser in Rust — day 3"), not the mood ("chill vibes").
- **Category** — must match what is actually on screen; a wrong category is a policy issue,
  and category browse is a real discovery path in small categories.
- **Tags** — up to 10 free-form tags (25 characters each). They feed search and browse
  filters. Include language, format and niche ("Deutsch", "Programmierung", "Rust").
- **Content Classification Labels (CCL)** — self-applied labels for mature content (violence,
  sexual themes, gambling, drugs/alcohol, profanity). Set them honestly: they are Twitch's
  own tool, and in DACH they do **not** replace legal youth-protection duties
  (see `germany-youth-protection.md`).
- **Language** — set the broadcast language; it drives which browse surfaces you appear in.

## Schedule

Publish a schedule in the Creator Dashboard (Stream Schedule). It surfaces on your channel
page, triggers follower notifications, and lets viewers see "next stream in …" when offline.
A schedule you keep beats a schedule that is ambitious — see `discovery-and-growth.md`.

## Roles and permissions

| Role | Grants | Give to |
|---|---|---|
| Editor | Dashboard access, can edit stream info, run ads, access some analytics | People you trust with the business |
| Moderator | Chat moderation, Shield Mode, timeouts/bans | Community members, see `moderation-and-safety.md` |
| VIP | Bypasses slow/followers/sub-only chat modes, VIP badge | Regulars you want to reward, not moderate |
| Artist | Can upload emotes | Your emote artist |

Editors and moderators are separate — a moderator cannot change your title, an editor is not
automatically a mod. Review the list quarterly; remove people who left.

## Before the first public stream

1. Do a **private test broadcast** (start streaming with an unlisted title) and watch the VOD
   for audio balance, black frames, readability at 480p.
2. Check what the capture actually shows: notifications, tabs, tokens, `.env` files, email
   preview. See the pre-flight list in `../templates/stream-checklist.md`.
3. Confirm the **VOD/Clips settings**: store past broadcasts on/off, clips allowed on/off.
4. Set chat defaults (see `community-and-chat.md`): follower-only chat is the single most
   effective anti-spam default for a new channel.
