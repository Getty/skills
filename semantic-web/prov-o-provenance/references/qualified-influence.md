# Qualified influence, roles, plans, and times

## Add an intermediate node for relation details

Use a qualified influence when a bare edge cannot carry the needed information. The subject of the simple relation links to an influence node; that node identifies the influencing entity, activity, or agent. Do not reverse the edge to the qualification node or mistake the influence node for the responsible actor.

| Simple relation | Qualification property | Node class | Influencer property |
| --- | --- | --- | --- |
| `wasGeneratedBy` | `qualifiedGeneration` | `Generation` | `activity` |
| `used` | `qualifiedUsage` | `Usage` | `entity` |
| `wasDerivedFrom` | `qualifiedDerivation` | `Derivation` | `entity` |
| `wasAttributedTo` | `qualifiedAttribution` | `Attribution` | `agent` |
| `wasAssociatedWith` | `qualifiedAssociation` | `Association` | `agent` |
| `actedOnBehalfOf` | `qualifiedDelegation` | `Delegation` | `agent` |
| `wasInvalidatedBy` | `qualifiedInvalidation` | `Invalidation` | `activity` |
| `wasInformedBy` | `qualifiedCommunication` | `Communication` | `activity` |

All entries in the table use the `prov:` namespace. The qualified pattern can support corresponding simple relations through PROV-O property chains. Emitting those simple relations explicitly improves interoperability where inference is unavailable. Ensure both forms agree; duplicate serializations of one relation should not become duplicate process events.

## Place qualifiers on the appropriate relation

Use `prov:hadRole` on an association or instantaneous event, including usage or generation. Define the role resource and its meaning in the application's vocabulary. A role belongs to the participation in a particular activity, not necessarily to the agent for all time.

Use `prov:hadPlan` on a qualified association to identify a `prov:Plan`, which is an entity describing intended steps. A plan does not prove those steps were executed. Capture the actual run independently. Attach versioned configuration or model artifacts as entities used by the run when they are actual inputs.

Use `prov:atTime` for an instantaneous event. Use `prov:startedAtTime` and `prov:endedAtTime` for activity boundaries. Generation and invalidation also have direct entity time properties. Do not attach `prov:atTime` arbitrarily to an association, attribution, or derivation merely because a timestamp is available; doing so can impose an unintended event type. Use a defined metadata property for the time the assertion was recorded.

## Qualified usage and association example

```turtle
@prefix ex: <https://example.org/prov/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:input a prov:Entity .
ex:software a prov:SoftwareAgent .
ex:method a prov:Plan .
ex:sourceRole a prov:Role .
ex:operatorRole a prov:Role .
ex:run a prov:Activity ;
    prov:used ex:input ;
    prov:qualifiedUsage ex:readInput ;
    prov:wasAssociatedWith ex:software ;
    prov:qualifiedAssociation ex:operatorAssociation .
ex:readInput a prov:Usage ;
    prov:entity ex:input ;
    prov:hadRole ex:sourceRole ;
    prov:atTime "2026-01-10T10:00:02Z"^^xsd:dateTime .
ex:operatorAssociation a prov:Association ;
    prov:agent ex:software ;
    prov:hadRole ex:operatorRole ;
    prov:hadPlan ex:method .
```

## Express derivation and delegation precisely

A qualified derivation can identify `prov:hadActivity`, `prov:hadUsage`, and `prov:hadGeneration`. Link the actual usage of the source and generation of the output. If those events are unknown, omit them rather than creating fictitious times or unrelated events. If a transformation spans several activities, choose whether a documented aggregate activity is appropriate; do not assume PROV automatically invents it.

In a qualified delegation, link the principal with `prov:agent` and the relevant activity with `prov:hadActivity`. This scopes the responsibility relationship. Employment, account ownership, or a shared organization name is not enough by itself to assert that delegation occurred.

For attribution-specific role metadata, use a suitable application extension instead of assuming `prov:hadRole` applies everywhere. The [PROV-O qualification tables and term definitions](https://www.w3.org/TR/prov-o/#description-qualified-terms) are authoritative; their domain restrictions matter even when an RDF parser accepts the triples.
