using System.IO;
using UnrealBuildTool;

public class LuaEmbedded : ModuleRules
{
    public LuaEmbedded(ReadOnlyTargetRules Target) : base(Target)
    {
        Type = ModuleType.External;
        if (Target.Platform != UnrealTargetPlatform.Win64)
        {
            throw new BuildException("LuaEmbedded scaffold supports Win64 x64 only; build a platform-specific library before extending it.");
        }
        if (Target.bUseStaticCRT || Target.bDebugBuildsActuallyUseDebugCRT)
        {
            throw new BuildException("LuaEmbedded scaffold requires release dynamic CRT (/MD); rebuild and revalidate for another CRT.");
        }
        string Root = Path.Combine(ModuleDirectory, "lua-5.4.9");
        string Header = Path.Combine(Root, "src", "lua.h");
        string Library = Path.Combine(ModuleDirectory, "lib", "Win64", "x64", "LuaEmbedded.lib");
        if (!File.Exists(Header) || !File.Exists(Library))
        {
            throw new BuildException("LuaEmbedded dependency is missing. Supply verified Lua 5.4.9 source and build the static library using the skill's custom-embedding reference. Expected " + Header + " and " + Library);
        }
        PublicIncludePaths.Add(Path.Combine(Root, "src"));
        PublicAdditionalLibraries.Add(Library);
    }
}
