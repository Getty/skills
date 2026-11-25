# Dependencies and execution

Checked: 2026-11-25. **Getty contract proposal v0.1:** the rules below are our integration policy, not an installed provider. Read [contract.md](contract.md) for ownership, runtime keys, and consumer bindings.

## Package a complete consumer

Ship the real `package.json`, application sources, and `bun.lock`. Put runtime imports in the appropriate ordinary dependency fields; declare the exact runtime separately using the Getty object defined in the contract. A dependency lockfile does not pin the Bun executable.

**Explicitly check that the shipped `bun.lock` exists before installation.** Current Bun documentation says `--frozen-lockfile` can succeed without any lockfile by installing from `package.json`; it can also migrate another lockfile in memory. A successful frozen command therefore does not prove the intended lockfile was shipped. [Bun install](https://bun.com/docs/pm/cli/install)

Stage each consumer release in its own content-identified cache outside the user's target repositories and the shared runtime store. Include manifest/lockfile digests and runtime key in the dependency-install identity. Package required workspace files and local dependencies. Publish the prepared release immutably; put mutable application data elsewhere. Never share a mutable `node_modules` tree merely because consumers share Bun.

## Provision dependencies deliberately

1. Resolve and verify the absolute Bun executable for the consumer's exact version and target.
2. Acquire consumer-specific coordination before mutating its staged dependencies or binding. The runtime-slot mutex protects neither operation; see [installation-locking.md](installation-locking.md).
3. With the staged package as `cwd`, invoke that executable with `install --frozen-lockfile`. Do not regenerate the shipped lockfile on the target machine. Fail setup on disagreement.
4. Set a reviewed lifecycle-script policy. Use `--ignore-scripts` when compatible. If scripts are necessary, document the allowed packages, project scripts, generated assets, and required toolchains. Bun supports `trustedDependencies` and also has a default trusted list; absence of a custom list is not a universal script prohibition. [Lifecycle scripts](https://bun.com/docs/pm/lifecycle)
5. Check native dependencies and generated assets on each supported target; do not infer compatibility from Bun availability. Verify actual imports and a consumer smoke test before publishing the release and binding.

## Execute without incidental installation

Recheck the binding and executable at execution boundaries. Use argument arrays and an explicit package directory. Illustrative invocation shape:

```text
executable = validatedAbsoluteBun
args = ["--no-install", "run", absoluteEntry,
        "--target-project", absoluteTargetProject]
cwd = absoluteConsumerPackageRoot
```

`--target-project` is an illustrative application argument that the consumer must implement; it is not a Bun option. Keep Bun flags before `run`. Bun documents `--no-install` as disabling runtime auto-installation. [Runtime options](https://bun.com/docs/runtime)

Fail missing imports with an actionable setup error. Do not substitute `bunx`, `npx`, or an on-demand package download. Pass the same validated absolute executable to Bun child processes; audit scripts and shebangs rather than assuming they inherit runtime selection through PATH.

Reserve stdout for the consumer's protocol or documented output. Send diagnostics to stderr and keep setup output separate from MCP/JSON streams. Preserve exit codes and cancellation; do not report success for skipped or failed application work. Test paths containing spaces and execution from an unrelated user-project directory.
