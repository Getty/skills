---
name: smart-home-video-media
description: "Use when integrating or debugging cameras, NVRs, doorbells, chimes, TVs or media players in Home Assistant — Reolink, RTSP, ONVIF, WebRTC, go2rtc, Frigate, snapshots and notifications, LG webOS, Fire TV, Android TV, Sonos, Music Assistant."
---

# Smart Home Video and Media

Separate control, events, video, recording, audio, wake and notifications. A working picture establishes only one of those paths.

## Establish identity and topology

1. Record exact model, hardware revision, firmware, HA/integration version, transport and account type.
2. Map physical camera → direct LAN or NVR channel → integration → stream/recording consumers. Identify duplicate paths and session counts.
3. Inspect each NVR independently (an RLN8-410 has several hardware revisions), the doorbell's power/transport/generation and each chime. Do not infer these from retail names.
4. For Fire TV, identify Fire OS versus Vega OS before suggesting ADB. For LG, identify webOS and network-wake behavior before promising power-on.
5. Reproduce the exact failed function with a timestamp, then apply the corresponding reference.

## Reference map

| Task | Read |
|---|---|
| Reolink families, NVR revisions, doorbell/chimes | [reolink.md](references/reolink.md) |
| Distinguish stream, codec, events and network faults | [streams-and-events.md](references/streams-and-events.md) |
| Add Frigate/go2rtc and size recording/detection | [frigate-and-go2rtc.md](references/frigate-and-go2rtc.md) |
| LG, Fire TV, Android TV and audio | [televisions-and-audio.md](references/televisions-and-audio.md) |
| Compare other camera ecosystems | [camera-market.md](references/camera-market.md) |
| Doorbell/occupancy automations and protected media | [notifications-and-control.md](references/notifications-and-control.md) |
| Dated firsthand reports | [community-evidence.md](references/community-evidence.md) |
| Refresh primary support references | [sources.md](references/sources.md) |

## Operating rules

- Prefer the native integration for device controls/events when supported. Add an NVR/analytics service only for a required capability; HACS integration, server application and dashboard card are separate components.
- Preserve native doorbell/chime operation and recording while diagnosing HA. Do not repeatedly reset cameras or delete chimes: deletion can change physical pairing.
- Match firmware to exact hardware; an NVR firmware update does not necessarily update its cameras.
- Do not assume battery cameras provide continuous streams, every Reolink is directly accessible, or every camera branded ONVIF exposes every event.
- Keep stream credentials and snapshots out of public logs/dashboards. Use authenticated media routes where supported; do not expose management or debugging ports to the internet.
- Discover action/entity names in the installed HA instance. Treat examples as adaptable patterns rather than known entity IDs.
- Verify cloud/subscription and current integration dependencies before recommending Ring/Blink/Eufy or a new retail variant.

Route network design to `smart-home-architecture`, HACS lifecycle to `home-assistant-hacs`, and rule concurrency/restore to `home-assistant-automations`.

Return a per-function capability matrix, bounded change, evidence and rollback. Research baseline: **2026-10-22**. Do not claim testing on cameras or TVs without access and observed results.
