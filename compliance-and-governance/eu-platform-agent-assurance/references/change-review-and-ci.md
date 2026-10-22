# Change review and CI integration

## Place review at behaviour changes

Review architecture before committing to data flows; review a feature before exposure; review provider/model/terms changes before switching production routes; and review incidents after containment. Use the smallest affected set of controls. An unaffected domain can retain valid evidence when its assumptions, code and dependencies remain unchanged and that determination is recorded.

Suggested integration is a product/profile inventory, an applicability decision, implementation tickets, tests and a release report. A workflow file or hook is only one implementation option. Do not install one without a request covering repository changes.

## Trust boundary

The feature-building agent may propose changes to tests and compliance files. Material changes to required-control selection, the checker, release authority and evidence review need the existing independent review path. Otherwise the agent can remove the failing obligation and claim success.

In CI, choose the scope and checker from a trusted reviewed revision or protect their changes with appropriate review. Use the exact proposed source revision as the release identifier, and the actual test environment. Do not run untrusted pull-request code with production credentials or privileged tokens. A test that mutates production is not a harmless validation step.

The checker is a consistency tool, not a policy engine. The reviewed scope must explicitly list every control selected for this change. A small green package cannot establish that omitted areas were evaluated. Record the feature, countries and assumptions in the scope record.

## Useful evidence package

Collect meaningful test reports, manual observations, relevant configurations, contract/version references and source-review results. Redact sensitive fields and retain protected evidence in the appropriate system. When the checker uses a local evidence copy, identify its provenance and authoritative location. Do not copy secrets or full production records simply to satisfy hashing.

Bind evidence to release, environment and observation dates. Reusing a report from another branch requires a justified equivalence decision and fresh metadata; never falsify a test's original observation. Distinguish 'implemented in source', 'tested in staging' and 'observed in production'.

## Rollout

Use feature flags, canary exposure and rollback where appropriate. Verify that disabled features cannot be reached via API, old client or fallback. Do not let a launch flag bypass consent, access control or lawful scope. Record which release is actually live and which customer cohorts saw which legal notices/terms.

The product/release owner makes the release decision within existing authority. The agent supplies the exact change, evidence, unresolved questions and material limitations. Routine low-impact fixes do not require a new legal committee when their scope and authority are already clear.
