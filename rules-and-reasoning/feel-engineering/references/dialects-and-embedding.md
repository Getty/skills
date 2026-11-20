# Dialects and embedding

## Choose the language contract

| Profile | Scope | Main caution |
| --- | --- | --- |
| S-FEEL | Simpler subset for basic decision logic and tests | Do not assume full lists, contexts, or functions |
| FEEL | Full typed expression language from DMN | Null/errors and typed operations require care |
| B-FEEL | DMN 1.6 dialect sharing FEEL grammar | Invalid-operation defaults change outcomes |
| Vendor extension profile | Product-specific functions, syntax, or binding rules | Portability requires explicit feature checks |

FEEL is defined within DMN, but a host can embed an interpreter without a whole
DMN model. Conversely, a DMN engine may support only a subset of the newest
expression features. [DMN 1.6 clauses 9–11](https://www.omg.org/spec/DMN/1.6/PDF)
are the normative reference, not the feature set of any single playground.

## Keep parser entry points distinct

`weight < 10` is a complete expression. `< 10` is a unary test that consumes an
implicit value. A product may select this mode based on the cell or form field.
Record that selection and use the corresponding API when testing independently.

Some workflow products prefix an expression field with `=` to distinguish it from
literal text. That marker is a host convention; do not add it blindly to source
sent to a FEEL interpreter. Likewise, JavaScript object syntax around a context or
XML escaping around a DMN expression belongs to the container, not the language.

## Treat B-FEEL as a semantic migration

B-FEEL preserves grammar while changing invalid-operation results. For example,
`"x" = 1` yields null in FEEL and false in B-FEEL. Several functions that return
null on invalid input instead return a type-specific value such as zero, an empty
string, or an empty collection. Numeric collection functions can ignore nonnumeric
items; this can affect Collect Sum in a surrounding DMN table.

Do not describe B-FEEL as removing all possible missing data. Missing information
still exists, and warnings remain important. Do not apply a universal
`null -> false` post-processing rule and call it B-FEEL: the changes are defined
per operation. Confirm the runtime actually supports the dialect.

The OMG issue history includes later clarifications around null collections in
B-FEEL. Keep a reduced case and the selected version when behavior is ambiguous;
read [issues](https://issues.omg.org/issues/spec/DMN/1.6) instead of silently
borrowing a 1.7 beta resolution.

## Separate language and host restrictions

Standard names can be more expressive than a workflow variable naming convention.
A host may restrict names, expose only specific built-ins, coerce input values, or
reject expressions at deployment. Record the product rules separately. A script
that parses in a standalone interpreter may still fail in a product field whose
allowed names or expected result type are narrower.
