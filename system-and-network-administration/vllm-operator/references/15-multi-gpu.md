# 15 — Two to Four GPUs: Shard or Replicate?

## First question: must the model span multiple cards?

When the model fits on one card with KV and reserve included, independent
replicas are often a useful first comparison: little intra-model communication,
separate failure domains, and greater total capacity. The costs are duplicated
weights and separate prefix caches. When it does not fit, compare TP/PP against
a larger single GPU or a smaller/quantized model. [S28](28-sources.md)

| Method | Basic idea | Especially important on small hardware |
|---|---|---|
| TP, tensor parallelism | Split operations/weights across GPUs | Frequent collectives; head/model partitionability and P2P |
| PP, pipeline parallelism | Distribute layer stages | Pipeline bubbles, load balance, activation transfer |
| Independent replicas / DP | Complete copies serve different requests | More total capacity, not automatically a faster individual answer |
| EP, expert parallelism | Distribute MoE experts | All-to-all, expert imbalance, high weight requirements remain |
| Context/decode-context distribution | Distribute specific context/KV work | Specialized model/backend support, communication costs |
| Prefill/decode split | Separate resources for different phases | KV transfer, router, additional failure/warmup paths |

Native DP is not identical in every architecture to an external load balancer
in front of independent serving processes. Check DP/EP/communication paths
and specialized flags for the specific version. Two inexpensive PCIe cards
do not automatically justify the most complex parallelism.
[S28, S33](28-sources.md)

## VRAM does not add up transparently

2 × 24 GB is not a single 48 GB allocator. Each rank requires runtime and graph
memory and potentially replicated model/KV data. Uneven layer/expert requirements
can fill one card first. GQA can require KV replication at certain TP sizes.
The simple calculator in this package therefore deliberately does **not**
perform blanket TP division.

Record `nvidia-smi topo -m`, PCIe link state under load, GPU process occupancy,
and an environment-appropriate P2P/communication test. Physical x16 slots are
not guaranteed to provide x16 electrical connectivity; a chipset path or missing
P2P can route traffic through host RAM. Account for the VM, container, IOMMU,
and driver setup. An NVLink connector alone does not prove effective transfer
in the chosen stack. According to the manufacturer, the 4090 and 5090 do not
have NVLink. [H02–H03](28-sources.md)

## Experiment rather than use a rule of thumb

With the same model and total budget, compare: one GPU; TP=2; PP=2 where
supported; and two single-GPU replicas where the model fits. Load profiles:
one request, several short interactive requests, long prefill, and long decode.
Report TTFT/TPOT, total throughput, SLO goodput, VRAM per rank, communication
share, and energy/cost. State “TP is faster” only for cases actually demonstrated.

Use example options `--tensor-parallel-size 2` or `--pipeline-parallel-size 2`
as **alternatives** to the baseline startup, and check model/topology support.
Do not set both to 2 when only two GPUs are available in total. Explicitly
record GPU visibility and worker placement. An externally balanced replica
has its own port and a clearly assigned GPU.

## Replica routing

Route stable prefixes to a warm replica where possible, but allow an escape
to an available replica under overload. Otherwise, strict session affinity can
create hotspots. Derive affinity keys from trusted identity and workload class;
do not store sensitive prompt text in logs or labels. Plan warm caches,
replica draining, and model-revision changes together.

## Multiple hosts: only for a concrete benefit

Connecting individual rented cards with TP over the public internet is not a
standard recommendation. Network latency and collectives can consume the benefit.
Small replicas with application-level load balancing are a different, less
tightly coupled approach. Private worker networks, rendezvous/Ray/NCCL ports,
and version consistency are mandatory; do not expose these ports publicly.

Two Spark systems have an official specialized connection/serving path, but
remain two systems with distribution and communication costs:
[Spark](17-dgx-spark.md). For a small service, disaggregated prefill initially
remains a specialized experiment, not the baseline. [H07–H08, S33](28-sources.md)
