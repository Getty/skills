# Authentication, permissions, sessions, and TLS

## Separate the identities

Use dedicated FRITZ users for integrations where supported. Router administrative users, telephony/SIP accounts, NAS permissions, MyFRITZ account credentials, HA tokens, Matter fabrics, and webhook IDs are distinct credentials. Success with one does not establish access with another.

Create only the rights needed for the chosen surface: Smart Home for native HA smart-home access; FRITZ!Box Settings for the Tools integration; phone rights for call-list/phonebook access. Current HA setup requirements are documented for [SmartHome](https://www.home-assistant.io/integrations/fritzbox/), [Tools](https://www.home-assistant.io/integrations/fritz/), and [Call Monitor](https://www.home-assistant.io/integrations/fritzbox_callmonitor/). Some rights are broad; a dedicated account does not automatically make every exposed action read-only.

Inspect the actual username. Do not assume `admin` on modern firmware or assume that a repeater uses the same app-access identity as the mesh master. Use a user already authorized for this task rather than repeatedly asking for the same credential, and do not retrieve unrelated secrets.

## SID handshake

The [official session specification](https://fritz.support/resources/HTTP_Session-ID_DE.pdf) defines `login_sid.lua?version=2`, `BlockTime`, and the modern challenge. A challenge starting `2$` carries two iteration counts and salts for two PBKDF2-HMAC-SHA256 rounds. Use password UTF-8 bytes for the first round, its binary output for the second, then form the response from the second salt and hex result. A legacy challenge uses the documented MD5/UTF-16LE path; do not force downgrade. Respect `BlockTime`, reject the all-zero SID, reuse sessions, and renew after expiry rather than continuously logging in.

Use a maintained implementation or test your implementation against official vectors. Build tests for non-ASCII passwords, malformed challenges, numeric iteration parsing, missing XML fields, blocked logins, invalid SID, and expiry. Bound computational and network work when parsing responses. Never log password, computed response, SID, or a full authenticated URL.

## Authorization is not authentication

| Symptom | Correct distinction |
| --- | --- |
| Zero SID after login | Credential/account/challenge or block-time problem |
| AHA 403 | SID invalid or operation unauthorized; check both |
| Overview works but configuration fails | Different endpoint rights or unavailable action |
| Read succeeds, sensitive action requires confirmation | Physical-confirmation boundary, not necessarily wrong password |
| Repeater fails after update | Inspect that repeater's app-access user and current requirements |
| SmartHome works but Tools fails | Separate permission/protocol prerequisites |

For TR-064 protected writes, follow the [FRITZ authentication service](https://fritz.support/resources/TR-064_Authentication.pdf). Preserve physical confirmation when required. Explain the exact blocked action rather than broadly disabling confirmation or granting an unrelated account full administration.

## TLS and local addressing

Verify that the contacted origin is the expected router before sending any credential. `fritz.box` depends on DNS; custom DNS, VPN DNS, or a container resolver can change where it resolves. Read the IP result from the execution environment, not only from the user's desktop browser. Use a stable local address for routing while solving certificate hostname/trust properly.

Prefer validated HTTPS. A self-signed local certificate can be explicitly trusted or pinned after identity verification; global `verify=False` is not a permanent design. Check clock, hostname, trust chain, and the correct HTTPS port separately. Never copy a certificate-trust workaround into every unrelated HTTP client.

## Protect diagnostics

Temporarily enable targeted debug logging, reproduce one event, then disable it. Inspect logs before sharing: even libraries that hide passwords may emit SIDs, names, phone numbers, MACs, IPs, or configuration URLs. Retain a private original if needed and publish a redacted minimal excerpt. A sanitized HA diagnostic file still deserves review for household-identifying fields.

For secrets in custom clients, use an approved secret store, environment injection, or an interactive hidden prompt. Do not pass credentials as shell arguments, include them in Git, or store an active SID inside an automation URL. A webhook ID is a bearer secret; choose a high-entropy value and rotate it if disclosed.
