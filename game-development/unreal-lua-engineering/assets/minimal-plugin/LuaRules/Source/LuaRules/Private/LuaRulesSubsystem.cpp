#include "LuaRulesSubsystem.h"

#include "Containers/StringConv.h"
#include "Interfaces/IPluginManager.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"

THIRD_PARTY_INCLUDES_START
extern "C"
{
#include "lua.h"
#include "lauxlib.h"
}
THIRD_PARTY_INCLUDES_END

#if LUA_VERSION_NUM != 504
#error This proof scaffold is pinned to the Lua 5.4 C API. Revalidate other runtimes.
#endif

DEFINE_LOG_CATEGORY_STATIC(LogLuaRules, Log, All);

namespace
{
    FString DescribeLuaError(lua_State* L)
    {
        // lua_tolstring could allocate when converting a number. Only accept
        // an actual string here; never invoke a script's tostring/metamethod.
        const int Type = lua_type(L, -1);
        if (Type == LUA_TSTRING)
        {
            size_t Length = 0;
            const char* Text = lua_tolstring(L, -1, &Length);
            const int32 LimitedLength = Length > 4096 ? 4096 : static_cast<int32>(Length);
            const FUTF8ToTCHAR Converted(Text, LimitedLength);
            return FString(Converted.Length(), Converted.Get());
        }
        return FString::Printf(TEXT("Lua error object has type %s"),
            UTF8_TO_TCHAR(lua_typename(L, Type)));
    }
}

bool ULuaRulesSubsystem::DoesSupportWorldType(EWorldType::Type WorldType) const
{
    return WorldType == EWorldType::Game || WorldType == EWorldType::PIE;
}

void ULuaRulesSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    check(IsInGameThread());
    bReady = false;
    State = luaL_newstate();
    if (!State)
    {
        UE_LOG(LogLuaRules, Error, TEXT("Could not allocate a Lua state"));
    }
    // Deliberately do not call luaL_openlibs. This is still trusted code:
    // there is no CPU budget, allocator quota, or process isolation.
}

void ULuaRulesSubsystem::OnWorldBeginPlay(UWorld& InWorld)
{
    Super::OnWorldBeginPlay(InWorld);
    check(IsInGameThread());
    FString Error;
    bReady = LoadRule(Error);
    if (!bReady)
    {
        UE_LOG(LogLuaRules, Error, TEXT("Rule initialization failed: %s"), *Error);
    }
}

bool ULuaRulesSubsystem::LoadRule(FString& Error)
{
    if (!State)
    {
        Error = TEXT("No Lua state");
        return false;
    }
    lua_settop(State, 0);

    const TSharedPtr<IPlugin> Plugin = IPluginManager::Get().FindPlugin(TEXT("LuaRules"));
    if (!Plugin.IsValid())
    {
        Error = TEXT("LuaRules plugin was not found");
        return false;
    }
    const FString ScriptPath = FPaths::Combine(Plugin->GetContentDir(), TEXT("LuaRules/main.lua"));
    FString Source;
    if (!FFileHelper::LoadFileToString(Source, *ScriptPath))
    {
        Error = FString::Printf(TEXT("Could not read staged script: %s"), *ScriptPath);
        return false;
    }
    const FTCHARToUTF8 Utf8Source(*Source);
    // luaL_loadbufferx handles compilation errors through its status result.
    // Text mode excludes precompiled chunks. The named conversion owns its bytes.
    int Status = luaL_loadbufferx(State, Utf8Source.Get(), Utf8Source.Length(),
        "@LuaRules/main.lua", "t");
    if (Status == LUA_OK)
    {
        Status = lua_pcall(State, 0, LUA_MULTRET, 0);
    }
    if (Status != LUA_OK)
    {
        Error = DescribeLuaError(State);
        lua_settop(State, 0);
        return false;
    }
    if (lua_gettop(State) != 1 || lua_type(State, 1) != LUA_TFUNCTION)
    {
        Error = TEXT("main.lua must return exactly one function");
        lua_settop(State, 0);
        return false;
    }
    // Private-state invariant: the root function stays at stack slot 1.
    // Each evaluation pushes a copy and restores this exact stack shape.
    return true;
}

bool ULuaRulesSubsystem::Evaluate(double Input, double& Output, FString& Error)
{
    Output = 0.0;
    Error.Reset();
    if (!IsInGameThread())
    {
        Error = TEXT("Evaluate must run on the game thread");
        return false;
    }
    if (!bReady || !State)
    {
        Error = TEXT("Lua rules are not ready for this world");
        return false;
    }
    if (!FMath::IsFinite(Input))
    {
        Error = TEXT("Input must be finite");
        return false;
    }
    if (lua_gettop(State) != 1 || lua_type(State, 1) != LUA_TFUNCTION)
    {
        bReady = false;
        Error = TEXT("Lua stack invariant failed; evaluator disabled");
        return false;
    }
    if (!lua_checkstack(State, 2))
    {
        Error = TEXT("Could not reserve Lua stack space");
        return false;
    }
    lua_pushvalue(State, 1);
    lua_pushnumber(State, Input);
    if (lua_pcall(State, 1, LUA_MULTRET, 0) != LUA_OK)
    {
        Error = DescribeLuaError(State);
        lua_settop(State, 1);
        return false;
    }
    if (lua_gettop(State) != 2 || lua_type(State, -1) != LUA_TNUMBER)
    {
        Error = TEXT("Rule must return exactly one number, without string coercion");
        lua_settop(State, 1);
        return false;
    }
    const double Result = lua_tonumber(State, -1);
    lua_settop(State, 1);
    if (!FMath::IsFinite(Result))
    {
        Error = TEXT("Rule returned a non-finite number");
        return false;
    }
    Output = Result;
    return true;
}

void ULuaRulesSubsystem::OnWorldEndPlay(UWorld& InWorld)
{
    bReady = false;
    Super::OnWorldEndPlay(InWorld);
}

void ULuaRulesSubsystem::Deinitialize()
{
    check(IsInGameThread());
    bReady = false;
    lua_State* StateToClose = State;
    State = nullptr;
    if (StateToClose)
    {
        lua_close(StateToClose);
    }
    Super::Deinitialize();
}
