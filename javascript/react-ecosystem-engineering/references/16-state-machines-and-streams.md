# XState, state machines, and reactive streams

**Read when:** workflows have many asynchronous stages, cancellations, or illegal state combinations.

## When explicit machines help

Model a workflow with named states, events, guards, effects, and cancellation semantics when boolean flags permit contradictory combinations. Examples include upload/retry/cancel, multi-step authorization, device connection, and a job runner. Do not use a state machine merely to store a text field. XState's React integration connects actors to UI; inspect the installed major rather than copying older interpreter APIs.

Define what owns each actor, whether it survives route changes, how it stops, and which state can be persisted. Treat events from network, IPC, and plugins as untrusted input. An event name does not authorize the requested transition. External effects should return structured outcomes instead of mutating UI state through unrelated callbacks.

## Design artifact

Write a transition table with current state, event, guard, next state, side effect, and failure outcome. Include timeout, cancellation, duplicate event, and restart after crash. Separate a durable backend job from the UI's observation of that job. Losing a renderer should not silently redefine whether an acknowledged server operation completed.

RxJS and other stream libraries are discovery options for composition of event streams, backpressure, and cancellation. Verify their current operators and React adapters before writing integration code. A subscription is still a resource requiring teardown; wrapping a promise in a stream does not automatically cancel its underlying operation.

## Acceptance

Generate or handwrite event sequences that try every prohibited transition. Complete an obsolete request after cancellation. Deliver duplicate completion events. Restart from persisted data with an incompatible schema. Verify that the visual status is a projection of the machine rather than a second independently editable set of flags. Keep pure transition tests independent of React, then test actor lifecycle at the component boundary.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R23: XState React integration](https://stately.ai/docs/xstate-react)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
