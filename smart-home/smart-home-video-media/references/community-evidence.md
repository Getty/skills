# Firsthand integration experiences

Checked **2026-10-22**. These are specific reports, not statistically representative reviews. Retain later replies and fixes when interpreting the first post.

| Record | Setup/date | Report and later outcome | Operational lesson |
|---|---|---|---|
| [HA core #90620](https://github.com/home-assistant/core/issues/90620) | 2023-03-31; doorbell PoE through RLN8-410 N3MB01, initial NVR firmware v3.2.0.218_23020151 | Motion worked while visitor/person behavior failed. Original reporter later saw visitor events after HA/NVR updates; another reporter needed doorbell firmware too. Closed completed 2023-04-04 | NVR, camera and HA versions all matter. Historical resolved issue; do not label PoE doorbells incompatible today |
| [Reolink Chime V2 volume thread](https://community.home-assistant.io/t/reolink-doorbell-chime-v2-control-volume/753197) | 2024-07-25; 2024 doorbell/V2 chime | User lacked chime controls. On Aug 8 maintainer described support in HA 2024.8.0 and subsequent ringtone action support | Verify generation and released integration. Old feature absence can become obsolete |
| [Doorbell through NVR discussion](https://community.home-assistant.io/t/reolink-wifi-doorbell-or-something-else/981213) | 2026-01-31 thread; user quotes a vendor-support response | Discussion distinguishes independent camera call behavior from NVR-mediated connection | Secondary quoted support within a firsthand thread is a lead, not a universal product contract; verify exact current topology with vendor |
| [Amazon developer community: missing ADB](https://community.amazondeveloper.com/t/no-aparece-la-opcion-de-habilitar-depuracion-adb/27812) | 2026 thread; Fire TV Stick 4K Select | User could not find ADB debugging; reply distinguishes Vega from Android Fire OS | Match OS before applying an ADB tutorial; primary vendor documentation supplies the technical conclusion |

## How to extend this ledger

For a new device, find a recent matching-model success and a matching failure if available. Record model/firmware, integration, direct versus hub topology, exact symptom and resolution. If no useful report exists, say so; do not invent community consensus. Separate maintainer-confirmed behavior from a user's suspected cause.

When a current issue is closed, inspect why. A stale or duplicate closure is not a confirmed fix. For a fix PR, check the first containing release and whether the user's installed version includes it. Preserve useful positive outcomes rather than collecting only complaints.

For an existing installation, prioritize actual NVR hardware codes, chime generations and TV operating systems. Generic brand reviews cannot settle those differences.
