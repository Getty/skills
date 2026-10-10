# Trust distribution and authenticated bootstrap

**Read when:** installing a private CA or explaining why host trust did not fix an application.

## A root bundle is a security policy deployment

Provision anchors through an authenticated channel with an independently verified fingerprint or signed management policy. Fetching a root from the very server whose identity cannot yet be verified is circular unless another authenticated bootstrap mechanism establishes it.

Distribute public root certificates and required constraints, not root private keys. Limit the trust scope where possible: an application-specific bundle is less expansive than installing a new root for every browser and service on a machine.

## Inventory the actual consumers

A host OS store, browser store, JVM trust store, Python package bundle, container filesystem, Docker daemon, BuildKit instance and application-managed trust pool can all be distinct. Updating one does not prove another changed. Record each consumer's loading behavior: startup-only, reloadable, dynamically queried, image-baked or centrally managed.

For a TLS server accepting client certificates, the client-CA trust set is a separate configuration from the server's own certificate chain. For a proxy connecting upstream, its upstream trust bundle is another separate input. Do not use one ambiguous file named `ca.pem` without documenting its role.

## Deployment sequence

1. Verify and approve the intended root and scope out of band.
2. Publish a versioned bundle through trusted configuration management.
3. Apply the platform/application-specific installation mechanism and reload/restart when required.
4. Test one approved identity and one untrusted identity with the actual consumer.
5. Record the observed bundle/version and provide a scoped removal procedure.

Avoid replacing an entire system bundle with one private root unless that is explicitly the intended isolation policy. Conversely, an application that should trust only one workload domain should not inherit all public roots accidentally.

## Constraints and distrust

Certificate constraints, trust-store metadata and application identity rules are not interchangeable. Some platforms process trust-anchor constraints differently from ordinary intermediate constraints. Test the exact restriction with a deliberately out-of-scope certificate.

A trust anchor's removal is an operational deployment with convergence time. Measure offline devices, immutable images, dormant jobs and long-lived processes. Removing a CA from the central source file is not proof it has disappeared from every client.

Use [root rotation and recovery](rotation-and-recovery.md) for overlap planning. Trust-manager can distribute Kubernetes trust bundles, but issuing a cert-manager Certificate resource alone is not a trust-distribution design.

## Primary references

- **DEBIAN-CA** — [Debian update-ca-certificates manual](https://manpages.debian.org/bookworm/ca-certificates/update-ca-certificates.8.en.html).
- **RHEL-CA** — [RHEL 9 shared system certificate storage](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/securing_networks/using-shared-system-certificates_securing-networks).
- **FIREFOX** — [Firefox enterprise certificate authorities](https://support.mozilla.org/en-US/kb/setting-certificate-authorities-firefox).
- **ANDROID** — [Android Network Security Configuration](https://developer.android.com/privacy-and-security/security-config).
- **JAVA-JSSE** — [Java 25 JSSE reference guide](https://docs.oracle.com/en/java/javase/25/security/java-secure-socket-extension-jsse-reference-guide.html).
- **DOCKER-CA** — [Docker host and container CA certificates](https://docs.docker.com/engine/network/ca-certs/).
- **CM-TRUST** — [cert-manager trust-manager](https://cert-manager.io/docs/trust/trust-manager/).
- **NODE-CLI** — [Node.js CLI and trust-store environment](https://nodejs.org/api/cli.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
