# Define acceptance and recovery

## Agree on observable outcomes

For each requested feature, specify event, expected result, maximum acceptable delay, stale-data handling, manual override and recovery. Set thresholds from the household's needs and measured device behavior; the values below are categories, not promised device performance.

| Scenario | Observe | Pass condition |
|---|---|---|
| Physical button | Event + affected actuator | Intended action once; no duplicate competing automation |
| Temperature reading | Timestamp and reference instrument | Plausible calibrated value within agreed tolerance |
| Quiet-hours doorbell | Press + chime + phone behavior | Native fallback remains available; intended quiet policy applies |
| WAN outage | Local control, native schedule, local UI | Explicitly chosen functions continue |
| HA restart | Helpers, deadlines, device reconnect | No unsafe replay or lost persistent alert |
| Hub restart | Entity availability and physical state | State reconciles after reconnect |
| Device power loss | Physical output and reported output | Documented restart state; no unintended energizing |
| Stale leak/presence sensor | Health indicator and automation | Unknown data is distinguishable from dry/absent |
| Broker restart | Discovery, availability and commands | No stale retained command replay; sensors reappear correctly |
| Restore to spare host | Config, secrets, radio/server identity | Recovery completes in the required window |

Do not run outage or actuator tests against occupied rooms without agreeing on scope. Use a harmless light or test sensor first. Do not simulate a dangerous event with real water or unattended heating.

## Back up each owner

HA's [backup integration](https://www.home-assistant.io/integrations/backup/) is one part of recovery. Explicitly inventory separately hosted MQTT, Zigbee2MQTT, Matter server, Frigate/NVR, router, ESPHome source and secrets, certificates and external storage. Verify what the chosen HA installation's backup actually contains.

Preserve radio network backups and keys, not only YAML. Record firmware compatibility and the restore procedure for replacement hardware. Store recovery keys somewhere independent of the failed installation. One untested encrypted archive is not evidence of recoverability.

## Migrate in bounded steps

1. Export configuration and record baseline behavior.
2. Select one representative noncritical device.
3. Describe the desired result and feature losses in advance.
4. Change one ownership path; disable competing writers.
5. Verify normal control, manual override, restart and stale-input behavior.
6. Update names/automations deliberately and retain mapping from old to new IDs.
7. Expand by room or device family only after the sample passes.
8. Remove obsolete paths after observing that no required automation depends on them.

Some migration steps have expensive rollback: Zigbee re-pairing, Matter factory reset, irreversible device firmware, chime deletion, and lost cloud keys. Mark these explicitly. Preserve original data; do not repeatedly reset a device as an unfocused troubleshooting strategy.

## Report the result precisely

Separate structural validation of a skill/configuration from live hardware validation. Record exact versions and observed tests. A linted YAML example is not a proven heating controller. Leave unresolved hardware behavior visible, with a specific test that would settle it.
