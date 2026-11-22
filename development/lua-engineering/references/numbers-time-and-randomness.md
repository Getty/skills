# Numbers, time and randomness

## Contents

- Establish the numeric representation
- Validate arithmetic contracts
- Choose the correct clock
- Control randomness and replay
- Test boundary behavior

## Establish the numeric representation

Inspect the exact runtime/build rather than assuming every Lua number is a double. Standard PUC 5.3+ has integer and floating subtypes; configuration can change integer and float widths. Arithmetic overflow for integer operations follows the manual's wraparound semantics. LuaJIT and Luau have their own numeric and native-value behavior. [Source: Lua 5.5 values/types](https://www.lua.org/manual/5.5/manual.html#2.1); read luajit-and-luau.md for those implementations.

Record whether values are identifiers, counts, measurements, fixed-point quantities or money. Choose the representation according to the domain and every serialization/native boundary, not only the arithmetic available in the source language.

| Domain | Recommended questions |
|---|---|
| IDs | Must values round-trip through JSON/JavaScript or a double-only host? |
| Counts | Maximum, minimum, integer exactness and overflow behavior? |
| Measurements | Units, tolerance, range and treatment of nonfinite values? |
| Currency/decimal | Decimal arithmetic library or bounded integer minor units? |
| Coordinates | Local/world space, float precision, origin and conversion? |
| Bit fields | Runtime operator syntax, signedness and field widths? |

PUC 5.3+ floor division and bitwise syntax will not parse in ordinary 5.1/5.2 code. A runtime if statement cannot rescue syntax the parser rejects. Put syntax-specific implementations in separately selected modules or compile controlled diagnostic strings. [Sources: arithmetic and bitwise operators](https://www.lua.org/manual/5.5/manual.html#3.4.1), [5.1 manual](https://www.lua.org/manual/5.1/manual.html).

## Validate arithmetic contracts

Check type, finiteness, allowed range and integrality before arithmetic at an external boundary. Do not allow numeric coercion to silently turn an identifier string into a different value. For exact-count code, reject fractional or out-of-range inputs deliberately.

~~~lua
-- Original bounded-count predicate, compatible with PUC 5.1+.
local function is_count(x)
    return type(x) == "number" and x == x
        and x >= 0 and x <= 2147483647 and x == math.floor(x)
end
~~~

The chosen cap is an application limit, not Lua's universal maximum. Bound multiplication before computing it, and addition using remaining capacity. Test the target runtime's integer/float transitions if the application operates near representation limits.

Do not assume equality of independently computed floats. Select tolerance based on units, error accumulation and the algorithm, or use an exact representation if exact equality is required. Keep tolerance out of identity keys and structural schema versions.

NaN does not compare equal to itself; mathematical libraries and division can produce values unsuitable for ordering or persistence. Decide whether to reject, propagate or explicitly encode them. Never use a NaN table key. [Source: values/types and table indexing](https://www.lua.org/manual/5.5/manual.html#2.1).

## Choose the correct clock

os.clock reports an approximation of CPU time, not a universal elapsed monotonic clock. os.time represents host-system time and os.date formats it; timezone and platform semantics matter. [Sources: os.clock](https://www.lua.org/manual/5.5/manual.html#pdf-os.clock), [os.time](https://www.lua.org/manual/5.5/manual.html#pdf-os.time), [os.date](https://www.lua.org/manual/5.5/manual.html#pdf-os.date).

Inject a monotonic host clock for timeouts/elapsed durations, a wall-clock source for timestamps, and explicit ticks or supplied durations for simulation. Test wall-clock jumps independently from deadline behavior. Do not assume a standard high-resolution timer exists in every embedded host.

For fixed-step systems, specify what happens when real time exceeds the catch-up budget: catch up, slow simulation, skip presentation, or explicitly drop time. Bound accumulated work; never let a stalled frame generate an unbounded callback storm. This is application design, not a Lua language guarantee.

## Control randomness and replay

Use math.random for appropriate pseudorandom tasks, with the selected runtime's range and seeding rules. PUC 5.4/5.5 provide a two-component seed interface; older runtimes differ. Random functions are not documented as a cryptographic randomness source. Use a suitable host capability for tokens or cryptographic operations. [Sources: math.random](https://www.lua.org/manual/5.5/manual.html#pdf-math.random), [math.randomseed](https://www.lua.org/manual/5.5/manual.html#pdf-math.randomseed).

For reproducible domain tests, inject a deterministic source or fixed stream. For replay, record the algorithm/version, seed/state, draw ordering and all external inputs that affect decisions. Avoid one implicit global generator shared by unrelated systems if adding a cosmetic draw would change authoritative decisions.

Do not promise identical output across runtime upgrades, different implementations, native libraries or nondeterministic iteration order merely because a seed is fixed. Lockstep needs a complete agreement about update order, numeric behavior, RNG and host calls. Server-authoritative state synchronization can be a simpler requirement when exact lockstep is unnecessary.

## Test boundary behavior

Include zero, negative values, fractions, maximum permitted counts, overflow attempts, NaN/infinity, large external IDs, units conversion and serialization round trips. Test clock rollback, long stalls, zero elapsed time and deterministic RNG fixtures where relevant. Compare invariants or expected ranges when exact floating-point equality is not the intended contract.
