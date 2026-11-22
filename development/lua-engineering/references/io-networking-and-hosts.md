# I/O, networking and host integration

## Contents

- Discover available capabilities
- Handle files and processes
- Choose the I/O model
- Specify network protocols
- Integrate existing hosts
- Diagnose blocked or leaking systems

## Discover available capabilities

Separate Lua's standard libraries from native extensions and host APIs. Standard PUC Lua offers basic file and OS facilities; sockets, HTTP, directory iteration and event loops come from additional libraries or the embedding host. Embedded applications may omit or restrict even standard libraries. [Source: standard libraries](https://www.lua.org/manual/5.5/manual.html#6).

Inspect what the application already uses before adding dependencies. Record exact module versions, native ABI, event-loop owner, TLS backend and supported platform. A successful require on a development machine does not establish packaged-build availability.

## Handle files and processes

Check io.open failures and close handles deterministically. Use binary mode for binary payloads. When streaming, bound chunk sizes and total input; distinguish EOF, malformed content and I/O failure. Check write/flush/close results where data integrity matters. [Source: I/O library](https://www.lua.org/manual/5.5/manual.html#6.8).

Use PUC 5.4+ to-be-closed variables when their semantics fit; choose explicit cleanup for older versions or host resources that need asynchronous shutdown. A resource becoming unreachable is not a timely release contract. See errors-resources-and-coroutines.md.

Keep path handling platform-aware. Decide root resolution, symlink policy, allowed extensions and case behavior. Use host filesystem APIs or an appropriate extension for directory traversal. LuaFileSystem provides directory and attribute operations, with platform/native-runtime constraints. [Source: LuaFileSystem manual](https://lunarmodules.github.io/luafilesystem/manual.html).

os.execute and io.popen invoke platform command facilities; return conventions differ across Lua versions and platforms. Prefer a host process API that accepts an executable and argument vector when manipulating external programs. Avoid interpolating untrusted strings into shell text. [Sources: os.execute](https://www.lua.org/manual/5.5/manual.html#pdf-os.execute), [io.popen](https://www.lua.org/manual/5.5/manual.html#pdf-io.popen).

Do not assume file replacement is atomic/durable on every target. Make those guarantees in the storage adapter and test failure recovery if required.

## Choose the I/O model

| Context | Appropriate starting point | Check |
|---|---|---|
| Small synchronous CLI | LuaSocket or existing host client | Timeouts, bounded input, TLS and redirects |
| Long-running event-driven app | Existing event loop; luv if appropriate | Callback lifetime, cancellation, backpressure |
| OpenResty request | Host-supported ngx/cosocket facilities | Allowed phase, yielding rules, worker scope |
| Engine/editor plugin | Host async facilities | Main-thread ownership and world teardown |
| Restricted script | Injected narrow capabilities | No implicit files/network access |

LuaSocket supplies TCP/UDP and higher-level protocol modules. luv supplies libuv bindings. Neither choosing a coroutine nor calling a synchronous library automatically makes I/O nonblocking. [Sources: LuaSocket](https://lunarmodules.github.io/luasocket/), [luv](https://github.com/luvit/luv), [Lua coroutine semantics](https://www.lua.org/manual/5.5/manual.html#2.6).

Use the loop already owned by the host. Do not run a second blocking loop inside a render callback or request handler. Model cancellation and completion exactly once; reject results whose session/request generation has expired.

## Specify network protocols

TCP carries bytes; define framing, limits, parser state and truncation behavior. Handle partial writes and partial reads explicitly. LuaSocket's send/receive APIs return partial progress on relevant failures; read their exact return contracts rather than restarting a message from byte one. Set suitable timeouts. [Source: LuaSocket TCP reference](https://lunarmodules.github.io/luasocket/tcp.html).

For HTTP, specify connect/request deadlines, maximum response size, redirects, retries, status handling and cancellation. Treat a retryable transport failure separately from a rejected application command. Use idempotency or deduplication where repeating a request could duplicate side effects.

TLS is a capability of the chosen client/backend. Confirm certificate and hostname verification in that implementation instead of assuming a URL string supplies it. Avoid disabling verification to fix an installation problem. Do not invent a generic Lua TLS API.

Bound concurrent work and buffers. Define what happens when producers outrun consumers: queue, drop, reject or slow down. Expose queue size, in-flight count, timeouts and bytes as diagnostics when needed.

## Integrate existing hosts

OpenResty, Neovim, game engines and device firmware provide different globals, scheduling rules and libraries. Do not port snippets solely because both sides say Lua. For OpenResty, use the official module's phase and yielding restrictions; blocking calls can stall a worker. [Source: lua-nginx-module documentation](https://github.com/openresty/lua-nginx-module#readme).

Use host-owned identifiers rather than persisting pointers. Wrap access in a small adapter with explicit lifetime and error rules. Keep a pure logic module independent where it makes tests or migration easier; avoid duplicating the host's networking or filesystem stack without a concrete need.

## Diagnose blocked or leaking systems

Measure whether the delay is DNS, connect, read, application CPU, callback backlog or GC. Inspect open handles, retained closures, active timers and requests that never complete. Capture the first error and cancellation path. Check whether callbacks execute after the owning world/VM is destroyed.

Test one successful exchange, timeout, partial message, cancellation and teardown where the application uses those mechanisms. A generic networking suite is unnecessary for a one-shot local script.
