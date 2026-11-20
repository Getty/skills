# Sources and versioning

PDDL does not have one universally implemented
runtime version; cite the language feature profile and tool build together. Examples
and scripts here are original educational fixtures, not an IPC conformance suite.

## Language sources

- [IPC PDDL resources](https://ipc08.icaps-conference.org/deterministic/PddlResources.html):
  curated links to the original definitions and later extensions.
- [PDDL 1.2, McDermott et al.](https://ipc08.icaps-conference.org/deterministic/data/mcdermott-et-al-tr-1998.pdf):
  original language; distinguish later competition subsets from every original feature.
- [PDDL2.1, Fox and Long](https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume20/fox03a-html/JAIRpddl.html):
  numeric state, durative actions, concurrency, formal semantics, and validation.
- [PDDL2.2, Edelkamp and Hoffmann](https://ipc08.icaps-conference.org/deterministic/data/edelkamp-hoffmann-ipcbooklet-2004.pdf):
  derived predicates and timed initial literals.
- [PDDL3 preferences, Gerevini and Long](https://strathprints.strath.ac.uk/3149/1/strathprints003149.pdf):
  hard/soft constraints and preference penalties.

## Tool sources and observed versions

- [Fast Downward support](https://www.fast-downward.org/latest/documentation/pddl-support/),
  [usage](https://www.fast-downward.org/latest/documentation/planner-usage/),
  [exit codes](https://www.fast-downward.org/latest/documentation/exit-codes/), and
  [26.6 release](https://www.fast-downward.org/latest/releases/26.6/).
  The current documentation still excludes general numeric/temporal planning,
  preferences, and object fluents. No Fast Downward binary was run here.
- [VAL repository](https://github.com/KCL-Planning/VAL) and
  [application usage](https://github.com/KCL-Planning/VAL/blob/master/applications/README.md):
  independent plan validation and diagnostic options. Pin a build when using it.
- [pyperplan project](https://github.com/aibasel/pyperplan) and
  [PyPI 2.1 package](https://pypi.org/project/pyperplan/2.1/):
  the tested runtime, supporting STRIPS without action costs.

## Refresh procedure

Recheck the selected planner's requirements, heuristic properties, compilation steps,
plan syntax, exit codes, and validator support. Record version/build hashes and
resource limits with each solve. Rerun a valid case, a meaningful invalid candidate,
a blocked instance, and an initially solved instance. Broaden tests only for features
the application actually uses.

Do not infer engine support from a language paper or infer formal semantics from
one permissive parser. If sources disagree, identify the target profile and retain
the disagreement explicitly. Never label an interrupted search “unsolvable” merely
because the plan artifact is absent.
