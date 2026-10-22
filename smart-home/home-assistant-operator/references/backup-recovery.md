# Backup and recovery

Define acceptable data loss/downtime separately for configuration, history, video, and essential controls. Local heating fallback can restore comfort before the full server returns.

Home Assistant backups are encrypted by default; preserve recovery information outside the instance. HAOS and Container backup scopes differ. Independent brokers, databases, and video services require their own recovery. Verify selected contents and destination. [Backup guide](https://www.home-assistant.io/common-tasks/general/).

## Recovery worksheet

| Layer | Preserve or document | Verify |
| --- | --- | --- |
| HA | Config, custom-code versions, dashboards, automation state | Isolated restore; Repairs/logs |
| Recorder | Consistent database backup if history matters | History and statistics |
| Zigbee/Z-Wave | Network backup, adapter identity, keys, migration procedure | Stack-specific recovery |
| Thread/Matter | Credentials, server storage, fabric/controller topology | Recovered subscriptions/control |
| MQTT | Broker config, ACLs, credentials, persistence | Representative clients |
| ESPHome | YAML/secrets, build context, recovery route | Rebuild a harmless node |
| Cameras | Accounts, channels, recording store | One stream/event path |
| Network | Router export, DHCP/DNS/firewall | Management access |

Do not assume an HA backup contains every radio secret for every deployment. Read the radio/vendor skill for exact ownership.

## Prepare

Check free space; create a checkpoint named after the actual change/version. Keep an off-host copy and accessible recovery information. Preserve deployment definitions without exposing secrets. Know the restore entry point and local console route. A snapshot on the same failed storage is not an independent backup. Live external databases need their consistency mechanism; arbitrary file copies during writes are insufficient.

## Restore

Isolate the restored instance from production actuators and the original host. Restore platform/configuration, external data/services, then radio access. Verify clock/timezone before schedules. Inspect restored helper values, pending deadlines, and duplicate integrations. Replacement hardware can change USB mappings, MAC/IPs, and callback/proxy URLs; HA restore does not recreate router reservations.

## Prove it

Observe one harmless device per used route before a reversible command. Check feedback, one deadline missed during downtime, and notifications. Record restore duration and gaps. A working home page alone does not demonstrate database, radio, or external-service recovery. Keep critical local physical controls available throughout.
