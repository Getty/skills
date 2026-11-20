# Troubleshooting

## Reproduce a complete decision

Collect modules, exact query, input, relevant data, runtime version, profile, and
capabilities. Preserve the integration envelope until it is proven irrelevant.
A reduced condition without its real data path often hides the original failure.

| Symptom | First checks |
| --- | --- |
| Parser expects `if`/`contains` | Source dialect versus selected parser |
| Unsafe variable | Scope, spelling, binding, or negated use |
| Unexpected undefined | Missing path, failed built-in, wrong query, legacy negation |
| Output conflict | Complete rules deriving incompatible values |
| False despite matching role | Tenant gate, envelope, role type, identity status |
| Permission with violations | Consumer ignores `deny` or wrong entrypoint |
| CLI succeeds, controller fails | Embedded version, code engine, envelope |
| New rule has no effect | Active bundle and actual query path |
| Intermittent disagreement | Data snapshots, cached answers, rollout, mutable resource |

Preserve parse, compile, and evaluation error categories. Consult the
[errors guide](https://www.openpolicyagent.org/docs/errors) for the actual message.

## Investigate undefined

Query intermediate documents and locate the missing dependency. Check explicit
null separately from absence. Strict built-in errors can expose malformed values
where supported; production error behavior is a separate decision. Do not add a
permissive default simply to obtain a Boolean.

For negation, determine whether a nested reference or call failed before legacy
negation applied. New imports can repair one case while changing others, so replay
the compatibility corpus rather than changing syntax blindly.

## Investigate deployment

Observe the actual enforcement point's answer and active revisions. A healthy
management endpoint may coexist with stale policy. Confirm the client uses the
right path and understands the selected Boolean/object response contract.

Exercise true, false, missing result, null, wrong type, malformed JSON, error object,
timeout, and HTTP failure. Check both the external outcome and the diagnostic signal.
A generic “denied” response may be appropriate externally but should not erase an
internal evaluator outage.

## Close the defect

Retain a minimal regression case that would fail before the repair. Explain the
incorrect assumption, changed logic/integration, and observed tests. Stop optional
verification after concrete risks and required gates are covered. An ever-growing
list of unrelated checks can make the evidence harder to assess rather than stronger.
