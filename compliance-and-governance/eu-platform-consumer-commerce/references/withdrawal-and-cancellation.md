# Withdrawal and cancellation

## Model rights separately

Build separate commands for withdrawal, ordinary cancellation, extraordinary termination, statutory digital-product remedies and data deletion. The legal basis determines consequences; a generic “close account” endpoint cannot safely decide all of them. Withdrawal can require refunding a contract, while cancellation usually ends future performance. Deleting personal data has separate retention exceptions. Preserve an intake record even if account matching initially fails.

## Withdrawal entitlement

Determine the start and duration of the applicable withdrawal period, whether the required notice was provided, and whether an exception or early extinction actually applies. BGB §§ 355–356 govern the German baseline. Current § 356(5) addresses services; § 356(6) addresses digital content not supplied on a tangible medium. For paid services, simply giving access or consuming some tokens does not equal complete performance and extinguish the right. Digital content has its own cumulative conditions, including the proper confirmation. [C8]

If performance begins early, evaluate compensation under § 357a separately from the existence of a right to withdraw. A valid early-performance request, proper information and correct service classification matter. Do not invent a universal “used tokens are non-refundable” rule. Digital content has different compensation treatment. Maintain a refund calculation that can explain the legally permitted basis and distinguish discretionary goodwill. [C9]

## German online withdrawal function from 2026-06-19

Implement § 356a for qualifying distance contracts concluded through an online interface. Provide an easily accessible, prominent function throughout the applicable withdrawal period, with a clear withdrawal label. The statutory German labels are “Vertrag widerrufen” and “Widerruf bestätigen,” with equivalent unambiguous wording permitted. Allow name, contract or relevant part identification and the electronic destination for acknowledgement. Provide a separate clear confirmation action. Send an acknowledgement on a durable medium without delay, including declaration content and receipt date/time. Preserve dispatch timing for the statutory deadline rule. Do not demand a reason. [C10]

Recommended architecture: public entry point → minimal identification form → confirmation → durable receipt → entitlement/refund workflow. Authentication may help prefill data, but review any login requirement or recovery failure that makes the right difficult to exercise. Use anti-abuse controls proportionately; do not disclose whether another person's email has an account. Record unmatched declarations for prompt resolution rather than rejecting them outright.

## German cancellation button

Independently assess § 312k for eligible paid continuing consumer contracts available through a website. The entry action leads directly to a confirmation page with the statutory information categories and clear final action. The statutory German labels are “Verträge hier kündigen” and “jetzt kündigen,” with equivalent unambiguous wording permitted. Ensure persistent, direct and easy access, a saveable declaration and immediate electronic confirmation. If no end date is supplied, apply the statutory interpretation rather than forcing an arbitrary date. Missing compliant controls can permit termination without observing a notice period. Exceptions include the specific financial-services and stricter-form cases in the statute. [C11]

## State and failure design

- Preserve an immutable `declaration_received_at` independently of asynchronous refund success.
- Queue and retry receipts; alert an owner on delivery failure.
- Accept declarations near midnight using a documented legal time-zone rule, with UTC also retained.
- Prevent repeat clicks from causing duplicate refunds, without losing the first declaration.
- Keep a lawful non-login route usable after lost credentials, suspension or payment failure.
- Distinguish cancellation of one subscription from removal of all workspaces or team data.
- Preserve ordinary withdrawal methods; the online function does not erase other legally valid declarations.

Escalate disputed entitlement or compensation with the contract, performance log, information version and customer declaration. Never have an LLM decide refunds solely by classifying the customer's sentiment. Automate only within approved legal and commercial policy.
