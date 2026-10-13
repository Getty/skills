# How to derive an integration from the real client code

**Read when:** building a narrowly scoped adapter rather than guessing backend requests.

Pin the repository revision and trace one operation end to end: initiating UI action, native/IPC command, HTTP binding, shared request type, response/job type and result retrieval. Record each file/revision in the adapter's evidence manifest. The reviewed client conventions keep routes, methods, request construction and endpoint-specific types together, making that trace more reliable than searching for a model name in UI text.

Preserve actual HTTP methods, route constants, headers, cookie behavior and error handling. Do not copy a route string without its authentication, user/account context or request serialization. Keep shared wire types shared rather than reconstructing partial JSON from screenshots. An internal client type can change independently of a published release.

Use the upstream client's local fixture tests where applicable. Its instructions identify offline checks for `artcraft_client` and native login-bridge tests using local HTTP fixtures and temporary cookie jars. Those are useful developer tests, not proof that a production account, provider or paid generation will work.

Expose only the operations required by the agent task. Keep arbitrary native invocation, unrestricted file paths, credential access and unrestricted network calls outside a narrow adapter. Apply separate authorization to uploading an asset, spending credits, saving output and publishing it. Never turn a private backend binding into an unauthenticated network service for convenience.

Document unsupported operations and version boundaries explicitly. A functioning integration for one generation endpoint does not establish full desktop automation, scene editing or all-provider support.

## Evidence

- [artcraft-client](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_client/AGENTS.md)
- [artcraft-readme](https://github.com/storytold/artcraft/blob/main/README.md)
