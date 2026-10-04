# Workflows and monitors

## Choose the lifecycle

Use a workflow for a finite orchestrated task. Use a monitor for events throughout an interactive session. Use an external service for persistent delivery or scheduling that must outlive that session. Avoid turning every task into a long-running observer.

## Workflow authoring

Current saved workflows use JavaScript with an exported `meta` block and runtime helpers including `agent`, `pipeline`, and `parallel`. Plugin workflows live in `workflows/` or a declared location and receive the plugin namespace. When available, the installed `/workflow-authoring` material helps inspect the target's runtime helpers; that bundled authoring skill requires v2.1.248. Use the documented runtime contract directly when it is absent. [Dynamic workflows](https://code.claude.com/docs/en/workflows).

Treat orchestration as a plan with explicit data edges:

1. Discover a bounded list of work items.
2. Validate and deduplicate the list.
3. Run independent items under a concurrency and cost budget.
4. Collect successes, partial results, and failures without dropping evidence.
5. Verify the aggregate against the original objective.

Example design specification for an implementation agent:

> Inspect the requested changed files, assign one evidence review per file, cap parallelism at the task's budget, retain the result for every file including failures, and produce one deduplicated report with links to supporting code. Stop after one retry for a transient read failure. Perform no edits.

Do not blindly copy helpers from ordinary Node code. The workflow runtime restricts nondeterministic time/random APIs so replay can reproduce agent calls. Pass a timestamp as input when it is genuinely needed. Stopped or unrecoverable `agent()` work may return `null`; preserve that as incomplete work when completeness matters. [Workflow script and execution model](https://code.claude.com/docs/en/workflows#what-the-saved-script-looks-like).

The `ultracode` keyword has origin-sensitive behavior; a webhook string or `-p` prompt is not equivalent to interactive human opt-in. Use the documented Workflow invocation for the target host instead of relying on a magic word in remote input.

## Monitors

A plugin monitor is a persistent shell command whose output enters the session as notifications. It is an experimental component, limited to supported interactive environments. It does not receive plugin option variables, and disabling the plugin does not necessarily terminate an already-running monitor; current documentation says it stops at session end. [Monitor component](https://code.claude.com/docs/en/plugins/components#monitors).

Implement monitoring with event deduplication, output bounds, backoff, and an explicit shutdown path. Emit meaningful state changes rather than every polling result. Keep secrets out of stdout because notifications are model-visible.

Test start, no-data state, duplicate data, temporary disconnection, process failure, and session end. A command that remains alive is not evidence that it delivers useful events. For unsupported hosts, supply an explicit on-demand status tool or external channel/service.
