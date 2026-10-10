# Perl IO::Socket::SSL and HTTPS stacks

**Read when:** writing Perl TLS clients or debugging LWP/Mojo/runtime differences.

## Require peer verification and a reference name

Use maintained IO::Socket::SSL/Net::SSLeay builds and inspect the linked OpenSSL version. Make peer verification, service identity and SNI explicit when working at socket level.

```perl
use IO::Socket::SSL qw(SSL_VERIFY_PEER);
my $socket = IO::Socket::SSL->new(
    PeerHost => '127.0.0.1', PeerPort => 8443, Timeout => 5,
    SSL_verify_mode => SSL_VERIFY_PEER,
    SSL_ca_file => 'approved-roots.pem',
    SSL_hostname => 'api.svc.test',
    SSL_verifycn_name => 'api.svc.test',
    SSL_verifycn_scheme => 'http',
) or die IO::Socket::SSL::errstr();
close $socket;
```

The `verifycn` option names are historical API terminology; they do not justify issuing CN-only certificates. Confirm SAN behavior with the installed version and the package's negative tests. Apply the documented version policy to the real application rather than copying an unverified SSL_version string.

## High-level clients

LWP, Mojo and other HTTP libraries can wrap different defaults, agents, proxies and CA options. Identify the exact transport stack and its trust source. Test the high-level client's normal request path after the socket check; do not assume a raw IO::Socket::SSL success reproduces redirects, hostname changes or connection reuse.

Bundled CA packages can drift from the OS bundle. A packaged Perl binary may have a different OpenSSL, CA search path or file layout from the build machine. Record runtime library versions and resources in deployment diagnostics.

## Error and secret handling

Treat handshake, verification, timeout and application errors separately. Keep private-key passwords and CA-management tokens out of logs. Certificate details are useful, but SANs and subjects can reveal internal structure.

For mTLS, supply the client credential and its chain while keeping server verification. Then verify application authorization independently. Use restrictive permissions for leaf keys and never embed a private CA signing key in a distributed binary.

## Primary references

- **PERL-SSL** — [IO::Socket::SSL author-maintained POD](https://metacpan.org/pod/IO::Socket::SSL).
- **OPENSSL-VERIFY** — [OpenSSL 3.5 verification options](https://docs.openssl.org/3.5/man1/openssl-verification-options/).
- **CURL-TRUST** — [curl TLS certificate verification](https://curl.se/docs/sslcerts.html).
- **RFC9525** — [Service identity verification in TLS](https://www.rfc-editor.org/rfc/rfc9525.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
