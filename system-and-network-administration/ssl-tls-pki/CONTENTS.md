# Contents and reading routes

Start with [SKILL.md](SKILL.md). Read only relevant references; this package is designed for selective loading, not for dumping every file into an agent context.

**Fast routes:** Incident → [runbook](references/debugging/incident-runbook.md) → [client matrix](references/clients/capability-matrix.md) → [recipes](references/debugging/openssl-curl-recipes.md). New infrastructure → [private architecture](references/private-pki/architecture.md) → [bootstrap](references/private-pki/trust-distribution-bootstrap.md) → [rotation](references/private-pki/rotation-and-recovery.md). Public certificates → [governance](references/public-pki/global-web-pki.md) → [ACME](references/acme/protocol-state-machine.md) → [renewal](references/acme/renewal-deployment.md).

## Foundations

| Reference | Read when |
|---|---|
| [Certificate profiles and service identities](references/foundations/certificates-and-identities.md) | issuing certificates or determining why an apparently valid certificate is rejected. |
| [Chains, path building, roots and cross-signing](references/foundations/chain-building-cross-signing.md) | one client works while another reports an unknown issuer, or a CA hierarchy is changing. |
| [PEM, DER, PKCS#8, PKCS#12, CSRs and key custody](references/foundations/encodings-keys-csr.md) | importing credentials, converting formats, or checking a certificate/key pair. |
| [Handshake, keys and the security properties](references/foundations/handshake-and-cryptography.md) | explaining what TLS actually proves, or locating a negotiation failure. |
| [Protocol versions, algorithms and compatibility policy](references/foundations/protocol-policy.md) | selecting a TLS baseline or interpreting old hardening advice. |
| [Scope: SSL, TLS, PKI and adjacent systems](references/foundations/scope-and-terminology.md) | the request says “SSL”, or several security technologies are being conflated. |

## Public Pki

| Reference | Read when |
|---|---|
| [Certificate Transparency and public visibility](references/public-pki/certificate-transparency.md) | assessing public-name disclosure, suspicious issuance, or browser CT errors. |
| [How the international public Web PKI works](references/public-pki/global-web-pki.md) | explaining public trust, comparing CAs, or designing a trust boundary. |
| [Issuance authorization, CAA, DNSSEC and network perspectives](references/public-pki/issuance-caa-dnssec.md) | hardening domain validation or debugging an issuance failure that looks like DNS. |
| [Dated policy calendar: current versus announced](references/public-pki/policy-calendar.md) | using a remembered certificate lifetime, EKU rule, ACME profile or TLS standard. |
| [Revocation, CRLs, OCSP and actual client enforcement](references/public-pki/revocation-crl-ocsp.md) | designing compromise containment or interpreting revocation-related failures. |

## Acme

| Reference | Read when |
|---|---|
| [ACME challenges across DNS, proxies and private networks](references/acme/challenges-and-topologies.md) | choosing HTTP-01, DNS-01 or TLS-ALPN-01 for a real topology. |
| [ACME failure isolation, rate limits and recovery](references/acme/failures-limits-and-recovery.md) | orders fail, renewals loop, or automation is exhausting CA limits. |
| [Let’s Encrypt from the TLS and PKI perspective](references/acme/lets-encrypt-service.md) | selecting Let’s Encrypt or replacing outdated assumptions about its certificates. |
| [Persistent validation, delegation and automation privileges](references/acme/persistent-validation-and-delegation.md) | considering delegated DNS solvers, managed issuance or DNS-PERSIST-01. |
| [ACME: account, order, authorization, challenge, certificate](references/acme/protocol-state-machine.md) | implementing certificate automation or explaining how Let’s Encrypt proves control. |
| [Renewal is an end-to-end deployment transaction](references/acme/renewal-deployment.md) | automating certificates or diagnosing “renewed successfully, still expired”. |

## Private Pki

| Reference | Read when |
|---|---|
| [Designing private CA infrastructure and trust domains](references/private-pki/architecture.md) | building an internal SSL infrastructure rather than obtaining one certificate. |
| [CA key custody, ceremonies and dependable operation](references/private-pki/key-custody-and-ca-operations.md) | taking a CA from a demo to a recoverable service. |
| [Mutual TLS: identity proof is not authorization](references/private-pki/mtls-identity-authorization.md) | using client certificates for APIs, workloads, devices or administrative access. |
| [Implementation patterns: OpenBao, step-ca and SPIFFE/SPIRE](references/private-pki/openbao-step-spiffe.md) | selecting a private-PKI implementation without confusing product roles. |
| [Certificate profiles, enrollment and requester authorization](references/private-pki/profiles-and-enrollment.md) | defining CA roles or deciding who may obtain which identities. |
| [Leaf, issuer and root rotation; disaster recovery](references/private-pki/rotation-and-recovery.md) | planning renewal, CA replacement or recovery after compromise. |
| [Trust distribution and authenticated bootstrap](references/private-pki/trust-distribution-bootstrap.md) | installing a private CA or explaining why host trust did not fix an application. |

## Deployment

| Reference | Read when |
|---|---|
| [Containers, registries and Kubernetes TLS boundaries](references/deployment/containers-registries-kubernetes.md) | TLS works on the host but fails in a build, registry pull or pod. |
| [Database TLS: PostgreSQL and transferable checks](references/deployment/databases.md) | securing database links or diagnosing libpq certificate failures. |
| [QUIC, DTLS, PSKs and raw public keys](references/deployment/datagrams-and-alternate-forms.md) | the traffic is not conventional HTTPS over TCP, or no CA certificate is used. |
| [Managed devices, EAP-TLS and certificate-based access](references/deployment/devices-vpn-eap.md) | TLS certificates are used for Wi-Fi, network admission, devices or VPNs. |
| [Email TLS, STARTTLS, DANE and MTA-STS](references/deployment/email-starttls-dane.md) | debugging mail transport or confusing implicit TLS with a STARTTLS upgrade. |
| [TLS termination, load balancers and verified upstreams](references/deployment/termination-and-proxies.md) | designing a multi-hop deployment or debugging proxy-specific TLS failures. |
| [Web servers, certificate loading and HTTPS policy](references/deployment/web-servers.md) | deploying TLS on NGINX, Apache or Caddy. |

## Clients

| Reference | Read when |
|---|---|
| [Apple and Android trust and application policy](references/clients/apple-android.md) | a mobile app rejects a CA accepted by a desktop browser. |
| [Browsers, public trust, interception and pinning](references/clients/browsers.md) | a browser rejects a site that command-line tools accept, or vice versa. |
| [C/C++ OpenSSL and Rust TLS integration](references/clients/c-cpp-rust.md) | integrating TLS below a high-level HTTP library. |
| [Client capability and trust matrix](references/clients/capability-matrix.md) | choosing compatible certificates or explaining different results between clients. |
| [.NET, SslStream and HTTP client policy](references/clients/dotnet.md) | building .NET clients or comparing Windows and Linux behavior. |
| [Go crypto/tls and crypto/x509](references/clients/go.md) | building Go clients, trust pools or mTLS services. |
| [Java JSSE, key stores and endpoint identification](references/clients/java.md) | debugging PKIX errors or building a Java TLS client. |
| [Linux/Unix trust stores and crypto backends](references/clients/linux-unix.md) | a Linux service or container cannot validate a private or public CA. |
| [Node.js TLS and HTTPS clients](references/clients/nodejs.md) | writing Node clients or debugging differences between tls.connect and HTTPS. |
| [Perl IO::Socket::SSL and HTTPS stacks](references/clients/perl.md) | writing Perl TLS clients or debugging LWP/Mojo/runtime differences. |
| [Python ssl, Requests and explicit verification](references/clients/python.md) | writing or debugging Python TLS clients. |
| [Windows, Schannel and application-specific trust](references/clients/windows-schannel.md) | Windows behaves differently from a Linux/OpenSSL test. |

## Debugging

| Reference | Read when |
|---|---|
| [DNS, networking, SNI, ALPN and protocol routing](references/debugging/dns-network-sni-alpn.md) | TLS changes across IPv4/IPv6, proxies, virtual hosts or transports. |
| [Failure signatures and discriminating tests](references/debugging/failure-signatures.md) | an error message needs interpretation without guessing a fix. |
| [TLS incident runbook: evidence before configuration changes](references/debugging/incident-runbook.md) | a TLS connection fails or behaves inconsistently. |
| [OpenSSL and curl: safe diagnostic recipes](references/debugging/openssl-curl-recipes.md) | running concrete checks without weakening verification. |
| [Packet captures, TLS key logs and evidence handling](references/debugging/packet-capture-and-keylogs.md) | the handshake or application exchange requires packet-level analysis. |

## Operations

| Reference | Read when |
|---|---|
| [Acceptance tests for TLS and PKI changes](references/operations/acceptance-tests.md) | approving a new service, certificate profile, client library or CA migration. |
| [Crypto agility, post-quantum migration and compliance claims](references/operations/crypto-agility-and-pqc.md) | planning algorithm transitions or evaluating “post-quantum TLS” claims. |
| [Incident response, certificate linting and authorized scanning](references/operations/incident-response-and-scanning.md) | checking deployment security or responding to possible compromise. |
| [Certificate inventory, monitoring and operating objectives](references/operations/lifecycle-and-monitoring.md) | making TLS dependable beyond the initial deployment. |
| [Performance, resumption, connection lifetime and 0-RTT](references/operations/performance-resumption-0rtt.md) | optimizing TLS without weakening authentication. |

## Executable material and evidence

| Entry | Purpose |
|---|---|
| [Local lab](labs/README.md) | Prerequisites, 108-test suite, manual fixture exploration and limits |
| [Fixture generator](labs/generate_pki.py) | Disposable positive and negative PKI material |
| [Lab runner](labs/run_lab.py) | Offline, client-runtime and NGINX tests |
| [Secure TLS probe](tools/tls_probe.py) | Explicit trust/name verification, optional client credential and HTTP check |
| [Certificate inspector](tools/inspect_cert.py) | Public metadata parsing without claiming trust |
| [Package validator](tools/validate_package.py) | Link, source, syntax and integrity checks |
| [Examples](examples/README.md) | Language probes, NGINX, cert-manager and deploy hook |
| [Validation report](validation/REPORT.md) | Exact evidence, rerun history and untested boundaries |
| [Source register](sources/SOURCES.md) | 103 primary references and review metadata |
| [Claim ledger](sources/CLAIMS.md) | Critical claims mapped to documentary and executed evidence |
| [Security contract](SECURITY.md) | Keys, trust changes, diagnostic privacy and production boundaries |
