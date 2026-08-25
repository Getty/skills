# Germany/DACH — Taxes and Running It as a Business

**Not tax advice.** Verified 2026-08. Thresholds change; a Steuerberater is cheaper than a
Betriebsprüfung. The point of this file is to stop an agent quoting the pre-2025 numbers,
which are the ones most guides still carry.

## 1. Is it a business?

In Germany, streaming income is normally **gewerblich** (a trade), not artistic freelancing:

- **Gewerbeanmeldung** at the local Gewerbeamt as soon as the activity is aimed at profit and
  is sustained. Cost is typically €15–60. Do it *before* the first payout, not after.
- The Finanzamt then sends the **Fragebogen zur steuerlichen Erfassung** — this is where you
  choose Kleinunternehmer status (below) and get a Steuernummer.
- **Gewerbesteuer**: a free allowance of **€24,500** profit per year for natural persons and
  partnerships; below that, no trade tax. Above it, it is largely offset against income tax.
- **IHK membership** is mandatory for Gewerbetreibende, with fee exemptions for small
  businesses in the first years.
- **KSK (Künstlersozialkasse)** is generally *not* available for gaming streamers; it can
  apply to genuinely artistic/journalistic output. Do not promise it.

## 2. Umsatzsteuer and the Kleinunternehmerregelung (§ 19 UStG)

**Reformed with effect from 2025 — these are the current numbers:**

| | Threshold |
|---|---|
| Previous calendar year turnover | **≤ €25,000** (was €22,000) |
| Current calendar year turnover | **≤ €100,000** (was €50,000 *estimated*) |

Two changes that matter beyond the numbers:

- Since 2025 the current-year limit is a **hard limit, not an estimate**: the moment turnover
  exceeds €100,000 during the year, you switch to standard taxation **from that transaction
  onward** — mid-year, not from January.
- Since 2025 Kleinunternehmer turnover is **steuerfrei** (exempt) rather than "tax not
  levied", which changes input-tax and invoicing details.

Sources: § 19 UStG as amended by the Jahressteuergesetz 2024; IHK München; Finanzamt NRW.

Being a Kleinunternehmer means: no VAT on your invoices, no input-tax deduction, and a
mandatory note on invoices citing § 19 UStG.

## 3. Twitch payouts, reverse charge and W-8BEN

- Twitch pays European streamers through **Twitch Interactive Germany GmbH** or another EU
  entity depending on the agreement — check *your* payout statements rather than assuming.
  Where the payer is in another EU country, **reverse charge** (§ 13b UStG) applies: you
  invoice without VAT, the recipient accounts for it, and you need a **USt-IdNr.** even as a
  Kleinunternehmer, plus a **Zusammenfassende Meldung (ZM)**.
- **W-8BEN** (individuals) / W-8BEN-E (entities) in the Twitch tax interview claims the
  Germany–US double-taxation treaty. Without it, US withholding is deducted at the maximum
  rate and is painful to recover.
- Payout threshold is **US$50**; from summer 2026 SEPA payouts to Eurozone streamers avoid
  the 1–2.5 % currency-conversion fee Twitch previously passed on (Twitch, 2026-05-30).

## 4. Donations are income

The most common and most expensive misconception: **viewer "donations" to a streamer are
normally taxable income**, not tax-free gifts. They are consideration for the entertainment
provided. This applies to PayPal, Streamlabs, StreamElements and Bits alike. Charity streams
are only tax-neutral if the money goes **directly** to the charity (via a proper fundraising
platform), never through your own account.

## 5. Bookkeeping in practice

- **EÜR** (Einnahmen-Überschuss-Rechnung) is sufficient below the accounting thresholds.
- Keep: Twitch payout statements, PayPal/donation exports, invoices for hardware, software
  subscriptions, internet share, room costs where deductible.
- Deductible in the normal case: streaming hardware, software licences, a proportion of
  internet, elements of the room (strictly limited in DE), Twitch/platform fees, and
  professional services.
- **Retention: 10 years** for accounting records, 6 years for business correspondence.
- Foreign-currency payouts must be converted at the correct rate and documented.

## 6. Employment and social insurance

- Streaming alongside employment: check the employment contract for secondary-activity clauses
  and inform the employer where required.
- Streaming alongside studies: watch the working-hours and income limits that affect
  Krankenversicherung and BAföG.
- Health insurance: a self-employed main occupation changes your KV status — this is the item
  most often forgotten and the most expensive to fix retroactively.

## 7. Austria and Switzerland

- **Austria**: Gewerbeanmeldung with the WKO where applicable; VAT small-business limit is
  **€55,000** net since 2025 (raised from €35,000); social insurance via SVS with its own
  thresholds. Notification duty to KommAustria — see `germany-legal.md`.
- **Switzerland**: VAT registration duty from **CHF 100,000** annual turnover; AHV
  contributions on self-employed income; no Gewerbeanmeldung equivalent, but registration with
  the AHV Ausgleichskasse.
