# Binding contracts, ownership and lifetime

Read this when exposing UObjects, native containers, delegates, asynchronous operations or script-owned resources. The following design rules complement the exact integration's source; they do not assume every plugin uses the same ownership model.

## Define the boundary before binding it

Specify for every exported operation: argument types and limits, units, nullability, ownership, world/session identity, allowed thread, authority requirement, failure shape and whether it can yield or invoke callbacks. Generate editor annotations from that contract where possible.

Prefer domain operations such as `reserve_materials`, `request_route` and `complete_job` over unconstrained access to internal storage. Returning a copied result snapshot and returning a live native view are different APIs. Make the distinction explicit, especially when the underlying array may reallocate.

UnLua documents static binding through `IUnLuaInterface`/`GetModuleName`, dynamic binding for spawned objects, reflected access and separate static exports for non-reflected C++ types. Source: [Programming Guide](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/Docs/EN/UnLua_Programming_Guide.md). Do not infer that an arbitrary C++ method becomes callable merely because its class is visible.

## Three different lifetimes

| Thing | Owner to identify | Common failure |
|---|---|---|
| Lua value/closure/userdata | A VM stack, registry reference, table or other Lua root | Native code retains a pointer/reference after Lua collection or VM destruction |
| UObject | Unreal's ownership/reference graph and its gameplay destruction state | Lua still has a wrapper while the actor has ended play or become invalid |
| Native allocation/resource | Explicit host contract or owning userdata | Both runtimes free it, or neither one does |

Lua reachability and UObject reachability are separate mechanisms. The inspected UnLua source includes [`FObjectReferencer::AddReferencedObjects`](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/Plugins/UnLua/Source/UnLua/Private/ObjectReferencer.h) and environment methods for adding/removing manual references in [`LuaEnv.cpp`](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/Plugins/UnLua/Source/UnLua/Private/LuaEnv.cpp). Review the selected wrapper path before deciding whether a Lua reference is owning.

For a custom facade, expose stable IDs with generation/session information and resolve them on the correct thread. An ID must fail predictably after deletion, world change or generation reuse; a raw address is not a durable game identity.

## Unreal references

Epic's [Object Pointers](https://dev.epicgames.com/documentation/en-us/unreal-engine/object-pointers-in-unreal-engine) distinguishes non-owning weak references, reflected strong references and strong references from non-UObject owners. A `TObjectPtr` member is not automatically GC-tracked solely by its C++ type; the documented reflected ownership path uses `UPROPERTY`. Use a suitable UE ownership mechanism when a host object must keep another UObject alive.

Test destruction rather than merely testing pointer non-nullness. Clear script callbacks when their target ends play. A strong reference should have an explicit release point; using it to keep dead gameplay objects accessible hides a lifecycle bug.

## Marshaling checklist

| Value | Contract to settle |
|---|---|
| Integer/ID | Required width, signedness and whether any conversion passes through a double; reject lossy coercion |
| Number | Finite values, units, range, rounding and intentional integer/float conversion |
| String | UTF-8 versus byte string, embedded NUL policy, maximum length, conversion ownership |
| `FName`/`FText` | Identifier versus localized display text; preserve each intended meaning |
| Native array/map | Index convention, copy/view behavior, invalidation and iteration order |
| Struct | Value copy, borrowed field reference, temporary lifetime, output/inout handling |
| UObject | Owning/non-owning wrapper, validity checks, world identity and permitted operations |
| Callback | VM identity, registry retention, thread handoff, cancellation, error policy |

Test the selected plugin's indexing and out-parameter behavior rather than extending ordinary Lua-table assumptions to UE containers. Type declarations and annotations improve tooling but do not replace runtime validation at external boundaries.

Unreal conversion macros can produce short-lived buffers. Use a named conversion object when its bytes must survive more than a single full expression, and use its encoded byte length. Source: [Character Encoding](https://dev.epicgames.com/documentation/unreal-engine/character-encoding-in-unreal-engine?lang=en-US). Lua strings can contain arbitrary bytes; translate diagnostic text deliberately and pass binary payloads with explicit lengths.

## Callbacks, errors and teardown

Create callback handles containing at least the owner world/session, VM generation and retained Lua callable. When native work finishes, dispatch to the owning game thread, reject stale generations, re-resolve target validity and only then enter Lua. Cancel handles or discard their results before closing the VM.

Never treat a thread-safe shared-pointer reference count as permission to call the Lua state from concurrent threads. The inspected UnLua locator uses `ESPMode::ThreadSafe` for shared pointers; that flag alone establishes no serialization of VM operations.

Place Lua errors inside a protected call boundary and convert status/results into ordinary UE return values. The Lua C API may use nonlocal jumps; a Lua error raised inside a callback must not skip C++ stack objects whose destructors need to run. Source: [Lua 5.4, error handling in C](https://www.lua.org/manual/5.4/manual.html#4.4). For future bindings, isolate error-raising C API work in a protected C-compatible dispatcher and return to C++ after protection catches failures.

During shutdown: stop admitting work, stop timers/listeners, cancel or invalidate outstanding handles, release retained script/native references, close Lua, then unload the owning module. Exercise this ordering under repeated PIE runs, travel, actor destruction and forced collection; success on a normal application exit does not establish it.
