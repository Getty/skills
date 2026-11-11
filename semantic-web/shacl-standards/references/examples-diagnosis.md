# Worked example and diagnosis

## Define a small input contract

Require every targeted sample to have exactly one site IRI typed as a site and exactly one decimal confidence between zero and one. Permit only those predicates and `rdf:type` on the sample itself.

```turtle
@prefix ex: <https://example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:SampleShape a sh:NodeShape ;
    sh:targetClass ex:Sample ;
    sh:closed true ;
    sh:ignoredProperties ( rdf:type ) ;
    sh:property ex:RequiredSiteShape ;
    sh:property [ sh:path ex:confidence ;
        sh:datatype xsd:decimal ;
        sh:minCount 1 ; sh:maxCount 1 ;
        sh:minInclusive "0"^^xsd:decimal ;
        sh:maxInclusive "1"^^xsd:decimal ] .

ex:RequiredSiteShape a sh:PropertyShape ;
    sh:path ex:site ; sh:minCount 1 ; sh:maxCount 1 ;
    sh:nodeKind sh:IRI ; sh:class ex:Site .
```

A conforming data graph:

```turtle
@prefix ex: <https://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:sample8 a ex:Sample ;
    ex:site ex:site3 ; ex:confidence "0.85"^^xsd:decimal .
ex:site3 a ex:Site .
```

The related site is not itself closed by `ex:SampleShape`. Add a nested shape if the site's own fields require validation. The example needs no external imports or inference.

## Exercise meaningful boundaries

Removing `ex:site` should produce a minimum-count violation for the sample. Adding a different second site should produce a maximum-count violation. Repeating the identical site triple does not create a second RDF value. Replacing the site IRI with a blank node tests node-kind behavior, even if the blank node has type `ex:Site`.

Remove the site's type to test class membership under the chosen graph context. Then test an explicit subclass/type chain if the contract relies on subclass recognition. Do not attribute this basic SHACL class behavior to arbitrary OWL reasoning.

Try confidence values at zero, one, and beyond each boundary; try a string instead of a decimal; and try a malformed decimal lexical form while preserving it through the parser. Add an unexpected sample predicate to exercise closedness. Each case should isolate one requirement when practical.

Finally, remove the sample's `rdf:type`. A class target may select no sample and yield a clean report. This tests coverage rather than demonstrating that the malformed record passed the contract.

## Diagnose the right layer

| Observed issue | Likely layer to inspect |
| --- | --- |
| No results for obviously incomplete records | Targets, deactivation, selected data graph |
| Expected referenced class is missing | Available type/subclass triples and inference settings |
| Many new closed-shape violations | Newly included metadata or inferred predicates |
| Constraint succeeds on a missing property | Absent minimum count or intentionally optional field |
| Same data differs across engines | Feature support, recursion, datatype handling, inference defaults |
| SPARQL constraint finds no violation | Pre-binding, filter errors, query scope, graph selection |

Fix the diagnosed cause rather than broadening a shape until every input passes. A shape can be wrong, data can be wrong, or the run can select the wrong graph. Explain the chosen correction in those terms.

## Verify proportionately

For a simple shape change, parse the artifact and check the affected boundary. For a generated shapes collection, add metavalidation and representative target coverage. For an engine migration, compare structured report fields on the constructs actually used. Preserve failure outcomes separately from ordinary reports.

Use the [W3C SHACL test suite](https://github.com/w3c/data-shapes/tree/gh-pages/data-shapes-test-suite) as a reference for interoperability checks. These original examples support focused verification without requiring a permanent testing framework.
