-- Read-only capability observations. PUC 5.1+ common syntax.
-- Compiles trusted literal probes; never loads a project or native module.
local function emit(key, value)
    print(key .. "=" .. tostring(value))
end
local function compile(source)
    if type(loadstring) == "function" then return loadstring(source, "=probe") end
    if type(load) == "function" then return load(source, "=probe", "t", {}) end
    return nil, "dynamic compilation unavailable"
end
local function syntax(name, source)
    local ok, chunk = pcall(compile, source)
    emit("syntax." .. name, ok and type(chunk) == "function")
end
emit("runtime", _VERSION or "unknown")
local j = rawget(_G, "jit")
emit("jit.version", type(j) == "table" and j.version or "absent")
emit("jit.arch", type(j) == "table" and j.arch or "unknown")
emit("number.integer_subtype", type(math.type) == "function")
emit("number.maxinteger", math.maxinteger or "unavailable")
emit("library.table_pack", type(table.pack) == "function")
emit("library.table_create", type(table.create) == "function")
emit("library.string_pack", type(string.pack) == "function")
emit("library.utf8", type(rawget(_G, "utf8")) == "table")
emit("library.coroutine_close", type(coroutine.close) == "function")
emit("library.package_searchers", type(package.searchers) == "table")
emit("library.setfenv", type(rawget(_G, "setfenv")) == "function")
syntax("floor_division", "return 7 // 2")
syntax("bitwise", "return 3 & 1")
syntax("to_be_closed", "local x <close> = nil; return true")
syntax("named_varargs", "return function(... args) return args.n end")
syntax("global_declaration", "global probe_value; probe_value = 1")
syntax("loop_variable_assignment", "for i = 1, 2 do i = 0 end")
emit("scope", "observations only; not a conformance or security certificate")
