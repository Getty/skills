# Modeling workflow

## Write the contract before the tree

Name the result and scope in one sentence. List facts and authoritative sources.
Do not let an expression silently resolve ambiguity in a business requirement.

Construct cases for acceptance, rejection, exact threshold, just below threshold,
missing data, null, wrong type, and empty collections. Decide whether malformed
input is an adapter error or a business outcome. These are different contracts.

## Preserve authoring structure

Keep related predicates together. For long ordered decisions, maintain a source
table with priority and fallback, and compile only through a tested mapping.
A visual editor must preserve grouping, operand order, and stable rule identity
through round trips. Reformatting must not flatten operands or reorder branches.

The core AST has no standard imports, named rule registry, variable declarations,
or comments. Put these in an application envelope or a declared extension. Pass
only the expression field to the evaluator, not the full envelope.

For repeated fragments, choose build-time expansion or a host extension. Expansion
produces a self-contained tree but increases size. Extensions create a runtime
dependency. Include effective behavior in review and testing; a source macro is not
a core execution feature.

## Use schemas deliberately

Require integer ages, Boolean flags, known status values, and bounded arrays when
the rule expects them. A schema can guide a form generator, but browser checks
are a usability aid. Repeat authoritative checks server-side.

Use synthetic fixtures. Store requirement wording with case rationale so future
maintainers know a threshold is deliberate. Add the motivating case when repairing
a rule; remove earlier cases only when the intended contract changes.

## Review the complete behavior change

Review requirement, expression, input/output schemas, and evaluator profile.
A dependency upgrade can change behavior with an unchanged AST. A schema expansion
can expose previously impossible inputs. Compare old/new results on identical
fixtures, then explain intentional differences.

If a source sentence is ambiguous, demonstrate the ambiguity with two concrete
inputs. Do not claim equivalence merely because generated expressions execute.
Use a more expressive decision language when JSON Logic nesting obscures the rule.

This is original engineering guidance using the format documented by the
[project](https://jsonlogic.com/) and its [operations](https://jsonlogic.com/operations.html).
