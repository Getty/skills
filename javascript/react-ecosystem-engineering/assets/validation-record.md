# Validation evidence record

| Check | Scope / artifact stage | Command / manual procedure | Environment and revision | Actual result | Limitations |
|---|---|---|---|---|---|
| Pure unit test | | | | Not run | |
| Typecheck | | | | Not run | |
| Production build | | | | Not run | |
| Runtime integration | | | | Not run | |
| Accessibility/manual | | | | Not run | |
| Security negative case | | | | Not run | |
| Packaged/signed/update stage | | | | Not run | |

Use observed output and exit codes. Source review is not execution; syntax transpilation is not dependency typechecking; mocks do not establish an OS boundary. Include failure evidence and unresolved limitations rather than only successful commands.
