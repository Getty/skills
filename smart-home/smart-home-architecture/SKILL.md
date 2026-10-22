---
name: smart-home-architecture
description: "Use when designing, expanding or migrating a smart home around Home Assistant — choosing protocols or hubs, local versus cloud control, deciding which smart-home skill applies, buying devices from Amazon or EU listings, comparing compatibility, resilience and failure testing, VLANs and discovery."
---

# Smart Home Architecture

Treat the home as a set of independently functioning subsystems with explicit control ownership. Optimize for the user's required functions, maintainability, and recoverability. Preserve useful existing hardware and working local controls.

## Establish the task

1. Identify the outcome: operate existing equipment, diagnose a failure, design a change, or compare purchases. Do useful read-only work before requesting missing details.
2. Record the actual HA version and installation type, exact hardware/firmware, integration and transport, local/cloud dependency, and required features. Distinguish a device, entity, room/group, and network host record.
3. Record the household's inventory with [inventory-and-identity.md](references/inventory-and-identity.md). Treat quantities the user reports as reports, not discoveries. Do not infer a total from overlapping groups.
4. Draw the smallest dependency map needed: physical device → radio/hub → integration/server → automation → actuator. Mark the controller that owns each schedule and setpoint.
5. Read only the references and companion skills relevant to the decision.

## Route the work

| Task | Load |
|---|---|
| Choose the right skill or divide a large task | [suite-routing.md](references/suite-routing.md) |
| Normalize inventory and resolve ambiguous models | [inventory-and-identity.md](references/inventory-and-identity.md) |
| Design independent operation and failure boundaries | [system-design.md](references/system-design.md) |
| Compare Zigbee, Matter, Thread, BLE, Wi-Fi, wired buses | [protocol-selection.md](references/protocol-selection.md) |
| Plan LAN, discovery, VLANs, or remote access | [network-and-discovery.md](references/network-and-discovery.md) |
| Evaluate an Amazon listing or product family | [procurement.md](references/procurement.md) |
| Research users' experiences and conflicting claims | [evidence-method.md](references/evidence-method.md) |
| Define acceptance, restoration, and migration checks | [resilience-and-acceptance.md](references/resilience-and-acceptance.md) |
| Revisit live sources | [sources.md](references/sources.md) |

Use [device-record.json](assets/device-record.json) as an empty evidence template, not as a discovered device. Keep credentials, pairing codes, camera URLs, household location, and raw identifiers out of public deliverables.

## Apply these decision rules

- Separate protocol support, exact-device support, and feature support. A logo, working vendor app, or successful pairing proves only part of the chain.
- Prefer a maintained native local integration when it satisfies the required functions. Evaluate Matter, a vendor bridge, direct Zigbee, or community integration against those functions.
- Keep one authoritative writer for each continuously controlled value. Explicitly arbitrate manual controls, HA, vendor schedules, voice assistants, and adaptive controllers.
- Evaluate local operation after disconnecting WAN in an agreed test. Separate local control from cloud-free setup, firmware distribution, remote notifications, and service support.
- Require current exact-model evidence for purchases. Family lists are navigation aids; no static collection covers every SKU sold on Amazon.
- Treat community posts as dated firsthand observations. Record fixed and positive outcomes as well as failures; never infer failure rates from issue counts.
- Inspect an AI integration's actual API scope. Entity exposure for Assist is not automatically a restriction on an administrative API or MCP tool.
- Make high-impact actions concrete before execution: router reconfiguration, pairing resets, firmware flashing, deleting integrations, unpairing, shutting water valves, unlocking, or changing heating policy. A diagnostic request does not authorize a blanket reset.

## Return a decision the user can act on

Report known facts, unresolved identifiers, chosen control path, alternatives with feature losses, a minimal change sequence, acceptance criteria, and rollback. Cite exact sources for changing compatibility claims. Distinguish documented, reported, inferred, and tested here. Claim live-device success only after observing it.

Research baseline: **2026-10-22**. Refresh release-sensitive details at use time; do not treat future-dated documentation or unreleased code as installed functionality.
