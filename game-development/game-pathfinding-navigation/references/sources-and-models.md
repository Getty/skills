# Primary sources, models and implementations

Use primary papers and official documentation to understand a model's conditions. Verify current engine/package APIs before integration.

The skill's domain contracts, selection tables, synthetic fixtures and engineering examples are original guidance. Source links do not imply that their authors validated the bundled code.

## Contents

- [Graph search and heuristics](#graph-search-and-heuristics)
- [Acceleration and changing graphs](#acceleration-and-changing-graphs)
- [Geometry and navigation meshes](#geometry-and-navigation-meshes)
- [Movement and multi-agent coordination](#movement-and-multi-agent-coordination)
- [Benchmarks and engine adapters](#benchmarks-and-engine-adapters)
- [Use evidence and dependencies deliberately](#use-evidence-and-dependencies-deliberately)

## Graph search and heuristics

| Primary source | Useful subject | Limit to retain |
|---|---|---|
| [Red Blob: A* introduction](https://www.redblobgames.com/pathfinding/a-star/introduction.html) | Graph/search concepts | A route does not itself move a physical body |
| [Red Blob: implementation](https://www.redblobgames.com/pathfinding/a-star/implementation.html) | Readable graph and search implementations | Examples require adaptation to the game's complete contract |
| [Amit Patel: heuristics](https://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html) | Lower bounds, scale and quality tradeoffs | Preserve admissibility/consistency when claiming exactness |
| [Red Blob: flow fields](https://www.redblobgames.com/pathfinding/tower-defense/) | Shared work for many starts and one target | Directed costs, zero-cost plateaus and caches need explicit rules |
| [Likhachev et al.: ARA*](https://papers.neurips.cc/paper_files/paper/2003/file/ee8fe9093fbbb687bef15a38facc44d2-Paper.pdf) | Controlled anytime search | Bounds rely on complete algorithm assumptions |

## Acceleration and changing graphs

- [Goldberg and Harrelson: ALT](https://www.microsoft.com/en-us/research/publication/computing-the-shortest-path-a-search-meets-graph-theory/): landmark and triangle-inequality bounds. Directed graphs need distances both to and from landmarks.
- [Botea, Müller and Schaeffer: HPA*](https://webdocs.cs.ualberta.ca/~mmueller/ps/2004/hpastar.pdf): clustered pathfinding. Reported empirical quality is not a universal approximation factor.
- [Harabor and Grastien: JPS](https://users.cecs.anu.edu.au/~dharabor/data/papers/harabor-grastien-aaai11.pdf): pruning for the stated uniform-grid movement model. Arbitrary polygon/weighted graphs require different reasoning.
- [Daniel et al.: Theta*](https://idm-lab.org/bib/abstracts/Koen10r.html): any-angle grid paths, with explicit limits on global shortest-path guarantees.
- [Koenig, Likhachev and Furcy: LPA*](https://www.cs.cmu.edu/~maxim/files/aij04.pdf): retained search state for related changed-graph problems.
- [Koenig and Likhachev: D* Lite and errata](https://idm-lab.org/bib/abstracts/Koen02e.html): moving-start replanning; consult author corrections alongside the paper.
- [Orda and Rom: time-dependent routes](https://sites.cs.ucsb.edu/~suri/cs231/Rlist/ordaRom.pdf): arrival functions and waiting restrictions. This is distinct from repeatedly solving static snapshots.

## Geometry and navigation meshes

| Primary source | Use | Boundary |
|---|---|---|
| [LaValle: configuration-space obstacles](https://www.lavalle.pl/planning/node156.html) | Finite footprints and forbidden configurations | Rotation and kinematics can add dimensions |
| [Recast Navigation repository](https://github.com/recastnavigation/recastnavigation) | Optional mesh construction/runtime toolkit | Select modules and inspect their versions/licenses |
| [Recast rcConfig](https://recastnav.com/structrcConfig.html) | Build resolution, radius, headroom, climb and slope | Some parameters are voxel counts, others world quantities |
| [Detour navigation queries](https://recastnav.com/classdtNavMeshQuery.html) | Polygon paths, straight paths, sliced queries | Preserve partial/buffer-limited status and profile filters |
| [Detour query header](https://github.com/recastnavigation/recastnavigation/blob/main/Detour/Include/DetourNavMeshQuery.h) | Current source-level contracts | Pin a release/commit when implementing |
| [Detour path corridor](https://recastnav.com/classdtPathCorridor.html) | Maintaining a corridor during motion | A runtime representation, not global optimality proof |
| [Mononen: funnel implementation](https://digestingduck.blogspot.com/2010/03/simple-stupid-funnel-algorithm.html) | Portal-based corridor refinement | Valid portal geometry and clearance remain prerequisites |

## Movement and multi-agent coordination

- [ORCA authors' project](https://gamma-web.iacs.umd.edu/ORCA/): reciprocal local velocity constraints and research papers. Retain modeled-body, reciprocity, sensing and execution assumptions; local avoidance does not guarantee global progress.
- [RVO2 documentation](https://gamma-web.iacs.umd.edu/RVO2/documentation/2.0/index.html) and [parameters](https://gamma-web.iacs.umd.edu/RVO2/documentation/2.0/params.html): reference implementation and horizon/neighborhood settings. A finite neighbor cap can omit relevant interactions.
- [Stern et al.: MAPF definitions](https://ojs.aaai.org/index.php/SOCS/article/view/18510): state conflict types, objectives and goal occupancy rather than using “multi-agent pathfinding” as an underspecified guarantee.
- [Sharon et al.: CBS author summary](https://www.movingai.com/papers/sharon2015cbsjournal.html) and [journal article](https://doi.org/10.1016/j.artint.2014.11.006): constraint-tree search with individual low-level planners. Match low-level optimality, conflict semantics and the high-level objective.

## Benchmarks and engine adapters

[Moving AI benchmark collection](https://www.movingai.com/benchmarks/), [file formats](https://www.movingai.com/benchmarks/formats.html) and [MAPF scenarios](https://www.movingai.com/benchmarks/mapf.html) support comparable experiments. Match movement, diagonal, cost, conflict and goal conventions before comparing a reported optimum. Keep dataset attribution and redistribution terms.

For integration, consult:

- [Unity AI Navigation surfaces](https://docs.unity3d.com/Packages/com.unity.ai.navigation@2.0/manual/NavMeshSurface.html) and [obstacles](https://docs.unity3d.com/Packages/com.unity.ai.navigation@2.0/manual/AboutObstacles.html).
- [Epic navigation modification](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-how-to-modify-the-navigation-mesh-in-unreal-engine) and [avoidance](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-avoidance-with-the-navigation-system-in-unreal-engine).
- [Godot NavigationAgent guide](https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationagents.html).

Use the [engine adapter reference](engine-adapters.md) for the reviewed API distinctions. Floating “stable/latest/main” links can change; record the actual version used by a game.

## Use evidence and dependencies deliberately

The bundled fixtures are synthetic analytical cases, not measured player behavior or a benchmark leaderboard. Unit tests verify a bounded reference implementation; they do not establish production navigation performance or correctness over arbitrary geometry.

Distinguish four claims: a mathematical guarantee under conditions, a tested implementation property, an empirical benchmark result, and a designer approximation. State which one supports each recommendation.

No listed engine or library is a mandatory dependency. The executable examples use Python's standard library. Adopt a larger package when its representation, supported agents, update model and licensing fit the project.

Check source/code disagreement instead of silently copying equations or pseudocode. Preserve a small exact oracle and representative regressions when modifying an optimization. Historical speedups are evidence about the authors' experiments, not promised speedups for a new game.
