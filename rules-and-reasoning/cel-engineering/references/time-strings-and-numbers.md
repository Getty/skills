# Time, strings, and numbers

## Make temporal conventions explicit

Declare whether facts are timestamps, durations, or source strings requiring
conversion. Use explicit UTC offsets in test values. A timestamp comparison does
not imply a local business-day interpretation. If a rule refers to today's date,
supply a trusted clock value through the host so decisions can be reproduced.

For intervals, choose inclusive/exclusive boundaries deliberately. Compare exactly
at activation, immediately before expiry, and exactly at expiry. Do not mix seconds
and milliseconds or assume a duration string means calendar months.

Version timestamp and duration functions against the implementation's supported
standard and extension library. The [CEL API reference](https://cel.dev/reference/api-reference)
provides supported signatures; preserve timezone behavior in cross-runtime cases.

## Normalize outside the expression where appropriate

Specify case sensitivity, Unicode normalization, identifier canonicalization, and
whether whitespace is meaningful. A policy matching an owner ID should consume the
same canonical ID used by authentication and storage. A case-insensitive display
name is not necessarily a case-insensitive identity key.

Choose bytes versus strings consciously. Test non-ASCII input if a limit counts
characters, code points, or bytes at a host boundary. A length check is meaningful
only with its chosen representation.

## Treat regex as a precise predicate

Use the documented RE2-compatible syntax where the host follows core CEL's regex
model. Do not assume PCRE backreferences or look-around. Decide whether a match
must cover the whole string; anchor an entire identifier pattern explicitly.
[RE2 syntax](https://github.com/google/re2/wiki/Syntax).

Keep patterns bounded and prevalidated when they are configuration. A fast regex
engine still spends work proportional to input/pattern size. Avoid repeatedly
rebuilding large dynamic patterns for every element of a nested comprehension.

## Preserve numeric meaning

Distinguish integer division from floating-point division, signed from unsigned,
and exact large integers from double precision. Define overflow and conversion
failure behavior through actual tests rather than assuming another language's rules.
Avoid introducing floats merely to silence a type-check mismatch.

For a quota expression, test negative usage, zero, exact limit, and one beyond it.
For IDs encoded as numbers, test the largest expected values through the actual
JSON adapter. If identifiers never need arithmetic, strings can avoid accidental
numeric conversions, but changing representation requires an explicit API migration.
