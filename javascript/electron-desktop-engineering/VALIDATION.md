# Validation evidence and limits

Recorded **2026-10-15**. Environment: Linux x86-64 authoring container; Node.js **22.16.0**; Python **3.13.5**; global TypeScript **5.8.3**. These are execution-environment observations, not a recommended universal application toolchain.

## Executed checks

| Check | Result | Scope / evidence |
|---|---|---|
| Dependency-free Node tests | **69/69 passed** | [TAP output](tests/results/node-tests.txt) |
| Python tooling tests | **14/14 passed** | [Output](tests/results/python-tests.txt); same shared tooling suite is distributed in each skill |
| TypeScript declaration consumer | **Passed** | [Command/output](tests/results/type-contracts.txt); pure graph/bridge declarations, including expected compile errors |
| TS/TSX syntax transpilation | **2 files passed** | [Output](tests/results/ts-syntax.txt); no dependency resolution/typechecking |
| JavaScript syntax | **6 files passed** | [Per-file results](tests/results/javascript-syntax.json); `node --check` |
| Bundle structure, local links, JSON and hashes | **Passed** | Local targets/reachability, JSON, basic frontmatter and complete SHA-256 manifest; no external HTTP requests |

The policy tests exercise fixed asset routing, parsed application/external URL policies, credential/port/suffix/encoding/traversal cases, mocked WebContents/top-frame authorization, malformed/extra/oversized theme values, and token-bucket behavior. Sender/frame tests use mocks, not real Electron frames.

The Python tests cover read-only manifests, skipped dependency/symlink paths, scan/size limits, malformed inputs, heuristic reporting, npm-lock distinction, catalog lookup, and local-link resolution. They do not establish a complete static security analysis or parse every package-manager lock format.

## Not executed / not claimed

Electron and Playwright were not installed/launched. The shell was not packaged, signed, notarized, installed, updated, or tested on Windows/macOS/Linux desktops. Real sandbox/permission/CSP enforcement, sender/frame behavior, native modules, fuse state, secure-storage backend, and update authenticity were not tested. The integration specification is supplied but unexecuted. The example preferences are intentionally memory-only.

Registry access from the execution container failed with DNS resolution errors. Current official documentation was accessible through web research, but that is not the same as installing dependencies. No lockfile was fabricated and no unverified Electron release number was supplied. No penetration test, complete accessibility audit, external-link crawler, commercial-license audit, or exhaustive library compatibility matrix was executed.

## Evidence interpretation

The source register identifies documents actually reviewed; catalog discovery pointers are explicitly not contemporaneous maintenance/API endorsements. Original procedures and test designs are engineering recommendations. Passing mocked/pure tests does not prove browser, Electron, OS, signing, or update enforcement.

`MANIFEST.json` protects packaged file integrity relative to the recorded hashes; it is not a signature proving publisher identity. It excludes itself. The externally supplied ZIP checksums cover archives. The local validator checks a basic frontmatter subset and reference reachability, not the complete upstream Agent Skills specification.

## Next environment's release gate

Use [the validation record](assets/validation-record.md) to record resolved dependencies, supported target environments, actual type/build/runtime tests, negative cases, packaged-stage checks, and residual risks. Keep each unexecuted stage explicitly marked Not run. Do not promote this report into a production certification.
