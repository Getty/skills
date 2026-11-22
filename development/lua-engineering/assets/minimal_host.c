/*
 * Synchronous trusted-script host for PUC Lua 5.4 and 5.5.
 * Opens ALL standard libraries, including io, os, package, and debug.
 * Text-only file loading is format restriction, not a sandbox.
 * The script path is the sole command-line argument. Script return values are
 * discarded; Lua runtime errors produce a traceback and a nonzero exit status.
 * Diagnostics do not preserve loader status codes, non-string payloads or
 * embedded-NUL suffixes passed through luaL_traceback. Retain those separately
 * when the host's error protocol requires exact causes or binary data.
 *
 * Build with headers and library from the SAME Lua build. Example on a system
 * with a matching pkg-config file (the file name is distribution-dependent):
 * cc -std=c99 -Wall -Wextra -Wpedantic minimal_host.c \
 *    $(pkg-config --cflags --libs lua5.4) -o minimal_host
 *
 * API references:
 * https://www.lua.org/manual/5.4/manual.html#4.4
 * https://www.lua.org/manual/5.5/manual.html#4.4
 * https://www.lua.org/source/5.5/lauxlib.c.html#luaL_traceback
 */

#include <stdio.h>
#include <stdlib.h>

#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

#if LUA_VERSION_NUM != 504 && LUA_VERSION_NUM != 505
#error "This example targets PUC Lua 5.4 or 5.5; port deliberately."
#endif

static void print_error(lua_State *L, int status) {
    size_t length = 0;
    fprintf(stderr, "Lua failed (status %d): ", status);
    if (lua_type(L, -1) == LUA_TSTRING) {
        const char *message = lua_tolstring(L, -1, &length);
        if (message != NULL) {
            (void)fwrite(message, 1, length, stderr);
        }
    } else {
        fprintf(stderr, "error object type %s", luaL_typename(L, -1));
    }
    fputc('\n', stderr);
}

static int traceback(lua_State *L) {
    const char *message = NULL;
    if (lua_type(L, 1) == LUA_TSTRING) {
        message = lua_tostring(L, 1);
    }
    if (message == NULL) {
        message = "non-string Lua error object";
    }
    /* Never invoke an untrusted __tostring metamethod while reporting errors. */
    luaL_traceback(L, L, message, 1);
    return 1;
}

static int initialize(lua_State *L) {
    luaL_openlibs(L);
    return 0;
}

static int execute_file(lua_State *L) {
    const char *path = (const char *)lua_touserdata(L, 1);
    int status = luaL_loadfilex(L, path, "t");
    if (status != LUA_OK) {
        return lua_error(L);
    }
    /* This host intentionally does not support yielding across this call. */
    lua_call(L, 0, 0);
    return 0;
}

int main(int argc, char **argv) {
    lua_State *L;
    int status;
    int handler;

    if (argc != 2) {
        fprintf(stderr, "Usage: %s script.lua\n", argv[0]);
        return 2;
    }

    L = luaL_newstate();
    if (L == NULL) {
        fputs("Unable to allocate a Lua state.\n", stderr);
        return 1;
    }
    if (!lua_checkstack(L, 4)) {
        fputs("Unable to reserve the host call stack.\n", stderr);
        lua_close(L);
        return 1;
    }

    /* Zero-upvalue C function pushes do not allocate. Library initialization,
     * file loading, and execution all happen within protected calls. */
    lua_pushcfunction(L, traceback);
    handler = lua_gettop(L);
    lua_pushcfunction(L, initialize);
    status = lua_pcall(L, 0, 0, handler);
    if (status == LUA_OK) {
        lua_pushcfunction(L, execute_file);
        lua_pushlightuserdata(L, argv[1]);
        status = lua_pcall(L, 1, 0, handler);
    }
    if (status != LUA_OK) {
        print_error(L, status);
    }

    lua_settop(L, 0);
    lua_close(L);
    return status == LUA_OK ? 0 : 1;
}
