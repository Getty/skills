# Source register and evidence policy

Reviewed **2026-10-14**. URLs point to primary project material, official language-library documentation, or inspected upstream source. This is a curated evidence register, not an assertion that every optional component was installed or executed.

## Evidence precedence

For version-sensitive behavior use the deployed binary's help/build information and reproducible tests, then the matching tagged source and release notes. Website pages may mix generations: the public options page still displayed the old retry default during this review. A current documentation build hash is not the same as the deployed server version. Recommendations in this skill are engineering proposals, not undocumented product promises.

## Server and protocol

| ID | Source | Scope |
|---|---|---|
| G1 | https://github.com/gearman/gearmand/releases | 2.1.0 and 2.0.0 release notes; current baseline discovery |
| G2 | https://gearman.org/manual/job_server/ | Historical architecture/persistence explanation, not current option defaults |
| G3 | https://gearman.org/protocol/ | Binary framing, packet field layout, administrative protocol |
| G4 | https://gearman.org/gearmand/gearmand/ | Server options; explicitly cross-check stale sections |
| G5 | https://gearman.org/gearmand/bin/gearman/ | CLI syntax, milliseconds, ECHO probe, TLS environment names |
| G6 | https://gearman.org/gearmand/bin/gearadmin/ | Administrative CLI and mutation surfaces |
| G7 | https://gearman.org/gearmand/protocol/text/ | Native administrative commands and shared port |
| G8 | https://gearman.org/gearmand/gearmand/ssl/ | Native TLS build requirements and certificate guidance |
| G9 | https://gearman.org/gearmand/gearmand/queues/ | Backend overview; not an exhaustive current build inventory |
| G10 | https://gearman.org/gearmand/gearmand/queues/sqlite/ | SQLite schema example, historical version qualifier |
| G11 | https://gearman.org/gearmand/gearmand/queues/postgres/ | libpq configuration and historical schema |
| G12 | https://gearman.org/gearmand/gearmand/queues/mysql/ | MySQL backend documentation |
| G13 | https://gearman.org/download/ | Implementation distinctions; historical project list |

## Tagged source actually inspected

Tag `2.1.0` resolves to commit `516ffac9376a533413a748eef9295808f1bf319a`. Source was read through GitHub; fetching a buildable archive into the execution container was blocked. No third-party source tree is bundled.

| ID | Source | Inspected behavior |
|---|---|---|
| S1 | https://github.com/gearman/gearmand/blob/2.1.0/libgearman-server/job.cc | Function-scoped unique lookup; empty and `-` unique handling; queue limit admission; persistence enqueue; retry/drop path; epoch wakeup |
| S2 | https://github.com/gearman/gearmand/blob/2.1.0/libgearman-server/server.cc | CAN_DO/TIMEOUT, PRE_SLEEP, GRAB_JOB variants; WORK_COMPLETE/FAIL/EXCEPTION cleanup; exception negotiation; unsupported scheduled packet case |
| S3 | https://github.com/gearman/gearmand/blob/2.1.0/libgearman-server/queue.h | Queue add/flush/done interface shape |
| S4 | https://api.github.com/repos/gearman/gearmand/git/trees/2.1.0?recursive=1 | Tag commit and source-tree inventory; not proof every listed file was reviewed |

Important inspected ranges: `job.cc` around `gearman_server_job_add_reducer()` and lines 460–660; `server.cc` lines 450–955; `queue.h` lines 40–end. Prefer function names over line numbers when updating. Search results from the default branch were used only for navigation, not silently substituted for tagged semantics.

## Language interfaces

| ID | Source | Scope |
|---|---|---|
| C1 | https://gearman.org/gearmand/libgearman/gearman_client_do/ | C single-job API, return codes and result ownership |
| C2 | https://gearman.org/gearmand/libgearman/gearman_worker_add_function/ | Callback registration and context |
| C3 | https://gearman.org/gearmand/libgearman/gearman_client_add_task_background/ | Background task API |
| C4 | https://gearman.org/gearmand/libgearman/gearman_client_add_task_status/ | Task status polling API |
| C5 | https://gearman.org/gearmand/libgearman/gearman_worker_error/ | Error accessor API |
| P1 | https://metacpan.org/pod/Gearman::Client | Classic Perl binding; scalar-reference result; explicit unique recommendation |
| P2 | https://metacpan.org/pod/Gearman::Worker | Registration, callbacks, prefixes, stop_if and worker methods |
| P3 | https://metacpan.org/pod/Gearman::XS | XS/libgearman relationship |
| P4 | https://metacpan.org/pod/Gearman::XS::Client | XS return tuples; timeouts and task callbacks |
| P5 | https://metacpan.org/pod/Gearman::XS::Worker | XS worker API |
| P6 | https://metacpan.org/pod/Gearman::XS::Job | XS job API |
| P7 | https://metacpan.org/pod/AnyEvent::Gearman::Client | Asynchronous Perl candidate; not locally installed |
| P8 | https://metacpan.org/pod/EV::Gearman | Search-indexed documentation describes a direct-protocol XS/EV implementation; full page fetch failed, so detailed API claims are intentionally omitted |
| P9 | https://github.com/p-alik/perl-Gearman/blob/master/lib/Gearman/Worker.pm | Inspected callback/exception and stop loop code, lines 350–530, blob 7d0cd257bf366d62374b28b7c23bfca1d8259689; default branch, not a pinned CPAN release |
| H3 | https://www.php.net/manual/en/gearmanworker.addfunction.php | Worker callback API |
| H4 | https://www.php.net/manual/en/gearmanjob.sendfail.php | Explicit terminal failure method |
| H1 | https://www.php.net/manual/en/book.gearman.php | PHP extension classes and methods |
| H2 | https://www.php.net/manual/en/gearman.examples-reverse-bg.php | Background result behavior |
| Y1 | https://docs.opendev.org/opendev/gear/latest/ | Python gear API, reconnect model, explicitly non-production test server |

## Deployment API references

| ID | Source | Scope |
|---|---|---|
| O1 | https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/ | Stable identity/storage/controller concepts; target-cluster verification still required |
| O2 | https://kubernetes.io/docs/concepts/services-networking/network-policies/ | Network-policy semantics and enforcement requirements |
| O3 | https://docs.docker.com/reference/compose-file/services/ | Compose service configuration, dependencies and lifecycle |

The systemd upstream manual fetch failed during this review. Units are conservative
unapplied examples and must be checked with the installed systemd version and local policy.

## Update procedure

Record the new date/tag/commit, diff relevant source paths, recapture local binary help, rerun the release acceptance matrix, and update [the validation report](../VALIDATION.md). Do not replace source-derived claims with search snippets. For a library not listed here, inspect its own repository, release history, supported runtimes, API, and failure tests before providing exact installation or TLS instructions.
