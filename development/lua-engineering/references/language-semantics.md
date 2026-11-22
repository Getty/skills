# Language semantics that cause application defects

Scope: PUC Lua 5.1–5.5 unless marked otherwise. Reviewed 2026-11-22. Examples are intentionally small enough to turn into regression probes.

## Contents

- [Truth, absence, and defaults](#truth-absence-and-defaults)
- [Numbers and arithmetic](#numbers-and-arithmetic)
- [Scope, closures, and calls](#scope-closures-and-calls)
- [Multiple results and nil-bearing tuples](#multiple-results-and-nil-bearing-tuples)
- [Control flow and review procedure](#control-flow-and-review-procedure)

## Truth, absence, and defaults

Only `false` and `nil` are false in a condition. Zero, the empty string, and an empty table are true. Assigning `nil` to a table field removes that field; `false` remains a stored value. [Values and types](https://www.lua.org/manual/5.4/manual.html#2.1).

Use presence checks when `false` or zero is a legitimate setting:

```lua
local function with_default(value, fallback)
    if value == nil then return fallback end
    return value
end
assert(with_default(false, true) == false)
assert(with_default(0, 10) == 0)
```

`value or fallback` deliberately substitutes for both false values. The expression `condition and a or b` fails as a general conditional expression when `a` may be false or nil. Use `if` for such cases. Do not compare arbitrary results to `true` unless the API promises a boolean; values can be truthy without equaling `true`. [Logical operators](https://www.lua.org/manual/5.3/manual.html#3.4.5).

At external boundaries, separate these cases in validation: field absent; field explicitly false; empty string; empty collection; wrong type. Application protocols may need an explicit null sentinel because a plain table cannot store a nil-valued entry.

## Numbers and arithmetic

PUC Lua 5.3+ distinguishes integers and floats. Default builds use 64-bit integers and double-precision floats, but configuration can change this. Integer arithmetic can wrap; floating-point conversion can lose integer precision. Inspect the actual runtime instead of inferring numeric layout from `_VERSION`. [5.3 values](https://www.lua.org/manual/5.3/manual.html#2.1), [configuration macros](https://www.lua.org/source/5.5/luaconf.h.html).

For PUC 5.3+:

```lua
assert(7 / 2 == 3.5)
assert(7 // 2 == 3)
assert(-7 // 2 == -4)
assert(-7 % 2 == 1)
assert(3 == 3.0)
assert('3' ~= 3)
```

Floor division and modulo use floor-oriented arithmetic. Integer division by zero is an error; do not generalize all float exceptional values into errors. Validate denominator and finite-number requirements at the application boundary. [Arithmetic](https://www.lua.org/manual/5.3/manual.html#3.4.1), [VM implementations `luaV_idiv`, `luaV_mod`](https://www.lua.org/source/5.5/lvm.c.html#luaV_idiv).

Avoid relying on implicit string-to-number arithmetic. Parse with `tonumber`, validate the result and range, and keep IDs separate from quantities. Use a fixed binary or textual representation when round-tripping values between Lua, C, JSON, databases, and other languages.

`^` binds more tightly than unary minus: `-2^2` means `-(2^2)`. Concatenation and exponentiation associate to the right. Parenthesize mixed expressions for reviewability, especially generated code. [Precedence](https://www.lua.org/manual/5.2/manual.html#3.4.7).

## Scope, closures, and calls

Local declarations take effect after their initializer. Therefore `local x = x` reads an outer binding on the right. Closures capture variables, so changing a captured variable affects later calls. [Visibility rules](https://www.lua.org/manual/5.4/manual.html#3.5).

Use `local function name(...)` for local recursion, or predeclare a local before assigning its function:

```lua
local function countdown(n)
    if n == 0 then return 'done' end
    return countdown(n - 1)
end
assert(countdown(3) == 'done')
```

A method call `object:method(x)` passes `object` as the first argument. Match the declaration and call conventions; passing a colon-defined method as a callback does not automatically bind its receiver. Prefer a closure when the callback signature has no receiver argument. [Function calls](https://www.lua.org/manual/5.1/manual.html#2.5.8).

```lua
local counter = { n = 0 }
function counter:add(delta) self.n = self.n + delta end
local callback = function(delta) counter:add(delta) end
callback(2)
assert(counter.n == 2)
```

For callbacks stored beyond their creator's lifetime, review every captured object for retention, validity, and cancellation. Capturing a local is an ownership decision even when the syntax looks small.

## Multiple results and nil-bearing tuples

Lua adjusts expression lists. A final function call or vararg expression can expand; most other positions keep one result. Parentheses force one result. Return forwarding must preserve the intended cardinality. [Expression-list adjustment](https://www.lua.org/manual/5.5/manual.html#3.4.12).

```lua
local function values() return 'a', nil, 'c' end
local function pack(...) return { n = select('#', ...), ... } end
local expand = table.unpack or unpack
local a = pack(values())
local b = pack((values()))
assert(a.n == 3 and a[2] == nil and a[3] == 'c')
assert(b.n == 1)
assert(select('#', expand(a, 1, a.n)) == 3)
```

Use an explicit count when trailing or internal nil values matter. `#tuple` is not tuple arity, and `ipairs` does not enumerate nil holes. Forward with `return callback(...)` when all results belong to the API. Use one-result assignment when deliberately adapting a multi-result function to a scalar interface.

A function returning no results differs from one returning a single nil in a context that preserves cardinality. Include both in callback adapters, event systems, protected-call wrappers, and serialization tests. [Basic library `select`](https://www.lua.org/manual/5.1/manual.html#pdf-select).

## Control flow and review procedure

PUC Lua has no general `continue` statement. Refactor into a helper, use conditional structure, or use a carefully scoped `goto` only where the supported parser allows it. Generic iteration ends when its control result becomes nil; false can still be a valid iterator result. [5.2 control structures](https://www.lua.org/manual/5.2/manual.html#3.3.4), [for statement](https://www.lua.org/manual/5.2/manual.html#3.3.5).

When reviewing a suspicious expression:

1. Write down the exact values and their types; do not substitute JavaScript/Python/C truthiness.
2. Expand colon syntax and implicit argument/result adjustments.
3. Identify the binding each free name resolves to.
4. Remove side effects from compound expressions before comparing outcomes.
5. Run a tiny assertion on the target interpreter and then test the real host path.

Keep these probes in meaningful regression tests when they protect a public API or a previously observed failure. Avoid adding dozens of tests that only restate trivial assignments.
