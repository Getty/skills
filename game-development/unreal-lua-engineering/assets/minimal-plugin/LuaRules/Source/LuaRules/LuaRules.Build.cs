using System.IO;
using UnrealBuildTool;

public class LuaRules : ModuleRules
{
    public LuaRules(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        PublicDependencyModuleNames.AddRange(new[] { "Core", "CoreUObject", "Engine" });
        PrivateDependencyModuleNames.AddRange(new[] { "Projects", "LuaEmbedded" });
        RuntimeDependencies.Add(
            Path.Combine(PluginDirectory, "Content", "LuaRules", "main.lua"),
            StagedFileType.UFS);
    }
}
