# Sources and versioning

## Baseline and authority

Use [OMG DMN 1.6](https://www.omg.org/spec/DMN/1.6)
as the formal baseline. Its history lists September 2026; the normative document
identifier is `formal/25-12-02`. The [OMG catalog](https://www.omg.org/spec/About/)
also lists DMN 1.7 beta. A beta is not a replacement for a pinned formal profile.
Read the [normative PDF](https://www.omg.org/spec/DMN/1.6/PDF), especially clauses
2, 6–11 and XML interchange. This skill uses original explanations and examples;
it does not redistribute the specification.

Keep three independent versions: the DMN interchange language, the business model
revision, and the implementation release. A model exported yesterday can still use
an older namespace. A runtime supporting FEEL does not thereby support every DMN
construct or B-FEEL.

## Primary source map

| Source | Use it for |
| --- | --- |
| [DMN 1.6 release](https://www.omg.org/spec/DMN/1.6) | Normative artifacts and formal publication status |
| [DMN16 XSD](https://www.omg.org/spec/DMN/20240513/DMN16.xsd) | Model XML grammar and default language URI |
| [DMNDI15 XSD](https://www.omg.org/spec/DMN/20230324/DMNDI15.xsd) | Diagram interchange referenced by 1.6 |
| [OMG issue tracker](https://issues.omg.org/issues/spec/DMN/1.6) | Reported ambiguities and later dispositions |
| [DMN TCK repository](https://github.com/dmn-tck/tck) | Concrete tests, runner instructions, and license |
| [TCK results](https://dmn-tck.github.io/tck/index.html) | Versioned submissions and missing/unsupported cases |
| [Apache KIE DMN](https://kie.apache.org/drools/dmn/) | KIE implementation capabilities and documentation |
| [Camunda DMN](https://docs.camunda.io/docs/components/modeler/dmn/) | Camunda's model and runtime profile |
| [Camunda hit policies](https://docs.camunda.io/docs/components/modeler/dmn/decision-table-hit-policy/) | A concrete supported-policy subset |
| [Camunda FEEL](https://docs.camunda.io/docs/components/modeler/feel/) | Implementation semantics, functions, and examples |

Documentation paths without release numbers can move. Record the displayed release
and the retrieval date when making a product claim. The inspected Camunda pages
identified version 8.10; do not project that profile onto Camunda 7 or all engines.

## Refresh procedure

1. Resolve the latest formal version from OMG, then inspect actual artifacts.
2. Read changebars and relevant resolved issues; do not migrate on version labels alone.
3. Pin the modeler, engine, adapter, schema bundle, and TCK revision used for checks.
4. Rerun boundary, no-hit, duplicate-output, null, import, and expression cases.
5. Compare output types, diagnostics, and matched-rule traces as well as values.

Preserve normative/implementation differences in the report. In particular, DMN 1.6
clause 8 permits compound Output Order while clause 10's invocation semantics
restrict it. Acknowledge this textual disagreement; do not turn one reading into a
universal promise. The safe portable modeling choice is a single output or an
explicitly tested post-processing step.
