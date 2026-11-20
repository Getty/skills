# Execution and replanning

## Bind abstract actions to controlled operations

For every PDDL action, define an adapter contract: external operation, argument map,
current precondition check, authorization check, timeout, success evidence, failure
classification, idempotency key, and possible compensation. The planner chooses
symbolic actions; it does not invoke tools or provide credentials.

Keep an explicit distinction between predicted effects and observed effects. A
successful request submission does not necessarily mean the action completed. For
an asynchronous job, record the pending state and observe completion before asserting
the final effect. Do not update the planning state merely because an action appears
in the plan.

For agent tooling, map names to a fixed operation registry rather than letting action
strings become shell commands. Resolve objects through validated IDs and enforce the
user's requested scope at execution time. Authorization systems such as Cedar or OPA
can check protected operations; a model predicate named `authorized` is not itself
an authorization check.

## Reconcile changing state

Before each action, compare relevant facts with the latest trusted observations.
If a precondition no longer holds, stop that action and choose a documented recovery:
refresh the problem and replan, retry an idempotent transient failure, request needed
information, or abort the workflow. Do not silently amend the domain to declare a
failed operation successful.

Maintain a plan revision and state snapshot ID. If two agents act on shared resources,
use transactional checks, leases, or locks in the execution system. PDDL resource
predicates alone cannot prevent another process from consuming the real resource.
When leases expire or ownership changes, refresh facts and invalidate affected steps.

## Model uncertainty honestly

Classical PDDL assumes the supplied abstract transition behaves as modeled. If an
action can fail unpredictably, a single deterministic plan may be used only within
an execution-and-replanning architecture whose limits are stated. For contingent,
probabilistic, or partially observed decisions, consider a formalism that explicitly
models those outcomes and observations.

Do not convert “not observed” into “known absent” without a chosen abstraction policy.
A sensor inspection action needs an observation mechanism; simply adding its desired
result as an unconditional effect fabricates knowledge. Likewise, rollback is another
action with its own preconditions and effects, not a universally available inverse.

## Make traces useful for diagnosis

Record planned action, bound external IDs, policy decision, observed start/end,
returned result, state delta, and replan cause. Keep credentials and sensitive payloads
out of general planner logs. Compare planned versus observed effects to discover
missing preconditions or unrealistic durations.

These are integration design rules, not features supplied by the PDDL file format.
They follow from the distinction between a formal state-transition model and the
system realizing it. The [PDDL2.1 semantics](https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume20/fox03a-html/JAIRpddl.html)
provides the model interpretation; the application must implement the observation
and enforcement contract.
