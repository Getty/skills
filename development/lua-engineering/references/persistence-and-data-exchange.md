# Persistence and data exchange

## Contents

- Define a durable model
- Preserve identity and numbers
- Map Lua values to JSON
- Save, load and migrate
- Validate format boundaries

## Define a durable model

Choose a durable schema independently of the live Lua object layout. Specify fields, types, units, version, optionality, bounds and references. Serialize data needed to reconstruct behavior, not native pointers, coroutine stacks or function identities.

Lua tables can represent maps, sequences, shared subgraphs and cycles without identifying a serialization format. Function, userdata and thread are separate value types. [Source: values and tables](https://www.lua.org/manual/5.5/manual.html#2.1).

~~~json
{
  "schema_version": 1,
  "rules_version": "example-rules-1",
  "next_entity_id": "1043",
  "entities": [
    {"id": "1042", "kind": "workshop", "progress_ticks": 17}
  ]
}
~~~

This is an illustrative envelope. Distinguish schema version, file-container version, rules/content version and Lua runtime version. Include only identities relevant to compatibility or replay.

## Preserve identity and numbers

Assign durable IDs and serialize edges by ID. On load, validate uniqueness, create records and then resolve references. Decide whether missing references fail, remain optional or receive an explicit repair. Recreate transient host handles only after their owners exist.

Check the receiving system's number representation. Standard PUC 5.3+ distinguishes integers and floats, but numeric build options and other implementations differ. [Source: numeric types](https://www.lua.org/manual/5.5/manual.html#2.1). For IDs beyond any intermediary's exact integer range, choose decimal strings or a specified integer format. Exactness at the source alone is insufficient.

Reject or explicitly encode nonfinite numbers. Specify precision, rounding and units; preserve decimal text when exact decimal meaning is required. Define missing values separately from explicit null.

## Map Lua values to JSON

| Lua input | Policy to establish |
|---|---|
| Empty table | Empty array, object or explicitly tagged collection |
| Sparse integer keys | Reject, null-fill or normalize by schema |
| nil | Missing field versus explicit null sentinel |
| false | Preserve false without truthiness defaults |
| Mixed numeric/string keys | Reject or explicitly convert |
| Numeric object keys | Key type may be lost through string conversion |
| Cycles/shared tables | Reject, duplicate values or encode reference IDs |
| Function/userdata/thread | Reject or map to a domain identifier |
| Large integers | Defined string or exact integer representation |

Lua CJSON documents null, sparse arrays, maximum depth and invalid-number controls. These are encoder-specific. The historical 2.1.0 author manual has an older runtime scope; verify the maintained implementation and rock actually selected. [Source: CJSON author manual](https://www.kyne.au/~mark/software/lua-cjson-manual.html).

Use explicit conversion at the boundary. Never assume every reachable field on a live object is appropriate for transmission or saving.

## Save, load and migrate

Recommended write protocol: take a coherent snapshot; normalize and validate; serialize with size/depth bounds; write using the host's supported replacement/durability mechanism; publish after success. Preserve a recoverable previous version when required.

Do not equate io.flush with power-loss durability or assume identical os.rename replacement behavior across platforms/filesystems. These APIs delegate to the underlying system. [Sources: I/O](https://www.lua.org/manual/5.5/manual.html#6.8), [OS](https://www.lua.org/manual/5.5/manual.html#6.9).

Recommended load protocol: bound input; parse; check version and fields; migrate a candidate; validate references and invariants; create host state; publish. Keep the current state intact if parsing or migration fails.

Write migrations between known schema versions and test old fixtures. Decide whether unknown extension fields survive a round trip. For event logs, specify ordering, duplicate processing and which external inputs must be recorded. Event storage does not itself establish deterministic replay.

## Validate format boundaries

Do not use load, loadfile or dofile to parse untrusted data. A chunk remains executable even when it returns a table; text-only loading only rejects binary chunks. [Source: load](https://www.lua.org/manual/5.5/manual.html#pdf-load).

string.dump produces a function's binary representation, with upvalue and version/build constraints. It is not a portable save-state format. [Sources: string.dump](https://www.lua.org/manual/5.5/manual.html#pdf-string.dump), [Lua compatibility policy](https://www.lua.org/versions.html).

For binary data specify byte order, signedness, lengths, alignment, text encoding and size bounds. Version-gate string.pack/unpack (PUC 5.3+) and avoid implicit native formats for a portable protocol. [Source: pack formats](https://www.lua.org/manual/5.5/manual.html#6.4.2).

Test semantic round trips containing false, zero, empty string, null, empty collections, rejected sparse data, numeric boundaries, non-ASCII text, embedded zeros where legal, shared references, unsupported versions and truncation. Compare reconstructed meaning rather than table identity.

For canonical hashes, define map ordering and numeric/text normalization independently of pairs or an ordinary encoder's current output. Test against the chosen canonicalization protocol.
