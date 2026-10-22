# Checkout and pricing controls

## Offer model

Define base price, billing period, minimum commitment, included units, overage formula, tax treatment, credit expiry, auto-top-up behavior and every unavoidable fee. For consumer-facing German offers, use the total-price requirements of PAngV §§ 3 and 6. Where usage prevents a fixed total, provide the legally required calculation method and an intelligible example. “€20/month” is insufficient product design if customers discover only after ordering that annual prepayment or mandatory usage charges apply. [C4]

Make tokens, GPU seconds, requests and credits interpretable. State how input/output tokens, cached tokens, tools, retries, failed requests and model-dependent multipliers affect the charge. The same event must not be billed twice when a streaming response reconnects. Add user-set spending caps and clear auto-top-up controls as risk-reducing product measures; do not portray them as a universal statutory requirement.

## Pre-contract information and final order

Use the current EGBGB Article 246a checklist for German distance sales, including identity/contact, main characteristics, total costs, payment and performance, duration/termination, withdrawal, complaint handling and relevant digital functionality, compatibility and interoperability. Include personalized-price disclosures where applicable. Map each item to a visible screen and durable record rather than burying every fact in an undifferentiated terms link. [C5]

For paid online orders, assess BGB § 312j. Required prominent information must be at the legally relevant ordering point. A payment button must communicate the obligation clearly in its actual locale. A friendly label such as “Continue” or “Start now” is not evidence that the legal payment-button rule is met. Recheck app-store, wallet and embedded PSP flows end to end; outsourcing payment does not automatically outsource the seller's duties. [C6]

## Separate acknowledgements

Store distinct facts for contract acceptance, early service performance request, legally appropriate loss-of-withdrawal acknowledgement and marketing consent. Never make a contract checkbox perform all four functions. Render only the branch justified for the performance type. Require meaningful affirmative action where the law requires it; do not infer from a page view or a preselected field.

Deliver the required contract confirmation on a durable medium under BGB § 312f. Preserve the exact offer/terms/notice version accepted, document generation hash, communication destination, send time and delivery outcome. An account page whose text can be silently replaced is not automatically a durable medium. [C7]

## Engineering acceptance tests

- Open checkout as logged-out and logged-in users, in each sold locale, with and without optional cookies.
- Verify that taxes, minimum term, renewal and usage model remain visible at small viewport sizes and zoom.
- Retry a paid order after timeout; ensure one contract, one charge and one confirmation.
- Trigger PSP failure after order capture; verify the actual contractual formation rule and accurate customer message.
- Upgrade and downgrade mid-cycle; display proration and future prices before commitment.
- Confirm the old accepted terms remain retrievable after a new deployment.
- Test trial conversion with explicit future price, correct first-charge date and accessible exit route.

Store test evidence against a build and contract version. Use synthetic purchases in staging unless live test transactions are authorized. Hand legal phrase approval to counsel with screenshots and the full flow, not isolated button text.
