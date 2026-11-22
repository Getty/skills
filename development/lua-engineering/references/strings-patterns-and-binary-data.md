# Strings, patterns, Unicode boundaries, and binary data

Scope: PUC Lua; UTF-8 and binary packing require 5.3+ unless supplied by the host. Reviewed 2026-11-22.

## Contents

- [Choose a text or byte contract](#choose-a-text-or-byte-contract)
- [Literal search and Lua patterns](#literal-search-and-lua-patterns)
- [Unicode handling](#unicode-handling)
- [Binary encoding](#binary-encoding)
- [I/O, escaping, and bounded parsing](#io-escaping-and-bounded-parsing)

## Choose a text or byte contract

Lua strings are immutable byte sequences and can contain embedded zero bytes. `#s`, ordinary substring positions, and many string operations use byte indices. State whether an API accepts raw bytes, valid UTF-8, ASCII identifiers, or a particular protocol encoding. [String value semantics](https://www.lua.org/manual/5.3/manual.html#2.1), [string library implementation](https://www.lua.org/source/5.5/lstrlib.c.html).

Do not equate these quantities:

| Quantity | Typical use | Lua boundary |
|---|---|---|
| Bytes | File offsets, packets, storage limits | `#s`, `string.sub`, byte-oriented APIs |
| Code points | Unicode scalar processing | `utf8.codes`, validated UTF-8 |
| Grapheme clusters | User-perceived text selection | Requires Unicode segmentation support beyond the base UTF-8 library |
| Display width | Terminal/UI layout | Depends on rendering environment |

For externally supplied strings, validate size before expensive processing. Keep normalization and case-folding requirements explicit; byte equality is not a Unicode normalization policy.

## Literal search and Lua patterns

Use plain mode for literal search:

```lua
local first, last = string.find('price[usd]=12', '[usd]', 1, true)
assert(first == 6 and last == 10)
```

Lua patterns have their own grammar. `%` introduces escapes/classes, captures use parentheses, and repetition uses the pattern operators. They do not provide the complete syntax or grouping semantics of PCRE/JavaScript regular expressions. `%bxy` balances matching delimiter characters; `%f[set]` denotes a frontier. [Pattern grammar](https://www.lua.org/manual/5.4/manual.html#6.4.1).

Choose a parser when nested or context-sensitive input exceeds what a small pattern states clearly. LPeg is a separate parsing library, not a built-in `string` feature; consult its own [official documentation](https://www.inf.puc-rio.br/~roberto/lpeg/).

For replacement strings, `%` and capture references have meaning. A replacement callback is convenient when external text must be inserted literally:

```lua
local replacement = '100% done'
local result, count = string.gsub('status: TOKEN', 'TOKEN', function()
    return replacement
end)
assert(result == 'status: 100% done' and count == 1)
```

Remember that `string.gsub` returns both transformed text and replacement count. A callback returning false/nil leaves the matched text unchanged. Capture one result deliberately when forwarding into another function. [gsub contract](https://www.lua.org/manual/5.3/manual.html#pdf-string.gsub), [replacement implementation `add_value`](https://www.lua.org/source/5.5/lstrlib.c.html#add_value).

For ASCII protocol names, use explicit byte ranges when that is the real specification; locale-sensitive classes should not silently broaden a wire format. Keep matching anchored when the entire input must satisfy the grammar. Test empty matches and malformed input, not only a successful example.

## Unicode handling

The base UTF-8 library works with encoding and code points. It does not implement normalization, grapheme segmentation, locale-aware casing, or a complete Unicode property engine. Choose a maintained host/library implementation when those behaviors are requirements. [UTF-8 library](https://www.lua.org/manual/5.4/manual.html#6.5).

```lua
-- PUC Lua 5.3+.
local text = '\195\164x' -- UTF-8 ä followed by x
assert(#text == 3)
assert(utf8.len(text) == 2)
local count, bad_at = utf8.len('\255')
assert(count == nil and bad_at == 1)
```

`utf8.len` reports invalid input rather than guaranteeing every byte string is valid. Some other UTF-8 functions raise errors; `utf8.offset` assumes valid input. Decide whether invalid sequences are rejected, replaced, or handled as bytes before invoking downstream functions. [5.3 UTF-8 APIs](https://www.lua.org/manual/5.3/manual.html#6.5), [decoder implementation](https://www.lua.org/source/5.5/lutf8lib.c.html#utf8_decode).

**5.5 migration:** `utf8.offset` returns start and end byte indices. Capturing only the first value preserves old single-position use, but directly forwarding all results can change a call's argument list. Test call sites, not just assignments. [5.5 utf8.offset](https://www.lua.org/manual/5.5/manual.html#pdf-utf8.offset).

## Binary encoding

For PUC 5.3+, `string.pack`, `string.unpack`, and `string.packsize` provide explicit binary formats. A durable format needs declared widths, signedness, byte order, alignment, maximum lengths, and schema version. Native defaults are not a portable wire specification. [Pack format](https://www.lua.org/manual/5.3/manual.html#6.4.2).

```lua
-- PUC Lua 5.3+; little-endian, explicit integer widths, no padding.
local format = '<!1I2I4'
local packet = string.pack(format, 513, 100000)
local kind, value, next_index = string.unpack(format, packet)
assert(kind == 513 and value == 100000)
assert(next_index == #packet + 1)
```

`unpack` returns the next position after decoded values. Validate that position against the expected framing policy: exact consumption, permitted trailing fields, or a next-record boundary. Check input size and declared payload lengths before allocating or parsing nested content. [unpack](https://www.lua.org/manual/5.4/manual.html#pdf-string.unpack), [packing implementation](https://www.lua.org/source/5.5/lstrlib.c.html#str_unpack).

Avoid platform-dependent `size_t` fields or unbounded length prefixes in interchange formats unless both endpoints explicitly agree. Do not serialize a raw pointer, userdata layout, or dumped closure as portable data. For JSON bridges, explicitly define integer range and representation, null/absence, array/object distinctions, non-finite numbers, cycles, and encoding behavior.

## I/O, escaping, and bounded parsing

Use binary file modes for byte-exact payloads. Read fixed-size chunks or bounded records when the input can be large. Check file-open, read/write, and close outcomes under the chosen Lua version and platform. [I/O library](https://www.lua.org/manual/5.4/manual.html#6.8), [file implementations](https://www.lua.org/source/5.5/liolib.c.html).

Escaping is context-specific. `string.format('%q', value)` is not a shell-quoting, SQL-escaping, HTML-escaping, or JSON-encoding API. Prefer structured process/database APIs and dedicated encoders. A Lua literal, a pattern, a pattern replacement, a shell word, and a JSON string each have a different grammar.

For parsers, define maximum total bytes, nesting, fields, token length, and work budget according to the application. A syntax-valid document can still violate semantic or resource constraints. Where exact diagnostics matter, report byte position, field path, source name, and expected contract rather than a generic “invalid string.”
