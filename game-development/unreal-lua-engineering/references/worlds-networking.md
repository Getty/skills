# Worlds, authority and networking

Use this for client/server/shared modules, multiplayer PIE, listen servers, dedicated servers and map travel.

## Separate code roles from process count

| Unreal mode | Authoritative simulation | Local presentation | Suggested modules |
|---|---|---|---|
| Standalone | Yes | Yes, for local players | `shared`, `server`, local-player `client` |
| Listen server | Yes | Yes, for the host's local players | `shared`, `server`, local-player `client` |
| Dedicated server | Yes | No local player | `shared`, `server` |
| Remote client | No authority over the replicated world | Yes | `shared`, `client` |

These modes and `GetNetMode` are documented by [Epic's Networking Overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-overview-for-unreal-engine). The module mapping is a proposed application convention. A directory name does not select a mode, stage a build artifact or replicate state.

Determine world mode and local-player context separately. An actor's `HasAuthority` is not a process-wide server predicate: non-replicated actors on clients can have `ROLE_Authority`. Actor authority and ownership are also distinct. Source: [Actor Role and Remote Role](https://dev.epicgames.com/documentation/en-us/unreal-engine/actor-role-and-remote-role-in-unreal-engine).

The bootstrap should consequently have independent simulation and presentation decisions, rather than one `if authority ... else ...` branch. For split screen, presentation ownership may be per local player while simulation ownership remains per world.

## Scope mutable Lua state explicitly

PIE can run several game worlds in one engine process. Source: [PIE Multiplayer Options](https://dev.epicgames.com/documentation/en-us/unreal-engine/play-in-editor-multiplayer-options-in-unreal-engine). A mutable process-global Lua table can therefore mix server/client state even when packaged executables appear correct.

| VM scope | Useful when | Required handling |
|---|---|---|
| World | The simulated state ends with the map/world | Restrict world types, dispose callbacks and state during world teardown |
| Game instance | Session services must survive map travel | Explicitly replace world references and reject callbacks from old worlds |
| Local player | UI/input logic differs by player | Avoid duplicating the authoritative simulation |
| Process | Immutable utilities or deliberately shared service only | Prove it never contains unintended mutable world state |

The inspected UnLua default `ULuaEnvLocator::Locate` lazily returns one environment. `ULuaEnvLocator_ByGameInstance::Locate` maintains a map keyed by `UGameInstance`, with a default environment fallback for objects lacking a resolvable instance. `UUnLuaSettings::EnvLocatorClass` defaults to the former in the inspected revision. Sources: [LuaEnvLocator.cpp](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/Plugins/UnLua/Source/UnLua/Private/LuaEnvLocator.cpp), [UnLuaSettings.h](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/Plugins/UnLua/Source/UnLua/Public/UnLuaSettings.h).

Select and test the locator deliberately; a per-game-instance locator is not automatically a per-world lifecycle. Inspect whether startup code has the required world context, particularly for class defaults and editor-only objects. The minimal custom scaffold instead uses a world-owned subsystem, which makes its lifetime contract explicit.

For the inspected revision, a candidate configuration in `Config/DefaultUnLuaSettings.ini` is:

```ini
[/Script/UnLua.UnLuaSettings]
EnvLocatorClass=/Script/UnLua.LuaEnvLocator_ByGameInstance
```

This follows the inspected config class/property and [locator class declaration](https://github.com/Tencent/UnLua/blob/4a534502bbf2c5e51b456d9142acfa631e53350c/Plugins/UnLua/Source/UnLua/Public/LuaEnvLocator.h). Confirm the effective class in the running build and log actual VM identities; copying the setting is not the isolation test.

## Commands and replicated state

Define a bounded command schema, for example `{command_id, player_id, building_type, site_id, client_sequence}`. Treat the authenticated connection/player identity as host-provided context; do not trust a Lua field supplied by the client as identity. Validate placement, ownership, resources and current state on the authoritative side before committing the command.

Client-to-server RPCs must use an actor/component with the appropriate owning connection. A server-owned building is not automatically a valid RPC endpoint for every client. Route requests through a player-owned controller or suitable owned component when that matches the game's design. Source: [Remote Procedure Calls](https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-procedure-calls-in-unreal-engine).

Replicate the resulting state needed by each client. A transient "construction started" event alone cannot reconstruct a building for a late joiner. Plan initial state, incremental changes, removal and reconnection; attach stable entity IDs and version/sequence information to custom payloads where needed. These are application design requirements, not automatically supplied by Lua.

Unreal's property replication requires explicit reflected replication declarations and configuration. Source: [Replicate Actor Properties](https://dev.epicgames.com/documentation/en-us/unreal-engine/replicate-actor-properties-in-unreal-engine). A plugin may add Lua-facing declarations: slua's [README](https://github.com/Tencent/sluaunreal) demonstrates RPC lists and `GetLifetimeReplicatedProps`. Do not impose a universal "all declarations must be C++" rule; verify the selected bridge.

## Shared modules

Put item/building definitions, schemas and pure calculations in `shared`. Each VM loads its own runtime values. Pass state as an explicit argument and keep authoritative mutations in one owner. If a shared formula is used for client prediction or a construction preview, the server must still apply the authoritative decision.

Version the shared definitions and native API together. For multiplayer, make incompatible content versions observable and handle them at connection/session setup; do not let differing recipes silently simulate different costs.

## Required scenarios

Exercise standalone; listen server plus remote client; dedicated server plus clients; single-process PIE; and separate-process clients. Include different local player counts, late join, disconnect during pending work, and travel. Check both correct simulation and absent unintended execution: one production completion must create one result, and a dedicated server must never require a UI widget or local camera.

For a simulation, begin with one authoritative state owner and explicit command/result paths. Add prediction only for the interactions that need it. Script placement, network serialization and replay determinism remain separate design choices.
