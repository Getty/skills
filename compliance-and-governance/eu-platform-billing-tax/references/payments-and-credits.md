# Payments, credits and regulatory perimeter

## Draw the money flow

Identify payer, payee, legal seller, PSP, bank accounts, custody, settlement, fees, refunds and third-party payouts. Distinguish selling the platform's own service from collecting money for another merchant. Read the actual PSP/merchant-of-record contract and determine who is responsible for tax, invoices, refunds, disputes and licensing. An integration logo is not proof that responsibility transferred.

## Prepaid AI credits

Describe whether credits are a prepaid entitlement to the operator's service, transferable value, redeemable cash, a single-purpose/multi-purpose voucher, or accepted by independent merchants. The VAT voucher framework and e-money/payment framework are separate tests. For Germany, assess UStG § 3(13)–(15) and ZAG § 1/§ 2 with a specialist for uncertain designs. [T15, T16]

ZAG's e-money definition includes, among other elements, value issued against funds and acceptance by persons other than the issuer. Do not assert that every closed-loop service token is e-money, or that any “utility token” label makes a transferable wallet unregulated. Other payment-service activities can still require assessment even where e-money is not involved.

## Marketplace and payout changes

Treat adding third-party model sellers, creator earnings, transferable balances or user-to-user payments as a perimeter-change trigger. Assess payment services, e-money, AML/KYC, platform tax reporting and the role of an authorized provider. A marketplace may have contractual and tax duties despite using a PSP. Do not apply a commercial-agent or limited-network exclusion without analyzing its precise conditions and notification requirements. [T16]

## Credit and installment features

Screen deferred payment, revolving balances, financed subscriptions and consumer installment offers separately. The relevant EU/national consumer-credit and authorization rules can change by effective date. Check the national implementation and application of Directive (EU) 2023/2225, whose general application date is 2026-11-20, before offering a feature around that date. Do not treat a future directive date as proof that today's national rule is absent. [T17]

## Technical payment controls

Use appropriate PSP-hosted/tokenized handling to minimize sensitive payment data. Verify webhook authentication, replay protection, idempotency, least-privilege keys, account-change controls and reconciliation. Assess PSD2/SCA responsibilities and exceptions with the provider; do not hardcode an exemption based on a broad product assumption. PCI DSS is a payment-industry contractual standard with a scoped compliance process, not an EU statute. [T18]

## Agent boundary

Allow the agent to analyze the structure, draft policy and test a sandbox. Require actual authorization to move money, change payout destinations, issue credits or submit regulatory filings. Preserve approved routine refund rules. Present exact transactions, amounts, reasons, beneficiaries and supporting evidence when seeking a financial decision.
