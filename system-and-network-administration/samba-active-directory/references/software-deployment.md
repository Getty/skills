# Central Windows software deployment

Core wish: "be able to use software just because I install it on the server." That means two technically **different** things:

- **(1) App streaming / RemoteApp:** the app is installed **once on the server** and runs **on the server**; clients only get a window. "Install once, run on server." More convenient, more expensive in licences.
- **(2) Central distribution:** software is **defined centrally** (package/policy) and **copied to every client + installed locally**. "Define once, install everywhere." Cheaper, more robust, industry standard.

GPOs are processed by the **Windows client** — as long as the machines are domain-joined Windows machines, GPO software deployment works fully. Samba is the distribution/control point (share + GPO), the installation is done by the client.

## Option matrix

Fit: ●●● very good · ●●○ usable · ●○○ niche · ○○○ unsuitable.

| Option | Capability | Prerequisite | Cost (2026) | Fit | Samba DC? |
|---|---|---|---|---|---|
| **A1 · RDS RemoteApp** | (1) real app streaming, app on the session host, published as a window. | **Windows Server** (RDSH + RD Licensing + RD Web/Gateway) | Win Server Std ~$1,000 + **RDS CAL/user** (~€30 grey … ~$220 retail; on top) | ●●○ | **Server must be Windows**; RDS authenticates against Samba AD. |
| **A2 · AVD / Windows 365** | Cloud desktops/apps by subscription. | Azure/Entra, M365 | W365 ~$28/user/month; AVD usage-based | ○○○ | Cloud, no local DC. Poor fit for an on-prem setup. |
| **A3 · Kasm Workspaces CE** | Container desktops + individual apps in the browser (streaming), self-hosted. | Docker host | CE free, **cap 5 sessions** | ●●● Linux/browser · ●○○ Win GUI | Independent of the DC; LDAP SSO paid only. |
| **A4 · Apache Guacamole** | Clientless gateway (RDP/VNC/SSH in the browser), can display RemoteApp. | Docker + RDP/RemoteApp backend (RDS **or** xrdp `initial_program`) | free | ●●○ | Yes (protocol-agnostic). Delivers no app itself. |
| **B1 · GPO Software Installation (MSI)** | (2) assign MSI via GPO (per-machine/-user), install at boot/login. | Samba DC, clients in the domain, MSI on SYSVOL/share | free | ●○○ | Yes, but **`.msi` only**, slow, brittle. Fallback. |
| **B2 · winget (+ Configuration/DSC)** | (2) packages from the MS/own repo; `winget configure` (YAML+DSC) = whole desired states. | Win 10/11, startup script/task via GPO | **free** | ●●● | **Yes, ideal.** The GPO only delivers a script/task, winget runs locally. |
| **B3 · Chocolatey OSS + internal repo** | (2) .exe/.msi/zip/script as packages, large community repo, internal NuGet feed possible. | Win, PowerShell; opt. Nexus/ProGet | **OSS free**; C4B from $18/node/year, min. $1,800 | ●●● OSS · ●○○ C4B | **Yes** — like winget via GPO startup script. GUI costs, CLI suffices. |
| **B4 · Scoop** | Portable/user scope, no admin. | Win | free | ●●○ | Yes, more for single users/devs. |
| **B5 · PDQ Deploy & Inventory** | (2) + inventory, push deploy without GPO, large library, schedules. | Windows host for the console, admin share | **~$1,950/admin/year** (perpetual gone) | ●●○ function · ●○○ price | **Yes** — needs **no** domain, also works with Samba/without. |
| **B6 · WSUS** | Central Windows updates. | Windows Server | free | ●○○ | Yes, but **deprecated since 09/2024**. Small setups: clients straight from Windows Update. |
| **C1 · MDT + WDS** | Provisioning via PXE, reference images. | Windows Server | free (server licence) | ●○○ | **deprecated.** |
| **C2 · Autounattend.xml** | Unattended setups without a server (USB/ISO). | answer file only | free | ●●○ | Independent of the DC. Good minimal provisioning. |
| **C3 · FOG Project** | Capture/deploy via PXE (Win/Linux/Mac), free. | Linux host | **free** | ●●○ | Independent of the DC. Best free imaging option, little active development. |
| **D1 · Roaming profiles + folder redirection** | Profile + My Documents on an SMB share, follows the user. | Samba DC + file server, GPO | free | ●●○ | Yes (classic AD). Roaming is fragile. |
| **D2 · FSLogix Profile Container** | Profile as VHDX container on an SMB share, mounted at login. | SMB share (Samba works), FSLogix agent, GPO | Agent free (entitlement via eligible Win/M365) | ●●○ | **Yes** — any SMB share. Shines with RDS/VDI. |
| **D3 · Home shares** | Central user/team folders, drive mapping via GPO. | Samba file server + AD | free | ●●● | **Yes** — core benefit, simplest step, greatest everyday value. |

## Key findings

- **Only A1 (RDS) fulfils (1) literally** — and is the only option with a real Windows Server licence **+ RDS CALs**. The DC can stay Samba.
- **A Windows client OS cannot do multi-user RDP / no legitimate RemoteApp:** Win 10/11 Pro = **exactly one** active RDP session. "RDPWrap" = ToS violation, do not recommend.
- **80% case = way (2):** winget/Chocolatey via GPO startup script, **free** + fully Samba-compatible. Feels like "maintained centrally once".
- **PDQ** is functionally convenient, but ~$1,950/year is hard to justify — only when script-based distribution gets too fiddly.
- **Samba AD carries everything except the RDS server role** (GPO, winget/Choco, roaming/FSLogix, home shares, printers). FL 2016 is enough, Win 11 joins cleanly.

## Phased recommendation

Guideline: **first centralise domain + data (cheap, high value), then distribution (cheap), RemoteApp only if wanted + licence available.**

- **Phase 0 — inventory/recon:** Which Windows machines actually exist (edition/build/VM)? Which apps must be central (MSI/EXE/portable)? Do not force game servers into the domain in phase 1. Printers as a GPO candidate. Clarify the RDS licensing question.
- **Phase 1 — domain/users/data:** DC VM (see `SKILL.md`), join Windows clients (pilot laptop + RDP host), central users, **home shares (D3) + drive mapping via GPO**, ADMX Central Store, optionally folder redirection.
- **Phase 2 — software (core wish, free):** **winget (B2) and/or Chocolatey OSS (B3) via GPO startup script/task.** Central `winget configure` YAML or Choco list in SYSVOL per OU, idempotent at boot/login. Fallback GPO MSI (B1). No WSUS. PDQ only if scripts get too tedious.
- **Phase 3 — app streaming (optional):** **3-A RDS RemoteApp (A1)** only with server licence + CALs (session host VM, optionally Guacamole frontend). **3-B Kasm CE (A3)** for Linux/browser apps licence-free (≤ 5 sessions), no native Win GUI apps. Provisioning: Autounattend (C2) / FOG (C3), avoid MDT/WDS.

## Cost traps

- **RDS is the only expensive line:** Win Server Std ~$1,000 **plus** RDS CALs per user/device (on top, often overlooked).
- **PDQ** ~$1,950/year (subscription only). **Chocolatey C4B** from $18/node/year, min. $1,800 — OSS CLI free, only the GUI costs.
- **Kasm > 5 sessions**, **W365/AVD**: ongoing OpEx, mostly unnecessary.
- **Free is enough:** domain (Samba), GPO, winget, Choco OSS, FSLogix agent, home shares, Autounattend, FOG — **phases 0–2 cost €0 in software.**
