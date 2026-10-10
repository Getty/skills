# PEM, DER, PKCS#8, PKCS#12, CSRs and key custody

**Read when:** importing credentials, converting formats, or checking a certificate/key pair.

## Identify the object before converting it

PEM is a textual wrapping convention; DER is binary ASN.1 encoding. Extensions such as `.crt`, `.cer`, `.pem` and `.key` are conventions, not reliable type declarations. A PEM file can contain a certificate chain, a private key, or several objects. A PKCS#12/PFX bundle can contain private keys, certificates and metadata; treat the entire file as secret until inspected safely.

PKCS#8 describes a private-key container. PKCS#10 is the usual CSR format. Java trust stores and key stores have different operational purposes even when both use the same underlying file format.

## Safe inspection

```sh
openssl x509 -in server.pem -noout -subject -issuer -serial -dates \
  -ext subjectAltName,basicConstraints,keyUsage,extendedKeyUsage
openssl req -in request.csr -noout -verify -subject
openssl pkey -in server.key -check -noout
openssl pkcs12 -in bundle.p12 -info -noout
```

Private-key commands may prompt for a passphrase. Do not place passphrases in shell arguments or scripts. Conversion can create an unencrypted output even when the input was protected; verify output permissions and encryption deliberately. Legacy PKCS#12 algorithms may need a version-specific import path, but that does not justify enabling an obsolete provider globally.

## Compare the public keys, algorithm-independently

```sh
# Bash: a failed earlier pipeline stage must remain a failure.
set -o pipefail
openssl x509 -in server.pem -pubkey -noout \
  | openssl pkey -pubin -outform DER | openssl dgst -sha256
openssl pkey -in server.key -pubout -outform DER \
  | openssl dgst -sha256
```

The digests should match. This works across supported key families and avoids RSA-only modulus recipes. It proves key correspondence, not chain trust, name entitlement or acceptable key quality.

## File and deployment discipline

Create keys with restrictive permissions in a non-shared directory. Avoid shell tracing during credential handling. Use authenticated distribution, least-privilege readers, encrypted backups and tested recovery. A web-server worker may need the leaf key; it should not gain the CA signing key or broad DNS credentials.

Publish a matched certificate/key/chain generation atomically where the server supports it. Test configuration before reload and verify the live generation afterward. A symlink update may not affect an already opened descriptor or a container's single-file bind mount; test the deployment mechanism.

A password on a private-key file protects it at rest only while that password remains protected. An unattended service still needs a secure unlock mechanism. HSM/TPM/KMS-backed keys alter export and signing interfaces; do not assume every TLS server or CA supports the selected key handle.

## Primary references

- **OPENSSL-X509** — [OpenSSL 3.5 x509](https://docs.openssl.org/3.5/man1/openssl-x509/).
- **OPENSSL-REQ** — [OpenSSL 3.5 req](https://docs.openssl.org/3.5/man1/openssl-req/).
- **OPENSSL-P12** — [OpenSSL 3.5 pkcs12](https://docs.openssl.org/3.5/man1/openssl-pkcs12/).
- **OPENSSL-MIGRATION** — [OpenSSL 3.5 migration guide](https://docs.openssl.org/3.5/man7/ossl-guide-migration/).
- **JAVA-JSSE** — [Java 25 JSSE reference guide](https://docs.oracle.com/en/java/javase/25/security/java-secure-socket-extension-jsse-reference-guide.html).
- **CRYPTO-X509** — [cryptography X.509 reference](https://cryptography.io/en/latest/x509/reference/).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
