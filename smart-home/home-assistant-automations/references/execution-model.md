# Execution model

Treat an automation as event → guards → ordered steps. A trigger reacts at a moment; a true condition by itself does not repeatedly start a run. A threshold trigger normally concerns crossing, not “already past threshold when loaded.” Add reconciliation when persistent truth must produce an action. [Triggers](https://www.home-assistant.io/docs/automation/trigger/).

## Structure and targeting

Use descriptive aliases and stable automation IDs so traces and maintenance remain intelligible. Use trigger IDs when branches correspond to different events. Prefer entity IDs for readable device-independent targets, or areas/labels when group intent is deliberate. Inspect the actual action schema; an entity can exist without supporting every action of its domain.

```yaml
alias: Study motion starts allowed lighting
id: study_motion_starts_allowed_lighting
triggers:
  - trigger: state
    entity_id: binary_sensor.study_motion
    to: "on"
conditions:
  - condition: state
    entity_id: input_boolean.study_automatic_lighting
    state: "on"
actions:
  - action: light.turn_on
    target:
      entity_id: light.study_lamp
mode: single
```

All IDs are illustrative. The helper encodes a user-owned enable/override decision; this example intentionally has no automatic off behavior.

## Choose concurrency deliberately

| Mode | Suitable intent | Risk to resolve |
| --- | --- | --- |
| `single` | Ignore overlapping work | New triggers can be dropped during a long run |
| `restart` | Latest request supersedes previous sequence | Earlier run stops midway; cleanup is not guaranteed |
| `queued` | Serialize a device's operations | Stale queued requests may execute later |
| `parallel` | Independent notifications/targets | Competing writes to one actuator can race |

Queued runs enter based on conditions at trigger time. Add an action-level recheck if conditions may change before the queued action. Bound queue/concurrency limits. [Modes](https://www.home-assistant.io/docs/automation/modes/).

## Separate responsibilities

Use scripts for reusable named operations, scenes for state combinations, and helpers for explicit user settings or durable control state. Use blueprints when the same verified behavior is deployed to multiple rooms; version and inspect their source before import. UI-generated YAML can be a reliable way to obtain the installed release's action shape.

Scripts and automations share control-flow building blocks. Use choose/if, waits, and repeats to express actual branches; give waits timeouts and avoid hiding a failed action with broad continue-on-error. [Building blocks](https://www.home-assistant.io/docs/automation/building-blocks/).

Avoid long cross-room monoliths. A failure in one device should not silently prevent unrelated notifications or cleanup. Maintain a visible owner for each state transition.
