# Germany/DACH — Music and Copyright

**Not legal advice.** Verified 2026-08 against GEMA's own published guidance.

## 1. The GEMA situation on Twitch — the counter-intuitive part

Most German guides state flatly "you need a GEMA licence to stream music". **For Twitch, GEMA
itself currently says otherwise:**

> "Wie YouTube betrachten wir auch den Plattform-Betreiber Twitch als Lizenzpartner – und
> nicht die einzelne Streamerin bzw. den einzelnen Uploader. Aktuell befinden wir uns im
> Gespräch mit der Plattform. **Bisher müssen Sie also keine zusätzliche Lizenz bei der GEMA
> erwerben, wenn Sie Musik aus dem GEMA Repertoire auf Twitch nutzen.** Sollte sich daran
> etwas ändern, erfahren Sie es auf dieser Seite."

— GEMA, *Ich möchte Musik auf einer Video-Plattform wie YouTube oder Twitch hochladen*
(retrieved 2026-08). **Re-check that page before relying on this**: GEMA states negotiations
are ongoing, so this is the single most likely fact on this page to change.

## 2. What GEMA does *not* cover

GEMA administers the rights of composers, lyricists and publishers. Three other rights sit
outside it and are the ones that actually cause trouble:

- **Leistungsschutzrechte** — the performers' and the record label's rights in a specific
  *recording*. Administered by **GVL** and the labels. A GEMA arrangement never covers the
  recording.
- **Herstellungsrecht** (synchronisation) — the right to combine a work with moving images.
  For **private** use on YouTube/Twitch this is inside the platforms' licence agreements. If
  you act **commercially** — and a monetizing streamer does — GEMA states you must obtain it
  **yourself**, from the music publisher (published works) or the authors directly.
- **Twitch's own DMCA regime** — entirely independent of German law. Twitch responds to US
  rightsholder notices with muted VODs, deleted clips and strikes regardless of what GEMA
  says. Three strikes ends the channel.

**So the honest summary for a monetizing German streamer:** GEMA is currently not the problem;
the recording rights, the sync right and Twitch's DMCA enforcement are.

## 3. What is actually safe

| Source | Live | VOD/Clips | Notes |
|---|---|---|---|
| Music licensed *for streaming* (Epidemic Sound, Artlist, Streambeats, NCS with terms checked) | ✅ | ✅ | Check the licence explicitly covers **livestream + VOD + monetization** |
| Game soundtrack (in-game music) | usually ✅ | ⚠️ | Depends on the publisher; some games have a "mute this track" streamer mode |
| Radio, Spotify, Apple Music, YouTube playback | ❌ | ❌ | Personal-use licences never cover public broadcast |
| "Royalty-free" found on the internet | ⚠️ | ⚠️ | Royalty-free ≠ licence-free. Read the terms; keep a copy |
| Your own composition, all rights held | ✅ | ✅ | If you are a GEMA member, your own use may still be reportable |
| Cover versions performed live by you | ⚠️ | ⚠️ | Composition rights still apply; recording rights do not |
| **Soundtrack by Twitch** | — | — | **Shut down 2023-07-17.** Any guide recommending it is stale |

## 4. Practical setup

- Route music on a **separate audio track** in OBS (see `../templates/obs-scene-collection.md`)
  so it can be stripped from the recording and from any YouTube re-upload.
- Keep a **licence folder**: invoice, licence text, date, scope. If a claim arrives you have
  minutes, not days, to respond.
- For DJ/music streams, the whole risk model is different — get advice before the first
  stream, not after the first strike.

## 5. Other copyright traps

- **Reaction content and watching other people's videos** — no general right to rebroadcast.
  German law has no US-style fair use; §§ 51, 51a UrhG (Zitat, Karikatur/Parodie/Pastiche) are
  narrow and require engagement with the work, not just playback.
- **Emotes and overlays** commissioned from an artist: agree in writing what rights transfer.
  Under German law copyright itself cannot be assigned, only usage rights (Nutzungsrechte) —
  the contract must grant them explicitly and broadly enough (including merch, if relevant).
- **AI-generated assets**: no copyright protection for purely AI-generated output in Germany,
  so you cannot stop others reusing it; and the training-data provenance may not be clean.
- **Game content**: streaming gameplay relies on the publisher's tolerance or an explicit
  streaming permission. Most large publishers grant it; some (notably around pre-release
  embargoes and cutscenes) do not.

## 6. Austria and Switzerland

- **Austria**: AKM (composers/publishers) and LSG (performers/labels) are the counterparts;
  the platform-level logic is similar but confirm AKM's position separately — it is not
  GEMA's.
- **Switzerland**: SUISA administers the equivalent rights; SUISA has its own tariffs for
  online/streaming use and its position on platform licences is separate from GEMA's.
