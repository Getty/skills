# Frigate, go2rtc and recording design

## Keep components distinct

| Component | Responsibility |
|---|---|
| Native HA camera/vendor integration | Device controls, events and camera entities |
| HA built-in go2rtc integration | WebRTC proxy connected to a go2rtc instance |
| Frigate server/app/container | Recording, object detection and its own media pipeline |
| Frigate HA integration | Exposes server data/entities/actions into HA |
| Dashboard camera card | Presentation and user controls |
| MQTT broker | Event/state exchange used by relevant Frigate entities |

HA [go2rtc documentation](https://www.home-assistant.io/integrations/go2rtc/) describes automatic setup with supported installs/default configuration. Do not install a second restream server merely because an old tutorial does. Frigate can have its own bundled go2rtc; identify which instance owns each stream and port.

The [Frigate HA integration](https://docs.frigate.video/integrations/home-assistant/) is separate from the Frigate server. Many entities require Frigate and HA to use the same broker. Installing the HACS integration alone does not install a recorder.

## Plan the pipeline

Start with one camera and one required output. Separate high-quality recording from lower-bandwidth detection where appropriate. Choose codecs and acceleration supported by the host; decoding and object inference are different workloads. A detector accelerator does not automatically accelerate video decode. Verify device passthrough and actual logs against [video acceleration guidance](https://docs.frigate.video/configuration/hardware_acceleration_video/).

Use the installed release's configuration schema. Set go2rtc stream names and Frigate camera mappings deliberately. [Live-view documentation](https://docs.frigate.video/configuration/live/) and [go2rtc troubleshooting](https://docs.frigate.video/troubleshooting/go2rtc/) explain mappings and app port exposure. A stream working in Frigate's UI does not prove HA uses the same named source or delivery path.

## Estimate resources transparently

For continuous recording, a useful first-order estimate is:

`storage GB/day ≈ total video bitrate in Mbit/s × 10.8`

This is decimal GB from seconds/day divided by eight; it excludes audio, overhead, variable bitrate peaks, filesystem reserve and retention policy. Measure real output before selecting disks. Event recording depends on actual activity and configured retention; do not claim a universal percentage saving.

Record CPU/GPU load, decode errors, inference latency, dropped frames and disk writes with the intended number of cameras. Include existing NVRs in the dependency map. An optional Frigate installation need not replace their recording; decide which system is authoritative for each retained artifact.

## Keep access and retention explicit

Use authentication and network boundaries for the recorder and restreamer. Do not publish go2rtc debug/API ports as a remote-view shortcut. Keep camera credentials in protected deployment configuration supported by the installed version. Verify exported clips and attachments do not expose permanent stream tokens.

Define retention by artifact type: continuous recording, events, snapshots and exported clips. A detection mask is not necessarily a privacy mask on recorded video. Confirm the actual result on an exported clip.

## Validate and recover

Test native recording continuity, Frigate recording, HA events, local/remote view and one restart. Record server config, credentials, storage location and database/media backup strategy. A HA configuration backup does not automatically include an independently hosted recorder or its video archive. Keep a functioning native camera/NVR path during rollout.
