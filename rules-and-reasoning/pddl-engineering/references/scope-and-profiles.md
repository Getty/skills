# Scope and feature profiles

## Select a language fragment rather than a marketing label

Treat PDDL as a family with feature declarations and competition/tool subsets.
The [IPC primary-source catalogue](https://ipc08.icaps-conference.org/deterministic/PddlResources.html)
connects the original PDDL 1.2 definition, the competition subset, and later extensions.
A higher version number does not mean every planner implements every earlier feature.

| Profile or extension | Modeling purpose | Typical compatibility issue |
| --- | --- | --- |
| STRIPS | Finite Boolean facts, conjunctions, add/delete effects | Does not supply arbitrary negation, disjunction, or numbers |
| Typing | Restrict objects and parameters | Type hierarchy and `either` support vary |
| ADL features | Rich conditions, quantifiers, conditional effects | Grounding and heuristic support can differ |
| PDDL 2.1 numeric | Numeric state and arithmetic updates | General numeric support differs from action costs |
| PDDL 2.1 temporal | Durative actions and concurrency | Sequential planners cannot emulate it automatically |
| PDDL 2.2 | Derived predicates and timed initial literals | A planner can support one without temporal machinery |
| PDDL 3.0 | Preferences and trajectory constraints | Metric and constraint support is often restricted |
| PDDL 3.1 features | Object fluents and competition action-cost conventions | Support is feature-specific, not uniform |
| PDDL+ | Autonomous events/processes with mixed dynamics | Different semantics and specialized tool support |

Use `:requirements` to declare the features actually used. Check both the language
requirements and the selected engine's accepted syntax. For example, an action can
have negative delete effects in ordinary STRIPS; that alone does not require
`:negative-preconditions`. Consult the [PDDL2.1 requirements grammar](https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume20/fox03a-html/node29.html).

## Match assumptions to the problem

Classical planning ordinarily uses a known finite object set, deterministic transitions,
a fully specified abstract initial state, and a goal over states. If the real system
has observations, unknown outcomes, continuous motion, or external changes, decide
which are modeled and which require execution monitoring. Do not encode lack of
knowledge as false unless that is the intended conservative abstraction.

A scheduling problem may have known jobs with ordering/resource constraints but no
need to search for which actions exist. An HTN problem may require task decomposition.
A stochastic or partially observed problem may need policies rather than a single
fixed action sequence. Choose such formalisms deliberately instead of extending an
ordinary PDDL file with unsupported keywords.

## Record a reproducible profile

Record declared requirements, planner name/version, search and heuristic, compiler
steps, validator/version, bounds, objective, and numeric tolerance. The bundled tests
use pyperplan 2.1's STRIPS-without-costs fragment. They do not substantiate broader
PDDL support. Fast Downward's researched support is PDDL 2.2 level 1 plus restricted
action costs; see its [support page](https://www.fast-downward.org/latest/documentation/pddl-support/).
