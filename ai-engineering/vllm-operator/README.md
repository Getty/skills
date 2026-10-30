# vLLM Operator

**A modular agent skill for vLLM on affordable hardware — with technical
references, diagnostic workflows, measurement tools, and explicit boundaries.**

Language: **English**. Package version: **1.0.1**. English localization:
**September 30, 2026**. Original technical research: **September 21, 2026**;
observed official release: **v0.29.0**. The actual installed version, local CLI,
and documented combination remain authoritative. This localization does not
claim a new technical-research pass. No sponsorship or vendor affiliation;
no GPU performance figures were fabricated for this package.

## Use as a skill

Copy the **entire `vllm-operator/` folder** into your agent's skill directory
or use its skill-import mechanism. Do not extract only `SKILL.md`:
the relative references, scripts, and templates are part of the package.
The exact installation directory depends on the agent and its version;
do not overwrite an existing `AGENTS.md` or `CLAUDE.md`.

Start with [SKILL.md](SKILL.md). The central file is a router and workflow,
not a documentation dump. It instructs the agent to load only relevant references,
document assumptions, and never fabricate measurements.

Example task for an agent with the skill loaded:

> Plan vLLM for my hardware and the following workload. Use vllm-operator,
> first check the local environment and compatibility, calculate memory with
> a reserve, and create a baseline plus a load-test plan. Prioritize visible
> answer onset and SLO goodput. No paid provisioning, driver/network changes,
> or load-test execution without approval.

## Contents

28 modular [references](references/28-sources.md): engine and capability matrix;
installation/versioning; memory; APC/prompt layout/tenant isolation; external
KV tiers; scheduler/admission/high load; TTFT/TTFA/ITL/TPOT/E2E; metrics, tracing,
and profiling; quantization, kernels/graphs/speculation; multi-GPU; consumer
hardware, DGX Spark, and small rented instances; APIs/tools/reasoning;
multimodal workloads, pooling/reranking; LoRA/sleep; operations/security;
diagnostics; concrete recipes; specialized features; flag register; glossary;
primary sources.

| Tool | Purpose | Does it run inference? |
|---|---|---|
| `scripts/audit_env.py` | Local read-only software/GPU inventory and CLI help | No; invokes local version/help commands |
| `scripts/capacity.py` | Transparent MHA/GQA capacity calculator | No |
| `scripts/stream_probe.py` | Chat SSE, time to model delta/answer, usage | **Yes**, a few sequential requests |
| `scripts/bench_sweep.py` | Official benchmark CLI, saturation or arrival rates | Only with **`--execute`** |
| `scripts/metrics_inventory.py` | Inventory HELP/TYPE/names without label values | No; optional metrics GET |
| `scripts/cost.py` | Effective costs from your own inputs | No |
| `scripts/validate_skill.py` | Local structure/link/JSON/Python syntax checks | No |
| `scripts/serve_single.sh` | Conservative single-GPU startup template | Starts only with **`--execute`** |

The Python tools require **Python 3.10+ and only the standard library**.
Actual serving/benchmarking requires a separately installed compatible vLLM.
The shell launcher requires Bash and targets Linux/WSL, not native Windows GPU
operation. A shared helper module handles input, URL, and file safety.

## Check locally, then use selectively

```bash
cd vllm-operator
python scripts/validate_skill.py
python -m unittest discover -s tests -v
python scripts/capacity.py --help
python scripts/stream_probe.py --help
python scripts/bench_sweep.py --help
```

[Recipes](references/24-recipes.md) describes the transition to real hardware.
Configuration examples are explained in [configs/README.md](configs/README.md).
[Templates](templates/workload-contract.md) make workloads, compatibility,
experiments, hardware decisions, and handover reproducible.

## Safe tools and honest limits

Probes default to loopback. Use HTTPS for remote endpoints; insecure HTTP
outside loopback requires explicit permission. The HTTP probe and metrics
inventory do not follow redirects or use implicit environment proxies.
Authentication comes from `VLLM_API_KEY`; for benchmarking, that key is mapped
to `OPENAI_API_KEY` only in the child process. An existing `OPENAI_API_KEY`,
possibly intended for another provider, is **not** forwarded automatically.

Probe results contain no prompt or response text. Audit/benchmark logs may still
contain local paths, model names, and internal operational data: review before
sharing. Benchmark `--save-detailed` writes additional responses/errors and is
explicitly optional. Benchmark values are not a quality evaluation.

The streaming probe measures SSE delta gaps, **not actual token ITLs**. It is
not a load generator, a complete agent test, or an exporting OpenTelemetry client.
The memory calculator supports neither MLA/SSM/hybrid models nor blanket TP
division. Do not present tokens/s estimates as hardware benchmarks.

Checks actually performed and outstanding hardware/service validation:
[VALIDATION.md](VALIDATION.md). Dated sources: [28-sources.md](references/28-sources.md)
and machine-readable [sources.json](sources.json).

## English localization

Version 1.0.1 translates the complete package: skill instructions, all reference
chapters, templates, configuration guidance, example prompts, source annotations,
and validation documentation. CLI/API identifiers, source URLs, and file paths
are preserved. Scripts already used English messages; placeholder checks now match the English
command examples and have a dedicated regression test. The Unicode test fixture
uses an English greeting with a non-ASCII character to retain UTF-8 coverage.
The example prompts have changed language, so tokenization and prompt-based
measurements must be re-baselined rather than compared directly with the earlier
German fixtures.
