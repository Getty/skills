# Community evidence and maintenance lessons

Reviewed 2026-10-22. These original upstream reports give context; they do not rank reliability or establish prevalence.

| Record | Exact scope | Outcome and lesson |
| --- | --- | --- |
| [Mushroom 1771](https://github.com/piitaya/lovelace-mushroom/issues/1771), maintainer notice 2025-09-11 | Mushroom 5 Template Card redesign affects prior theme/card-mod assumptions | Maintainer describes migration/legacy alternatives. Preserve working dashboard config and inspect CSS version coupling. |
| [Mushroom 1848](https://github.com/piitaya/lovelace-mushroom/issues/1848), 2026-02-02 | User report: Mushroom 5.0.8/5.0.10 with frontend 20260128.2/.3 generated duplicate button calls; native card did not | Closed through PR 1850 on 2026-02-04; later user reported update fixed behavior. Do not present as a current unresolved universal bug. |
| [Adaptive Lighting 1273](https://github.com/basnijholt/adaptive-lighting/issues/1273), 2025-10-13 | User requested attribute-scoped manual control; model/HA version not supplied | Closed 2026-01-07 as implemented in PR 1356. A formerly missing feature may now exist; recheck current installed docs. |

## How to use a report

Match release, route, exact model, firmware, and symptoms. Read the comments/linked fix and determine whether the report is open, completed, stale, or superseded. State missing details explicitly. Distinguish author observation from diagnosis proposed by commenters.

Build a reversible test around the useful distinction: native versus custom card, one light versus a mixed group, one controller versus competing schedules, previous versus current code with a coherent restored state. Do not downgrade household software solely because a search found an old complaint.

Maintain positive evidence with the same specificity: a user confirming the fix for a button action demonstrates that path, not all card features. Avoid invented labels such as “community consensus” unless a real structured body of evidence supports them.
