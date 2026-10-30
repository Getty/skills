#!/usr/bin/env bash
# A text-only single-GPU baseline experiment, NOT an auto-tuned hardware profile.
# No server start unless --execute is explicitly passed. Linux/WSL Bash only.
set -euo pipefail

mode=plan
case "${1:-}" in
  --execute) mode=execute ;;
  "") ;;
  -h|--help)
    cat <<'HELP'
Required: MODEL (repo or local snapshot), MODEL_REVISION (exact revision).
Optional: MODEL_ALIAS, MAX_MODEL_LEN, MAX_NUM_SEQS, MAX_NUM_BATCHED_TOKENS,
          GPU_MEMORY_UTILIZATION, DTYPE, PORT.
By default prints the command only. --execute validates CLI flags then execs vLLM.
Loopback binding only; no public gateway, implicit remote-code trust, or GPU install.
These numbers are experimental start values, not hardware performance guarantees.
HELP
    exit 0 ;;
  *) echo 'Usage: bash scripts/serve_single.sh [--execute|--help]' >&2; exit 2 ;;
esac
if [[ $# -gt 1 ]]; then echo 'Only one option is accepted.' >&2; exit 2; fi
: "${MODEL:?Set MODEL to the exact repository or local model snapshot.}"
: "${MODEL_REVISION:?Set MODEL_REVISION to the exact reviewed revision.}"
if [[ "$MODEL" == -* || "$MODEL" == 'ORG/EXACT-MODEL' || "$MODEL_REVISION" == 'EXACT-COMMIT' ]]; then
  echo 'Replace example placeholders with a real reviewed model and revision.' >&2; exit 2
fi
MODEL_ALIAS=${MODEL_ALIAS:-local-model}
MAX_MODEL_LEN=${MAX_MODEL_LEN:-8192}
MAX_NUM_SEQS=${MAX_NUM_SEQS:-8}
MAX_NUM_BATCHED_TOKENS=${MAX_NUM_BATCHED_TOKENS:-2048}
GPU_MEMORY_UTILIZATION=${GPU_MEMORY_UTILIZATION:-0.85}
DTYPE=${DTYPE:-auto}
PORT=${PORT:-8000}
for name in MAX_MODEL_LEN MAX_NUM_SEQS MAX_NUM_BATCHED_TOKENS PORT; do
  value=${!name}
  if [[ ! "$value" =~ ^[1-9][0-9]*$ ]]; then echo "$name must be a positive integer." >&2; exit 2; fi
done
if [[ ${#PORT} -gt 5 ]] || (( PORT > 65535 )); then echo 'Invalid port.' >&2; exit 2; fi
if [[ ! "$GPU_MEMORY_UTILIZATION" =~ ^(0\.[0-9]*[1-9][0-9]*|1(\.0+)?)$ ]]; then
  echo 'GPU_MEMORY_UTILIZATION must be in (0,1], e.g. 0.85.' >&2; exit 2
fi
cmd=(vllm serve "$MODEL" --revision "$MODEL_REVISION"
     --served-model-name "$MODEL_ALIAS" --host 127.0.0.1 --port "$PORT"
     --dtype "$DTYPE" --max-model-len "$MAX_MODEL_LEN"
     --gpu-memory-utilization "$GPU_MEMORY_UTILIZATION"
     --max-num-seqs "$MAX_NUM_SEQS" --max-num-batched-tokens "$MAX_NUM_BATCHED_TOKENS"
     --enable-prefix-caching --enable-chunked-prefill --generation-config vllm)
printf 'Planned command (no secrets):\n'
printf '%q ' "${cmd[@]}"; printf '\n'
if [[ "$mode" == plan ]]; then
  echo 'No server started. Check memory, model compatibility and quality before --execute.'
  exit 0
fi
command -v vllm >/dev/null || { echo 'vllm CLI not installed.' >&2; exit 1; }
help_text=$(vllm serve --help=all 2>&1) || help_text=$(vllm serve --help 2>&1) || {
  echo 'Cannot inspect local serve help; refusing to start.' >&2; exit 1;
}
for arg in "${cmd[@]}"; do
  if [[ "$arg" == --* ]] && ! grep -Eq -- "(^|[^[:alnum:]_-])${arg}([^[:alnum:]_-]|$)" <<<"$help_text"; then
    echo "Required flag not in local help: $arg; refusing to start." >&2; exit 1
  fi
done
echo 'Starting a LOCAL experimental baseline. Stop with Ctrl-C; no restart loop is configured.'
exec "${cmd[@]}"
