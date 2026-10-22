# LG, Fire TV, Android TV and audio

## LG webOS

Record model/year, webOS version, Ethernet/Wi-Fi address, wake options and pairing state. Use the native [LG webOS TV integration](https://www.home-assistant.io/integrations/webostv/) for supported controls, sources and notifications. Discover app IDs/actions in the installed instance; visible source names and backend IDs are different.

Power-on needs a separate wake path such as supported Wake-on-LAN or HDMI-CEC. Check model-specific settings and subnet reachability. An unavailable entity while the TV is asleep can be expected; repeated integration removal will not enable a disabled network-wake feature. Test wake after ordinary standby and after actual power loss, because behavior may differ.

Design TV announcements with quiet hours, occupancy and volume/restore policy. Do not turn on a sleeping bedroom TV merely because a doorbell notification occurred. Keep normal remote operation intact.

## Amazon Fire TV: identify the OS first

The native HA [Android Debug Bridge integration](https://www.home-assistant.io/integrations/androidtv/) can control supported Android/Fire OS devices through ADB, requiring debugging and authorized access. Start with its recommended built-in client; do not add an ADB server without a concrete need. Limit network access to the management path and preserve the authorized key.

**Do not assume all Fire TV products run Android.** Amazon's [Fire TV developer overview](https://developer.amazon.com/apps-and-games/fire-tv) identifies Vega OS products; [Vega developer mode](https://developer.amazon.com/docs/vega/latest/developer-mode.html) is a separate workflow. A Fire TV Stick 4K Select cannot inherit an ADB integration claim from a Fire OS 4K Max. Identify the exact OS and supported control interface before recommending a new device or issuing commands.

The separate [Android TV Remote integration](https://www.home-assistant.io/integrations/androidtv_remote/) requires Android TV Remote Service, which Fire TV generally lacks. Do not substitute this integration merely because both device families display television apps.

ADB state inference can be app/device-specific. Check observed playback properties before automating “pause means lights on.” Prefer explicit wake/sleep or source commands over power toggles when possible. ADB shell access can do more than media control; expose only the intended actions to household automation or AI.

## Audio and player ecosystems

| Family/path | Investigate | Caveat |
|---|---|---|
| Sonos | [Native integration](https://www.home-assistant.io/integrations/sonos/) | Event/network reachability, grouped playback and supported announcement restore |
| Google Cast / Android TV | [Cast](https://www.home-assistant.io/integrations/cast/) plus appropriate remote integration | Media URL must be reachable by the player; control paths can differ |
| Apple TV | [Apple TV](https://www.home-assistant.io/integrations/apple_tv/) | Pairing, protocol and OS support; not a universal Thread-control API |
| DLNA renderers | [DLNA DMR](https://www.home-assistant.io/integrations/dlna_dmr/) | Codec and URL support per renderer |
| Receivers | Vendor integration for exact Denon/Marantz, Yamaha or other model | Zone/input/standby behavior differs by model |
| Music Assistant | [HA integration](https://www.home-assistant.io/integrations/music_assistant/) plus its server | Server, provider account and supported player transport are separate dependencies |
| Echo/Alexa devices | Current supported HA cloud/voice or community path for required function | Smart-home exposure is not the same as arbitrary Echo media playback; account/region/API changes matter |

## Test behavior residents care about

Verify power, source selection, volume limits, mute, playback state, grouped playback and restore after an announcement. Recheck after standby, network interruption and HA restart. Avoid restoring a stale saved volume over a resident's new manual choice. Record supported functions individually rather than labeling the entire TV or speaker “fully supported.”
