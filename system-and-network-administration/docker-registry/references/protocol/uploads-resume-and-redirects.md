# Blob upload sessions, resumption, and redirects

> Read when: pushes fail on large layers or implementing a registry client.

A blob upload can use a session initiated by `POST`, subsequent data through `PATCH`, and a final digest-qualified `PUT`; supported monolithic/mount shortcuts depend on the contract. Follow the server-provided `Location` and upload state rather than constructing guessed session URLs. Preserve query parameters and use the reported offset/range when resuming.

## Ambiguous failures

After a transport interruption, query the upload status or check whether the target blob exists by digest before retransmitting. Do not assume every retry starts at byte zero or that a lost final response means the upload failed. Use bounded retries and garbage-collect abandoned uploads according to the registry's supported maintenance process.

Validate content digest against the intended bytes, including the correct compressed representation when uploading layers. A matching local uncompressed filesystem hash is not the blob digest. Keep upload buffers bounded and do not load a multi-gigabyte layer into RAM.

## Reverse proxies and object storage

Registry responses can redirect blob downloads to object storage or another content host. Clients must be able to resolve/reach that destination and trust its certificate. Do not forward registry Authorization headers to a different authority automatically. Presigned URLs are credentials: redact their query strings and avoid storing them in logs.

Reverse proxies must preserve method/body semantics, upload Location headers, request scheme/host information, long transfer behavior, and appropriate body limits. A proxy path rewrite that allows `/v2/` ping but changes an upload URL can break push only after the first chunk.

## Acceptance test

Push a representative large image, interrupt/resume an upload in a disposable repository, and pull through the actual client network. Test expired upload URLs, object-store redirects, proxy timeouts, and a client denied write permission. Check final digest and all referenced objects—not only the push command's initial status.

## Primary sources

- [Distribution HTTP API V2](https://distribution.github.io/distribution/spec/api/)
- [OCI Distribution specification 1.1.1](https://raw.githubusercontent.com/opencontainers/distribution-spec/v1.1.1/spec.md)
- [Distribution S3 storage driver](https://distribution.github.io/distribution/storage-drivers/s3/)
- [Distribution reverse-proxy recipe](https://distribution.github.io/distribution/recipes/nginx/)
