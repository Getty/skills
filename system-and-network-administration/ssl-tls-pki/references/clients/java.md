# Java JSSE, key stores and endpoint identification

**Read when:** debugging PKIX errors or building a Java TLS client.

## Key store and trust store are different roles

A key store supplies the client's/server's private key and certificate chain. A trust store supplies authorities used to verify the peer. They may share a file format but should not be treated as interchangeable. Identify the actual JVM, runtime image and configured store; changing a different JDK's `cacerts` does not fix the process.

PKCS#12 import success does not prove the right alias was selected or that the full chain/private key is available. Inspect aliases, entry types and key-manager selection under controlled logging.

## Raw sockets require identity policy

For raw SSLSocket use, explicitly enable the relevant endpoint-identification algorithm. HTTPS stacks normally establish their own HTTPS identity rules; a custom socket/engine integration must not assume chain validation also checks the intended host.

```java
SSLParameters parameters = socket.getSSLParameters();
parameters.setEndpointIdentificationAlgorithm("HTTPS");
socket.setSSLParameters(parameters);
socket.startHandshake();
```

The socket's peer host must be the intended reference identity, not accidentally the connection IP. The executable Java example creates a layered socket using the reference name and a deliberate in-memory trust store.

## Debugging

Capture JVM version, JSSE provider, trust/key-store configuration, endpoint identification and protocol restrictions. `javax.net.debug` can expose handshake/trust-manager detail, but logs may contain identities, session metadata and other sensitive information; enable it temporarily and redact appropriately.

A “PKIX path building failed” message suggests a path/trust issue but is not a full diagnosis. Check missing intermediates, actual roots, algorithm constraints and the runtime's selected store. A disabled-algorithm failure is not cured by importing more certificates.

## Revocation and lifecycle

Revocation checking has separate JSSE/PKIX configuration and availability implications; do not assume it matches the browser. After trust or key changes, determine whether the SSLContext, connection pool and session cache are refreshed.

Test the supported JVMs, not only a developer machine. Include wrong-host rejection, untrusted issuer, incomplete chain, wrong-purpose certificates and client alias selection. Keep store passwords out of process arguments and source code in production.

## Primary references

- **JAVA-JSSE** — [Java 25 JSSE reference guide](https://docs.oracle.com/en/java/javase/25/security/java-secure-socket-extension-jsse-reference-guide.html).
- **RFC9525** — [Service identity verification in TLS](https://www.rfc-editor.org/rfc/rfc9525.html).
- **RFC5280** — [X.509 certificates and CRLs / PKIX](https://www.rfc-editor.org/rfc/rfc5280.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
