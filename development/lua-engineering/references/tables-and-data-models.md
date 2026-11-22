# Tables, collections, and explicit data models

Scope: PUC Lua; version differences are identified below. Reviewed 2026-11-22. Data-structure recommendations are design choices, not claims that Lua requires one architecture.

## Contents

- [Choose a collection contract](#choose-a-collection-contract)
- [Length and iteration](#length-and-iteration)
- [Identity, copying, and keys](#identity-copying-and-keys)
- [Deterministic order](#deterministic-order)
- [Mutation and validation](#mutation-and-validation)

## Choose a collection contract

A table can represent several application concepts, but its users need one explicit contract:

| Concept | Suggested representation | Invariant to check |
|---|---|---|
| Dense list | Numeric keys `1..n` | No holes; order has a defined meaning |
| Sparse index | Numeric-key map plus explicit metadata | Length is not inferred with `#` |
| Dictionary | Keys to values | Absence and false are distinct |
| Set | Keys mapped to true | Keys have a canonical identity |
| Tuple with nils | Numeric fields plus `n` | Arity survives trailing nils |
| Queue | Storage plus head/tail indices | Empty state and compaction are explicit |
| Entity registry | Stable ID to record | ID lifetime and deletion rules are explicit |

Lua permits zero and negative numeric keys; the common one-based list convention comes from constructors and the standard sequence operations. Setting an entry to nil removes it. Numeric keys that compare equal refer to the same entry; nil and NaN cannot be stored as table keys. [Tables and values](https://www.lua.org/manual/5.4/manual.html#2.1), [table implementation](https://www.lua.org/source/5.5/ltable.c.html).

Choose stable integer or string IDs when records must survive save/load or cross process boundaries. Table identity is useful inside a runtime; it is not a persistent identifier.

## Length and iteration

`#t` is well-defined as a sequence length only when the table has the appropriate sequence structure, unless an applicable `__len` changes its behavior. A table with holes can have several borders; the returned border need not be the largest occupied index or the count of entries. `rawlen` bypasses metamethods, but does not turn a sparse table into a countable list. [Length operator](https://www.lua.org/manual/5.4/manual.html#3.4.7), [5.2 raw length](https://www.lua.org/manual/5.2/manual.html#pdf-rawlen).

Use the operation matching the contract:

```lua
-- Dictionary cardinality; works on plain tables in PUC 5.1–5.5.
local function count_entries(t)
    local n = 0
    for _ in pairs(t) do n = n + 1 end
    return n
end
assert(count_entries({ enabled = false, retries = 0 }) == 2)
```

- `ipairs` stops at the first absent/nil result; it is not a sparse-table iterator.
- `pairs`/`next` have no application-defined ordering. Do not infer ordering from a few executions.
- Metamethod participation differs across versions: `__pairs` is a 5.2+ feature, and historical `__ipairs` behavior must not be assumed on modern Lua.
- For an explicit tuple, iterate `for i = 1, t.n do` and permit nil values.

Sources: [5.1 base iteration](https://www.lua.org/manual/5.1/manual.html#pdf-next), [5.2 pairs](https://www.lua.org/manual/5.2/manual.html#pdf-pairs), [5.3 incompatibilities](https://www.lua.org/manual/5.3/manual.html#8.2), [current `luaB_ipairs`/`luaB_pairs`](https://www.lua.org/source/5.5/lbaselib.c.html#luaB_ipairs).

For FIFO workloads, repeated `table.remove(queue, 1)` changes indices throughout a dense list. A head/tail representation often states the intended operation more clearly:

```lua
local q = { first = 1, last = 0, data = {} }
local function push(value)
    assert(value ~= nil, 'queue requires non-nil values')
    q.last = q.last + 1
    q.data[q.last] = value
end
local function pop()
    if q.first > q.last then return nil end
    local value = q.data[q.first]
    q.data[q.first] = nil
    q.first = q.first + 1
    if q.first > q.last then q.first, q.last = 1, 0 end
    return value
end
```

A long-lived queue may also need rebasing, bounded capacity, or a ring buffer. Specify those policies before optimizing them. [Table library implementations](https://www.lua.org/source/5.5/ltablib.c.html#tremove).

## Identity, copying, and keys

Assignment copies a reference to a table. It does not clone the table or nested values. A shallow copy duplicates entries but keeps nested references. A generic deep-copy helper needs a written policy for cycles, shared references, metatables, userdata, functions, weak tables, and host objects. [Values and references](https://www.lua.org/manual/5.3/manual.html#2.1).

Prefer explicit copying of domain data when serializability and ownership matter:

```lua
local function copy_position(p)
    assert(type(p.x) == 'number' and type(p.y) == 'number')
    return { x = p.x, y = p.y }
end
```

Do not silently deep-copy an engine object, file handle, callback closure, or a cache whose identity is part of its behavior. For graph snapshots, maintain an old-to-new identity map so repeated references and cycles are handled intentionally.

A table's custom `__eq` does not establish structural equality for dictionary keys. Use canonical IDs or explicitly canonicalized values when equivalent records must address the same slot. [Raw equality and table indexing](https://www.lua.org/manual/5.5/manual.html#2.1), [raw equality API](https://www.lua.org/manual/5.5/manual.html#pdf-rawequal).

## Deterministic order

Deterministic output requires a chosen key order. If all keys are strings, collect and sort them before serialization, hashing, log comparison, or reproducible evaluation. Reject mixed key types or define a total order; do not let an accidental comparison rule become a file format.

`table.sort` requires a consistent strict ordering and is not stable. A comparator using `<=` is invalid; random decisions or mutations inside the comparator also destroy its contract. Use a stable secondary key when ties must be reproducible. [Sort contract](https://www.lua.org/manual/5.5/manual.html#pdf-table.sort), [sort implementation](https://www.lua.org/source/5.5/ltablib.c.html#sort).

```lua
local function ordered_jobs(a, b)
    if a.priority ~= b.priority then return a.priority > b.priority end
    return a.id < b.id
end
```

Validate NaN-sensitive priorities and uniqueness of IDs before relying on this ordering. A deterministic iterator alone does not make a whole simulation deterministic; time, randomness, arithmetic, external input, and processing order also need contracts.

## Mutation and validation

During `next` traversal, modifying existing fields, including clearing them, is permitted; adding previously absent fields is not a safe traversal contract. Collect intended additions separately and apply them afterward. [next restrictions](https://www.lua.org/manual/5.4/manual.html#pdf-next).

Validate at system boundaries:

1. Verify required fields and reject unknown ones where typo detection matters.
2. Distinguish immutable definitions from mutable instances.
3. Define whether callers receive a borrowed record, snapshot, or capability-limited proxy.
4. Validate dense-list continuity when an API uses `#`, sorting, or sequence operations.
5. Test insertion, deletion, empty collections, false values, holes, aliases, and duplicate IDs.

PUC 5.5 `table.create` preallocates an **empty** table; it does not populate slots or change the collection invariant. Do not transfer Luau's similarly named API semantics without checking them. [PUC 5.5 table.create](https://www.lua.org/manual/5.5/manual.html#pdf-table.create).
