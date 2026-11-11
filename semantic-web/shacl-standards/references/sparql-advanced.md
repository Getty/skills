# SHACL-SPARQL and advanced feature boundaries

## Extend Core only where useful

Use SHACL-SPARQL for cross-record relationships, calculations, or conditions that Core cannot express clearly. A SPARQL-based constraint returns solutions for violations, rather than returning the conforming rows. Keep the query scoped to the intended focus node and dataset.

The following original constraint requires an inventory code to be unique among resources carrying that predicate:

```turtle
@prefix ex: <https://example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .

ex:InventoryCodeShape a sh:NodeShape ;
    sh:targetSubjectsOf ex:inventoryCode ;
    sh:sparql [ a sh:SPARQLConstraint ;
        sh:message "This inventory code is used by another resource." ;
        sh:select """
            PREFIX ex: <https://example.org/>
            SELECT DISTINCT $this (ex:inventoryCode AS ?path) ?value
            WHERE {
                $this ex:inventoryCode ?value .
                ?other ex:inventoryCode ?value .
                FILTER(!sameTerm($this, ?other))
            }
        """ ] .
```

This does not require a code to exist on records lacking the predicate; use a separate target and minimum-count constraint for requiredness. Its uniqueness scope is the selected data graph, not every possible external dataset.

## Respect pre-binding and restrictions

`$this` is pre-bound to the focus node. Property-shape queries can use `$PATH` in the prescribed predicate position for substitution of the shape's path. Projection variables such as `?path` and `?value` influence report fields under the specification's mapping rules.

Do not rewrite a normal SPARQL query into a SHACL constraint by inserting arbitrary pre-bound variables and assuming equivalent scope. SHACL-SPARQL imposes restrictions, including on constructs such as `MINUS`, `SERVICE`, and inline `VALUES`, and on how pre-bound variables appear. Read the standard's restrictions before generating advanced queries.

Support for `$shapesGraph` and `$currentShape` is optional in the 2017 specification. A constraint depending on them is less portable, and unsupported required use must not be silently treated as conformance. Use explicit prefixes in query strings or valid SHACL prefix declarations; Turtle prefix declarations alone are not universally injected into SPARQL strings.

A SELECT-based constraint and a reusable custom constraint component have different declaration structures. Custom components can use supported validator forms and parameters; verify the actual implementation rather than assuming every Core validator supports all extension hooks.

## Keep advanced features explicit

The 2017 SHACL Recommendation defines Core and SHACL-SPARQL. SHACL Advanced Features is a separate Working Group Note covering areas such as custom targets, functions, node expressions, and rules. JavaScript extensions and vendor facilities have additional execution and support requirements.

Rules can derive data; validation checks conditions. Decide whether rules run before validation, whether they iterate, and where derived triples are stored. Do not assume a rule-enabled run has the same target set or outcome as validating the original graph.

## Treat recursion as a compatibility decision

The 2017 Recommendation leaves validation with recursive shapes undefined. Engines may support particular recursion semantics or report a failure. A cyclic graph is not automatically a recursive shape; recursion concerns shape references that return to a shape through the relevant constraint structure.

Inspect mutually referring `sh:node` shapes and logical/qualified references before relying on portable behavior. Record the engine's recursion policy and verify a concrete cyclic example when the model needs it. Do not assert that all engines use a common fixed point.

New SHACL 1.2 work separates several areas into evolving specifications. Consult [SHACL 1.2 Core](https://www.w3.org/TR/shacl12-core/), [SPARQL-related features](https://www.w3.org/TR/shacl12-sparql/), and their headers before selecting newer constructs. For the baseline, read [SHACL-SPARQL](https://www.w3.org/TR/shacl/#sparql-constraints) and [SHACL Advanced Features](https://www.w3.org/TR/shacl-af/).
