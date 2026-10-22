# Legacy SSH algorithms: what breaks when, and how to enable it per host

## OpenSSH client defaults that removed old crypto

| OpenSSH | Change | Symptom against old gear |
|---|---|---|
| 6.7 (2014) | CBC ciphers, `hmac-md5`, `hmac-sha1-96` removed from defaults | `no matching cipher found` / `no matching MAC found` |
| 7.0 (2015) | `ssh-dss` host/user keys off, `diffie-hellman-group1-sha1` off, RSA < 1024 refused | `no matching host key type found. Their offer: ssh-dss` / `no matching key exchange method found. Their offer: diffie-hellman-group1-sha1` |
| 8.2 (2020) | `ssh-rsa` deprecation announced | warnings only |
| 8.8 (2021) | `ssh-rsa` (RSA/SHA-1 signatures) disabled for host and user auth | `no matching host key type found. Their offer: ssh-rsa` |
| 9.x | `RequiredRSASize` (default 1024); SHA-1 KEX still available but opt-in | small RSA host keys refused; regenerate on the device |
| 10.x (2025) | DSA removed entirely | `ssh-dss` devices need an older client or a serial console |

Check what your client still has: `ssh -Q kex`, `ssh -Q cipher`, `ssh -Q mac`, `ssh -Q key`, `ssh -V`.

## Per-host enablement (prefer `~/.ssh/config`)

```
Host sw1 172.16.0.99
    User ops
    KexAlgorithms +diffie-hellman-group-exchange-sha1,diffie-hellman-group1-sha1,diffie-hellman-group14-sha1
    HostKeyAlgorithms +ssh-rsa,ssh-dss
    PubkeyAcceptedAlgorithms +ssh-rsa
    Ciphers +aes128-cbc,aes256-cbc,3des-cbc
    MACs +hmac-sha1
    PubkeyAuthentication no
    PreferredAuthentications password,keyboard-interactive
    StrictHostKeyChecking accept-new

Host rtr-b 172.16.0.5
    User admin
    KexAlgorithms +diffie-hellman-group-exchange-sha1,diffie-hellman-group14-sha1
    HostKeyAlgorithms +ssh-rsa
    PubkeyAcceptedAlgorithms +ssh-rsa
    Ciphers +aes128-cbc,aes256-cbc,3des-cbc
    MACs +hmac-sha1
```
`+` appends to the defaults (keeps modern algorithms first); `=`/no prefix replaces the list. Older clients spell `PubkeyAcceptedAlgorithms` as `PubkeyAcceptedKeyTypes`. On the command line: `-o KexAlgorithms=+… -o HostKeyAlgorithms=+ssh-rsa …`.

## Diagnosing

```
ssh -vv user@host 2>&1 | grep -E 'their offer|kex: (algorithm|host key|server->client|client->server)|Authentications that can continue'
ssh-keyscan -t rsa,ssh-dss 172.16.0.99          # prints host keys; append to known_hosts to pin
```
- "their offer:" lists exactly what to add.
- `Permission denied (publickey,keyboard-interactive)` on Cisco SB: the SSH-level auth succeeded or was skipped — the real login is the in-band prompt that follows; use a driver.
- Connection accepted then immediately closed with no prompt: the device's VTY `access-class`/management ACL denies your source IP, or the SSH server needs an RSA key (`crypto key generate rsa`).
- Host key changed after a firmware upgrade or factory reset: remove the old line (`ssh-keygen -R 172.16.0.99`), re-pin.

## Server-side options when you control the device

- Cisco IOS ≥ 15.5(2): `ip ssh server algorithm kex diffie-hellman-group14-sha1` (or `ecdh-sha2-nistp256`), `… encryption aes256-ctr`, `… mac hmac-sha2-256`; regenerate a 2048/4096-bit key (`crypto key generate rsa modulus 2048`). Host key type remains `ssh-rsa` unless the release supports `ip ssh server algorithm hostkey rsa-sha2-256`.
- Cisco Small Business 1.x: nothing configurable beyond on/off and key generation — permanently legacy.
- MikroTik: `/ip/ssh/set strong-crypto=yes` enables modern KEX/ciphers and host key types; import ed25519/rsa user keys with `/user/ssh-keys/import`.
- HP/Aruba, Ubiquiti EdgeOS, older Juniper: similar per-platform knobs; the client-side workaround is identical.

## When the client cannot be persuaded

Keep an older OpenSSH around for that one device: a Debian 12 container (OpenSSH 9.2, still has SHA-1 KEX and ssh-dss), `nix shell nixpkgs#openssh_hpn`, or Python `paramiko` with `disabled_algorithms` tuned (paramiko keeps ssh-dss and group1 available). Last resort: serial console (`screen /dev/ttyUSB0 9600` for IOS, `115200` for Sx300) or the web UI.
