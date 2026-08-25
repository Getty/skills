# OBS Scene Collection Template (single-PC, one main window + camera)

A minimal scene set that has proven sufficient for game, coding and talk streams. Numeric
prefixes keep the order stable in OBS and on a Stream Deck; the names say what is visible.

## Scenes

| # | Scene | Sources (top → bottom) | Use |
|---|---|---|---|
| 1 | `1 MAIN` | `MAIN WINDOW`, `MIC` | default: content only, voice on |
| 2 | `2 MAIN + CAM` | `MAIN WINDOW`, `CAM`, `MIC` | content with face; explaining, reacting |
| 3 | `3 MAIN NO MIC` | `MAIN WINDOW` | short pause, phone call, cough — viewers keep seeing content, audio is off |
| 4 | `4 CAM` | `BACKGROUND`, `CAM`, `MIC` | talk segment, intro/outro, Q&A, "no game/code yet" |
| 5 | `5 WAITING` | `BACKGROUND`, `MUSIC` | starting soon / BRB; music loop, no mic |
| 6 | `6 ENDING` (optional) | `BACKGROUND`, `ENDING TEXT`, `MUSIC` | outro while you pick a raid target |

Add a `CHAT` browser source (chat overlay) and an `ALERTS` browser source to scenes 1, 2
and 4 if you want them on screen; keep them off scene 5.

## Source conventions

- **`MAIN WINDOW` = Window Capture with "match title, otherwise find window of same
  executable"** (OBS window-match priority). The capture survives app restarts and window
  title changes. Use Game Capture only for full-screen exclusive games; Display Capture only
  when you really want the whole desktop (leaks notifications and secrets).
- **`MIC` lives inside scenes, not as a global audio device.** Disable the global mic under
  Settings → Audio → Global Audio Devices (or leave it but mute it). Then `3 MAIN NO MIC` is
  genuinely silent and you cannot leak audio by forgetting a hotkey. One `MIC` source can be
  referenced from several scenes.
- **`CAM` and `MIC` through a noise/virtual-camera layer** (e.g. NVIDIA Broadcast, OBS
  filters: noise suppression → noise gate → compressor → limiter). Feed the virtual camera and
  virtual mic into OBS as ordinary devices.
- **`BACKGROUND`** = a static image (1920×1080) in your visual identity; used behind the
  camera and in waiting/ending scenes.
- **`MUSIC`** = a Media Source with *Loop* and *Restart playback when source becomes active*;
  licence-safe music only (see `references/moderation-and-safety.md`, music section).
- Name sources by what they are and where they come from (`CAM - NVIDIA Broadcast`,
  `MIC - Wave XLR`), so a look at the mixer explains itself.

## Audio mixer checklist

- Desktop audio and mic on separate tracks; game/desktop lower than voice (voice peaks
  around −6 dB, desktop around −18 dB as a starting point).
- Monitor the mic once through headphones at stream start (mute/unmute sanity).
- Recording track split (Track 1 = mix, Track 2 = mic, Track 3 = desktop) so VOD edits can
  remove music later.

## Hotkeys (suggested)

| Action | Key |
|---|---|
| Switch to `1 MAIN` | F13 / Stream Deck 1 |
| Switch to `2 MAIN + CAM` | F14 / 2 |
| Switch to `3 MAIN NO MIC` | F15 / 3 |
| Switch to `4 CAM` | F16 / 4 |
| Switch to `5 WAITING` | F17 / 5 |
| Push-to-mute mic (safety) | Pause |
| Start/stop stream | Ctrl+Shift+F12 (not near anything else) |

## Per-content variants

Keep one collection per content type (`Game X`, `Coding`, `Talk`) that differ only in
`MAIN WINDOW` and `BACKGROUND`; everything else is identical so muscle memory carries over.
Export collections (Scene Collection → Export) into version control next to your stream
notes; the JSON is diffable.

## Before going live (30 seconds)

1. Scene `5 WAITING` active, music audible in monitor.
2. `MAIN WINDOW` still matched (not black) — check in `1 MAIN` preview.
3. Mic meter moves when you speak; desktop meter moves with game/app audio.
4. Title, category and tags set for today; no secrets on the captured window.
5. Start stream → wait for "Live" → 2–5 minutes waiting scene → switch to `4 CAM` or `1 MAIN`.
