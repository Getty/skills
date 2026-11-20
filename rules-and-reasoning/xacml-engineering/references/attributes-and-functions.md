# Attributes and functions

## Specify the attribute contract

For each fact, record category, AttributeId, datatype URI, allowed issuer(s),
cardinality, provenance, and freshness. Category distinguishes subject, resource,
action, environment, or an application-specific category. An identical AttributeId
in a different category is not automatically the same attribute.

An AttributeDesignator returns a bag. If no matching value exists and MustBePresent
is false, the result is empty; if true, evaluation encounters missing-attribute error.
Neither option invents a default. If a later `string-one-and-only` consumes an empty
or multi-element bag, it can fail even when MustBePresent was false.

Use bag membership when a subject legitimately has multiple roles. Use one-and-only
only when the input contract requires exactly one value and deviations should be
errors. Do not turn a multi-valued department into an arbitrary first department.

## Respect issuer matching

With an Issuer in the designator, request values must match it under the core rules.
Without an Issuer, values are not limited to one named issuer solely by that omission.
Some products offer stricter/faster modes; record deviations from core behavior.
Do not assume a provider's “strict” switch means the same thing across products.

Issuer is not proof of identity or source authenticity. Prevent untrusted callers
from asserting privileged attributes before the PDP sees them. Separate user-supplied
claims from validated attributes using trusted adapters and explicit categories or
issuer conventions where appropriate.

## Use typed functions

XACML function identifiers and datatype identifiers are URIs. Similar human-readable
names do not make them interchangeable. A scalar equality function expects scalar
arguments; bag functions and higher-order functions have different signatures.
Use the specified function family for strings, integers, dates, durations, or names.

Time comparisons require a deliberate timezone and source contract. The standard's
environment time attributes and the selected PDP's provider behavior can interact;
verify whether supplied current-time values are overridden, accepted, or populated.
Do not let a caller choose the trusted current time.

AttributeSelector and XPath features require additional context and engine support.
Select the XPath version and namespace bindings explicitly. An XML Content subtree
and a designator-based attribute are different retrieval surfaces. Disable selectors
when unneeded rather than assuming every PDP supports the same XPath facilities.

Authority: [core attribute and function semantics](https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-en.html)
and [AuthzForce attribute/provider configuration](https://github.com/authzforce/core).
