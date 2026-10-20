# Version gates and evidence discipline

**Read when:** starting any task, upgrading dependencies, or resolving conflicting examples.

## Establish the actual project

Inspect every relevant workspace manifest, the selected lockfile, package-manager version, Node engines, TypeScript options, bundler configuration, React renderer, framework mode, and deployment target. A dependency range is not its resolved version. Detect multiple React copies and mismatched React/React DOM versions before diagnosing hooks. Record findings in the intake template; do not install or upgrade merely to make an example resemble this skill.

The review snapshot is 2026-10-15. Official React documentation identifies 19.3; React Compiler 1.0 is stable. React Router's current documentation selector showed 8.4.0, TanStack Table's current surface is v9, and React Flow v12 uses `@xyflow/react`. dnd kit has distinct API generations. These are **documentation observations, not a generated dependency lock or a claim that all combinations interoperate**.

## Evidence hierarchy

Prefer the repository's installed declarations and lockfile for API shape, then version-specific official docs, migration guides, and release/security notes. Treat a current homepage as insufficient evidence for an older project. Reproduce disputed behavior with a minimal test. Community examples can generate hypotheses but do not overrule the installed API.

Label findings `observed`, `source-reviewed`, `inferred`, or `unverified`. Never describe transpilation as typechecking, a JSDOM test as browser validation, a screenshot as an accessibility audit, or a package audit with no findings as proof of safety. Record an exact command, environment, exit status, and scope for every validation claim.

## Stop conditions

Pause implementation of the affected feature when a security advisory, peer mismatch, unknown commercial license, or breaking API assumption is unresolved. Continue unrelated analysis. Do not silently downgrade, enable canary builds, run package lifecycle scripts, or relax security to get a green build. RSC advisory patch levels evolve; verify all framework-provided RSC packages rather than copying an old minimum patch from a blog.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R01: React reference](https://react.dev/reference/react)
- [R02: React 19.3 release](https://react.dev/blog/2026/09/09/react-19-3)
- [R03: React Compiler 1.0](https://react.dev/blog/2025/10/07/react-compiler-1)
- [R14: RSC security follow-up](https://react.dev/blog/2025/12/11/denial-of-service-and-source-code-exposure-in-react-server-components)
- [R15: React Router modes](https://reactrouter.com/start/modes)
- [R40: TanStack Table](https://tanstack.com/table/latest)
- [R48: dnd kit](https://dndkit.com/)
- [R58: React Flow v12 migration](https://reactflow.dev/learn/troubleshooting/migrate-to-v12)
- [S01: Agent Skills specification](https://agentskills.io/specification)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
