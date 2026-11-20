<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Validation and tooling

RUML release 1.0.0, dated 2026-11-15, at specification commit `d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4`. Documents declare `$specVersion: "1.0"`. Package observations below describe pinned source, not a claim that every package was installed, executed, or independently certified.

## Contents

- [Separate the questions](#separate-the-questions)
- [Official packages and inspected implementations](#official-packages-and-inspected-implementations)
- [Parser limitations that affect engineering choices](#parser-limitations-that-affect-engineering-choices)
- [A reproducible validation workflow](#a-reproducible-validation-workflow)
- [The current conformance-suite contract](#the-current-conformance-suite-contract)
- [Handling source drift](#handling-source-drift)
- [Sources](#sources)

## Separate the questions

RUML defines files, parsers, producers, evaluators, and validation tools as distinct conformance subjects. It explicitly defines no graded conformance levels. A validation tool additionally checks every catalogue rule classified `schema` or `semantic`; a schema-only check cannot establish that claim. [§1.4][conformance] [Chapter 8][rules]

| Question | Required evidence | What success does not establish |
| --- | --- | --- |
| Is the input JSON? | Strict UTF-8 decoding, JSON syntax, object root; preserve evidence needed for duplicate-key and field-order checks | RUML structure or references |
| Does its structure conform? | Appropriate draft 2020-12 schema, conditional constraints, asserted formats | Cross-object or external-reference validity |
| Is it semantically well formed? | Chapter 8 rules, capability registry, expression parsing, reference resolution, sidecar/base checks | Evaluation behavior |
| Does evaluation conform? | Operators, capability semantics, traversal, result schema, evaluation tests | Fidelity to a particular law or case |
| Is the model legally adequate? | Source coverage, interpretation, temporal applicability, evidence and domain review | A property derivable from JSON Schema or a test-suite badge |

The last row is an engineering review distinction, not an additional RUML conformance class. Keep it explicit in reports: “passes structural validation against pinned schema” is useful; “legally correct” is not a consequence.

The catalogue calls UTF-8, JSON syntax, duplicate LexID keys, and root field order semantic rules (`FMT-01`, `FMT-02`, `FMT-12`, `FMT-05`). A decoded dictionary may already have lost duplicate keys or original ordering evidence. Validate the original bytes before normalizing or reserializing. [Chapter 8][rules]

Choose the correct schema by the artifact being checked:

| Artifact | Discriminator | Schema |
| --- | --- | --- |
| Rulemap | `RUML` | `ruml.schema.json` |
| Result | `RUML-Result` | `ruml-result.schema.json` |
| Sidecar | `RUML-EXT` | `ruml-ext.schema.json` |

The catalogue is not a complete inventory of result, container, signature, or runner requirements; those also live in their own chapters. [Schema directory][schemas] [Chapter 8 scope][rules]

## Official packages and inspected implementations

These names and versions come from the pinned manifests and READMEs. Verify registry availability separately before recommending an installation in a fresh environment.

| Component | Exact package at inspection | Runtime/API | Source pin |
| --- | --- | --- | --- |
| Python schemas | `ruml-schema==1.0.0` | Python `>=3.9`; schema data/loaders | Specification pin above |
| npm schemas | `@law-as-code/ruml-schema@1.0.0` | JSON exports `.`, `/result`, `/ext` | Specification pin above |
| Python parser | `ruml-parser==1.0.0` | Python `>=3.14`; `RumlParser`, Pydantic integration | `1a421333ba0a2b4d134054417dc418c1142916ec` |
| TypeScript parser | `@law-as-code/ruml-parser@1.0.0` | ESM; `RumlValidator`, types, serialization | `cb7d754b42ff53940e154ae924b7f72f7fa8b218` |

Sources: [npm schema manifest][schema-manifest], [Python schema manifest][schema-python-manifest], [Python parser manifest][python-manifest], [JS parser manifest][js-manifest]. The Python parser pins `ruml-schema==1.0.0`. The JS repository requires pnpm 11 for its `catalog:` dependencies; consumer installation of a published npm package and development installation of the repository are different procedures. [Python README][python-readme] [JS README][js-readme]

Minimal documented Python APIs:

```python
from ruml_schema import load_ruml_schema
from ruml_parser import RumlParser

schema = load_ruml_schema()       # a schema object, not a validation verdict
parser = RumlParser()             # reuse the constructed validator
document = parser.parse_json(json_text)
```

Minimal documented JavaScript APIs:

```javascript
import { RumlValidator } from '@law-as-code/ruml-parser';
import {
  queryDatapointRefs,
  validateQueryExpression,
} from '@law-as-code/ruml-parser/query';

const validator = new RumlValidator({ expressionReads: queryDatapointRefs });
const structuralAndImplementedSemanticFindings = validator.validate(document);
const syntaxFinding = validateQueryExpression('dp_age >= 18');
```

`validate()` returns a result; `parse()` is the throwing variant. Validate each applicable expression, not just the literal demonstration above. These APIs do not turn either package into an evaluator. [JS README][js-readme] [JS query implementation][js-query]

## Parser limitations that affect engineering choices

**Python, inspected source:**

- The README explicitly describes parsing/validation only and says there is no evaluation logic.
- Generated Pydantic models are not faithful standalone validators: code generation drops top-level `allOf` and cannot follow the conditional capability routes. `RumlParser` validates against JSON Schema before mapping. Prefer its raw JSON/dict entry points. [Parser implementation][python-parser]
- `parse_model()` reserializes an already normalized model. An uppercase UUID normalized by Pydantic can therefore lose the evidence of its original invalid spelling. Do not use that path to certify submitted source bytes. [Parser implementation][python-parser]
- A `computed` DataPoint binding explicitly raises `NotImplementedError` during internal mapping. This is a parser feature gap; computed bindings are part of RUML. Do not rewrite a valid computed binding as manual input merely to make this version accept it. [Mapping `_binding`][python-mapping]
- The inspected mapping copies query/expression strings and has no JSONata parsing dependency. Successful parsing is not evidence for `CAP-29`, `CAP-38`, or computed-expression semantics. [Python manifest][python-manifest] [Mapping][python-mapping]

**JavaScript, inspected source:**

- The main entry is JSONata-free. Its default DataPoint-reference scan deliberately misses some reads inside function bodies; opt into `queryDatapointRefs` for the parser's AST-based check. [JS README][js-readme]
- Even that reader returns `[]` for an expression that fails to parse. Installing it as `expressionReads` does not validate syntax: call `validateQueryExpression` separately. The AST walker also explicitly leaves ancestor-context `%` resolution unresolved; do not claim arbitrary dynamic-expression analysis is complete. [JS query implementation][js-query]
- The dependency catalog allows `jsonata: ^2.2.1`, whereas RUML names JSONata 2.2.0. Record the actual resolved runtime and test the expressions in use instead of silently equating these versions. [JS catalog][js-catalog] [§4.8][query]
- `RumlResultValidator(id, hash)` checks both supplied reference values. It is a convenience API with stricter hash-presence expectations than the result schema's optional hash; choose the appropriate validation path deliberately. [Result validator][js-result]

Neither inspected public API supplies a complete evaluator or container processor. Treat feature support as a matrix of verified operations. “Official parser” is provenance, not proof that all normative obligations are implemented.

## A reproducible validation workflow

The following is operational guidance; the scripts bundled with this skill are deliberately limited tools.

1. Record the source commit, schema checksums, `$specVersion`, original file checksum, parser/runtime versions, and expected capability implementations.
2. Validate original UTF-8/JSON and retain duplicate-key/order evidence. Never repair invalid input silently before reporting its failures.
3. Run the pinned artifact schema with format assertions. Resolve schemas offline from a known local set; do not fetch arbitrary `$ref` targets supplied by documents.
4. Run semantic checks with rule IDs and JSON Pointers. Distinguish “failed,” “passed,” and “not checked because dependency unavailable.”
5. Check required capabilities before evaluation; resolve immutable tree versions, base files and sidecars; verify hashes where required.
6. For an evaluator, execute the applicable suite and focused regressions with test adapters, fixed clocks/IDs, and no live action effects. Validate every produced result independently.
7. Archive inputs, versions, findings, deviations and coverage. A skipped semantic or evaluation test is not a pass.

Example invocation for the bundled structural checker, from the skill directory:

```sh
python scripts/validate_schema.py /path/to/example.ruml --schemas-dir /path/to/pinned/schemas
python scripts/inspect_rulemap.py --help
python scripts/probe_operator.py --help
```

`validate_schema.py` checks schemas; `inspect_rulemap.py` inventories selected static checks; `probe_operator.py` probes six built-in logical operators over three evaluated statuses. None is a full RUML validator or runtime. Use their current `--help` output for the actual CLI, and report this boundary with results.

## The current conformance-suite contract

There is substantial drift between the runner prose and the shipped descriptors. **At the recorded pin, the executable test-data contract is the descriptor schema plus the actual descriptors.** This is a compatibility decision for running this snapshot, not an assertion that stale normative prose has been formally withdrawn. [Descriptor schema][test-schema] [Representative descriptor][and-tests]

Current descriptor handling:

1. Discover `tests/**/*.test.yaml` in a checkout; the release ZIP uses `cases/**/*.test.yaml`.
2. Parse YAML without converting quoted timestamps or status strings into other types. Validate descriptors against `tests/schema/spec-test.schema.json`.
3. Require top-level `title` and `tests`. Each test has `name` and `kind`; test names are unique within their descriptor. Resolve `ruml` relative to that descriptor, not the current directory.
4. Validation tests use `layer`, `expect: accept|reject`, optional `rules`, `at`, and `warnings`. Execute the claimed layers and state diagnostic assertions separately from acceptance assertions.
5. Evaluation tests require `run`, `inputs`, and `assertions`. `inputs` are DataPoint values, not path-indexed fabricated leaf statuses. Evaluate the referenced RUML, then evaluate each JSONata `assertions[].query` against the result and compare with `expectedValue`.
6. Apply `run.mode`; inject `evaluation.id` from `run.evaluationId` and pin the relevant clock fields when `run.frozenClock` is present. Preserve the optional nature of these settings.
7. Register the suite's synthetic capabilities with the prescribed roles when applicable: `org.ruml.test/data`, `/decision`, and `/combiner`. Their behavior is test-adapter behavior, not a production extension standard. [Runner prose][runner]

The current schema permits arbitrary `inputs` object members and leaves assertion item requirements weak; a runner should still fail malformed assertions explicitly. `LeafInput` remains in `$defs` but is not referenced by the current evaluation `inputs` schema. Do not infer the active contract from an unused definition.

The old runner prose instead describes `expect` result files and injected leaf statuses, then structural comparison with absent/null equivalence, instant-based timestamp equality, and optional free-text comparison. Current evaluation descriptors do not use that format, and their schema rejects `expect`. Do not apply absent/null equivalence to ordinary RUML schema validation or quietly drop assertion checks. [Runner prose][runner] [Descriptor schema][test-schema]

Diagnostics also drift: the descriptor's `rules` description says required codes, while the runner prose makes code/location checks optional; schema `warnings` are informational, while prose permits asserting them. State a runner policy explicitly and publish both acceptance and diagnostic coverage.

## Handling source drift

Keep a small discrepancy register with source commit, affected rule/API, reproducer, observed behavior, and chosen compatibility behavior. Do not patch upstream fixtures in place to make a run green.

- Use the actual npm package name `@law-as-code/ruml-schema`; Chapter 8 still prints `@law-as-code-institute/ruml-schema` and a GitHub-registry location. The current package manifest and README provide the installation identity. [Manifest][schema-manifest] [Chapter 8][rules]
- Distinguish package release `1.0.0`, wire format `1.0`, and the user's `metadata.version`. [§2.3][versioning]
- Preserve source bytes and unknown optional capability payloads when round-tripping; inspect serialization before assuming a normalized internal model is lossless.
- On upgrade, compare schema diffs, catalogue changes, descriptor shape, parser limitations, JSONata version, and changed outputs separately. Re-run relevant upstream cases and your known regressions against the new pinned set.

For reproducible examples and source-selection policy, see [worked-examples.md](worked-examples.md) and [sources-and-versioning.md](sources-and-versioning.md).

## Sources

[conformance]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/01-introduction/1-4-conformance.md
[rules]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/08-validation/index.md
[schemas]: https://github.com/Law-as-Code-Institute/ruml/tree/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/schemas
[schema-manifest]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/packages/npm/package.json
[schema-python-manifest]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/packages/python/pyproject.toml
[python-manifest]: https://github.com/Law-as-Code-Institute/ruml-python/blob/1a421333ba0a2b4d134054417dc418c1142916ec/pyproject.toml
[python-readme]: https://github.com/Law-as-Code-Institute/ruml-python/blob/1a421333ba0a2b4d134054417dc418c1142916ec/README.md
[python-parser]: https://github.com/Law-as-Code-Institute/ruml-python/blob/1a421333ba0a2b4d134054417dc418c1142916ec/ruml_parser/ruml_parser.py
[python-mapping]: https://github.com/Law-as-Code-Institute/ruml-python/blob/1a421333ba0a2b4d134054417dc418c1142916ec/ruml_parser/internal/mapping.py
[js-manifest]: https://github.com/Law-as-Code-Institute/ruml-js/blob/cb7d754b42ff53940e154ae924b7f72f7fa8b218/package.json
[js-readme]: https://github.com/Law-as-Code-Institute/ruml-js/blob/cb7d754b42ff53940e154ae924b7f72f7fa8b218/README.md
[js-query]: https://github.com/Law-as-Code-Institute/ruml-js/blob/cb7d754b42ff53940e154ae924b7f72f7fa8b218/src/capabilities/query-expression.ts
[js-catalog]: https://github.com/Law-as-Code-Institute/ruml-js/blob/cb7d754b42ff53940e154ae924b7f72f7fa8b218/pnpm-workspace.yaml
[js-result]: https://github.com/Law-as-Code-Institute/ruml-js/blob/cb7d754b42ff53940e154ae924b7f72f7fa8b218/src/validator/ResultValidator.ts
[query]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-8-ruml-query.md
[test-schema]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/schema/spec-test.schema.json
[and-tests]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/03-data-model/3-6-operators--and.test.yaml
[runner]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/appendix/A-spec-tests/runner-contract.md
[versioning]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/02-file-format-basics/2-3-versioning.md
