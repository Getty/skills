# ninjs model, examples, and migration

## Select the exact family and schema

Do not treat ninjs 1.x, 2.x, and 3.x as interchangeable spellings of one object. The 1.x family includes pattern-based property names and object-keyed renditions/associations. The 2.x family uses explicit arrays and more uniform property names. The 3.x family uses camelCase and adds event/planning and live-production capabilities. Use the official migration guidance for the actual versions involved.

For example, `versioncreated` becomes `versionCreated`; a 1.x `headline_*` field must be converted into the appropriate headline-array structure rather than merely capitalized. Preserve the role previously encoded in a property name. Do not assume recursive key renaming performs a semantic migration.

The verified ninjs 3.2 schema declares JSON Schema 2020-12. Its news object requires `uri`, with additional structures imposing their own requirements. A minimal schema-valid object is not a sufficient provider profile. Distinguish the news object `uri` from external URLs and distinguish `version` from `standard.version`. In 3.2, item `version` is a string; do not assume numeric ordering without the provider's contract.

## Preserve content and related objects

Keep `headlines` for publishable headlines and `title` for the item's short metadata name. Preserve each body's `contentType`, role, and text. Do not strip markup before recording the original content and language. Keep `renditions` as alternative media representations with their metadata. Keep `associations` as associated news objects; in the 3.2 schema these inherit the news-object structure and require an association `name` in addition to their own `uri`.

Preserve people, organizations, places, subjects, events, and information sources as distinct roles. Their presence says how metadata relates to the item; it does not establish arbitrary relations between all mentioned entities. Keep subject `confidence` and `relevance` in their declared 0–100 assignment context rather than reinterpreting them as probability that the story is true.

## Synthetic ninjs 3.2 example

```json
{
  "uri": "urn:newsml:example.org:20260110:concert1",
  "type": "text",
  "version": "1",
  "standard": {
    "name": "ninjs",
    "version": "3.2",
    "schema": "http://www.iptc.org/std/ninjs/ninjs-schema_3.2.json#"
  },
  "versionCreated": "2026-01-10T10:00:00Z",
  "pubStatus": "usable",
  "language": "en",
  "headlines": [{"value": "Concert series announced"}],
  "bodies": [{
    "contentType": "text/plain",
    "value": "Example Arts Centre announced a classical concert series."
  }],
  "subjects": [{
    "uri": "http://cv.iptc.org/newscodes/mediatopic/20000022"
  }]
}
```

The subject identifier denotes IPTC's classical-music concept. The publisher and story are fictional. This example illustrates a declared schema version and does not imply rights to any external content.

## Validate extensions and conversions

Inspect nested `additionalProperties`, root `unevaluatedProperties`, required fields, and any external `$ref` dependencies. Do not silently accept provider extensions under the unmodified official schema if that schema disallows them. Use the documented extension mechanism or a named provider schema, retain the original input, and report the conformance target honestly.

Treat `rightsInfo.linkedRights` and `encodedRights` according to their schema alternative, preserving the expression language identifier. Do not convert a structured rights expression into a plain copyright notice. Likewise, `embargoedUntil` is not a generic replacement for every NewsML-G2 conditional or indefinite embargo representation; document any conversion loss.

Validate both syntax and semantic preservation after migration. Compare identities, language, timestamps, body roles, nested associations, renditions, rights, and editorial status. Keep fields with no target equivalent visible in the conversion report. Consult the [user guide](https://www.iptc.org/std/ninjs/userguide/) and [3.2 schema](https://www.iptc.org/std/ninjs/ninjs-schema_3.2.json), then recheck the [distribution index](https://www.iptc.org/std/ninjs/) for newly published versions.
