# 18 — Small Rented Instances, Vast.ai/Runpod, and Honest Costs

## Look for a usable instance, not just a GPU name

An inexpensive single 24/32/48 GB host may be suitable. CPU share, RAM, local
NVMe, persistent storage, PCIe/P2P for multiple GPUs, network, location latency,
images/architecture, and actual host stability also matter. A GPU can be fast
enough while limited CPU or disk capacity slows tokenization or downloads.

For Vast.ai, check the specific instance/interruption conditions; for Runpod
and other providers, treat the storage lifecycle separately from compute.
Container disks, volumes, and network volumes do not necessarily share the
same lifecycle when stopped or terminated. Read current provider terms before
promising persistence or freedom from charges. [C01–C02](28-sources.md)

## Every price needs a timestamp and a unit

This package deliberately contains **no fabricated current hourly prices**.
For an actual decision, collect current GPU/instance prices, vCPU/RAM,
storage charges per time unit, egress, minimum billing, interruption model,
currency/taxes, and region. Save the result as an offer snapshot with date
and time. Do not turn an old blog post into a 2026 price quote.

Do not create instances, charge a card, delete storage volumes, or start
expensive load-test series without explicit approval. The included scripts
provision nothing; the benchmark sweep additionally requires `--execute`.

## Two valid cost perspectives

**Marginal cost in warmed-up continuous operation:**

```text
Cost / 1 million SLO-compliant output tokens
    = 1,000,000 × cost_per_hour / (3,600 × SLO_output_tokens_per_second)
```

**Actual campaign:**

```text
Total cost = billed_compute + storage + egress + other_costs
Cost / accepted request = total_cost / accepted_requests
Cost / 1 million useful tokens = 1,000,000 × total_cost / useful_tokens
```

Here, `useful` means successful, within the SLO, and at the agreed quality.
The benchmark tool does not automatically check quality. Failed attempts,
retry tokens, warmup, and downloaded but unused weights do not count as useful
output. Negative or zero denominators do not represent a valid bargain.

```bash
# Arbitrary calculation inputs, NOT a provider offer and NOT a GPU benchmark:
python scripts/cost.py --hourly 0.80 --hours 3 \
  --other-cost 0.15 --useful-tokens 900000 --successful-requests 600 \
  --currency EUR
```

For local hardware, include whole-system kWh plus purchase/depreciation/
maintenance according to the chosen comparison method. An already paid-for
device and a new purchase are different decisions; do not hide assumptions.

## A small, safe operational workflow

Before renting, establish compatibility and capacity hypotheses. Select the
model and revision, image/digest, and required data volumes. Time boot,
download, startup, and warmup separately. Initially use the endpoint privately
or through an SSH tunnel. Measure TTFT/TTFA from an actual user's location,
not only from localhost on the rented machine.

After a smoke/quality test, run a short controlled load curve. Only then extend
the rental or increase capacity. Container/weight caches on suitable persistent
volumes can accelerate restarts while continuing to incur storage costs.
Keep API keys in secrets, not images or public notebooks.

## Interruptible instances

These are generally more suitable for deferrable batch jobs with a resumable
job queue than an unbuffered interactive single server. Recovery costs more
than image boot: weight loading, compilation, graph warmup, and lost prefix
caches are part of it. Plan job/request IDs and idempotent result storage;
when completion is uncertain, do not blindly repeat a paid tool action.

**Exit check:** drain requests; preserve results and measurement manifests;
verify desired persistent data; actually stop/terminate compute; check remaining
volumes, public endpoints, keys, and continuing charges.
Do not hide automatic deletion in this skill.
