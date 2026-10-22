---
name: home-assistant-operator
description: "Use when installing, upgrading, backing up, migrating or debugging Home Assistant itself — HAOS, Container, Supervisor, apps and add-ons, restore, device and entity registries, REST or WebSocket API and tokens, recorder database growth, discovery, slow startup or high CPU, custom integration development."
---

# Home Assistant Operator

Operate the actual installation, version, and integration path. Establish an evidence packet before changing a running home. Preserve working physical controls and a tested recovery route.

## Start with evidence

Record installed Core version, installation method, OS/Supervisor versions where present, CPU architecture, host/VM, storage/free space, configured base URL, and affected integration versions. Ask only for missing facts that change the next action. Do not collect credentials, precise location, household history, or whole backups merely to identify a fault.

Separate physical devices, config entries, device-registry records, entities, and vendor accounts. A router-tracker count is neither a count of people nor necessarily of currently connected devices.

Verify version-sensitive instructions against the installed release and primary sources. Research snapshot: **2026-10-22**. Documentation can describe a coming release; do not apply it until its version gate is satisfied.

## Route the task

| Task | Load |
| --- | --- |
| Install, choose deployment, migrate old Core/Supervised | [Installation and lifecycle](references/installation-lifecycle.md) |
| Devices/entities/config entries, duplicates, IDs | [Data model and configuration](references/data-model-configuration.md) |
| Backup, restore, host migration, external dependencies | [Backup and recovery](references/backup-recovery.md) |
| Read state, actions, events, clients and credentials | [APIs and authentication](references/apis-auth.md) |
| Discovery, VLANs, proxy, HTTP, remote access | [Networking and access](references/networking-access.md) |
| Startup failures, CPU/RAM, logs | [Diagnosis and performance](references/diagnosis-performance.md) |
| History growth, energy, retention, database work | [Recorder and statistics](references/recorder-statistics.md) |
| Build or repair an integration | [Integration development](references/integration-development.md) |
| Compare incidents with this installation | [Community evidence](references/community-evidence.md) |
| Refresh evidence and version assumptions | [Source index](references/sources.md) |

Use `home-assistant-hacs` for extension lifecycle; `home-assistant-automations` for logic, dashboards, Assist, and MCP authority boundaries. Use `fritzbox-operator`, `smart-home-devices`, `smart-home-radio`, `smart-home-video-media`, and `smart-home-esphome-mqtt` for their systems. Companion skills are optional for a standalone operator task.

## Work in this order

1. Define the symptom and acceptance test: entity/action, expected/observed behavior, time window, and last known working state.
2. Map device → bridge/radio/cloud → integration → entity → automation → control. Check the affected boundary's power, reachability, DNS/time, authentication, and availability.
3. Read Repairs, logs, diagnostics, attributes, installed action schemas, and traces. Avoid blind restarts, mass re-pairing, registry deletion, and reinstalling integrations as the first step.
4. Choose one discriminating experiment, its rollback, and a repeatable observation. Separate frontend faults from backend faults.
5. Before upgrades, migration, storage changes, or integration removal, identify a restorable off-host backup and external dependencies.
6. Use the supported UI/API/configuration surface, validate, and verify both the requested behavior and a nearby failure path. Do not claim hardware validation without access.

## Operational rules

- Discover the configured URL and port. Do not assume every current installation uses `8123`.
- Treat `.storage` as application-managed data. Use supported interfaces for ordinary changes; exceptional direct repair requires a stopped instance and backup.
- Discover installed actions. An API state write changes the displayed representation; it does not operate hardware.
- Use the minimum actual permissions the workflow supports. A long-lived token is not automatically entity-scoped. Never print tokens/session IDs or unreviewed diagnostics.
- Keep HAOS apps, custom integrations, frontend cards, vendor integrations, and external services distinct.
- Do not infer offline operation merely because the HA host is local.
- Distinguish commissioning, reset, OTA, factory reset, and cloud unlinking; their recovery costs differ.

## Read-only helper

Run `python3 scripts/ha_readonly_snapshot.py --offline-states states.json` to summarize an existing `/api/states` export without network access. For live inspection, securely set `HA_BASE_URL` to the verified instance and `HA_TOKEN`, then run `python3 scripts/ha_readonly_snapshot.py --live`. It performs GET requests only, refuses redirects, and prints counts by default. Add `--include-entities` only when IDs/state values are needed. Read [API details](references/apis-auth.md) first.

## Return a useful result

State finding, installation/version scope, change, evidence, acceptance result, remaining uncertainty, and rollback. For architecture decisions identify who operates/restores external services. For incidents distinguish confirmed cause, correlation, and the next experiment.
