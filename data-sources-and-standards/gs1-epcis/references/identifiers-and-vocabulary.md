# Identifiers, CBV, and contextual fields

## Match identifier granularity to the object

| Object or scope | Common GS1 approach | Modeling caution |
|---|---|---|
| Trade-item type | GTIN | A type does not identify one serialized item |
| Serialized trade item | GTIN plus serial; corresponding EPC or Digital Link form | Preserve serial syntax and identity |
| Product lot | GTIN plus batch/lot | Use class-level quantity semantics where appropriate |
| Logistics unit | SSCC | A pallet identifier does not identify every contained item |
| Party or location | GLN, with the appropriate role and extension where applicable | Do not conflate company, site, and read point |
| Asset | GRAI or GIAI as applicable | Asset identity is distinct from goods carried by the asset |

Use the [EPC Tag Data Standard](https://ref.gs1.org/standards/tds/archive) and [GS1 Digital Link URI Syntax](https://ref.gs1.org/standards/digital-link/uri-syntax/) for the precise encodings. EPCIS is not restricted to RFID as a capture technology. A valid URI encoding does not prove an identifier was legitimately assigned.

## Distinguish URI forms

An EPC pure-identity URI describes identity independently of RFID tag encoding details. Do not place a tag-encoding URI into a field requiring a pure-identity representation. GS1 Digital Link represents keys and qualifiers in web URI form. Equivalent GS1 identities can have different supported representations, so string equality alone can be insufficient.

Use documented conversion rules and the required GS1 Company Prefix partition information. Do not infer prefix length from arbitrary digit splits or guess missing check digits and serial qualifiers. Preserve the original form and record a canonical comparison form where a profile needs it. A successful HTTP response from a Digital Link resolver is different from proof of the underlying identity assignment.

## Use CBV meanings precisely

CBV supplies standard vocabulary values for business steps, dispositions, business transaction types, sources/destinations, and related concepts. A business step describes the process activity; a disposition describes the business state after the event. The [CBV standard](https://ref.gs1.org/standards/cbv/2.0.0/) and [browsable vocabulary](https://ref.gs1.org/cbv/) are the authority for definitions.

For example, `shipping` and `in_transit` answer different questions. A receiver's observation can concern a different step and state. Do not map a local status to the nearest-sounding CBV label without checking its definition. If no standard value fits, use an appropriately governed extension and document the interoperability consequences.

In JSON-LD, the official context expands supported compact terms to their defined IRIs. XML and other representations can use URI forms prescribed by the standard. Preserve semantic equivalence through the context and vocabulary rules; arbitrary replacement of punctuation or URI prefixes is unsafe.

## Separate location and transfer concepts

A read point identifies where the observation occurred, such as a dock door. A business location gives the business location associated with the objects following the event under the model. They can differ. A physical read point is not necessarily the reporting party's headquarters or the object's destination.

Sources and destinations are typed. A possessing party, owning party, and physical location have different meanings. Record only the type supported by the business evidence. A purchase-order reference can describe commercial context without establishing a transfer of ownership or possession.

## Interpret quantities and master data

Use instance lists for individually identified objects and quantity lists for classes or lots. Preserve the class identifier, quantity, and unit. Counts and measured quantities are different; omission of quantity is not zero. Read the event-specific allowed structures and [quantity definitions](https://ref.gs1.org/standards/epcis/2.0.1/), including restrictions on units for physical quantities. Sensor units have a broader purpose than object quantity units.

Do not double-count a pallet and its child cases as equivalent inventory. Conversions from case counts to individual units require master data and effective packaging definitions. Keep descriptive master data, instance/lot master data, and changing event observations separate.

## Govern extensions

Use a namespace controlled by the extension's publisher, publish meanings and datatypes, and map JSON-LD terms deliberately. Keep standard terms protected. Agree which extensions are required, ignored, or preserved by trading partners. A syntactically accepted unknown field is not proof that another party understands its meaning.
