# Validation and evidence

Source review date: 2026-10-12. Product: PdfCraft.

| Check | Status and scope |
|---|---|
| Relevant source/documentation review | Performed; exact limits in references/sources.md and assets/sources.json. Not a complete code audit. |
| Package syntax, links and structure | Validated by the collection's offline package checker; root validation report records results. |
| Bundled helper unit tests | 32 synthetic tests passed on Linux/Python; copied helpers are byte-identical. No Craft app or provider was used. |
| Installed Craft CLI | Not found on this build environment's PATH; application workflow not run. |
| Application CLI/MCP smoke recipe | Source-reviewed recipe included; not executed against the actual application. |
| Save/reopen, rendering, media/formula/security fidelity | Not tested against the application here. |
| Fresh-agent task evaluation | Not run. Cases are supplied as test plans. |
| External source links in final offline check | Syntax checked, not all re-fetched. |

Do not translate a package/helper pass into an application or agent pass. Record binary hash/version, catalog snapshot, actual inputs/outputs and checks when running locally. Windows and macOS execution were not tested here. The helpers are bounded process controllers, not security sandboxes.
