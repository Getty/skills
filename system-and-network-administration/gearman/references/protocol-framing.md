# Binary protocol framing and parser design

Read when implementing a binding, inspecting captures or debugging corruption. Evidence: [G3](sources.md); implementation: [gearman_wire.py](../scripts/gearman_wire.py).

Packets have a 12-byte header: four magic bytes, an unsigned 32-bit command, and an unsigned 32-bit body length. Integer fields use network byte order. Requests use `00 52 45 51` (`\0REQ`), responses `00 52 45 53` (`\0RES`). The body length excludes the header.

Arguments preceding a final opaque workload/result are NUL-delimited where specified by the command. The trailing workload is binary and can contain NULs. Therefore split only the required number of fields: `JOB_ASSIGN_UNIQ` needs the first three delimiters, not an unrestricted split over the payload.

## Parser requirements

TCP is a byte stream. One write is not guaranteed to equal one read: headers and bodies can arrive fragmented, and multiple packets can arrive together. Read exactly the header, validate its magic and declared length, then consume precisely that body. Do not allocate an unbounded peer-specified size. A 32-bit length field is not a sensible application payload budget.

Apply both a byte cap and a monotonic total deadline to a frame. If a timeout occurs after consuming only part of it, either retain the partial parser state or discard the connection. Starting a fresh header on the same socket corrupts the stream. Idle waiting before a frame and timeout while a frame is incomplete are different states.

Reject incorrect magic, unsupported message types for the current state, missing delimiters, malformed numeric fields, wrong job handles and unexpected response ordering. Return a structured diagnostic without dumping secret payload bytes. Fuzz these boundaries and test coalesced packets as well as one-byte fragmentation.

## Limits in this package

The lab uses a 1 MiB frame cap, a 64 KiB request contract, printable non-space ASCII function/unique fields capped at 64 bytes, and a bounded total event budget. These are **package safety policies**, not Gearman's universal protocol limits. The function-name policy intentionally excludes the tab-separated prefix encoding used by the classic Perl helper. Use the same explicit function string across languages.

The library exposes selected packet numbers for educational interoperability tests. It is not an exhaustive implementation of scheduling, reducers, concurrent tasks, multi-server routing or all extensions. A constant's presence does not mean a method implementing that capability exists.

## Capture procedure

First determine whether TLS is in use. Prefer redacted library tracing and header-only diagnostics. On an authorized isolated network, capture a known test request and correlate packet sequence with request ID, server handle and worker identity. Verify byte counts before assuming a semantic server problem. Never disable production TLS merely to obtain a convenient packet capture.
