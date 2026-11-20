# Engines and integration

## Compare the needed capability profile

Choose an implementation by required constructs and operational constraints. Inspect
its actual version and documentation before recommending a package. Use
[Apache KIE's DMN documentation](https://kie.apache.org/drools/dmn/), the
[Camunda DMN profile](https://docs.camunda.io/docs/components/modeler/dmn/), and
[versioned TCK submissions](https://dmn-tck.github.io/tck/index.html) as starting
points. A FEEL interpreter alone is not a DMN engine, and a modeler alone does not
supply execution.

Record support for interchange versions, FEEL/B-FEEL, boxed forms, all required hit
policies, type definitions, imports, BKMs, decision services, external function
kinds, and diagnostics. Match the runtime used in production to the one measured.
Do not rely on a dashboard percentage without examining missing and unsupported
cases relevant to this model.

## Define the execution adapter

Expose an entry point with model identity/version, decision/service identifier, and
a typed input context. Normalize application data once at the boundary. Prefer
stable unit conventions, exact decimal conversion where required, and explicit
serialization for dates/durations. Do not let an absent JSON field silently become
a string `"null"` or a host zero value.

Return an envelope that distinguishes decision value, null/no-hit outcome, invalid
input, unsupported model, technical failure, and diagnostics. Capture matched-rule
or decision traces only to the degree the runtime actually supplies them. An
annotation or synthetic explanation must not be reported as an engine trace.

## Integrate with processes and services

BPMN/workflow code can invoke a DMN decision and act on its result. Keep retries and
idempotency around external actions in the process/application layer. Re-evaluating
a model during debugging should not resend an email or execute a transaction.
A decision such as `eligible=true` is not itself access enforcement.

Select in-process evaluation for low-latency local integration when dependencies
fit the host. Select a service boundary when independent deployment, centralized
models, or multiple caller languages justify the operational cost. Neither choice
changes the DMN semantics; both need explicit model version selection.

## Cache and observe safely

Compile/parse models once where the engine permits it. Cache results only with all
semantic inputs: model version, input values, external function versions, relevant
reference time, and data snapshot identifiers. Avoid caching a decision merely by
customer ID when other facts may change.

Measure parse/compile time separately from evaluation time, and report latency
under realistic input sizes and concurrency. Bound model/input size and expensive
custom functions. Redact sensitive facts from routine logs while retaining the
minimum provenance needed to reproduce the decision under appropriate access.
