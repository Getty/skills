# Profiles and capability selection

## Build a capability matrix

Do not describe an implementation as supporting “XACML” without stating the needed
features. Record core/errata version, algorithms, datatypes/functions, request formats,
selectors/XPath version, policy-reference resolution, attribute-provider behavior,
and optional profiles. A parser can understand XML without implementing its semantics.

| Requirement | Profile or feature to inspect |
| --- | --- |
| JSON requests/results | JSON Profile 1.1 and exact engine implementation |
| Multiple resources/actions | Multiple Decision Profile and supported mechanisms |
| Role hierarchy | Core/Hierarchical RBAC Profile and entity/role representation |
| Hierarchical resources | Hierarchical Resource Profile and scope semantics |
| Delegated policy administration | Administration and Delegation Profile |
| Additional composition pattern | Additional Combining Algorithms Profile |
| Network/DLP attributes | DLP/NAC Profile and implemented datatype subset |

These are candidates to verify, not a claim that all are mandatory or supported
by a particular PDP. Check the publication status and selected revision of each
document; a Committee Specification or draft must not be called an OASIS Standard
without evidence.

## Avoid accidental feature escalation

Start with core single-request evaluation when it meets the requirement. Add a
profile because a concrete requirement needs it. Each extra feature introduces
capability and interoperability tests. A product may implement only one mechanism
from a broad profile, such as repeated attribute categories rather than every
multiple-decision request form.

Test an actual representative request and policy for each selected capability.
A marketing statement or a namespace in an XSD is not enough. Preserve the precise
configuration switches and modules needed to enable features.

## Track product distinctions

AuthzForce Core is an embedded PDP/CLI; AuthzForce Server adds administration and
service boundaries. Their release numbers and supported APIs differ. Other PDP
products have their own formats, algorithms, extensions, and compatibility options.
Choose based on the required feature matrix and measured deployment behavior,
not solely on language age or an unsupported claim of market adoption.

The tested fixtures intentionally use a small core subset. A passing fixture does
not test delegation, RBAC hierarchy, multiple decisions, XPath, or provider plugins.

Primary profile sources:
[RBAC](https://docs.oasis-open.org/xacml/3.0/rbac/v1.0/xacml-3.0-rbac-v1.0.html),
[multiple decisions](https://docs.oasis-open.org/xacml/3.0/multiple/v1.0/cs02/xacml-3.0-multiple-v1.0-cs02.html),
[additional combining](https://docs.oasis-open.org/xacml/xacml-3.0-combalgs/v1.0/xacml-3.0-combalgs-v1.0.html),
and [OASIS technical committee](https://www.oasis-open.org/committees/xacml/).
