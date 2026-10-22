# Recorder and statistics

Separate current state, history/events, short-term statistics, and long-term statistics. A functioning live card does not demonstrate historical health.

Recorder supplies history and statistics. Read its retention/filter and purge/repack behavior before changes; deleting records and reclaiming disk space are different operations. Reserve space for maintenance/migration. [Recorder](https://www.home-assistant.io/integrations/recorder/).

## Retention decisions

Create a value/volume matrix: heating trends, incidents, energy, and required occupancy transitions versus noisy diagnostics and timestamps. Avoid blanket exclusions that remove required historical inputs. For a large set of FRITZ! or other router trackers, decide which availability records deserve history; host discovery is not automatically a long-term occupancy archive.

Measure growth over a known interval. Identify high-rate entities, large attributes, repeated events, and new integration/error loops. Prefer supported diagnostics and consistent backups; do not manually mutate tables to hide symptoms.

SQLite is a supported default. An external database adds network, credentials, backup, version, and availability responsibilities. Migrate only against a measured bottleneck and current supported versions, not an assumption that external storage is faster.

## Preserve measurement meaning

W is power; Wh/kWh is energy. Meter reset, negative net flow, and a fabricated zero from an unavailable sensor are different. Correct device class, unit, and state class matter. `total_increasing` describes a monotonic total with possible resets, not every energy-like value. [Sensor semantics](https://contributors.home-assistant.io/core/entities/sensor/).

Inspect statistics errors, unit changes, and duplicate aggregate meters. Incorrectly including a whole-house total plus its subcircuits can double-count. Prefer a reliable native energy counter; power integration needs assumptions about sampling/outages. [Energy FAQ](https://www.home-assistant.io/docs/energy/faq/).

## Recovery

For corruption, preserve logs and a consistent copy before destructive actions; inspect storage health/free space. Database deletion may restore startup while losing history/statistics, so state that consequence before selecting it. Validate historical samples and statistics after recovery, not just live states.
