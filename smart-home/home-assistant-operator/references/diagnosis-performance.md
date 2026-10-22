# Diagnosis and performance

Record symptom time/timezone, versions, last change, exact error, affected integration/entity, and vendor-app behavior. Capture evidence before restarting.

Use integration-specific debug logging for a bounded reproduction, download diagnostics where supported, then turn debug logging off. Review exports before sharing. [Official troubleshooting](https://www.home-assistant.io/docs/configuration/troubleshooting/).

## Diagnose by boundary

1. Power, storage errors, adapter disconnects, battery, physical link.
2. Host free disk, OOM/memory pressure, CPU, clock, DNS, packet loss.
3. Core startup/migration, setup failures, event-loop blocking, retry storms.
4. Integration credentials, quotas, firmware/model support, push versus polling.
5. Entity disabled/hidden/unavailable status, units, updates, duplicate paths.
6. Automation traces/actions and native-card comparison in a second browser.

Choose a test distinguishing adjacent layers. A power cycle changes too much at once to establish a cause.

## Measure before tuning

Compare idle baseline, symptom window, and controlled reproduction. Separate Core/database/sidecar/camera/browser resource use. Track event/state update rates and repeated errors rather than entity count alone. Many router trackers and power telemetry can create polling/history load; a few transcoding cameras can dominate CPU.

Only change polling where supported. Faster polling can stress devices, quotas, and recorder together. Sleeping-device reporting cannot be fixed by issuing global refreshes.

## Isolate custom code

Record custom integration revisions and inspect their issues. Safe mode can isolate custom-code effects; it temporarily removes functionality and is not normal operation. Use the installed release's documented entry/exit route and compare the same workload before attributing cause. A card failure belongs first in a duplicate dashboard with native cards, not a backend device deletion.

Cache clearing follows a resource/version check; it cannot repair incompatible Python code. A reported regression is a hypothesis until reproduced or independently explained.

## Report and stop

Provide sanitized minimal configuration, logs, versions, reproduction, expected/actual behavior, and one useful next experiment. Distinguish fixed issues from stale closures. After a controlled fix meets the acceptance test and recurrence window, stop optional tuning. Preserve rollback where state migrations make reversal nontrivial.
