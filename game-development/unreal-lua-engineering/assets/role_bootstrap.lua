-- Original pure role mapping; the UE host supplies NetMode and local-player state.
-- This module neither loads scripts nor performs network calls.
local M = {}
local known = {Standalone = true, DedicatedServer = true, ListenServer = true, Client = true}
function M.select(net_mode, has_local_player)
    assert(known[net_mode], "unknown network mode")
    assert(type(has_local_player) == "boolean", "local-player flag must be boolean")
    assert(not (net_mode == "DedicatedServer" and has_local_player),
        "dedicated server cannot have local presentation")
    return {
        shared_definitions = true,
        authoritative_simulation = net_mode ~= "Client",
        local_presentation = has_local_player and net_mode ~= "DedicatedServer",
    }
end
return M
