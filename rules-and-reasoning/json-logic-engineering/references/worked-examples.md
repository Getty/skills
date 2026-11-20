# Worked examples

## Synthetic training request

`assets/examples/training-eligibility.logic.json` returns true when a request has the
required facts, age is at least 18, active is Boolean true, and completed modules are
at least 3. These are synthetic program rules, not legal eligibility criteria.

`assets/examples/input.schema.json` declares the intended types and bounds.
`assets/examples/training-cases.json` separates input validity from the expected
business result. Validate the schema before using the rule in an application.
An invalid numeric string must be rejected even if raw coercing comparison would pass.

## Static inspection

```bash
python3 scripts/inspect_rule.py assets/examples/training-eligibility.logic.json
```

The restricted authoring profile accepts core operation objects, scalar literals,
and arrays. It rejects inline record literals, unsupported operators, selected
dangerous static path segments, unsuitable arities, duplicate keys, non-finite values,
and excessive size/depth. It requires an explicit fallback for authored `if` and an
explicit initial accumulator for `reduce`. These restrictions intentionally exceed
what a raw evaluator may accept.

It reports static paths and a dynamic-path count. Paths inside a collection body
are relative to that body; the inventory is not a complete external dependency graph.
A dynamic path cannot be treated as fully known.

## Execute the behavioral corpus

The runner requires Node.js 18 or newer (including `structuredClone`). Use a trusted
installed `json-logic-js` module or its pinned `logic.js` file:

```bash
node scripts/run_cases.cjs --engine /trusted/path/to/logic.js assets/examples/semantic-cases.json
```

The runner checks literal values, missing/null, truthiness, lazy control paths,
strict/coercing scalar comparison, collection scope, empty quantifiers, reductions,
unknown operations, and non-finite raw outputs. Expected non-finite results are
diagnostic observations; a production JSON adapter should reject them.

The helper loads trusted local code. It is not a sandbox or a package downloader.
Each case declares exactly one expected value, expected error substring, or expected
special numeric value. A mismatch produces a nonzero exit.

## Verification scope

The bundled fixtures and helpers were checked against downloaded
`json-logic-js 2.0.5` source, with its SHA-256 recorded in sources-and-versioning.
The original semantic corpus was executed with Node. Input schema cases were
checked separately with a JSON Schema validator. Static negative probes tested
duplicate keys, unknown operations, invalid arity, path restrictions, and depth.
These checks do not establish compatibility with PHP, Python, Rust, or other ports.

Do not vendor a dependency merely to run these helpers. Record the chosen package
and lockfile in the consuming project.
