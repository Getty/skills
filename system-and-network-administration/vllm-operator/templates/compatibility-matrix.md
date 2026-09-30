# Compatibility matrix

Date/deployment/hardware: …
Status values: documented / locally functionally tested / load-tested /
not supported / not verified. A check mark without evidence is not acceptable.

| Combination / feature | Status | Version/source | Reproducible test | Boundary/rollback |
|---|---|---|---|---|
| OS + GPU architecture + driver + image | | | | |
| Model + tokenizer + chat template | | | | |
| Weight quantization + KV dtype + attention kernel | | | | |
| Context + active sequences + multimodal limits | | | | |
| Chunked prefill + APC + hybrid manager | | | | |
| Salt/tenant boundaries + external KV | | | | |
| Tools + parser + structured output | | | | |
| Reasoning + stream + usage + cancellation | | | | |
| API/SDK/proxy contract | | | | |
| LoRA + quantization + cache + parallelism | | | | |
| Speculation + kernel + concurrency | | | | |
| TP/PP/DP/EP + network/P2P | | | | |
| Metrics + tracing + sampling | | | | |
| Sleep/wake + weight update + readiness | | | | |
