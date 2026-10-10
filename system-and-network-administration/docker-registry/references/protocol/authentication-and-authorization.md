# Registry authentication, authorization, and token challenges

> Read when: handling 401 responses or protecting private repositories.

A `401` from `/v2/` can be the expected beginning of an authentication flow. Parse the `WWW-Authenticate` challenge, identify the auth scheme, and for bearer-token flows request a token for the specified service and repository scope. Authenticate to the authorized token service over verified TLS, then retry the registry request with that token.

Treat challenge realms as untrusted routing input. Enforce an approved authority policy before forwarding credentials. Do not automatically send Basic credentials or a bearer token to an arbitrary redirect or realm. Token-service DNS, CA trust, clock accuracy, and reachability are separate dependencies from registry storage.

## Separate privileges

Use pull-only identities for nodes and deployments, push identities for CI, and separately controlled deletion/admin access. A token scope can include repository/action permissions; it is not a substitute for server-side authorization. Native htpasswd authentication identifies users but does not by itself supply a full repository-level policy/RBAC system.

Do not log tokens, Basic auth values, upstream passwords, or Engine `X-Registry-Auth`. Base64 is an encoding, not encryption. A local Compose secret file is not automatically an encrypted secret service; protect its source.

## Cache-specific hazard

An upstream cache account may read private repositories. Downstream users reaching that cache can potentially access content authorized to the upstream account unless the cache's own access policy prevents it. Do not add privileged upstream credentials to a broadly accessible cache merely to reduce pull friction. Split trust domains or use narrowly scoped identities and tested downstream authorization.

## Failure diagnosis

Distinguish bad credentials, insufficient repository scope, wrong token audience/service, expired token/clock skew, TLS failure, and a reverse proxy stripping headers. Test expected anonymous rejection, allowed pull, denied push for pull-only identity, and denied cross-project access. A successful `docker login` is not proof that every repository operation is permitted.

## Primary sources

- [Registry token authentication](https://distribution.github.io/distribution/spec/auth/token/)
- [Distribution configuration](https://distribution.github.io/distribution/about/configuration/)
- [Distribution pull-through cache](https://distribution.github.io/distribution/recipes/mirror/)
- [Engine-specific registry auth header](https://raw.githubusercontent.com/moby/moby/v28.5.2/api/types/registry/authconfig.go)
- [Compose secrets](https://docs.docker.com/compose/how-tos/use-secrets/)
