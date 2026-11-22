-- Original PUC Lua 5.1+ example. Trusted plain tables only.
-- Inventory values and aggregate per-command quantities are capped at 2^31-1.
-- This function is synchronous, non-yielding and validates before mutation.
local M = {}
local MAX = 2147483647

local function count(value, minimum)
    return type(value) == "number" and value == value
        and value >= minimum and value <= MAX and value == math.floor(value)
end

local function plain(value)
    return type(value) == "table" and getmetatable(value) == nil
end

local function valid_map(map, minimum)
    if not plain(map) then return false end
    for item, value in pairs(map) do
        if type(item) ~= "string" or item == "" or not count(value, minimum) then
            return false
        end
    end
    return true
end

function M.apply(inventory, recipe, batches)
    if not valid_map(inventory, 0) then return nil, {code = "invalid_inventory"} end
    if not plain(recipe) or not valid_map(recipe.inputs, 1)
        or not valid_map(recipe.outputs, 1) then
        return nil, {code = "invalid_recipe"}
    end
    if not count(batches, 1) then return nil, {code = "invalid_batches"} end

    local candidate = {}
    for item, quantity in pairs(recipe.inputs) do
        if batches > math.floor(MAX / quantity) then
            return nil, {code = "quantity_overflow", item = item}
        end
        local needed = quantity * batches
        local available = inventory[item] or 0
        if available < needed then
            return nil, {code = "insufficient_stock", item = item}
        end
        candidate[item] = available - needed
    end
    for item, quantity in pairs(recipe.outputs) do
        if batches > math.floor(MAX / quantity) then
            return nil, {code = "quantity_overflow", item = item}
        end
        local produced = quantity * batches
        local current = candidate[item]
        if current == nil then current = inventory[item] or 0 end
        if current > MAX - produced then
            return nil, {code = "inventory_overflow", item = item}
        end
        candidate[item] = current + produced
    end
    for item, quantity in pairs(candidate) do inventory[item] = quantity end
    return true
end

return M
