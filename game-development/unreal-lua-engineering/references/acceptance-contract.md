# Acceptance contract and evidence

## Contents

- Identify the tested configuration
- Select the required gates
- Record evidence accurately
- Apply the read-only inspector
- Interpret failures and limits

## Identify the tested configuration

Record exact engine version, patch, changelist/source revision, platform, architecture, compiler/toolchain, C/C++ runtime, target and configuration. Record the Lua plugin revision, any local patch identity, the embedded Lua build and script-content revision. A .uproject EngineAssociation is a selection hint; inspect the engine actually invoked by the build and launch command.

Epic exposes engine version information through Build.version and its build tooling. Plugin descriptors and module rules describe compilation/loading requirements; they do not prove successful compilation or runtime behavior. [Sources: build configuration](https://dev.epicgames.com/documentation/en-us/unreal-engine/build-configuration-for-unreal-engine), [plugins](https://dev.epicgames.com/documentation/en-us/unreal-engine/plugins-in-unreal-engine), [third-party libraries](https://dev.epicgames.com/documentation/en-us/unreal-engine/integrating-third-party-libraries-into-unreal-engine).

## Select the required gates

Use only gates relevant to the requested target. Dedicated-server and remote-client tests become required for a multiplayer deliverable; they are not a prerequisite for a local scalar-evaluator experiment.

| Gate | Concrete observation |
|---|---|
| Dependency build | Matching Lua headers/library/toolchain, no stale DLL or conflicting runtime |
| Editor compilation | UHT, C++, link and plugin load all succeed for the selected engine |
| Script startup | Intended file loads via the actual loader and a known function returns expected output |
| Error handling | Syntax/runtime/non-string/type errors are reported without corrupting later calls |
| State ownership | Required PIE worlds and sessions have separate mutable state |
| Lifecycle | Repeated start/stop, travel and object destruction leave no stale callbacks/handles |
| Packaged game | File staging, dependencies and module load work outside the source tree |
| Shipping target | Required behavior does not depend on editor-only modules or debug facilities |
| Dedicated server | Server target compiles/starts without UI/editor dependencies |
| Remote clients | Owned command path and authoritative state update behave on separate clients |
| Performance | Representative data/workload meets the project's measured budget |

For the included explicit-embedding scaffold, first prove finite-number evaluation, stack stability and world lifetime. Its own pure function does not need network authority. When adding state mutation, introduce and test the command/authority contract separately.

## Record evidence accurately

Use statuses passed, failed, not_run and not_applicable. For passed/failed, record the exact command or action, timestamp, result and evidence location. Give a reason for not_applicable. Do not replace a missing log with a narrative that the same setup usually works.

Store commands as an argument array where possible. Describe interactive steps precisely enough to repeat. A record may refer to local logs or CI artifacts without copying secrets or user data into the skill.

Keep these distinctions:

- Source review verifies what a function appears to do at a specific revision.
- A syntax/metadata check verifies only the inspected representation.
- A native build verifies one target/toolchain/configuration.
- A runtime test verifies the scenario actually exercised.
- A packaged test checks deployment paths unavailable in an editor-only test.

The evidence template is deliberately incomplete. Filling it is part of the consuming project work. Do not mark gates passed when using the template merely as a plan.

## Apply the read-only inspector

scripts/inspect_unreal_lua.py reads only explicitly selected project, engine, plugin and evidence paths. It reports EngineAssociation, Build.version fields, plugin modules, embedded Lua header macros and limited source review markers. Its review markers are search results, not confirmed defects.

The inspector deliberately does not infer version support, resolve C++ semantics, inspect private credentials, fetch repositories, run build commands, execute Lua or modify source. Metadata-only use can succeed while the actual plugin still fails to compile.

Evidence inspection checks field structure and whether completed gates have a record. It does not read or authenticate referenced logs. A complete record is not a certified build.

## Interpret failures and limits

Classify build-system errors, C++ API changes, linkage/ABI issues, plugin load errors, script lookup errors, runtime errors, ownership failures and network behavior separately. Fix the earliest relevant failure before adding unrelated patches. Preserve compiler warnings that reveal real logic problems.

When the exact engine is unavailable, complete source inspection, candidate changes, staged-file configuration, test scripts and the expected verification procedure. State that engine compilation/runtime remain unverified. Avoid presenting a hypothetical result as a working UE 5.8 integration.

The creation-time environment for this skill had a native Linux C compiler and standalone Lua builds, but no Unreal installation. The template therefore carries no Unreal build certification. The role-selection fixture was tested independently; it proves only its pure decision table.
