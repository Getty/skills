# Terminal access, consent, and subsequent processing

Sources: T1–T3, T5–T8, T10. Separate legal layers even where one UI obtains more than one permission.

## Layer 1: storing or accessing information

Assess operations covered by the national implementation of ePrivacy Art 5(3): cookies, local/session storage, IndexedDB, device identifiers, SDK storage/access, fingerprint inputs, pixel/URL identifiers and other relevant techniques. Coverage is not limited to personal data, third-party cookies or advertising. Trace what the device and recipient actually do rather than trusting the library's name.

**German overlay:** TDDDG §25 generally requires informed consent for storing/accessing information in terminal equipment, with narrow exceptions for the sole purpose of transmitting a communication over a public communications network or strict necessity to provide a digital service explicitly requested by the user. Describe the specific requested function and why this operation is essential to it.

Examples that may be defensible when properly scoped include necessary authentication/session state, a requested cart, load balancing or proportionate security operations necessary to provide the requested service. The same identifier used for cross-site advertising or product analytics needs its own analysis. Funding the service or improving conversion does not automatically make tracking strictly necessary.

If all actual terminal operations are properly exempt and no other consent-dependent processing exists, do not invent a requirement for an intrusive consent banner merely because the site uses technology. Provide the applicable information and document the exemption reasoning.

## Layer 2: personal-data processing

After the terminal-access decision, assess GDPR scope and basis for subsequent use. A terminal exception is not a blanket Art 6 basis. Consent to store an identifier does not authorise unlimited recipient sharing or unrelated model training. A legitimate-interest argument does not override a consent requirement for terminal access.

Map identifiers, IP addresses, account links, event contents, recipients, retention and transfers. Hashing identifiers can preserve identifiability and matching capability. Evaluate the actual possibility of identifying/linking people rather than treating hashing as anonymisation.

## Design valid consent

State purposes and relevant actors clearly before consent-dependent operations occur. Obtain a specific affirmative action; silence, scrolling, continued use and pre-ticked optional choices are not a substitute. Avoid misleading prominence, bundled unrelated purposes, obscured refusal, inaccessible controls or detriment that undermines free choice.

A practical baseline is equally easy, clear accept/refuse controls at the initial choice layer, granular settings, and a persistent easy withdrawal route. Mark this as an implementation of consent principles and relevant national guidance; the GDPR does not prescribe one universal button label or colour code.

Keep consent separate from contractual acceptance where the purposes differ. Record notice/purpose/vendor version and scope. If a material new purpose or recipient changes what the person agreed to, determine whether new consent/information is necessary before enabling it. Do not use a new SDK behind an old broad category without checking scope.

## Server-side and cookieless implementations

Server-side tagging can still begin with terminal access and can add further sharing/identity joins. The fact that a browser contacts only the platform's domain does not establish that no downstream vendor receives data. Inspect the backend fan-out.

Some genuinely server-derived events may not involve an additional consent-requiring terminal operation; assess actual technical facts and the national rule rather than inventing a universal rule. GDPR can still apply to those events. Reduced cookie use or shortened IP addresses can mitigate risk without making the entire system anonymous or exempt.

## Recognised consent services and browser preferences

For Germany, assess TDDDG §26 and the EinwV when integrating a recognised consent-management service. Verify the service's recognition, technical scope, correct transmission of choices, information and applicable integration duties. Their existence does not itself remove the need for valid consent where §25 requires it.

Treat machine-readable signals according to applicable law and their actual semantics. A refusal signal is not consent; a missing signal is not opt-in. Do not assume an arbitrary browser preference or vendor token proves the required informed, specific choice.

## Decision record

Record operation, device information, purpose, trigger, requested service, necessity reasoning or consent requirement, GDPR basis, recipients, duration, national rule/source and evidence. Escalate uncertain exceptions or coercive consent-or-pay designs with concrete alternatives; do not silently grant an exemption.
