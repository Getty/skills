# Security, TLS, and the execution boundary

Read for every deployment and any worker that touches privileged resources. Evidence: [G3, G7, G8, G5, G1](sources.md).

## Threat model

Treat native Gearman connectivity as privileged. The job protocol and native administrative commands share the listener. Do not expose that listener to the public Internet or consider a function prefix an authorization boundary. Untrusted submission can become privileged work when a worker interprets the payload. A registered malicious worker can also be a risk to confidentiality and correctness.

Use private networking/firewalls and explicit producer/worker allowlists. When tenants need different trust levels, use separate server/pool identities or an authenticated admission gateway that enforces function/payload policy. A generic TCP proxy that only encrypts traffic does not automatically authorize particular Gearman commands. Audit access to persistence storage and result databases as separate trust boundaries.

## Transport options

Native TLS requires server support, a TLS-capable binding and compatible client/worker configuration. Inspect `--enable-ssl` build evidence and `--ssl` runtime support. The reviewed 2.1 server refuses SSL startup without the build feature; older binaries must not be assumed to fail closed. Native CLI certificate paths include `GEARMAND_CA_CERTIFICATE`, `GEARMAN_CLIENT_PEM`, and `GEARMAN_CLIENT_KEY`.

Alternatively, a protected VPN or mutually authenticated TLS tunnel can carry the native protocol. Explicitly describe where plaintext exists, who can reach the tunnel endpoints, and whether clients can bypass the protected path. Do not add guessed server certificate environment-variable names; obtain them from the matching build/source.

## Certificate acceptance tests

A successful handshake is only the positive control. Also test wrong CA, missing client certificate when required, wrong server name, expired certificate, wrong client trust chain, and a plaintext attempt. Check every language binding independently. CA chain validation and hostname verification are distinct; do not assume one implies the other. Where direct bindings cannot meet the verified policy, put the connection behind a separately validated secure transport.

The Python lab's `--ca` path enables a verifying SSL context and hostname checking; certificate/key must be supplied as a pair. It does not include an insecure-skip-verify option. This is local code behavior, not a claim that every Gearman binding has the same defaults. Its negative configuration tests are not a full live mTLS interoperability test.

## Payload and worker safety

Use bounded interoperable formats. Avoid loading untrusted Perl Storable objects, Python pickle, PHP serialized objects or arbitrary classes. Never pass job bytes into `eval`, a shell command string, a filesystem path, an unrestricted URL fetch, or a privileged command without a separately defined validation policy. Gearman is a transport, not a sandbox.

Workers should use least-privilege service identities, limited filesystem/network access, time-bounded dependencies, bounded child processes and resource limits. Retrieve secrets locally from an approved secret mechanism instead of carrying credentials in every payload. Do not log complete workloads or unrestricted worker exception strings.

## Rotation and incident response

Keep certificate/credential ownership and renewal policy explicit. Test reconnect after rotation, including persistent connections that retain old sessions. During an incident freeze unauthorized producers, preserve redacted queue/outcome evidence, and reconcile unknown requests before replaying. Deleting everything is not a substitute for understanding which effects have already occurred.
