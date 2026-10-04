# Authentication, identity, and secrets

Separate host login, MCP connection login, and authorization to access a particular record. Successful authentication does not imply permission for every tool or tenant.

Authenticated plugin MCP servers follow the MCP OAuth contract. The documented flow uses protected-resource discovery, authorization-server metadata, resource indicators, PKCE, and a supported client identification/registration mechanism. Validate tokens at the resource server on each request. [Authentication](https://developers.openai.com/plugins/build/auth)

## Design the identity path

Record:

1. The identity initiating the request.
2. The external account or service identity used by the tool.
3. How the tenant and resource are selected.
4. Which scopes authorize the operation.
5. How revocation, account switching, and expiration behave.

Do not infer tenant access from an ID supplied by the model. Authorize against the authenticated principal and server-owned account mapping.

For local OAuth setup, register the callback the host actually displays. Avoid copying a callback from another client, machine, or historical recipe. HTTP token environment references and OAuth credentials are separate configuration choices.

## Keep secrets outside distributable content

Store credentials in the host's supported credential mechanism or a backend secret store. Pass names/references where supported. Never place usable credentials in plugin manifests, skill examples, marketplace catalogs, tool results, screenshots, or test transcripts.

A UI's hidden metadata is still data delivered to a client; it is not a secret vault. Minimize sensitive data and redact logs. [Security and privacy](https://developers.openai.com/plugins/guides/security-privacy)

## Failure tests

Test unauthenticated access, expired tokens, revoked scopes, wrong audience, wrong tenant, account switching, missing write permission, and interrupted OAuth. Ensure failures produce a useful reconnect or permission explanation without leaking record existence across tenants.

Separate credential repair from authorization expansion. Restoring an expired session should not silently request broader access. For review submissions, prepare a dedicated sample-data account through the documented review flow rather than shipping real credentials.
