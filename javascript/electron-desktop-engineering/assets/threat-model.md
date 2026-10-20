# Desktop threat model

## Assets and trust zones

List documents, credentials, process execution, devices, local databases, update/signing authority, and private telemetry. Map renderer, preload, main, services/plugins, OS, network, and release pipeline.

| Entry point / attacker control | Asset | Required capability | Control | Negative test | Residual risk | Owner |
|---|---|---|---|---|---|---|
| Compromised renderer | Local files | Scoped document operation | Main authorization, validated handle | Arbitrary path / other frame | | |
| Imported project | Execution | Explicit allowed job | Schema + external isolation | Unknown code node | | |
| External URL | OS handler | Fixed/allowlisted destination | Parsed URL policy | Suffix/userinfo/scheme tricks | | |
| Update metadata | Executable release | Trusted update authority | Channel/verification/signing | Tampered artifact | | |

Do not describe a process as a sandbox without specifying what OS capability enforcement it provides. Record tests actually executed and unavailable environments.
