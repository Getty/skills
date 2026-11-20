# Rules and reasoning skills

Logic written down so that an engine can evaluate it — decision models, authorization
policies, expression languages embedded in a host, and planning domains. Each skill
covers one language on its own terms: its semantics, how to validate and test it, how
a host embeds it, and how it maps to its neighbours, independent of any one engine or
cloud service. Data that arrives in a domain's exchange format lives in
[data-sources-and-standards](../data-sources-and-standards/README.md); ontologies and
the W3C graph stack in [semantic-web](../semantic-web/README.md).

## [dmn-engineering](dmn-engineering/SKILL.md)

OMG Decision Model and Notation: decision requirements graphs, decision tables and hit
policies, boxed expressions, business knowledge models, decision services, DMN XML and
DMNDI, engine portability and TCK conformance, and decision governance. Keeps business
meaning, model structure, expression semantics and engine behaviour apart.

**Load when** modeling, validating or executing a `.dmn` model, choosing an engine, or
migrating rules from another format into DMN.

## [feel-engineering](feel-engineering/SKILL.md)

FEEL, the expression language of DMN, standalone or inside a decision model:
expressions versus unary tests, Decimal128 numbers, null and three-valued logic, lists
and contexts, functions and iteration, dates, times and durations, the S-FEEL subset
and the B-FEEL dialect, and host bindings.

**Load when** writing or evaluating a FEEL expression, or when two engines return
different results for the same one.

## [ruml-engineering](ruml-engineering/SKILL.md)

RUML, the Rulemapping Logic Format, for legal and policy decisions modeled as Law as
Code: rulemaps with ordered AND, OR and XOR operators and their optimized and
complete evaluation modes, JSONata queries and DELEGATED combiners, typed
DataPoints, modular nodes and recursion, AI checks and actions, result traces,
signed containers, and the bridges to Akoma Ntoso, LegalRuleML, DMN and RDF. Keeps a
valid file, a correct evaluation and a correct legal reading apart. The prose adapts
the specification and is CC BY-SA 4.0; scripts and examples are Apache-2.0.

**Load when** writing, validating or evaluating a `.ruml` file, building an
evaluator, or when a rulemap returns a result nobody expected.

## [cedar-engineering](cedar-engineering/SKILL.md)

Cedar authorization policies independent of any cloud service: permit and forbid with
skip-on-error, schemas and validation, entities, hierarchies and request context,
RBAC, ABAC and ReBAC patterns, templates, tenant boundaries, partial evaluation,
embedding the authorizer, and Amazon Verified Permissions. Keeps the policy decision,
the authenticity of its inputs and the enforcement of the operation apart.

**Load when** writing, validating or testing Cedar policies, integrating an
authorizer, or migrating authorization to or from Cedar.

## [opa-rego-engineering](opa-rego-engineering/SKILL.md)

Open Policy Agent and Rego: rule semantics with undefined results and conflicts, Rego
v0, v1 and v2, input and data contracts, policy tests, bundles and capabilities, the
CLI and REST API, Kubernetes Gatekeeper, Terraform plan checks, partial evaluation and
Wasm, decision logs and performance. An `allow` that evaluates true changes nothing
until an enforcement point acts on it.

**Load when** writing or testing `.rego` policies, wiring OPA into a service, cluster
or CI pipeline, or when a policy returns undefined or runs slow.

## [xacml-engineering](xacml-engineering/SKILL.md)

OASIS XACML 3.0 attribute-based access control: the PDP, PEP, PAP and PIP roles,
targets and conditions, attribute bags and issuers, combining algorithms, the four
decisions Permit, Deny, NotApplicable and Indeterminate, obligations and advice, the
JSON Profile, and PDPs such as AuthzForce.

**Load when** reading, writing or testing XACML policies and requests, integrating a
PDP, or migrating to or from another authorization system.

## [cel-engineering](cel-engineering/SKILL.md)

The Common Expression Language: declarations and type environments, the parse, check
and evaluate pipeline, macros and comprehensions, missing fields, errors and unknowns,
host functions, cost limits, and the hosts that embed it — Kubernetes CRD validation
rules and ValidatingAdmissionPolicy, Envoy, Google Cloud IAM Conditions. A CEL Boolean
enforces nothing by itself.

**Load when** writing or embedding CEL expressions, debugging a CRD or admission rule,
or porting an expression between hosts.

## [json-logic-engineering](json-logic-engineering/SKILL.md)

JSON Logic rules as serialized expression trees: json-logic-js and its ports, `var`
and missing values, truthiness and coercion, collection scope, custom operations and
their security, rules shared between browser and server, storage and lifecycle, and
execution profiles that keep evaluators in agreement. No standards body defines JSON
Logic; the evaluator is the profile.

**Load when** writing, embedding or testing JSON Logic rules, or when two evaluators
disagree on the same rule.

## [pddl-engineering](pddl-engineering/SKILL.md)

PDDL planning domains and problems: STRIPS and ADL, typed actions and goals, numeric
fluents and action costs, durative and concurrent actions, derived predicates, timed
initial literals, preferences and trajectory constraints, planner selection, plan
validation, and execution monitoring and replanning for agents. A validated plan
shows the goal reachable in the model, not safe in the world.

**Load when** modeling or generating a planning task, choosing a planner, validating a
plan, or connecting plans to the tools that carry them out.
