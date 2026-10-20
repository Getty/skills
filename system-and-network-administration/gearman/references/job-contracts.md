# Job contracts, identities and schema evolution

Read before writing any payload or result implementation. The contracts below are **application conventions**, not native Gearman fields. See [the request schema](../assets/contracts/job-request.schema.json) and [Python contract implementation](../examples/python/contract.py).

## Keep identities separate

Use an application request ID for permanent correlation/deduplication; a transport unique ID for a particular queue/coalescing policy; a server-issued handle for a live assignment's diagnostics; and a trace/span identity for observability. Do not place credentials or personal data in any of these identifiers. Namespace/version the function explicitly, for example `documents.thumbnail.v2`.

## Reference envelope

```json
{
  "schema_version": 1,
  "request_id": "129d8f21-24e2-4e91-a579-5cd3c4c94203",
  "operation": "sum.v1",
  "payload": {"numbers": [4, -2, 11]}
}
```

The demo also accepts `deadline_unix_ms`. It limits the request to 64 KiB, the integer array to 1..1000 elements, and each value to +/-1,000,000,000. These intentionally small limits make arithmetic exact on the supported 64-bit runtimes. Boolean values and numeric strings are not integers in the contract. The UUID-shaped string is validated for shape, not proof of random generation or globally verified uniqueness.

## Validation order

Bound raw bytes before parsing; decode UTF-8 strictly; bound nesting/parser behavior; require a JSON object; validate version and field set; validate operation; validate payload types/ranges; validate the business deadline before a new execution. Python additionally rejects duplicate JSON keys. The Perl/PHP teaching adapters use their standard JSON decoders and do not claim equivalent duplicate-key detection; add a strict parser/admission gateway before treating them as identical security boundaries.

Never infer schema safety from successful JSON decoding. A string containing a huge URL, a number outside a downstream integer range or a syntactically valid path traversal is still invalid input. Each real operation must validate its own domain fields.

## Fingerprinting

Hash only fields that define the business effect, using an explicitly shared canonicalization scheme. The Python result store fingerprints schema version, operation and payload; it excludes deadline and request ID. A replay of the same request ID with a different business fingerprint is rejected, not treated as success. For general multilingual JSON with decimals/Unicode, choose a formal cross-language canonical representation or a typed binary schema instead of assuming ordinary `json.dumps` implementations agree.

## Version rollout

Prefer versioned functions for breaking handler contracts. Deploy workers supporting the new function first, then change producers. Keep old workers until the old queue and the application's owed-work ledger are drained. Additive fields still require a declared acceptance policy; this strict demo rejects unknown fields intentionally. Do not broaden it silently while claiming unchanged validation semantics.

A result contract should distinguish success, permanent domain failure and request correlation. Protocol failure packets do not supply a durable application error model by themselves.
