#pragma once

#include "CoreMinimal.h"
#include "Engine/World.h"
#include "Subsystems/WorldSubsystem.h"
#include "LuaRulesSubsystem.generated.h"

struct lua_State;

// One VM per supported world. This class intentionally has no Tick function.
UCLASS()
class LUARULES_API ULuaRulesSubsystem : public UWorldSubsystem
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void OnWorldBeginPlay(UWorld& InWorld) override;
    virtual void OnWorldEndPlay(UWorld& InWorld) override;
    virtual void Deinitialize() override;

    // Call on the game thread after this world's BeginPlay notification.
    // This is a pure numeric proof operation, not an authoritative game command.
    UFUNCTION(BlueprintCallable, Category = "Lua Rules")
    bool Evaluate(double Input, double& Output, FString& Error);

    UFUNCTION(BlueprintPure, Category = "Lua Rules")
    bool IsReady() const { return bReady; }

protected:
    virtual bool DoesSupportWorldType(EWorldType::Type WorldType) const override;

private:
    bool LoadRule(FString& Error);
    lua_State* State = nullptr;
    bool bReady = false;
};
