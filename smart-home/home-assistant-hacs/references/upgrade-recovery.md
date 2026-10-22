# Upgrade, recovery, and trust

## Preflight

Identify the repository and exact release; inspect release notes and HA compatibility. Check repository ownership changes, dependencies, required permissions, and relevant unresolved issues. Preserve a coherent backup outside HA and know the restoration route. HACS repository data is stored under HA-managed `.storage` and is included in ordinary HA backups, but external services are separate. [HACS data/backup](https://www.hacs.xyz/docs/use/data/).

A catalog entry is discovery/distribution, not proof that arbitrary code is safe for every home. Backend custom code runs with HA's practical access; browser code acts inside an authenticated frontend. Inspect functionality and scope accordingly, without pretending a generic checklist can prove code free of defects.

## Upgrade

For classic HACS itself, follow the official update process, read incompatibilities, and restart as required. [Update HACS](https://www.hacs.xyz/docs/use/update/). Update one coherent dependency set at a time and record its version. Test an actual representative function and fallback after the change; a green update entity alone does not prove it works.

For frontend projects, verify resource loading and actual browser version. For backend projects, verify startup/config-entry setup and commands. For bridges, verify their separate process and network dependencies.

## Diagnose the failure direction

If a HACS update broke HACS, its official recovery guidance points to restoring the prior backup. [HACS-update recovery](https://www.hacs.xyz/docs/use/troubleshooting/hacs_update_broke_my_hacs/). If an HA update broke an old HACS release, the docs instead advise updating HACS. [HA-update recovery](https://www.hacs.xyz/docs/use/troubleshooting/ha_update_broke_my_hacs/). Do not confuse these cases.

For an individual extension regression, inspect its migration/rollback contract. Replacing code with an older release may not reverse stored-data changes. Preserve logs and restore a coherent checkpoint when needed.

## Remove deliberately

Inventory dashboards, automations, helpers, custom services, and entity IDs that depend on the project. Migrate consumers to a fallback, then use the supported removal procedure. Deleting HACS alone does not logically reverse every installed project's configuration and dependents. Follow the classic HACS removal sequence, including its documented restart boundaries, for the relevant version. [Remove HACS](https://www.hacs.xyz/docs/use/remove/).

Do not delete random `.storage` files, remove all custom components to fix one card, or apply classic removal instructions to a newer built-in Marketplace without reading its own lifecycle documentation.
