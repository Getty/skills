# Sources and versioning

Treat project documentation and reference source as authority
for the selected profile; JSON Logic is not an independently ratified standards-body
specification. The project’s official pages can lag package behavior, so preserve
disagreements rather than silently choosing a convenient interpretation.

| Source | Use |
| --- | --- |
| [Project home](https://jsonlogic.com/) | Format and intended scope |
| [Operations](https://jsonlogic.com/operations.html) | Core operations and examples |
| [Truthiness](https://jsonlogic.com/truthy.html) | Cross-language truthiness contract |
| [Custom operations](https://jsonlogic.com/add_operation.html) | Extension API, eager arguments, historical security change |
| [Shared tests](https://jsonlogic.com/tests.json) | Project compatibility cases |
| [Reference repository](https://github.com/jwadhams/json-logic-js) | Package/API and implementation |
| [Releases](https://github.com/jwadhams/json-logic-js/releases) | Package release evidence |
| [2.0.5 source](https://github.com/jwadhams/json-logic-js/blob/2.0.5/logic.js) | Exact inspected evaluator |
| [2.0.5 package metadata](https://github.com/jwadhams/json-logic-js/blob/2.0.5/package.json) | Identity/version/license |
| [2.0.5 tests](https://github.com/jwadhams/json-logic-js/blob/2.0.5/tests/tests.js) | JavaScript-specific cases |

Inspected runtime: `json-logic-js 2.0.5`, retrieved from
`https://raw.githubusercontent.com/jwadhams/json-logic-js/2.0.5/logic.js`.
SHA-256: `73a6dc521e8990c2eed330dcfdb35605d7e1065a6e19d26673cb7ad4cd09d881`.
The release listing showed 2.0.5 when checked; do not convert that observation into
an evergreen “latest” claim. Record actual installed versions in every integration.

## Refresh procedure

1. Inspect project releases and official docs.
2. Pin exact packages for every supported host language.
3. Diff relevant operation and scope implementations, extension APIs, and advisories.
4. Run the upstream corpus and the application corpus with typed comparisons.
5. Update profile claims, fixtures, and migration notes together.
6. Record tests actually run and unsupported or untested paths.

Documentation and source may have different licenses. These references and
fixtures are original explanatory material; no upstream runtime is bundled.
If redistributing an evaluator, preserve its actual license and notices.
