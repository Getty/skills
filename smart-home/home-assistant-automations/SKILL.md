---
name: home-assistant-automations
description: "Use when writing or debugging a Home Assistant automation, script, scene, helper, blueprint, template or dashboard — triggers firing twice or not at all, delays lost on restart, manual override, lighting, heating, leak response, presence, energy, Assist or LLM/MCP control, traces."
---

# Home Assistant Automations

Translate an intended household behavior into explicit states, transitions, ownership, and failure behavior. Use the existing entities and installed actions; do not invent device capabilities.

Research snapshot: **2026-10-22**. Verify current syntax/API behavior against the installed release. Treat examples as adaptable patterns with explicit fictional entity IDs.

## Load only the relevant references

| Task | Reference |
| --- | --- |
| Automation structure, triggers, conditions, IDs, modes | [Execution model](references/execution-model.md) |
| Templates, unavailable inputs, numeric and time handling | [Templates and helpers](references/templates-helpers.md) |
| Delays, timers, restart recovery, idempotency | [Durable timing and state](references/durable-timing.md) |
| Hue and mixed lighting, scenes, physical/manual control | [Lighting and manual control](references/lighting-manual-control.md) |
| FRITZ! and other thermostats, windows, leak response | [Climate and protective actions](references/climate-leaks.md) |
| Router trackers, people, rooms, occupancy uncertainty | [Presence](references/presence.md) |
| Dashboards, power/energy and useful household controls | [Dashboards and energy](references/dashboards-energy.md) |
| Voice, Assist, conversation agents, external MCP | [Voice and agent authority](references/voice-agents.md) |
| Traces, scenario acceptance and community cases | [Testing and experience](references/testing-experience.md) |
| Refresh sources | [Source index](references/sources.md) |

## Work from a behavior contract

1. State the desired outcome, target room/device, allowed times, manual override, and who is affected.
2. Inventory actual entity IDs, states, attributes, installed actions, and action schemas. Identify upstream controller schedules and duplicate paths.
3. Write a transition table with trigger, guard, action, expected feedback, timeout, and recovery. Define behavior for `unknown`, `unavailable`, old readings, restart, and repeated events.
4. Select one controller for the same actuator at a given time. Specify handoff between device schedule, vendor bridge, HA, and physical controls.
5. Choose a helper/script/scene/automation boundary and deliberate run mode. Keep important state outside long in-memory waits.
6. Implement the smallest reusable logic. Use current `triggers`, `conditions`, `actions`, and `action:` forms for new examples, while preserving valid existing syntax unless migration is needed.
7. Validate configuration, templates, and target capabilities, then test the actual trigger path and a recovery case. A manual “Run actions” test does not establish trigger correctness.

## Rules for dependable behavior

- Prefer explicit `turn_on`/`turn_off` to `toggle` when retries or duplicate events are possible.
- Do not default unavailable temperature to zero, or unknown occupancy to absent, just to make a template evaluate.
- Do not assume a `for:` trigger, a running delay, or queued execution survives restart/reload. A restored timer can expire during downtime without a `timer.finished` event on startup.
- For durable deadlines, store an absolute due time and pending state, and reconcile on startup and when dependencies become available.
- Recheck conditions immediately before consequential actions after a wait or queue.
- Preserve manual control. An automation must not continuously undo a user's selected brightness, temperature, or off state without an explicit policy.
- A service success is not physical confirmation. Observe device feedback where available and mark uncertainty where it is not.
- Keep routines for ordinary lights separate from safety-critical protection. Define protective hardware/local behavior independently from best-effort HA notifications.
- Distinguish Assist's exposed-entity boundary from administrative HA APIs and MCP configurations that grant wider access.

## Examples and output

Use [restart-safe light session](assets/restart-safe-light-session.yaml) as a complete package-style timing pattern. The hard-coded `light.study_lamp` is fictional and must be mapped before use. Read the timing reference for tradeoffs and failure cases. Use [scenario worksheet](assets/automation-scenarios.md) to define useful acceptance evidence without building tests that only repeat the YAML.

Return a behavior summary, required helpers/entities, code or UI steps, ownership/manual-override rule, tested scenarios, observed limitations, and rollback. Never report live tests when only static validation was performed.
