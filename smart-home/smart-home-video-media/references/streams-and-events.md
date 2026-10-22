# Separate camera data paths

## Function matrix

| Function | Typical path | Test |
|---|---|---|
| Device configuration | Vendor HTTP/HTTPS API | Read one known setting and compare with vendor UI |
| Video | RTSP, HTTP-FLV, WebRTC/HLS via a restreamer | Inspect codec, resolution, timestamps and sustained playback |
| Motion/visitor/person | Vendor push, ONVIF event subscription, polling | Trigger a physical event and correlate logs |
| Recording | Camera/NVR disk or separate recorder | Retrieve an actual interval, including before/after the event |
| Talkback | Device-specific bidirectional audio | Verify supported codec/path and browser microphone permissions |
| Notification | Automation → phone → media URL | Test on LAN and remotely, including attachment access |

RTSP describes media delivery; ONVIF provides a different control/discovery/event interface. The [HA ONVIF integration](https://www.home-assistant.io/integrations/onvif/) supports specified functions and requires usable media profiles. A printed ONVIF logo does not guarantee every vendor analytic event or two-way audio.

## Diagnose codec and transport failures

Determine whether the source produces H.264/H.265 and which audio codec it uses. Then inspect what the actual browser/phone and delivery path can decode. A stream that works in a desktop player can still fail in the web dashboard. Test a lower-resolution compatible substream before transcoding the main stream.

Use current [Frigate camera-specific guidance](https://docs.frigate.video/configuration/camera_specific/) for exact camera generations. Its Reolink recommendations now distinguish older/newer high-resolution models and FFmpeg capability; do not copy the old universal advice that every Reolink should use HTTP-FLV.

Prefer a supported restream path to multiplying direct camera sessions. Count consumers: native HA view, dashboard tabs, NVR, Frigate, mobile app and debugging players. When a camera is stable alone but disconnects under load, vary one consumer at a time and measure. Do not simply add unlimited reconnect loops.

## Verify event direction

Observe whether the integration uses a callback, subscription or polling for the target event. Check the advertised address from the camera's network, return route, protocol and firewall. Working HA-to-camera access does not prove camera-to-HA access. Account for polling latency when setting notification expectations.

For Reolink, inspect native integration debug output and the documented local HTTP callback requirement. Preserve remote HTTPS separately. For a generic ONVIF device, verify date/time/authentication and event support; do not assume NVR channel events match direct-camera events.

## Read-only inspection commands

Use `ffprobe` against a protected local configuration or an authenticated diagnostic endpoint to inspect stream metadata. Avoid placing real credential-bearing URLs in shared command transcripts, process listings or screenshots. A temporary test account may be appropriate when the device supports its required privileges.

Capture duration, dropped frames, transport errors, audio track, resolution and FPS. Test control and events after choosing a stream, because changing protocol can fix playback without changing detection.

## Escalation record

Provide exact model/hardware/firmware, direct/NVR topology, selected stream and codec, consumer count, HA/FFmpeg/restreamer versions, timestamped errors and one reproduction. Redact credentials and images. Link the relevant primary documentation or issue without treating an anecdote about another camera as a guaranteed cause.
