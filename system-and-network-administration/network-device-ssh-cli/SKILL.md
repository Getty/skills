---
name: network-device-ssh-cli
description: Use when a script or agent must talk to a network device CLI over SSH and plain "ssh host cmd" does not work — legacy SSH errors ("no matching host key type found", "no matching key exchange method", "their offer: ssh-rsa,ssh-dss", "diffie-hellman-group1-sha1"), devices that ignore the command argument and open a shell instead (Cisco IOS, Cisco Small Business Sx300/SB switches), in-band "User Name:/Password:" logins, "--More--"/"More:" pagers, enable mode, or when writing a pexpect/expect driver for routers, switches, MikroTik, modems. Also for pinning host keys and storing device passwords outside the repo.
---

# Driving network device CLIs over SSH

Three things break naive automation against network gear: (1) old SSH crypto that modern OpenSSH refuses, (2) devices that ignore the exec channel and want an interactive terminal, (3) pagers and prompts. The fix is one small driver per device *profile*, not per device.

## Decide the access mode

| Device family | `ssh host 'cmd'` works? | Login | Pager off | Prompt |
|---|---|---|---|---|
| MikroTik RouterOS 6/7 | **yes** — use it; add `+ct` to the user (`admin+ct@host`) | SSH auth (key or password) | not needed in exec mode | `[user@host] > ` |
| Cisco IOS 15.x (ISR 900/800/G2) | **no** (opens a shell, ignores the command) | SSH auth → `Password:` for `login local`, then optional `enable` | `terminal length 0` | `host>` / `host#` |
| Cisco Small Business Sx300/Sx500 1.x, Sx350/CBS 2.x/3.x | **no** | in-band `User Name:` + `Password:` after the SSH channel opens | `terminal datadump` | `host>` / `host#` |
| Cisco IOS-XE 17.x | mostly no | as IOS | `terminal length 0` | as IOS |
| JunOS | yes | SSH auth | `\| no-more` per command | `user@host> ` |
| Linux-based (Proxmox, OPNsense, EdgeOS shell) | yes | SSH auth | n/a | shell |
| AVM FRITZ!Box | no SSH at all | web UI / TR-064 SOAP (`fritzconnection`) | — | — |

Exec-channel devices: run `ssh -o … user@host 'command'` per command and parse stdout. Everything else: use `scripts/netcli.py` (pexpect) with the matching `--profile`.

## Quick start

```
scripts/netcli.py --profile sx300    --host 172.16.0.99 --user ops --password-file ~/router.txt "show vlan" "show lldp neighbors"
scripts/netcli.py --profile ios      --host 172.16.0.5  --user admin  --password-file ~/.secrets/rtr-b --enable "show ip interface brief" "show run | section ^ip route"
scripts/netcli.py --profile routeros --host 172.16.0.8  --user ops --password-file ~/router.txt "/ip/route/print terse" "/interface/print"
scripts/netcli.py --profile ios … --json "show version" > version.json
```
`--legacy` (default on for ios/sx300) adds the SHA-1/CBC/ssh-rsa options; `--no-legacy` for modern devices. `--prompt REGEX`, `--paging CMD`, `--timeout N` override a profile. Passwords come from `--password-file` (first line) or `NETCLI_PASSWORD_FILE`; never from argv.

## Working method

1. Probe what the device offers: `ssh -vv user@host 2>&1 | grep -E 'their offer|kex:|host key'`. The "their offer:" line names the algorithms you must enable (see references/legacy-ssh.md).
2. Pin the host key once (`ssh-keyscan -t rsa host >> ~/.ssh/known_hosts` or `StrictHostKeyChecking=accept-new`) so the driver never answers a yes/no prompt blindly on a changed key.
3. Put the per-host options into `~/.ssh/config` (`Host` stanza) so interactive use and the driver agree.
4. Run read-only `show` commands first; keep write operations (`configure terminal`, `copy run start`) as explicit separate calls with their own prompt expectations.
5. Store the driver invocation (not the password) in the host documentation; e.g. a project-local wrapper like `sw-cli.py` that sets host/user/profile.

## Common mistakes

- Passing the password on the command line or in the repo. Use a mode-600 file outside the repo and reference its path only.
- Matching the prompt with a loose regex (`[#>]`) without anchoring to a line start → output lines that end in `>` terminate the read early. The driver anchors on `\r?\n<prompt>$`.
- Forgetting the pager: the session hangs at `--More--`, the timeout fires, output is truncated. Send the paging-off command right after login.
- Treating "`% Unrecognized command`" as a driver bug — it usually means the user's privilege level (Sx300 level 1) or the IOS mode is wrong.
- Using `sshpass` + `ssh host cmd` against IOS/Sx300 and wondering why it hangs: the exec channel is ignored, the device is waiting for terminal input.
- Enabling legacy algorithms globally in `~/.ssh/config` (`Host *`) — scope them to the device hosts only.

Hosts, users and password-file paths in the examples (`172.16.0.99`, `ops`, `~/router.txt`) are illustrative; substitute your own.
