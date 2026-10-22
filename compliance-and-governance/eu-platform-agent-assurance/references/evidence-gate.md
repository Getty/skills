# Evidence consistency gate

## Inputs

Python 3.10+ standard library only. Run `scripts/check_evidence.py` with explicit `--scope`, `--report`, `--evidence-root`, `--release`, `--environment` and preferably `--as-of`. The evidence root holds local copies of actual minimised evidence. The input templates describe the field shape; they intentionally do not pass.

The scope contains schema version 1, profile ID/revision, release, environment, reviewed-control selection and review metadata. Its review must be marked `reviewed` with a reviewer and a valid review window. The report binds to its SHA-256, profile, release and environment.

Control IDs must match the reviewed required-control set exactly; empty and duplicate sets fail. The checker cannot discover omitted laws or verify that the selected controls are sufficient. Independent scope review is essential.

## Control fields

Every control supplies ID, owner, reviewer, reviewed date, normative type, applicability and reason, implementation status, source reference/provision/version, verification date and source review due date. Normative types are `binding_law`, `contract`, `internal_policy`, `guidance`, `standard`.

Applicable controls must be `verified`. Unknown/conditional applicability fails. Excluded controls must be explicitly `not_applicable`, include an exclusion evidence reference and supply evidence for that decision. The checker refuses a package in which all controls are excluded, because it contains no positive verification; choose a real scope-review/identity control rather than making up an applicable law.

Every evidence item needs a relative path, SHA-256, method, `pass` outcome, observation/expiry date, release and environment. Content bytes must match. Resolved paths must remain under the evidence root, so an external symlink or `../` escape is rejected. Evidence defaults to a 16 MiB per-file limit; change `--max-file-bytes` only with a reason. Use summaries/reports and references to protected raw data instead of oversized sensitive dumps.

Future/stale/inverted source and evidence dates, evidence newer than its control review, and source verification newer than its control review fail. 'Review due' and 'expiry' are internal assurance validity windows unless grounded in a specific legal source; this checker does not calculate statutory deadlines.

## Results

- Exit 0: `evidence_consistency_passed` for this declared package only.
- Exit 2: `evidence_consistency_failed`, with specific findings.
- Exit 1: malformed input, duplicate JSON keys, unreadable files or invalid command data.

An invalid or failed result must not be converted into a pass because a CI parser ignores the exit status. Preserve the JSON output and the underlying tests' actual results.

## Explicit limitations

The checker does not authenticate reviewer identities, validate legal citations, examine evidence meaning, contact regulators, fetch sources, run product tests or provide an electronic signature. A fabricated report with internally consistent data can pass. Prevent that through protected review, trustworthy test execution and provenance, not by claiming SHA-256 proves truth.

The report cannot authorise a release. It cannot waive legal obligations. A material change to scope/checker/CI configuration needs review under the project's existing policy. Never make the checker self-modify or remove controls to obtain exit 0.
