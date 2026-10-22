# Community evidence: operational incidents

Reviewed 2026-10-22. These are primary reports, not measured prevalence. Reopen before applying version-specific conclusions.

| Record | Reported environment/observation | Interpretation |
| --- | --- | --- |
| [Core 175877](https://github.com/home-assistant/core/issues/175877), 2026-07-07 | RPi4 4 GB, HAOS, Core 2026.7.1 after 2026.7.0; periodic memory spikes, reporter said restoring the prior version stabilized usage | Closed as stale/not planned on 2026-10-14, not a confirmed universal fix. Maintainer requested safe-mode reproduction. Separate Core/apps/custom-code load before attribution. |
| [New Green, missing add-ons](https://community.home-assistant.io/t/new-ha-green-add-ons-not-available-under-settings/1002982), 2026-04-09 | User could not find the expected menu; replies identified Apps naming/navigation | Verify release/UI/install method before recommending Supervisor installation or changing host type. |

An older version helping one reporter does not prove it is an appropriate rollback for migrated data. “Closed” can mean fixed, duplicate, stale, rejected, or moved.

## Add a record

Capture original URL, date, exact model/revision, Core/OS/integration versions, route, symptom, reproduction, mitigation, confirmed outcome, and uncertainty. Write “not provided” for missing facts; do not infer firmware from publication date.

Prefer reports with traces, narrow regression ranges, and maintainer-confirmed fixes. Scope positive reports to the tested features: switching success does not establish telemetry, OTA, or offline recovery. Use official docs/code for semantics and support; firsthand discussions generate experience evidence and hypotheses.
