# Capacity and recovery arithmetic

Use `scripts/storage_budget.py` for reproducible first-pass comparisons. It performs pure arithmetic, accesses no devices or networks, changes no files, and emits JSON. Treat its results as model outputs, not availability guarantees. No external Python packages are required.

## Capacity model

Supply raw capacity in TiB and either a number of full copies or erasure-code fragment counts. For `r` replicas, the ideal raw-to-logical ratio is `1/r`. For `k` data and `m` parity fragments, it is `k/(k+m)`.

With raw capacity `C`, protection ratio `P`, reserve fraction `R`, and lost raw capacity `L`:

- Ideal logical capacity: `C × P`.
- Planned logical budget: `C × P × (1 - R)`.
- Survivor budget at original protection: `(C - L) × P × (1 - R)`.

The last number answers how much logical payload could fit in the surviving raw capacity **if the original protection scheme could be restored there**. It does not describe how much data is currently readable. It cannot determine whether lost fragments were recoverable, whether a quorum exists, or whether placement rules permit reconstruction.

Example, run from the skill directory:

```bash
python3 scripts/storage_budget.py --raw-tib 60 --replicas 3 --reserve-percent 25 --occupied-tib 10 --lost-raw-tib 12
```

The ideal capacity is 20 TiB, the healthy planned budget is 15 TiB, and the survivor budget is 12 TiB. The supplied 10 TiB payload fits both arithmetic budgets. It may still fail a required three-host placement rule if only two eligible hosts survive.

```bash
python3 scripts/storage_budget.py --raw-tib 60 --ec 4 2 --occupied-tib 28 --lost-raw-tib 12
```

Using the default 20% reserve, the healthy budget is 32 TiB and the survivor budget is 25.6 TiB. The payload exceeds the latter. This flags insufficient raw capacity to restore the modeled protection and reserve; it does not claim the data is already lost. Check erasure-code stripe placement and surviving fragments separately.

`--occupied-tib` represents logical payload, not replicated physical usage. Values above the calculated budget are accepted deliberately to expose overcommit. Without occupancy, fit and margin fields are `null` rather than guessed. Reserve is a planning allowance: metadata, snapshots, journals, padding, skew, compaction, and implementation overhead are not automatically measured or deducted.

## Transfer and catch-up model

Supply `--transfer-tib` and `--bandwidth-mbps` together. Optionally supply `--efficiency` and `--ongoing-mib-s` with them. The default efficiency is 0.7; choose it from observations where possible, not because it is a universal network ratio.

Unit conversion is explicit:

- `1 TiB = 2^40 bytes` and `1 MiB = 2^20 bytes`.
- `1 Mbps = 10^6 bits/s`, divided by eight for bytes/s.
- `line_rate = Mbps × 10^6 / 8`.
- `effective_rate = line_rate × efficiency`.
- `net_drain_rate = effective_rate - ongoing_MiB/s × 2^20`.

The JSON distinguishes the ideal no-overhead transfer floor, the duration at assumed effective throughput without ongoing work, and the estimated drain time for the current backlog with continuing work. At positive net drain rate, the latter is `transfer_bytes / net_drain_rate`. At zero or negative rate it reports `cannot_catch_up`, a false catch-up flag, and `null` for the drain duration.

```bash
python3 scripts/storage_budget.py --raw-tib 12 --replicas 3 --transfer-tib 1 --bandwidth-mbps 1000 --efficiency 1
```

One TiB over an ideal 1,000 Mbps path takes 8,796.093 seconds, approximately 2.44 hours. This is a transfer-only floor under the inputs. At the default 0.7 efficiency, the no-ongoing-work estimate rises to about 3.49 hours.

```bash
python3 scripts/storage_budget.py --raw-tib 12 --replicas 3 --transfer-tib 1 --bandwidth-mbps 8 --efficiency 1 --ongoing-mib-s 1
```

Eight Mbps equals 1,000,000 bytes/s, while one MiB/s equals 1,048,576 bytes/s. Continuing demand exceeds the available rate, so the backlog cannot drain. Avoid mixing decimal network rates with binary application rates when assessing replication lag.

Interpret ongoing demand as **transfer-equivalent work on the same bottleneck**. If one application byte generates several replica or reconstruction bytes, convert that work before supplying the input. Likewise, specify the bytes the chosen repair process actually needs to move; raw capacity lost is not enough to infer them. The model assumes constant rates and does not include detection, election, provisioning, object enumeration, seek time, replay, verification, or application restart. Its output is not an RTO.

## Input and output contract

Require positive raw capacity; positive integer replicas or positive integer `k` and `m`; reserve from zero inclusive to 100 exclusive; nonnegative occupancy and loss; and loss strictly below raw capacity. Require nonnegative transfer size and ongoing demand, positive bandwidth, and efficiency greater than zero and at most one. Reject nonfinite values and results outside the numeric range. Fragment/copy counts are bounded by the exact-integer range of ordinary JSON consumers; this is an arithmetic-format limit, not a supported cluster size.

Successful calculations and `--help` produce JSON on stdout. Invalid arguments produce JSON on stderr and exit status 2; stdout remains empty. Unknown options, conflicting protection modes, and incomplete transfer inputs fail validation. Transfer modifiers without paired transfer inputs also fail. Normal results exit with status 0 even when capacity is insufficient or catch-up is impossible: inspect the result flags.

Use the model alongside [performance-and-sizing.md](performance-and-sizing.md) and [data-protection-and-placement.md](data-protection-and-placement.md). Derive formulas from conservation of bytes and the stated ideal protection geometry; no product-specific performance or durability claims are encoded. Validate a real design with observed repair/restore throughput, placement analysis, and application recovery tests.
