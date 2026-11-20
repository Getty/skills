# Sources and versioning

## Normative baseline

Use [OMG DMN 1.6](https://www.omg.org/spec/DMN/1.6)
as the formal baseline. The [normative PDF](https://www.omg.org/spec/DMN/1.6/PDF)
contains S-FEEL in clause 9, FEEL in clause 10, and B-FEEL in clause 11. The
[OMG catalog](https://www.omg.org/spec/About/) lists 1.7 beta separately. Do not
silently incorporate beta changes into a 1.6 contract.

Relevant 1.6 language identifiers are:

- FEEL: `https://www.omg.org/spec/DMN/20240513/FEEL/`
- B-FEEL: `https://www.omg.org/spec/DMN/20240513/B-FEEL/`

Use the release's actual artifacts instead of constructing namespace dates. A
standalone interpreter may choose the dialect through an API rather than these
XML identifiers; document that mapping.

## Primary source map

| Source | Scope |
| --- | --- |
| [DMN 1.6 PDF](https://www.omg.org/spec/DMN/1.6/PDF) | Grammar, value model, semantics, built-ins, dialects |
| [OMG issues](https://issues.omg.org/issues/spec/DMN/1.6) | Ambiguities and later fixes |
| [Camunda FEEL guide](https://docs.camunda.io/docs/components/modeler/feel/) | A concrete host/engine profile |
| [Camunda unary tests](https://docs.camunda.io/docs/components/modeler/feel/language-guide/feel-unary-tests/) | Input-test mode and examples |
| [Camunda Boolean expressions](https://docs.camunda.io/docs/components/modeler/feel/language-guide/feel-boolean-expressions/) | Runtime comparison and Boolean behavior |
| [Camunda temporal expressions](https://docs.camunda.io/docs/components/modeler/feel/language-guide/feel-temporal-expressions/) | Temporal implementation details |
| [feelin source](https://github.com/nikku/feelin) | JavaScript interpreter API and limitations |
| [DMN TCK](https://github.com/dmn-tck/tck) | Shared executable language cases |

The inspected Camunda documentation showed version 8.10. The executable examples
were tested with **feelin 8.2.0**, fetched as an exact package version on the check
date. No claim is made that this interpreter implements every DMN 1.6 feature.
The examples and helper are original; upstream specifications and packages are
not redistributed inside this skill.

## Separate claims and observations

Treat the specification as normative, engine docs as a supported profile, and an
actual run as an observation about one version/configuration. Keep all three when
they differ. For example, the bundled decimal probe expects true under normative
decimal semantics, but feelin 8.2.0 returned false without a warning. That observation
is a reason to test numeric requirements, not to redefine FEEL arithmetic.

## Refresh deliberately

Check formal versus beta status, changes to built-ins and dialect behavior, and
runtime release notes. Pin the engine and fixtures; rerun discriminating cases for
null, decimal arithmetic, unary-test mode, scope, empty collections, and time zones.
A newer parser version or an updated documentation page does not by itself justify
changing production decision behavior.
