# Temporal semantics

## Choose the value kind first

| Kind | Meaning | Avoid |
| --- | --- | --- |
| Date | Calendar year/month/day | Treating it as a UTC instant by default |
| Time | Time of day, possibly with offset | Guessing a date for daylight-saving rules |
| Date-time | Date plus time, with optional offset/zone information | Comparing unrelated local clocks without a contract |
| Days/time duration | Day/hour/minute/second-based duration | Assuming it is a calendar month |
| Years/months duration | Calendar month-based duration | Replacing it with a fixed number of seconds |

Construct values explicitly, for example `date("2024-02-29")` or
`duration("P2M")`. A string containing the same characters remains a string until
converted. Temporal literal shorthand and named-zone handling depend on the
selected grammar and runtime profile.

## Make reference time explicit

Pass an `asOf` date/time as input when results must be reproducible. Calls to
`today()` or `now()` depend on the runtime clock and time-zone policy; they also
change result-cache keys. Record the actual reference value used for an auditable
calculation. Do not interpret a German local date using the executor's UTC date
unless that is the application's contract.

For age, duration, or expiry calculations, state whether the rule is calendar-based
or elapsed-time-based. A month can have different numbers of days, and local days
can be affected by daylight-saving transitions. Define inclusion at the end boundary
rather than hiding it in string comparison.

## Test mixed-zone and calendar cases

Use offset-aware comparisons for instants where appropriate, and deliberately
normalize inputs. Do not claim that every mixed local/offset comparison necessarily
fails: the specification defines conversion/comparison rules, and implementations
have details that must be checked. A safer application contract can reject mixed
representations before evaluation when the business meaning is ambiguous.

Exercise leap day, month end, a daylight-saving transition for the actual zone,
equivalent instants with different offsets, absent offsets, and invalid dates.
For years/months arithmetic, inspect behavior when the destination month lacks the
source day. Do not implement your own date math to mimic an untested engine.

## Preserve result representation

An interpreter may return a temporal object whose JSON serialization loses zone or
kind information. Define an explicit output mapping and test round trips. Use typed
test expectations or compare a Boolean relation within FEEL when a simple JSON
fixture cannot represent the temporal value faithfully.

Read [DMN 1.6 temporal value/operation sections](https://www.omg.org/spec/DMN/1.6/PDF)
and the [selected Camunda profile](https://docs.camunda.io/docs/components/modeler/feel/language-guide/feel-temporal-expressions/).
Treat time-zone database and external clock versions as relevant runtime inputs
when their changes can affect a decision.
