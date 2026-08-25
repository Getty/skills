# Broadcasting and OBS

Encoder, network and scene mechanics. Numbers verified 2026-08 against Twitch's own
announcements — see `sources.md`.

## What Twitch accepts (as of 2026-08)

| Path | Resolution | Bitrate | Codec | Who |
|---|---|---|---|---|
| Standard ingest | up to 1080p60 | ~6,000 kbps ceiling in practice | AVC (H.264) | everyone |
| Enhanced Broadcasting | up to 1440p ("2K") | up to **9 Mbps at 1440p**, **7.5 Mbps at 1080p** | HEVC for 2K, AVC below | Partners and Affiliates (rolled out 2026-06) |
| Dual Format | horizontal + vertical simultaneously | as above | via Enhanced Broadcasting | all streamers (rolled out 2026-06) |

Sources: Twitch blog, *Introducing Dual Format and 2k Streaming on Twitch*, 2026-06-17;
*TwitchCon Rotterdam 2026 keynote recap*, 2026-05-30.

**Enhanced Broadcasting** encodes several variants **on your machine** and sends them all.
That is CPU/GPU load in exchange for viewers getting real quality options. Twitch added
**server-side transcoding for Partners and many Affiliates** in 2026-06 to offset it — if
your encoder is pegged, check whether you qualify before buying hardware.

**Transcoding is not guaranteed** on the standard path for small channels: if you send
1080p60 at 6,000 kbps and a viewer has a weak connection, they may only have "source" and
buffer. This is the single most common cause of "my stream lags for viewers" on new channels.
Streaming 936p or 720p60 at 4,500 kbps often gives *more* watchable streams than 1080p60.

## Baseline encoder settings (starting point, not dogma)

```
Output mode:      Advanced
Encoder:          NVENC (HEVC/H.264) / AMF / QuickSync — hardware, not x264, on a single PC
Rate control:     CBR
Bitrate:          4,500–6,000 kbps (standard path) · up to 7,500–9,000 (Enhanced)
Keyframe interval: 2 s   ← Twitch requirement, not a preference
Preset:           Quality / P5-P6 (NVENC)
Profile:          high
B-frames:         2
Resolution:       1920×1080 or 1664×936, scaled with Lanczos
FPS:              60 for games, 30 for talk/coding (halves the bitrate problem)
Audio:            160 kbps AAC, 48 kHz
```

Verify a live stream with **Twitch Inspector** (inspector.twitch.tv): it shows dropped
frames, bitrate variance and keyframe compliance for your last broadcasts. "It looked fine to
me" is not evidence; Inspector is.

## Network

- Upload headroom: send at most ~70–75 % of your measured sustained upload. Shared household
  upload is the usual culprit behind mystery frame drops.
- Wired ethernet. Wi-Fi is the second usual culprit.
- Pick the ingest server nearest you (OBS: Auto, or Twitch's ingest test) — for DACH usually
  Frankfurt/Amsterdam.
- Dropped frames in OBS stats = network. Skipped/lagged frames = encoder/CPU. They have
  different fixes; do not tune the wrong one.

## Scenes

The proven minimal set, with per-scene mic routing so a "no mic" scene is genuinely silent:
see `../templates/obs-scene-collection.md`. Key ideas from that template:

- **Window Capture with "match title, otherwise find window of same executable"** survives
  app restarts; Game Capture only for full-screen exclusive games; Display Capture leaks
  everything on your desktop.
- **Mic as a scene source, not a global audio device** — then muting is structural, not a
  hotkey you forgot.
- One collection per content type, differing only in the captured window and background.

## Dual Format (vertical) practicalities

Dual Format gives you a second, vertical layout of the same broadcast and produces vertical
Clips/VODs automatically. It matters because **70 % of new viewers reach Twitch on mobile**
(Twitch, 2026-06). Design the vertical layout deliberately: face and the one thing that
matters, no 3-column desktop layout squeezed into 9:16.

## Multistreaming

Streaming to Twitch and elsewhere at the same time is allowed for Affiliates and Partners
under current terms (the old exclusivity for Partners was relaxed years ago) — but simulcast
rules have changed repeatedly. **Check your current Affiliate/Partner agreement** before
building a workflow on it; do not rely on a blog post, including this one.

## Recording

Record locally in addition to streaming (OBS: separate recording, MKV or fragmented MP4 —
plain MP4 is unrecoverable if OBS crashes). Split audio tracks (mix / mic / desktop) so music
can be stripped from an edit later. Twitch VOD retention depends on account type and is not a
backup strategy.
