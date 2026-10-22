# Testing and experience

## Use the trace

Check whether the automation triggered, which guard passed, which branch executed, and which action failed. Manually running actions does not reproduce trigger variables or timing. A threshold already exceeded can explain why manual actions work while the trigger stays silent. [Troubleshooting automations](https://www.home-assistant.io/docs/automation/troubleshooting/).

Validate templates in isolation, then service data, then the real event path. Test with a harmless helper before physical actuators. Record whether verification was static, simulated, or observed on hardware.

## Scenario coverage

Select scenarios that could change the outcome: ordinary path, duplicate event, input unavailable/stale, actuator unavailable, manual override, restart before/after deadline, two controllers competing, and repeated request. Use the bundled worksheet. Avoid exhaustive tests of trivial formatting changes.

## Firsthand evidence records

Reviewed 2026-10-22; these are scoped reports, not a reliability ranking.

| Primary record | Scope | Lesson/status |
| --- | --- | --- |
| [A `for` trigger across restart](https://community.home-assistant.io/t/how-to-make-trigger-with-for-work-through-ha-restart/988889), 2026-02-20 | User tested a ten-minute light timeout and restarted HA; lamp remained on. Exact HA version/hardware not provided | Reproduce restart behavior; use persisted deadline/reconciliation if required. A timer's missed-expiry semantics still need handling. |
| [Mushroom 1848](https://github.com/piitaya/lovelace-mushroom/issues/1848), 2026-02-02 | Reporter used Mushroom 5.0.8/5.0.10 and dev frontend 20260128.2/.3; one tap generated duplicate button calls, native button control did not | Closed via PR 1850 on 2026-02-04; later user confirmed success after updating. Useful frontend/control comparison, not evidence every current Mushroom version duplicates actions. |
| [Adaptive Lighting 1273](https://github.com/basnijholt/adaptive-lighting/issues/1273), 2025-10-13 | User wanted brightness-only manual changes to preserve color adaptation; exact lamp/HA version not supplied | Closed 2026-01-07 after implementation via PR 1356. Read current manual-control features rather than perpetuating an old limitation. |

## Report an incident

Include versions, relevant YAML, sanitized trace, exact entity capabilities, timestamps, physical observations, and installed extension versions. Do not post raw tokens or entire household exports. Distinguish a mitigation, a confirmed fix, and a hypothesis. Keep the reproducible native-card/simple-automation case so upstream maintainers can separate device transport from frontend behavior.
