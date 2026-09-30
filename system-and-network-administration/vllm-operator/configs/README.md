# Configuration examples

All files are templates, not runtime-validated on a GPU or with their respective
services. Exceptions and checks are documented in the [validation report](../VALIDATION.md).
No secrets are included. Replace placeholders, check local help and the network
namespace, and validate the effective configuration before starting.

| File | Purpose / boundary |
|---|---|
| `client-request.json` | Small English-language chat probe; the probe script sets the model |
| `cache-request.json` | Artificial stable long prefix for cache tests, not a quality test |
| `kv-offload-native.json` | Example with a shared 4 GiB CPU budget; alternative to shorthand flags |
| `prometheus.yml` | Local scrape; Prometheus and vLLM share the same network namespace |
| `prometheus-rules.yml` | Example recording rules; verify current names and labels |
| `otel-collector.yaml` | Local OTLP debug path, not a trace database or UI |
| `nginx-vllm.conf` | Local text/SSE proxy as a `server` block inside the `http` context |

Example validation after installing the appropriate tools:

```bash
# Resolve paths from the configs directory:
(cd configs && promtool check config prometheus.yml)
promtool check rules configs/prometheus-rules.yml
otelcol validate --config=configs/otel-collector.yaml
# NGINX: include the file in a test parent config with http{}, then run nginx -t.
```

Repeat SSE/timing/cancellation tests **behind the actual deployed proxy**.
Do not expose telemetry or administrative endpoints to the public internet.
The proxy template deliberately does not forward every vLLM API; additional
required protocols must be tested and allowed individually.

Primary references: [S07–S10, S27, S41–S45](../references/28-sources.md).
