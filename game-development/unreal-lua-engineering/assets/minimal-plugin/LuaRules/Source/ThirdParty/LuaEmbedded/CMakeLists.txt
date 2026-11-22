cmake_minimum_required(VERSION 3.21)
project(LuaEmbedded LANGUAGES C)

if(NOT WIN32 OR NOT MSVC)
    message(FATAL_ERROR "This recipe is scoped to Windows with an MSVC-compatible toolchain.")
endif()
if(NOT CMAKE_GENERATOR MATCHES "^Visual Studio ")
    message(FATAL_ERROR "This recipe requires a Visual Studio generator with -A x64. Other generators need an explicit target-architecture check and separate validation.")
endif()
if(NOT CMAKE_SIZEOF_VOID_P EQUAL 8)
    message(FATAL_ERROR "A 64-bit toolchain is required. Configure the generator for x64.")
endif()
if(NOT DEFINED CMAKE_VS_PLATFORM_NAME OR NOT CMAKE_VS_PLATFORM_NAME STREQUAL "x64")
    message(FATAL_ERROR "This recipe supports x64, not another 64-bit Windows architecture.")
endif()

set(LUA_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/lua-5.4.9")
if(NOT EXISTS "${LUA_ROOT}/src/lua.h")
    message(FATAL_ERROR "Extract the verified lua-5.4.9 archive beside this CMakeLists.txt.")
endif()
set(LUA_SOURCE_NAMES
    lapi.c lcode.c lctype.c ldebug.c ldo.c ldump.c lfunc.c lgc.c
    llex.c lmem.c lobject.c lopcodes.c lparser.c lstate.c lstring.c
    ltable.c ltm.c lundump.c lvm.c lzio.c lauxlib.c lbaselib.c
    lcorolib.c ldblib.c liolib.c lmathlib.c loadlib.c loslib.c
    lstrlib.c ltablib.c lutf8lib.c linit.c)
set(LUA_SOURCES "")
foreach(SOURCE_NAME IN LISTS LUA_SOURCE_NAMES)
    list(APPEND LUA_SOURCES "${LUA_ROOT}/src/${SOURCE_NAME}")
endforeach()

add_library(LuaEmbedded STATIC ${LUA_SOURCES})
target_include_directories(LuaEmbedded PUBLIC "${LUA_ROOT}/src")
target_compile_definitions(LuaEmbedded PRIVATE _CRT_SECURE_NO_WARNINGS)
set_target_properties(LuaEmbedded PROPERTIES
    C_STANDARD 99
    C_STANDARD_REQUIRED YES
    MSVC_RUNTIME_LIBRARY MultiThreadedDLL
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/lib/Win64/x64"
    ARCHIVE_OUTPUT_DIRECTORY_RELEASE "${CMAKE_CURRENT_SOURCE_DIR}/lib/Win64/x64"
    ARCHIVE_OUTPUT_DIRECTORY_RELWITHDEBINFO "${CMAKE_CURRENT_SOURCE_DIR}/lib/Win64/x64"
    ARCHIVE_OUTPUT_DIRECTORY_DEBUG "${CMAKE_CURRENT_SOURCE_DIR}/lib/Win64/x64"
    ARCHIVE_OUTPUT_DIRECTORY_MINSIZEREL "${CMAKE_CURRENT_SOURCE_DIR}/lib/Win64/x64")
# lua.c and luac.c are standalone programs and are deliberately excluded.
# No LUA_BUILD_AS_DLL: this is a private static library, built as C, with /MD.
