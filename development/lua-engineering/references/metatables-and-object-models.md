# Metatables and maintainable object models

Scope: PUC Lua 5.1–5.5 with explicit gates. Reviewed 2026-11-22. Prefer the smallest object model that makes ownership and invariants visible.

## Contents

- [Understand the dispatch boundary](#understand-the-dispatch-boundary)
- [A small object pattern](#a-small-object-pattern)
- [Proxies and read-only views](#proxies-and-read-only-views)
- [Operators and inheritance](#operators-and-inheritance)
- [Lifetime and diagnostics](#lifetime-and-diagnostics)

## Understand the dispatch boundary

Metatables customize selected operations; they are not a universal interception mechanism. For table access, `__index` handles a missing entry and `__newindex` handles assignment to an absent entry. Existing stored fields are accessed or overwritten directly. Raw operations deliberately bypass these hooks. [Metatable semantics](https://www.lua.org/manual/5.4/manual.html#2.4), [VM `luaV_finishget`/`luaV_finishset`](https://www.lua.org/source/5.5/lvm.c.html#luaV_finishget).

| Symptom | Likely misunderstanding | Diagnostic |
|---|---|---|
| Validation only happens on the first assignment | `__newindex` stored the field on the object | Compare raw fields before and after assignment |
| Infinite recursion on property access | Hook reads/writes the same missing property | Use a separate backing store or intentional raw operation |
| A stored false value triggers a fallback | Hook tests truthiness instead of nil | Check `value ~= nil` |
| A method receives the wrong first parameter | Colon/dot conventions differ | Expand the implicit `self` argument |
| Parent methods work but an operator does not | Method lookup and metamethod lookup were conflated | Inspect the instance's actual metatable |

Do not add metatables to plain records merely to make them look object-oriented. Data passed between jobs, saved state, or wire messages is often easier to validate as ordinary fields.

## A small object pattern

The following pattern parses on PUC 5.1–5.5 and keeps methods shared while instance data is separate:

```lua
local Counter = {}
Counter.__index = Counter

function Counter.new(initial)
    assert(type(initial) == 'number', 'initial must be numeric')
    return setmetatable({ value = initial }, Counter)
end

function Counter:add(delta)
    assert(type(delta) == 'number', 'delta must be numeric')
    self.value = self.value + delta
    return self.value
end

local a, b = Counter.new(1), Counter.new(10)
assert(a:add(2) == 3)
assert(b.value == 10)
```

This is a design convention, not built-in class syntax. If invariants require every mutation to be checked, hide storage or expose explicit operations; the example's public `value` field is intentionally writable. [setmetatable](https://www.lua.org/manual/5.1/manual.html#pdf-setmetatable), [method syntax](https://www.lua.org/manual/5.1/manual.html#2.5.8).

Decide whether constructors return plain tables, userdata wrappers, or opaque handles. Decide whether methods mutate, return new objects, or borrow host resources. Document these choices as API behavior.

## Proxies and read-only views

An empty proxy can route ordinary reads to separate data and reject ordinary writes:

```lua
local function read_view(backing)
    return setmetatable({}, {
        __index = backing,
        __newindex = function() error('read-only view', 2) end,
        __metatable = 'locked view',
    })
end
```

This provides a cooperative API boundary. It is **shallow**, nested tables remain shared, `rawset` can modify the proxy, and privileged debug access can bypass metatable protection. Do not call it a hostile-code sandbox. Iteration and length also require explicit behavior; `__pairs` and table `__len` are unavailable in stock 5.1. [5.1 metatables](https://www.lua.org/manual/5.1/manual.html#2.8), [5.2 pairs](https://www.lua.org/manual/5.2/manual.html#pdf-pairs), [5.2 length](https://www.lua.org/manual/5.2/manual.html#3.4.6).

For a mutable proxy, keep the proxy empty if every ordinary write must pass through validation. Store data elsewhere, validate the incoming value, then update that backing data. Avoid exposing a helper that returns the backing table unless escape is part of the contract. For persistent settings, an explicit `set_option(name, value)` is often easier to inspect and audit.

## Operators and inheritance

Choose operator overloads only when their meaning is unsurprising: vectors, ranges, immutable quantities, or a controlled domain algebra. Specify mixed-operand behavior and whether an operation allocates. Test both operand orders. Do not assume an operand's `__add` is consulted symmetrically or that an equality rule changes table-key identity. [Current dispatch events](https://www.lua.org/manual/5.5/manual.html#2.4), [tag method implementation](https://www.lua.org/source/5.5/ltm.c.html).

Inheritance through a method table's `__index` does not automatically propagate every metamethod to instance metatables. Install the intended metamethods explicitly. Keep parent delegation visible and avoid a large implicit multiple-inheritance search chain unless a real use case requires it.

When migrating, specifically test `__eq`, `__lt`, `__le`, `__len`, `__pairs`, and historical `__ipairs`. Their availability or fallback rules have changed across PUC versions. A small native test on the target runtime is stronger evidence than reproducing a remembered metamethod algorithm. [5.2 incompatibilities](https://www.lua.org/manual/5.2/manual.html#8), [5.3 incompatibilities](https://www.lua.org/manual/5.3/manual.html#8).

## Lifetime and diagnostics

- Use explicit ownership and release methods for host resources. Finalizers are a fallback mechanism; inspect their exact runtime rules and the host's lifetime model.
- Weak tables support specific cache relationships. They do not replace ownership or guarantee a resource survives until the next frame.
- Ordinary method tables can accidentally retain instances through event handlers, reverse indexes, and closure captures. Trace the entire reference graph when memory grows.
- A `<const>` binding in 5.4+ makes the binding immutable; it does not freeze fields of the referred table.

Sources: [GC and weak tables](https://www.lua.org/manual/5.4/manual.html#2.5), [const declarations](https://www.lua.org/manual/5.4/manual.html#3.3.7), [finalization implementation](https://www.lua.org/source/5.5/lgc.c.html).

For a failing object, inspect its raw fields, actual metatable, `__index` target, captured references, and host validity before adding another wrapper. Reproduce the issue without inheritance first; restore one layer at a time until the dispatch boundary is clear.
