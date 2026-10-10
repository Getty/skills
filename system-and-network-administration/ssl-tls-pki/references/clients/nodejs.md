# Node.js TLS and HTTPS clients

**Read when:** writing Node clients or debugging differences between tls.connect and HTTPS.

## Low-level TLS needs an explicit name

A raw `tls.connect()` call does not automatically behave like an HTTPS request with a URL. Supply the intended DNS `servername` for SNI and normal identity verification when connecting by a different address. Keep `rejectUnauthorized: true` and do not replace `checkServerIdentity` with an unconditional success callback.

```javascript
const tls = require('node:tls');
const fs = require('node:fs');
const socket = tls.connect({
  host: '127.0.0.1', port: 8443, servername: 'api.svc.test',
  ca: fs.readFileSync('approved-roots.pem'),
  rejectUnauthorized: true, minVersion: 'TLSv1.2'
});
socket.on('error', err => { console.error(err.message); process.exitCode = 1; });
socket.on('secureConnect', () => socket.end());
```

Production code also needs deadlines, application-protocol handling and deterministic cleanup. See the executable client example for the testable version.

## Trust composition

A custom `ca` option replaces the default CA set for that context rather than blindly appending to it. Decide whether that narrow trust is intended. `NODE_EXTRA_CA_CERTS` has process-start semantics and documented limitations; changing the file/environment after process start is not proof that trust changed.

System-CA support and related CLI flags vary by Node version. Check the installed CLI documentation before using a flag from the latest website. Avoid global `NODE_TLS_REJECT_UNAUTHORIZED=0`; it weakens unrelated connections and hides the real defect.

## HTTPS and mTLS

High-level HTTPS agents may manage SNI, pooling, proxies and CA settings differently from a direct TLS socket. Test the application's agent, not only the sample above. For mTLS, provide the client key and full appropriate chain while retaining server verification.

After rotation, determine whether pooled connections and cached sessions persist. Test a new handshake and application response. A `secureConnect` event alone is insufficient evidence of HTTP authorization or of a TLS 1.3 client-authentication alert that appears during subsequent I/O.

## Primary references

- **NODE-TLS** — [Node.js TLS API](https://nodejs.org/api/tls.html).
- **NODE-CLI** — [Node.js CLI and trust-store environment](https://nodejs.org/api/cli.html).
- **RFC6066** — [TLS extensions, including SNI](https://datatracker.ietf.org/doc/html/rfc6066).
- **RFC9525** — [Service identity verification in TLS](https://www.rfc-editor.org/rfc/rfc9525.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
