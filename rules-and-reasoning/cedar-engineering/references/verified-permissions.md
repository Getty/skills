# Amazon Verified Permissions

## Separate the language from the service

Cedar is an open-source language and implementation family. Amazon Verified Permissions
is a managed service with its own policy stores, API envelopes, IAM permissions,
identity-source features, quotas, release timing, and operational behavior. Do not
assume every current Cedar SDK feature is accepted by the service. Verify its current
[service documentation](https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/what-is-avp.html)
and [Cedar considerations](https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/terminology-differences-avp-cedar.html)
for the target account and region.

At the checked date, the service overview reports Cedar 4.12. Its differences guide
now documents multiple-namespace support from May 2026; do not repeat older
single-namespace limitations. The service still has its own typed entity API envelope,
action-group handling, and template restrictions. For example, its template rules
require both principal and resource scopes to be constrained; native Cedar permits
some templates that the service rejects. Treat the service version label separately
from this skill's language and SDK baseline.

Map tenant routing to the intended policy store and protect that mapping. IAM
permission to call the service controls the calling application; the application's
Cedar decision controls its end user's action. These are distinct authorization
layers. A service API call that succeeds can still return a denied application request.

Use the documented IsAuthorized family for concrete decisions, with the correct
principal/action/resource/context and entity representation. Token-based APIs add
identity-source and token-verification behavior; they do not make arbitrary token
claims authoritative for resource ownership or tenant membership. Verify claim
mapping rather than passing a raw token payload as trusted entities.

## Deploy schemas and policies coherently

Enable the desired validation mode and validate existing policies during migration.
Turning on strict validation validates new creates/updates; it does not automatically
revalidate every previously stored policy. See [validation mode](https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/policy-validation-mode.html).

Keep static policies, templates, linked policies, schema revisions, and test requests
under review. Consider the blast radius of changing a shared template. Coordinate
application data changes with schema changes and test service behavior directly;
passing local SDK tests is necessary evidence, not proof of identical managed-service
feature support.

## Handle service failure and audit correctly

Distinguish a service timeout, throttling response, invalid request, or access-denied
API call from an application permission Deny. Record enough request identifiers and
revision context to debug decisions without logging complete sensitive token claims.
Specify retry limits and the application's failure behavior.

Test maximum input sizes, batch behavior, and response diagnostics using the current
API contract. Prefer verified service quotas over copied numeric limits in a generic
skill. Measure regional latency and revocation propagation for the actual deployment.
A local cache can improve latency but adds its own invalidation and freshness contract.

For local-only or offline use, choose an embedded Cedar runtime instead. Do not add
an AWS dependency when the user asked only for Cedar language or policy modeling.
