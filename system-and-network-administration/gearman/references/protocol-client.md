# Client protocol state machine

Read alongside [framing](protocol-framing.md). Evidence: [G3, S2](sources.md).

## Minimal foreground sequence

Open a verified connection. Negotiate optional features you need, such as exception delivery, and wait for the matching option response. Submit function, explicit unique key and workload with the chosen priority. Receive `JOB_CREATED` and remember its handle. Route subsequent work events by that handle until a terminal event arrives. Clean up client-side state even when the server rejects or disconnects.

`WORK_DATA`, `WORK_STATUS` and `WORK_WARNING` do not by themselves establish successful completion. `WORK_COMPLETE` carries the final payload; `WORK_FAIL` is a terminal failure. The inspected 2.1 C server also removes a job on `WORK_EXCEPTION`; do not implement exception handling as an unconditional wait for a later `WORK_FAIL`. Check the server/binding pair if it behaves differently.

## Background sequence

The background submission variant returns a created handle but not a subscription to durable future results. Save application identity and origin endpoint. A live `GET_STATUS` query provides current knowledge/progress, not a durable business outcome. Build an independent outcome query when results matter.

## Multiplexing correctly

A full asynchronous client may have multiple submissions outstanding and interleaved work events. Correlate creation replies with the submission ordering mechanism defined by your implementation, then switch to handle-based routing for work events. Never match final responses by “first request still waiting.” Reconnects invalidate connection-local assumptions.

Bound pending submissions, aggregate incoming data, callback work, result bytes and application waiters. A callback that performs a slow synchronous database query can stall the entire event loop. Cancellation of a local future must not be confused with cancellation of remote work.

## Failure classification

Distinguish local validation failure before transmission, connection establishment failure, explicit server rejection, explicit terminal worker failure, and transport loss after a send could have arrived. The last is **outcome unknown**, even when no handle was received. Do not silently reconnect and resend side-effecting work as a convenience feature.

The lab uses one foreground request at a time and exposes `OutcomeUnknown`; it deliberately omits transparent resubmission. It closes connections after command-line use and reports unexpected protocol states rather than trying to salvage a possibly desynchronized stream. Its end-to-end timeout covers submission through terminal response, while OS name resolution may have its own resolver behavior.

## Tests to port to a real binding

Inject a split header, multiple events in one read, a handle mismatch, an exception-only terminal event, an empty successful result, server EOF after submission, and an endless stream of progress that exceeds the overall deadline. Repeat with two concurrent jobs completing in reverse order for a multiplexed implementation. These tests validate your adapter; an ECHO test alone cannot.
