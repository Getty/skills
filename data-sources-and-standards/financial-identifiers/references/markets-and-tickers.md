# MIC, markets, and ticker context

## Distinguish market identity from entity identity

ISO 10383 MICs identify exchanges, platforms, market segments, and related facilities that act as sources of prices and associated information. The registration authority operated by SWIFT publishes the [official MIC list](https://www.iso20022.org/market-identifier-codes). A MIC does not identify a security, and the legal entity operating a venue can separately have an LEI.

A MIC has four uppercase alphanumeric characters. A segment MIC identifies a defined part of a market; its operating MIC identifies the associated operating level. The [registration authority FAQ](https://www.iso20022.org/sites/default/files/media/file/FAQ_ISO_10383_January2023.pdf) explains this hierarchy. Do not substitute an operating MIC when a reporting or matching task specifically needs a segment.

Treat the hierarchy as a market-organization relationship, not a substitute for every legal-entity relationship. A market group can have several operating entities or platforms. A brand name seen on a website may describe a broader organization than the MIC record in question.

## Read publication and effective dates

The MIC authority publishes scheduled updates and distinguishes publication from implementation dates. A published change can carry an implementation date that still lies ahead, which is why “in the newest file” is not sufficient to determine whether a change was already effective. Recheck the [current schedule](https://www.iso20022.org/market-identifier-codes) for any operational decision.

Retain the dataset version and relevant creation, update, validation, and expiry information. Read the current [dataset factsheet](https://www.iso20022.org/sites/default/files/media/file/ISO10383_MIC_Release_2_0_Factsheet_v2.pdf) before parsing columns. Do not treat a newly downloaded file as if every row began at download time.

For historical market data, match the venue's status and identity at the trade or observation date. Preserve expired records when they explain historical trades. A current venue name change should not rewrite the historical source label without a trace.

## Qualify every ticker

Ticker conventions are determined by venues and providers. There is no single global length, punctuation grammar, or universal permanent assignment. A value such as fictional `NHR.A` can be meaningful only within the declared namespace. One provider may use a suffix to represent the exchange; another may use punctuation for share class. Do not normalize those distinctions away.

Use at least symbol, namespace or provider, venue where known, and an applicable date for resolution. Add instrument type, currency, and class when these are needed to distinguish candidates. Check official venue instrument directories, issuer disclosures, or a licensed authoritative mapping source.

Do not infer a MIC from a vendor suffix without the provider's documented mapping. A generic country suffix can represent multiple venues. A provider's composite quote can also differ from a specific exchange listing or execution venue.

## Keep listing and price-series context

A listing records an instrument's relationship to a venue under specific terms. A price series adds observation time, currency, price type, trading session, adjustment policy, and source. Two series can refer to the same instrument while differing in all of these respects.

For an original example, suppose one instrument trades as `NHR` at venue A in one currency and `NHBR` at venue B in another. Confirm the instrument mapping independently. Preserve both listings and quote currencies. Do not generate two issuers because the symbols differ, or average the prices without a declared conversion and market-data policy.

## Report uncertainty clearly

Return all plausible candidates when the user supplies an unqualified symbol. Rank them only with evidence and explain which additional context would decide the match. If a match is historical, report the interval and source; if only a current directory was available, state that limitation. A lookup returning one row is not proof that no other market has ever used the symbol.
