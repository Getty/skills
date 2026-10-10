# Containers, registries and Kubernetes TLS boundaries

**Read when:** TLS works on the host but fails in a build, registry pull or pod.

## Separate each trust consumer

The Docker daemon pulling an image, a BuildKit builder fetching dependencies, a process inside the image and the browser reaching its web service may all use different trust inputs. Installing a CA on the host does not automatically place it in an image or in a remote builder.

For Docker registry access, the documented directory is `/etc/docker/certs.d/<registry-host[:port]>/`. CA certificates use `.crt`; client certificates use `.cert` with a matching `.key`. The authority naming must match the actual registry endpoint; default-port handling matters. This is Docker behavior, not a universal OCI-runtime filesystem contract.

Do not solve the failure with `insecure-registries`. Verify daemon trust and registry identity, then separately verify build/runtime trust where needed. A registry repository prefix is an authorization/organization concern, not part of the TLS server hostname.

## Container image design

Bake approved public/internal roots into the appropriate image store through a reproducible build or mount a versioned app-specific bundle. Record who updates it and when the process reloads it. Minimal images may omit both CA certificates and diagnostic tools; debug from a controlled matching environment without adding permanent debug utilities to production images unnecessarily.

Keep private keys out of image layers. Deleting a key in a later layer does not remove it from earlier layers. Use runtime secret delivery and least-privilege file access. Avoid broad DNS tokens in every frontend merely to renew one shared public certificate.

## Kubernetes responsibility map

cert-manager can manage issuance and write a Secret. It does not automatically configure every Ingress/Gateway, distribute all private roots, reload every application or validate the public endpoint. Model issuer scope, Certificate ownership, Secret access, controller permissions and renewal behavior.

Explicitly choose private-key rotation behavior, such as `rotationPolicy: Always`, instead of depending on version-sensitive defaults. Check requested EKUs against the issuer's actual profile: requesting clientAuth does not make an incompatible public issuer supply it.

Use trust-manager or another reviewed mechanism for trust bundles. Never distribute the CA signing key as a trust bundle. Namespace selectors and RBAC are part of the trust-distribution boundary.

## Test the real path

Exercise pull, push, build and application connections separately. For certificate replacement, verify the Secret generation, mounted file behavior, process reload and the live certificate on each termination point. Single-file bind mounts/subPath patterns can behave differently from directory mounts during replacement; test the chosen mechanism.

The included cert-manager staging example is a reviewed configuration template, not a cluster-executed integration test.

## Primary references

- **DOCKER-REGISTRY** — [Docker registry client certificates](https://docs.docker.com/engine/security/certificates/).
- **DOCKER-CA** — [Docker host and container CA certificates](https://docs.docker.com/engine/network/ca-certs/).
- **CM-CERT** — [cert-manager Certificate resources and renewal](https://cert-manager.io/docs/usage/certificate/).
- **CM-ACME** — [cert-manager ACME issuers](https://cert-manager.io/docs/configuration/acme/).
- **CM-DNS** — [cert-manager DNS01 and delegation](https://cert-manager.io/docs/configuration/acme/dns01/).
- **CM-TRUST** — [cert-manager trust-manager](https://cert-manager.io/docs/trust/trust-manager/).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
