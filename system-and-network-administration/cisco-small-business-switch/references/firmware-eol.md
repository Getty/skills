# Firmware, boot code, upgrade path, end of life

## Images and boot code

- Two firmware slots: `image-1`, `image-2`. `show bootvar` shows which is active and which boots next. Uploading a new image always goes into the *inactive* slot.
- Separate **boot code** (bootloader, `.rfb`) with its own version; newer firmware trains require a minimum boot code. Check `show version` ("Boot version").
- File names (Sx300): firmware `sx300_fw-1.4.11.5.ros` (older: `.ros` / `.bin`), boot `sx300_boot-1.3.5.06.rfb`. Sx500: `sx500_fw-…`. Sx350/550/CBS: `image_tesla_Sx250-350_Sx350X-550X_2.x.y.z.bin`, boot `boot_tesla_…`.

## Upgrade via CLI (TFTP server on the admin LAN)

```
show version ; show bootvar
copy running-config startup-config                       # save first
copy tftp://172.16.10.1/sx300_boot-13506.rfb boot          # boot code, only if "show version" reports an older Boot version than the target firmware needs
copy tftp://172.16.10.1/sx300_fw-1.4.11.5.ros image        # into the inactive slot
show bootvar                                             # new image listed as "Not active", selected for next boot
boot system image-2                                      # select if not auto-selected (check "boot system ?")
reload                                                   # Y
show version                                             # verify
```
2.x/CBS syntax: `boot system tftp://172.16.10.1/image_tesla_….bin` does upload + select in one step; `boot system image inactive` to flip back. Web UI: Administration → File Management → Firmware Operations (upgrade), same result.

## Intermediate steps on Sx300 (bricking risk)

- 1.1.x / 1.2.x → 1.3.x: first install boot code 1.3.0.56 (or the one named in the 1.3 release notes), then firmware.
- 1.3.x → 1.4.x: first boot code **1.3.5.06** (file `sx300_boot-13506.rfb`, shipped in the 1.4.0.88 zip), then firmware 1.4.0.88, then the latest 1.4.11.x. Skipping the boot code step leaves the switch at "image not compatible" or in boot loop. If `show version` already says `Boot version 1.3.5.06` (late 1.3.5.x units ship with it), the boot-code step can be skipped — the firmware steps still apply.
- Downgrade only within the same boot-code generation.
- Always via a wired admin port with a stable TFTP server; do not upgrade over Wi-Fi/VPN.

## Versions and lifecycle (Sx300 / Sx500)

| | |
|---|---|
| Last Sx300 firmware | **1.4.11.5** (2020, plus 1.4.11.x maintenance); boot code 1.3.5.06+ |
| Last Sx500 firmware | 1.4.11.x as well (same train) |
| End of sale | 2018-10 (SG300-52: 2018-11-15) |
| End of software maintenance / vulnerability fixes | ~2021 |
| End of support (hardware, last date of support) | **2023-10-31 / 2023-11-30** depending on SKU |
Cisco removed the Sx300 firmware from the public download site after EoS; images circulate on community threads (Cisco Community "Where to find SG300 firmwares", reddit r/Cisco). Verify the MD5 given in the original release notes before flashing anything from a mirror.

Successors: Sx350/SG350X (2.x, EoS 2024), CBS250/CBS350 (3.x, current), Catalyst 1200/1300 (same CLI lineage, supported). The CLI in this skill carries over almost unchanged.

## Known limitations worth remembering

- SSH algorithms are fixed on 1.x (see cli-and-access.md); no SHA-2 MAC/KEX options — the switch is a legacy SSH client target forever.
- HTTPS uses a self-signed cert with old ciphers; modern browsers need an exception.
- `show mac address-table` is privilege 15 only; read-only users cannot map MACs to ports.
- No `configure replace`/archive; keep TFTP/SCP copies of `startup-config`.
