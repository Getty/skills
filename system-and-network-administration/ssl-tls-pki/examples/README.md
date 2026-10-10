# Examples and their evidence status

Read [SECURITY.md](../SECURITY.md) first. No example installs a root into an operating-system store, disables verification, or provisions a production CA. Replace example identities only after defining the intended peer and trust boundary.

| File | Purpose | Evidence in this package |
|---|---|---|
| [go_probe.go](go_probe.go) | Explicit Go root pool, reference identity, timeout and HTTP check | Compiled and executed against six positive/negative scenarios; CN-only rejection also tested |
| [JavaTlsProbe.java](JavaTlsProbe.java) | In-memory JSSE trust store and HTTPS endpoint identification | Compiled and executed against six scenarios on Java 21; source targets Java 11+ |
| [node_probe.js](node_probe.js) | Explicit CA/name verification through Node TLS | Executed against six scenarios on Node 22 |
| [perl_probe.pl](perl_probe.pl) | Explicit IO::Socket::SSL peer/name verification | Executed against six scenarios; linked-library policy still matters |
| [nginx-verified-upstream.conf](nginx-verified-upstream.conf) | Independent front-end and back-end TLS authentication | Syntax and live good/wrong-name upstream tests after local substitutions |
| [cert-manager-staging.yaml](cert-manager-staging.yaml) | Staging Issuer and Certificate, rotating leaf key | YAML parse and local consistency only; **not** CRD/schema-validated or applied |
| [certbot-nginx-deploy-hook.sh](certbot-nginx-deploy-hook.sh) | Validate NGINX configuration before reload | Shell syntax only; **not** installed or executed against a system service |
| [architecture-decision-template.md](architecture-decision-template.md) | Record scope, trust boundaries, lifecycle and evidence | Authoring template, not executable |

## Probe invocation

All four language examples accept `connect-host port expected-DNS-name approved-ca.pem`. They deliberately separate the transport destination from the authenticated identity. Use only endpoints you are authorized to test. With the manual loopback server from [the lab](../labs/README.md):

```sh
go build -o /tmp/go-tls-probe examples/go_probe.go
/tmp/go-tls-probe 127.0.0.1 8443 api.svc.test /tmp/ssl-pki-manual/root.pem

mkdir -p /tmp/java-tls-probe
javac -d /tmp/java-tls-probe examples/JavaTlsProbe.java
java -cp /tmp/java-tls-probe JavaTlsProbe 127.0.0.1 8443 api.svc.test /tmp/ssl-pki-manual/root.pem

node examples/node_probe.js 127.0.0.1 8443 api.svc.test /tmp/ssl-pki-manual/root.pem
perl examples/perl_probe.pl 127.0.0.1 8443 api.svc.test /tmp/ssl-pki-manual/root.pem
```

These are bounded HTTPS/1.1 acceptance probes, not replacement HTTP libraries. They do not implement browser CT, universal revocation, redirect handling, HTTP/2 or production client identity enrollment. Java and Node examples are intended for DNS reference names; use the Python CLI for the explicitly tested IP-identity path.

The Perl example leaves protocol/cipher policy to the installed library/system configuration. Configure that policy for the target application using its current documentation; do not treat a successful name-check test as evidence that all obsolete versions are disabled.

## Deploying a template

The NGINX configuration uses a loopback front end, a separate TLS upstream, explicit upstream SNI/name verification and an explicit root bundle. It is intentionally not a complete production hardening profile or a client-mTLS setup. Preserve `proxy_ssl_verify on` and the intended upstream identity when adapting it.

The cert-manager example requires an existing namespace, matching ingress controller/CRDs, an owned publicly valid name and a functioning solver path. A staging certificate must not enter a production browser-trust path. Verify what your installed controller supports before relying on `renewBeforePercentage` or rotation defaults.

The deploy hook **will reload a real service when invoked**. Its presence in this package is not permission to run it. A configuration test plus reload is still insufficient: compare the externally served certificate after deployment and alert on stale replicas. See [renewal and deployment](../references/acme/renewal-deployment.md).
