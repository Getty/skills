# ISR 900 series (C921-4P, C921J, C926-4P, C927-4P/4PM, C931-4P)

## Hardware / ports

| Model | WAN | LAN switch ports | Notes |
|---|---|---|---|
| C921-4P | Gi4 + Gi5 (RJ45, routed) | Gi0–Gi3 (L2 switch, IP via SVI `interface VlanN`) | 4-port switch, no PoE on C921; C921J = Japan SKU |
| C926-4P | Gi4 (RJ45) + VDSL2/ADSL2+ over ISDN (Annex B/J) | Gi0–Gi3 | DSL Annex B |
| C927-4P / 4PM | Gi4 (RJ45 or SFP) + VDSL2/ADSL2+ over POTS (Annex A/M) | Gi0–Gi3 | |
| C931-4P | Gi4 + Gi5 (RJ45, one SFP-capable) | Gi0–Gi3 | more crypto throughput |

- WAN ports are full-duplex only; switch ports auto/half/full. `usbflash0:` for images/configs; console RJ45 (9600 8N1) and mini-USB.
- Crypto: onboard VPN engine, packet/bit-rate policed per SKU (`show crypto engine accelerator statistic`, "Max Bandwidth"). C921 ≈ 150 Mbps IPsec, C931 ≈ 250 Mbps.
- IOS: 15.8(3)M ("c900-universalk9-mz.SPA.158-3.Mx.bin"), last release train **15.9(3)M**; `-npe` images = no payload encryption.
- `memory-size iomem 5|10|15|20|25` reallocates DRAM for packet buffers (needs reload).

## Lifecycle (Cisco EoL bulletin EOL15644, 2025-07-28)

| Milestone | Date |
|---|---|
| End of sale (hardware + licenses) | 2026-07-28 |
| End of software maintenance releases | 2027-07-28 |
| End of vulnerability/security support | 2029-07-27 |
| Last date of support | 2031-07-31 |
Replacement: ISR 1100 (C1121-4P, C1116/C1117 for DSL) or Catalyst 8100 — those run IOS-XE. Sx300-era gear is already out of support; plan the ISR 900 similarly.

## Licensing (Right-to-Use, honor system)

```
show license                 # per feature: Permanent | EvalRightToUse | RightToUse, "Active, In Use"
show license feature         # which packages the image supports (ipbasek9, securityk9, appxk9)
show license all / detail    # evaluation period left, EULA state
show license udi             # PID + SN needed for PAK/portal
```
- ISR 900 ships with `ipbasek9` permanent; `securityk9` (ZBFW, IPsec/VPN, IPS) is usually an **evaluation RTU** license: not active until enabled.
- Activate:
```
configure terminal
license accept end user agreement          # one-time global EULA acceptance (optional, avoids prompts)
license boot module c900 technology-package securityk9
end
write memory
reload                                     # required; features are unavailable until then
show license | begin securityk9            # expect "Active, In Use"
```
The 60-day evaluation turns into a lifetime RTU automatically ("EvalRightToUse" → "RightToUse"); legally you still need to buy `SL-900-SEC`. Disable again with `license boot module c900 technology-package securityk9 disable` + reload. Permanent PAK licenses: `license install flash:<file>.lic` (no reload if the eval was already active).

## What needs securityk9

Zone-based firewall (`zone security`, `policy-map type inspect`), classic CBAC (`ip inspect`), IPsec/IKEv2/DMVPN/FlexVPN, SSL VPN, IOS IPS, Easy VPN. **ACLs, reflexive ACLs, NAT, DHCP, routing, SSH, NTP, QoS** work with `ipbasek9` alone.

## ROMMON and recovery pointers

`Ctrl-C` within 60 s of boot enters ROMMON; `confreg`, `boot flash:`, `tftpdnld`, `dir usbflash0:`, `reset`. ROMMON upgrade: `upgrade rom-monitor file flash:c900-CapsuleUpdateFile…` (see references/cli-and-access.md for the IOS-side upgrade flow).
