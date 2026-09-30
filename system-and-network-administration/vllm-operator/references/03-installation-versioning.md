# 03 — Installation, Platforms, and Reproducible Versions

## Starting point

The consulted GPU documentation lists Linux and describes WSL as a route on
Windows; native Windows is not the standard official path. NVIDIA, AMD, Intel,
and Apple paths have different packages and feature boundaries. For Linux with
NVIDIA, sufficient compute capability is only an entry requirement, not a
guarantee for every kernel. [S02](28-sources.md)

For a small server under sustained load, a dedicated Linux system is the
**operational preference** here. WSL is a practical development path, but the
Windows GUI, shared VRAM use, WSL RAM, filesystem paths, and network boundaries
must be included in testing. No global driver upgrade without a rollback plan.

## Installation contract

Record before startup:

```text
vllm_version, image_digest, architecture (x86_64/aarch64)
python, torch, CUDA/ROCm runtime, host_driver
GPU model and count, attention/quantization backend
model_id + revision, tokenizer_id + revision, chat_template hash
complete serving configuration, client/proxy version
```

`nvidia-smi` shows a CUDA version supported by the driver, not necessarily the
runtime actually used inside the container. Check both. Do not blindly install
a different Torch version over a working vLLM environment.

## The local CLI is authoritative

```bash
python scripts/audit_env.py --out ./audit
vllm --version
vllm serve --help=all > serve-help.txt
vllm bench serve --help > bench-help.txt
```

The audit script tries ordinary help when `--help=all` is unsupported.
A flag's presence establishes syntax support only. Combinations require startup
and functional tests. The audit changes neither drivers nor packages.

For x86 NVIDIA, use either an explicitly versioned official container or a fresh
virtual environment following the installation guide for that version.
For Spark, use the specific path in [17](17-dgx-spark.md).
Setting a CUDA environment variable does not make an x86 container ARM-compatible.
[S02, S32, H07–H08](28-sources.md)

## Moving documentation

The research baseline is 2026-09-21; the release page showed v0.29.0.
`stable`, `latest`, and `main` are not immutable version identifiers.
For example, a new optimization page may use shorthand for KV memory while
a target version still uses `--kv-cache-memory-bytes`. This package uses the
fully spelled-out form in executable examples only after checking the CLI.

Defaults are not documented as eternal truths. Set important values explicitly
and preserve the resolved startup log. Parsers, quantization, APC, chunked
prefill, async scheduling, and graph options are particularly relevant during
migration. [S01, S03–S04](28-sources.md)

## Upgrade gate

Copy the configuration, image digest, and model revision. Build a separate
canary instance or a maintenance-window experiment. Test the same tasks and
loads, then cache correctness, metric names, streaming, cancellations, tools,
long context, and OOM behavior. Selectively discard incompatible KV/compile
artifacts instead of blindly sharing the same directories between versions.
Separate external KV caches with versioned namespaces.

Rollback means being able to restart the old unchanged image/model/configuration
combination. “Just downgrade with pip” is not a reliable recovery path once
dependencies, tokenizers, or caches have already changed.

## Trust boundaries

`trust_remote_code` permits execution of model code. Use it only for reviewed,
revision-pinned repositories. Treat HF tokens as secrets; do not write them
into shell history, logs, or skill files. Never routinely mount the Docker
socket in rented containers. [S27](28-sources.md)
