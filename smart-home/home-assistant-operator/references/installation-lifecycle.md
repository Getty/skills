# Installation and lifecycle

Verified 2026-10-22. Recheck [installation methods](https://www.home-assistant.io/installation/) before recommending a deployment.

## Choose an operational contract

| Deployment | Appropriate use | Operator responsibility |
| --- | --- | --- |
| HAOS on dedicated hardware | Appliance-style home server | Power, storage, backup, network, radios |
| HAOS in a VM | Existing reliable virtualization host | Above plus hypervisor updates, VM startup, USB passthrough |
| Home Assistant Container | Deliberately self-managed stack | OS/runtime, images, discovery, device permissions, companion services |

Current supported choices are HAOS and Container. Container does not include HAOS apps or Supervisor management; operate MQTT, Zigbee2MQTT, Matter Server, or Z-Wave JS separately when needed. Do not “add Supervisor” to Container to fix a missing Apps menu. [Installation](https://www.home-assistant.io/installation/), [Apps](https://www.home-assistant.io/apps/).

Standalone Python Core and Supervised installation support, plus listed legacy 32-bit architectures, had a deprecation period ending at release 2025.12. The Core application itself continues inside supported installations. Treat old setups as migration tasks rather than destroying working configuration. [Deprecation notice](https://www.home-assistant.io/blog/2025/05/22/deprecating-core-and-supervised-installation-methods-and-32-bit-systems/).

## Size and isolate

Measure recorder writes, camera processing, STT/TTS inference, and custom integrations. Entity count alone is a weak sizing proxy. Keep heavy video/GPU services separable if they affect automation latency. Document VM memory overcommit, startup order, and persistent adapter mappings. For Container, document `/config`, image tag/digest, restart policy, and each external volume. Inspect upstream deployment requirements before broad device access or privileged mode.

Do not run a restored production copy simultaneously on the same device network: duplicate actions, radio ownership, and cloud sessions can conflict. Isolate restore drills.

## Upgrade and verify

Read target breaking changes, record old versions, and check Core/OS/Supervisor/custom-code/external-server compatibility separately. Preserve an off-host backup and recovery information. Update the smallest coherent component set; dependent migrations may need more than one change.

Allow database migration to finish before calling slow startup a crash. Do not blindly downgrade an executable against newly migrated data; restore a coherent checkpoint when necessary. Confirm UI/API, a local integration, a used cloud integration, radios, critical automation state, notifications, and backups. Record unperformed tests honestly.
