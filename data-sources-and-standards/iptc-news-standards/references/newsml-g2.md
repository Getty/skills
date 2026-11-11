# NewsML-G2 model and XML

## Identify the item before processing content

Distinguish `newsItem`, `packageItem`, `conceptItem`, `knowledgeItem`, `planningItem`, catalog items, and `newsMessage` wrappers. A news item can carry alternative content renditions. A package organizes related items; a message transports items. A concept item describes a concept and has an item identity distinct from the concept's own identifier.

Read the namespace, `standard`, `standardversion`, and `conformance` attributes. Core conformance development stops at 2.24; later features use Power conformance, with `conformance="power"` still explicitly required by the documented contract. Do not infer the correct XSD from the namespace alone, because multiple releases share it.

Keep the persistent globally unique `guid` and item `version`. Under the NewsML-G2 version model, an omitted version defaults to 1; explicit versions start at 1 and increase on updates. Keep provider/source context for operational deduplication and collision detection without redefining an already global identifier as a URL.

## Keep metadata layers distinct

`itemMeta` carries management information such as item class, provider, creation/version time, publication status, signals, and editorial notes. `contentMeta` describes the content, including language, subjects, headline, and relevant content times or attribution. `rightsInfo` can apply at identified scopes. Content itself lives in `contentSet`, with inline or remote representations.

Distinguish `inlineXML`, textual/binary inline data under the selected contract, and `remoteContent`. Preserve media type, encoding, rendition role, dimensions, duration, and payload identity where supplied. Do not assume XML markup inside a content wrapper belongs to NewsML-G2; it can be XHTML or another vocabulary.

Resolve QCodes through an inline `catalog` or applicable `catalogRef`. A QCode alias is unrelated to an XML namespace prefix. Preserve the scheme URI and code separately and resolve them using the standard processing rules. Full concept URIs can avoid catalog requirements where supported. Do not replace HTTP vocabulary identifiers with HTTPS strings merely because retrieval redirects.

## Synthetic 2.35 Power example

```xml
<newsItem xmlns="http://iptc.org/std/nar/2006-10-01/"
          standard="NewsML-G2" standardversion="2.35"
          conformance="power"
          guid="urn:newsml:example.org:20260110:concert1" version="1">
  <catalog>
    <scheme alias="ninat" uri="http://cv.iptc.org/newscodes/ninature/"/>
    <scheme alias="stat" uri="http://cv.iptc.org/newscodes/pubstatus/"/>
  </catalog>
  <itemMeta>
    <itemClass qcode="ninat:text"/>
    <provider uri="https://example.org/provider"/>
    <versionCreated>2026-01-10T10:00:00Z</versionCreated>
    <pubStatus qcode="stat:usable"/>
  </itemMeta>
  <contentMeta>
    <language tag="en"/>
    <headline>Concert series announced</headline>
  </contentMeta>
  <contentSet>
    <inlineXML contenttype="application/xhtml+xml">
      <html xmlns="http://www.w3.org/1999/xhtml">
        <head><title>Concert series announced</title></head>
        <body><p>Example Arts Centre announced a classical concert series.</p></body>
      </html>
    </inlineXML>
  </contentSet>
</newsItem>
```

This illustrates item identity, schema selection, catalog aliases, management, language, and inline content. It supplies no commercial rights policy or real news assertion. Validate against the pinned XSD before adapting it; a provider may require additional metadata.

## Process links and management semantics

Preserve typed links and their target identifiers, locators, and optional target versions. A link without a specified item version can denote the latest available version under the documented processing rules, which affects historical replay. Keep an acquisition record of what was actually resolved. Do not confuse an alternate representation of one item with a separate item inside a package.

A correction signal such as the resolved `signal/correction` concept indicates a correction, but does not itself identify all affected prior revisions. Read the editorial note and provider contract. Apply publication-status and embargo rules before displaying or redistributing the item; retain cancellation metadata even if a cancellation contains little content.

Consult the [2.35 specification](https://www.iptc.org/std/NewsML-G2/2.35/specification/NewsML-G2-2.35-specification.html), [Power XSD](https://www.iptc.org/std/NewsML-G2/2.35/specification/NewsML-G2_2.35-spec-All-Power.xsd), and [implementation guidelines](https://www.iptc.org/std/NewsML-G2/guidelines/). XSD validity does not alone verify catalog resolution, lifecycle processing, or rights interpretation.
