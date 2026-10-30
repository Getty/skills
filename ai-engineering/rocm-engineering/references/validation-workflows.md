# Validation workflows and acceptance gates

Use these workflows for installations, migrations, releases, hardware assessments and incident fixes. They are designed to distinguish evidence levels and avoid false success.

## Contents

- [Define evidence and acceptance](#define-evidence-and-acceptance)
- [Run the staged checks](#run-the-staged-checks)
- [Qualify the real workload](#qualify-the-real-workload)
- [Validate without the target hardware](#validate-without-the-target-hardware)
- [Interpret the bundled helpers](#interpret-the-bundled-helpers)

## Define evidence and acceptance

Before a test, state the stack, workload, expected result, failure condition and cost. Keep four judgments separate: published support, successful execution, numerical correctness and operational suitability. A test can establish some while leaving the others unknown.

Fill [the stack record](../assets/stack-record.yaml) with observed facts and source references. Leave unknown fields null. Use [the benchmark record](../assets/benchmark-record.json) for comparisons; do not turn unmeasured fields into zeros.

For each command, retain exit status and relevant output. Treat a missing prerequisite as unavailable, not passed. For multi-process tests, require the launcher to return success and all expected ranks to report completion. A single passing rank is insufficient.

## Run the staged checks

| Gate | Evidence | Pass meaning | Does not establish |
| --- | --- | --- | --- |
| 0: Documentation | Correct matrix, artifacts and known issues | Proposed combination has a stated support scope | Local machine works |
| 1: Inventory/access | Devices, driver, permissions, version provenance | OS/runtime can potentially access allocated hardware | Kernel execution or numerics |
| 2: Runtime | Small HIP program with checked copies/result | Simple target kernel executes correctly | Framework or advanced precision support |
| 3: Framework | HIP build and selected-dtype operations | Tested operators work in this environment | Every custom node/kernel/model works |
| 4: Application | Representative full graph/model | Intended path meets quality and memory criteria | Scale, soak, restart and service behavior |
| 5: Distribution | Correct collectives and application placement | Tested topology and rank mapping work | Every message/protocol or larger cluster |
| 6: Operations | Load, restart, checkpoints, health, rollback | Defined deployment objectives are met | Indefinite reliability or future-version compatibility |

Proceed only as far as the task requires. Do not run a long cluster stress suite to answer a narrow package question. Conversely, do not call a production migration complete after an import check.

From the skill directory:

```bash
python3 scripts/rocm_inventory.py
python3 scripts/rocm_inventory.py --probe-runtime --timeout 15
python3 scripts/torch_smoke.py --dtype float32 --sdpa
# Run only when the selected target/backend is expected to support this dtype.
python3 scripts/torch_smoke.py --dtype float16 --sdpa
```

These commands do not install prerequisites. Inventory is passive by default; optional probes can initialize the runtime. The Torch helper allocates small tensors and refuses CPU/NVIDIA builds. No hardware support status changes because a helper passed.

For distributed work, use allocated GPUs and an external job wall-time limit:

```bash
torchrun --standalone --nproc-per-node=2 scripts/distributed_smoke.py
```

On multi-node jobs, use the scheduler's documented launch/rendezvous configuration rather than copying the single-node command. A process-group timeout does not guarantee driver-hang recovery. Do not apply a GPU reset on a shared node as an automatic timeout handler.

## Qualify the real workload

**Inference:** use the exact model revision, tokenizer/template, context lengths, generation limits, dtype, quantizer and attention backend. Check output quality, request concurrency, prefix/cache policy, time to first token, inter-token latency, throughput and peak memory. Exercise shutdown/restart and error paths.

**Training:** compare loss/gradients and a meaningful parameter update against a baseline. Verify optimizer state, mixed precision, checkpoint contents and resumed behavior. Test the longest intended sequence and realistic microbatch. For distributed training, confirm rank assignment and sharded-state recovery.

**Image/video:** execute preprocessing, every custom node, denoising and output decoding. Check nonfinite values, black/corrupt outputs, dimensions, frame count and temporal quality. Measure phase-specific memory, not only the first successful preview.

**HPC/custom kernels:** use reference numerics, residuals/conservation properties, adversarial shapes and required precision. Profile after correctness; report compiler flags and fast-math assumptions. Reordered floating-point sums need a numerical contract rather than automatic bitwise equality.

**Infrastructure:** test allocation, process/container restart, device health, log/metric collection, tenant boundaries and rollback on an isolated/canary target. Review release-specific correctness issues before interpreting a throughput improvement.

## Validate without the target hardware

Useful checks include source and syntax review, dependency/artifact verification, JSON/YAML parsing, local link checks, CLI error paths and independent arithmetic. Controlled test doubles can verify orchestration/error handling but cannot validate HIP, RCCL or GPU numerics. Record that distinction.

Do not report CUDA or CPU execution as an AMD test. A CMake file that parses has not necessarily found a working HIP compiler. A successful cross-build has not demonstrated target execution. Prepare the exact remaining hardware checks and leave their status unperformed.

## Interpret the bundled helpers

| Helper | Expected behavior and limitations |
| --- | --- |
| `rocm_inventory.py` | Exit 0 means collection completed. Missing devices/tools and failed probes remain structured evidence, not a support verdict. No automatic install, privilege escalation or network. |
| `torch_smoke.py` | Exit 0 means requested bounded checks passed; 1 means execution/numerical/timeout failure; 2 means prerequisite or argument failure. Autograd is basic FP32; SDPA does not force a particular fused backend. |
| `distributed_smoke.py` | Exit 0 means rank-local checks and cleanup completed. Require the launcher and all ranks to succeed. Tiny exact sums do not cover all collectives, message sizes or protocols. |
| `memory_budget.py` | Exit 0 means a finite estimate was produced. It does not certify fit, dtype/backend support, training, MLA or hybrid architecture behavior. |
| HIP smoke assets | Check basic integer kernel/copies and error handling. Need a real compatible compiler/GPU; do not imply floating-point-library qualification. |

If a helper fails, preserve the earliest meaningful error, identify its layer and choose the next discriminating observation from [troubleshooting](troubleshooting.md). Avoid expanding tests after sufficient evidence has resolved the task's concrete risk.
