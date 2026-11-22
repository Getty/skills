-- Original dependency-free diagnostics, PUC 5.1+ common syntax.
local checks = 0
local function check(name, condition)
    assert(condition, name)
    checks = checks + 1
end
local function pack(...) return {n = select("#", ...), ...} end
local function values() return "a", nil, "c" end
check("zero truthiness", not not 0)
check("empty string truthiness", not not "")
check("nil and false", not nil and not false)
local p = pack(values())
check("multiple return arity", p.n == 3 and p[2] == nil and p[3] == "c")
check("parentheses collapse", pack((values())).n == 1)
check("nonfinal call collapse", pack(values(), "z").n == 2)
local t = {a = false, b = 0}
check("false entry exists", rawget(t, "a") == false)
t.a = nil
check("nil removes entry", rawget(t, "a") == nil)
local alias = t
alias.b = 5
check("table reference alias", t.b == 5)
local n = 0
for _ in ipairs({[1] = "a", [3] = "c"}) do n = n + 1 end
check("ipairs first hole", n == 1)
local obj = setmetatable({present = 1}, {
    __index = function(_, key) if key == "fallback" then return 7 end end,
    __newindex = function(tab, key, value) rawset(tab, key, value * 2) end
})
check("index fallback", obj.fallback == 7 and rawget(obj, "fallback") == nil)
obj.present = 3
obj.new = 3
check("newindex absent keys", obj.present == 3 and obj.new == 6)
local marker = {}
local ok, err = pcall(function() error(marker) end)
check("nonstring error", ok == false and err == marker)
local co = coroutine.create(function(x)
    local y = coroutine.yield(x + 1)
    return y * 2
end)
local resumed, yielded = coroutine.resume(co, 4)
check("coroutine initial result", resumed and yielded == 5 and coroutine.status(co) == "suspended")
local done, result = coroutine.resume(co, 6)
check("coroutine resume value", done and result == 12 and coroutine.status(co) == "dead")
check("coroutine dead resume", coroutine.resume(co) == false)
check("binary string length", #("a" .. string.char(0) .. "b") == 3)
check("plain substring search", string.find("a.b", ".", 1, true) == 2)
check("pattern special dot", string.find("abc", ".") == 1)

local name = "__lua_engineering_diagnostic__"
check("module test namespace unused", package.loaded[name] == nil and package.preload[name] == nil)
local loads = 0
package.preload[name] = function() loads = loads + 1; return {value = loads} end
local first, second = require(name), require(name)
check("require cache", first == second and loads == 1)
package.loaded[name], package.preload[name] = nil, nil

local Rules = dofile("assets/rules.lua")
local inventory = {logs = 10, planks = 0}
local recipe = {inputs = {logs = 2}, outputs = {planks = 3}}
check("production success", Rules.apply(inventory, recipe, 2) == true)
check("production exact changes", inventory.logs == 6 and inventory.planks == 6)
local applied, failure = Rules.apply(inventory, recipe, 4)
check("insufficient stock failure", applied == nil and failure.code == "insufficient_stock")
check("failure no mutation", inventory.logs == 6 and inventory.planks == 6)
check("false count rejected", Rules.apply({logs = false}, recipe, 1) == nil)
check("fractional batch rejected", Rules.apply(inventory, recipe, 1.5) == nil)
check("infinity rejected", Rules.apply(inventory, recipe, math.huge) == nil)
check("nan rejected", Rules.apply({logs = 0/0}, recipe, 1) == nil)
local full = {logs = 1, planks = 2147483647}
local overflow, why = Rules.apply(full, {inputs = {logs = 1}, outputs = {planks = 1}}, 1)
check("capacity rejection", overflow == nil and why.code == "inventory_overflow")
check("overflow no partial consume", full.logs == 1 and full.planks == 2147483647)
local cycle = {water = 5}
check("same item input output", Rules.apply(cycle, {inputs = {water = 2}, outputs = {water = 3}}, 2))
check("same item net change", cycle.water == 7)
check("metatable rejected", Rules.apply(setmetatable({}, {__index = function() return 9 end}), recipe, 1) == nil)
local empty = {}
check("empty recipe valid no-op", Rules.apply(empty, {inputs = {}, outputs = {}}, 1))
check("no-op leaves empty", next(empty) == nil)
print("PASS " .. tostring(checks) .. " checks on " .. tostring(_VERSION))
