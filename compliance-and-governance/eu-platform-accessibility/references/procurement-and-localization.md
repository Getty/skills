# Procurement and localization

## Evaluate third-party components

Inventory identity providers, payment widgets, chat editors, code viewers, tables, PDF generators, consent managers, support systems and mobile SDKs. Obtain an accessibility conformance report or equivalent evidence where available, noting exact product/version, criteria, exclusions and test method. Treat a vendor's report as a starting point and test the integrated journey. Configuration and styling can introduce barriers not present in the vendor demo.

Include accessibility criteria, testing, remediation, support and change notification in procurement. Set a realistic remediation path for a critical dependency. An inaccessible sole payment route can break the overall service even when the platform's own components pass.

## Public-sector customers

Assess the customer's actual procurement and public-sector obligations. The Web Accessibility Directive, national public-sector laws and contracts can require a different scope or additional information than the EAA private-service path. Do not claim that a BFSG microenterprise exemption overrides a voluntarily accepted procurement requirement or a separate public-law obligation. [A2]

Identify the requested edition and test scope. If a tender references an older standard, clarify whether it demands that edition, the current harmonized edition or additional criteria. Record agreed interpretations before delivery. Do not substitute a generic WCAG badge for an explicit procurement matrix.

## Localization

Maintain correctly declared page and passage languages, localized labels, useful error instructions and sensible reading order. Check long translations, dates, currency, number formats and text expansion. A legal button translated by a model needs both semantic accessibility and local legal review. Consent, withdrawal and cancellation routes must remain discoverable in each sold language.

For voice interfaces, evaluate available input and output languages, captions/transcripts, pronunciation and alternatives. Do not assume a screen reader understands unlabeled model-generated code or mixed-language output. Provide language context and control when content changes dynamically.

## Avoid impossible blanket promises

Separate authored UI, generated output, user uploads and third-party embedded content. Determine which duties and exceptions apply to each, and what the platform controls. Implement accessible authoring defaults and remediation support. Do not promise that an LLM automatically guarantees accessibility of all content; validate important generated documents and provide alternatives.

## Vendor change trigger

A new widget version, PSP redirect, SSO flow or document renderer should trigger targeted journey regression testing. Keep a rollback or alternate route for essential failures. Route customer notices and contract commitments through approved authority, with evidence of what actually changed.
