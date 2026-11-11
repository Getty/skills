# Select the right identifier

## Compare scope and function

| Scheme | Standard or authority | What it describes | What it does not establish |
|---|---|---|---|
| LEI | ISO 17442; Global LEI System | A legal entity within the scheme's eligibility rules | Its securities, every subsidiary, or beneficial ownership |
| ISIN | ISO 6166; ANNA and numbering agencies | A financial or referential instrument | The issuer's identity alone or a universal listing identifier |
| MIC | ISO 10383; registration authority operated by SWIFT | An exchange, platform, market segment, or related facility | A particular security or an issuer |
| CFI | ISO 10962 | An instrument's classification | Unique instrument identity or full contractual terms |
| FISN | ISO 18774 | A standardized human-readable short name | A collision-free key or complete legal name |
| Ticker | Venue or data-provider convention | A symbol in a particular namespace and period | Global, permanent identity |

Use the [ISO reference-data catalogue](https://www.iso.org/committee/6534796/x/catalogue/), [ANNA identifiers overview](https://anna-web.org/identifiers/), and [MIC authority](https://www.iso20022.org/market-identifier-codes) as starting points for scope. Retrieve actual records from the responsible source.

## Model objects before mappings

A fictional group, North Harbor, could contain a holding company and several operating subsidiaries. One subsidiary may issue a bond guaranteed by the holding company. The holding company may issue two share classes, each with multiple market listings. A single “company ID” column cannot represent all those relationships reliably.

Write the intended propositions explicitly:

- This LEI identifies this legal entity.
- This ISIN identifies this instrument.
- This entity is the issuer of this instrument according to this source.
- This listing is associated with this instrument and this market segment during this period.
- This symbol denotes this listing within this venue's or provider's namespace.

Only the first two are identifier-to-subject assignments. The remaining statements are relationships between subjects. Preserve that distinction in tables, graphs, APIs, and prose.

## Choose a key for the task

For entity aggregation, use a verified entity identifier and retain hierarchy separately. For position aggregation, use instrument identity with quantity, currency, and account context. For prices and trading, include venue, quote currency, price type, timestamp, and provider as needed. For classification, retain the CFI version or source date and decode its attributes with the appropriate code tables.

Do not make one key serve every use. An instrument can appear in several feeds; a feed can publish several price series for the same instrument. An entity can have many securities; a security's issuer can change through a legally documented event. A stable key does not make every associated attribute stable.

## Represent time and provenance

Keep both effective time and retrieval time where they matter. “This mapping was valid on 1 March” and “we downloaded it on 8 March” are different facts. Retain terminated identifiers and superseded mappings for historical queries. When the source supplies only a snapshot, do not invent precise historical validity intervals.

Give each mapping an evidence record: source, source record or URL, retrieval time, relationship type, applicable interval, and resolution outcome. Include the original vendor value alongside a standardized counterpart. This enables correction without losing the origin of a decision.

## Handle adjacent schemes

BICs, national registration numbers, CUSIPs, SEDOLs, fund identifiers, and provider-specific IDs may be useful evidence. Establish their scope and rights separately. A mapping service can connect schemes, but it does not make their subjects interchangeable. In particular, a service connecting instruments to issuers is not asserting that an instrument and its issuer are the same object.

For a task involving transaction or derivative-product identifiers, first determine whether the user means the product definition, a particular contract, a reportable transaction, or the trading venue. Add the relevant standard only after that distinction is clear.
