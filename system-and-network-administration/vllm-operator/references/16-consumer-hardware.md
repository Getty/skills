# 16 — Consumer GPUs and Small Workstations

## Select hardware by bottleneck, not marketing FLOPS

Answer four separate questions: Do **all weights**, KV, and reserve fit?
How much memory bandwidth is available? How fast is the appropriate prefill/
quantization kernel? What CPU, PCIe, and thermal limits does the complete system
have? Large VRAM makes a model executable, not automatically fast enough for
interactive use. A high peak figure at a specialized precision is not a
TTFT/decode measurement. [S02, S12–S14, H01–H06](28-sources.md)

## Capacity classes — orientation, not fit guarantees

| Physical memory | Plausible search space for a first experiment | Typical trap |
|---|---|---|
| 8 GB dedicated VRAM | Small models, short contexts, low concurrency | Desktop/display and graphs leave little KV space |
| 12–16 GB | Small to medium quantized models | Treating full nominal VRAM as the weight budget |
| 24 GB | Evaluate, for example, 7–9B at higher precision or larger quantized models | 32B W4 may fit but leave insufficient KV/reserve under load |
| 32 GB | More KV or a larger weight class than on 24 GB | Equating 32 GB with 32 GiB; longer outputs keep growing |
| 48 GB | Large quantized models, including 70B W4 as a careful fit experiment | Raw weights fit, but high concurrency/long context still may not |
| 128 GB unified memory | Spark: large capacity including OS/CPU usage | Treating it as 128 GB of dedicated fast GPU memory |

For dense models, use total parameter count; for MoE, do not use only the
parameters **active** per token to size resident weights. Experts, scales,
routing, and runtime remain. All sizes are only candidates for
[memory sizing](04-memory-capacity.md), startup logs, and real load tests.
The model ranges above are not manufacturer approvals or measured fits.

## Specific reference hardware

| Reference | Manufacturer specification | Implication for vLLM |
|---|---|---|
| GeForce RTX 3090 / 3090 Ti, desktop | 24 GB GDDR6X | Used-hardware capacity class; check condition, cooling, consumption, and kernel path |
| GeForce RTX 4090, desktop | 24 GB, Ada; no NVLink | More compute without more VRAM than a 3090; quantization/workload determines the result |
| GeForce RTX 5090, desktop | 32 GB GDDR7, Blackwell; no NVLink | More capacity; requires an appropriately recent software/kernel combination |
| NVIDIA RTX A6000 | 48 GB, Ampere | Larger single card; not equivalent to RTX 6000 Ada or RTX PRO |
| NVIDIA L4 | 24 GB | Relevant small rental/inference class rather than an entire large server |
| NVIDIA DGX Spark | 128 GB coherent shared memory | Separate Arm/GB10 path; see [Spark](17-dgx-spark.md) |

Sources: [H01–H07](28-sources.md). No prices or measured tokens/s are implied.
Laptop GPUs with similar names are not automatically in the same VRAM, power,
or performance class as desktop cards.

## “Cheap old CUDA card” is not a sufficient compatibility check

The NVIDIA installation documentation consulted for the original research
requires compute capability **7.5** or higher. Do not present old P40/P100/V100
offers as a trouble-free default for that stack. An older release or community
build is a separate path requiring deliberate maintenance, with feature/security
consequences, not a free bargain comparison. [S02](28-sources.md)

AMD/Radeon/ROCm, Intel/XPU, and CPU paths have their own support matrices,
kernels, and limitations. For such a host, check the **exact SKU** in the
applicable installation and quantization matrices; “ROCm supported” does not
mean “every Radeon runs all NVIDIA features.” Apple and other local stacks
are not drop-in CUDA environments. [S02, S12](28-sources.md)

## Check before buying or renting for an extended period

Power supply/connectors according to manufacturer requirements; case clearance
and airflow; motherboard lanes and network card; actual RAM/NVMe capacity;
Linux/driver path; noise and sustained load. For used cards, run memory and
sustained-load tests only after approval, and observe temperatures, clocks,
and errors. Do not change power limits or fan curves without authorization.

Measure host energy at the whole-system level: board TGP is neither actual
inference power consumption nor total electricity use. Price/performance
comparisons must include idle time, CPU, memory, power-supply losses, and
utilization.

## Decision framework

Model fits comfortably and single-request performance suffices → single card.
Model barely fits and multiple users are expected → first evaluate a smaller
model, weight quantization, KV quantization, and context-related limits.
Larger model is mandatory → compare a larger single card against TP/PP and Spark
using actual load. Rare large jobs → compare bounded rental with permanently
expensive local hardware. The result is a budget/workload decision, not a
universal winner list.
