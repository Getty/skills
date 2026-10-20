# Production client design

Read when integrating an API, web application, batch producer or command-line tool. Evidence: [G3, C1, C3, P1, Y1](sources.md). Most controls below are application design requirements.

## Submission contract

Define whether the caller needs an immediate result or only durable acceptance of a business request. Generate the business request ID before the first possible network write. Keep the function name/version, schema, payload hash, origin endpoint and creation time with application state. Use a distinct attempt/delivery identity when the application's retry design requires it.

Validate the payload before occupying network capacity. Limit batch size, pending futures, outstanding bytes and retry queue length. Prefer object storage references for large artifacts, but make those references integrity-checked, access-controlled and sufficiently long-lived for the retry window. Do not enqueue expiring credentials whose lifetime is shorter than worst-case backlog.

## Connection policy

Use long-lived connections when supported and useful, but allocate clear ownership per process/thread/event loop. Set explicit connection and operation budgets. Back off reconnect attempts with jitter and an upper bound. Circuit breaking should prevent an unavailable job service from consuming every web request thread.

Inspect the chosen binding's automatic reconnect and multi-server selection. An API named add_server may merely add configuration and perform no I/O immediately. Initialization success is not proof of a reachable server. A producer should distinguish failure to connect from uncertain outcome after partial submission.

## Results and errors

Map outcomes into domain terms: validation rejected; accepted/in progress; completed; terminal business failure; infrastructure failure with known non-acceptance; unknown outcome requiring reconciliation. Do not treat every falsey payload as failure: empty bytes, zero and false can be valid business results. Check the transport return code and then parse the result contract.

Treat progress as optional advisory information. Protect the client from huge or frequent data/warning events. Retain only what the application actually needs, and apply a total deadline that cannot be extended forever by progress packets.

## Retry ownership

Pick one owner for logical retries, normally the application dispatcher/outbox workflow rather than every client layer simultaneously. A web framework retry, transport retry and worker retry can multiply into a storm. Preserve request identity across caller retries; decide explicitly when a fresh transport unique key is required. Enforce a maximum age as well as a maximum attempt count.

## Practical review

Before release answer: Does a timeout cause an unsafe blind resend? Can a slow server exhaust the caller pool? Are old/new schemas accepted during rollout? Does a background response clearly say accepted rather than completed? Can every accepted request be reconciled independently of its Gearman handle? Are secrets absent from payloads and diagnostics? Do tests exercise reverse-order completions and ambiguous sends?

The Python CLI demonstrates these distinctions but not a production pool. For concurrent use implement or adopt a tested adapter rather than sharing one `Session` instance across callers.
