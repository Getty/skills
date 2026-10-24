---
name: game-balance-math
description: "Use when pricing or tuning game objects and systems by the numbers — cost curves for units, ships, buildings or upgrades; counter tables and payoff matrices; dominant or useless strategies; designing or auditing an economy's sources, sinks, converters and trade; inflation, hoarding, infinite-money loops; snowballing, runaway leaders, catch-up mechanics and kingmaking in strategy games."
---

# Game Balance Math

Numbers are balanced inside a system you can draw. Draw it first, then compute.
Measured inputs such as weights, win rates and earn rates come from the sim
(`simulation-balancing`), not from the designer's intuition.

## Economy as a flow graph

Nodes are **sources** (mining, production, rewards), **sinks** (consumption,
upkeep, decay, losses), **converters** (recipes, refining, trade at a price),
**pools** (stocks per actor) and **transfers** (between actors). Edges carry rates
per tick per actor.

- **Conservation per good per tick.** `stock(t+1) = stock(t) + sources − sinks ±
  transfers`, booked per cause. A sim that cannot print this balance has bugs you
  cannot see. A non-zero residual is a bug, not rounding.
- **Infinite-money loops.** A cycle in the converter and trade graph whose product of
  rates exceeds 1 creates value from nothing. To detect it, weight each edge with
  `−log(rate)` and search for a negative cycle (Bellman-Ford). It is cheap; run it on
  every config change. Fixed NPC buy/sell prices need a spread, or they form such a
  cycle by themselves.
- **Round trips are lossy.** A → B → A must end with less A.
- **Net flow** per good, for at least three actor archetypes (small, median, large).
  Positive means accumulation. Whether that is inflation depends on design intent;
  the arithmetic itself is certain.
- **Stock vs flow** in physical economies: deposits and stockpiles are stocks
  (tonnes); extraction and consumption are flows (tonnes per tick). Balance on
  flows, gate on stocks.
- **Distribution.** Gini over actors' wealth per tick. A rising Gini combined with a
  positive feedback loop means stratification ahead.

## Feedback loops — the strategy-game core problem

For each loop, ask whether having more X raises the rate of gaining X.

- **Positive loops** (more planets → more output → more planets) reward success and
  produce snowballs. Each one needs a brake that grows with size: upkeep,
  administration or distance cost, corruption, diminishing returns, unrest.
  Structural brakes feel fair; visible handouts to the trailing player feel
  patronising.
- **Let skill compound, not time spent.** Better decisions may compound. Pure
  playtime should hit diminishing returns.
- Measure the snowball rather than arguing about it: decisiveness tick and comeback
  rate (`simulation-balancing` §3).
- **Kingmaking.** A player who can no longer win but can still decide who wins
  appears whenever weak players keep leverage (alliances, votes, last-hit
  conquest). It is a design property to choose deliberately, not a tuning bug.

## Cost curves — transitive systems

Use them where stronger is supposed to cost more: units, ships, buildings, upgrades.

1. List every object and the attributes that carry value.
2. Treat a drawback as an addition to cost, not as a negative value; keep every
   number positive.
3. `value = Σ weightᵢ · attributeᵢ`. Estimate the weights from the sim (the
   marginal win contribution of +1 of an attribute), not by feel.
4. Plot cost against value and fit a curve. Flag objects more than 15 % off the
   curve; a deliberate outlier gets a documented reason.

| Ship | Cost | Attack | Hull | Speed | Value (w = 2/1/3) | Δ vs fit (value ≈ cost) |
|---|---|---|---|---|---|---|
| Corvette | 40 | 4 | 9 | 8 | 41 | +3 % |
| Frigate | 90 | 10 | 32 | 6 | 70 | −22 % ← |
| Cruiser | 160 | 30 | 86 | 4 | 158 | −1 % |

**Value is not additive in combat.** Under aimed fire (Lanchester's square law),
fighting strength ∝ quality · N². At equal cost, two ships of half quality beat one
ship of double quality: 2² · 1 = 4 against 1² · 2 = 2. Check cost curves in
simulated fights between equal-cost fleets, not by summing stats.

## Counter systems — intransitive

Build the payoff matrix from the league's measured win rates, not from guesses.

- **Strict dominance.** If row j is ≥ row i in every column and > in at least one,
  option i is never needed. Eliminate it, then repeat; iterated elimination can
  cascade.
- **Nash support.** Solve the matrix: two-player zero-sum is a linear program
  (`nashpy` or OpenSpiel; a 3×3 by hand). A healthy counter system gives every
  option non-zero weight in the equilibrium. Row sums only show performance
  against uniform play, which nobody plays.
- With more than three options, look for subsets that beat everything outside them.
- These tools assume two players. With N players, pairwise matrices miss alliances
  and kingmaking; check results against mixed fields (`simulation-balancing` §3).

## Fixing a dominant option, in order

1. **Find why it dominates.** A synergy with a core mechanic, a cost it doesn't pay,
   a missing counter, or just low execution difficulty (which may be acceptable).
2. **Add the missing cost or counter.** That addresses the cause.
3. **Strengthen alternatives**, but only when the dominance comes from their
   weakness. Raising everything is power creep.
4. **Weaken the dominant option** directly, as a last resort.

Change one value per run, in steps of 10–20 %, and re-run the same seeds.

Sources: Schreiber & Romero, *Game Balance* (2021), for cost curves and the
transitive/intransitive split; Sirlin, *Playing to Win*, for remedying dominant
strategies; Lanchester (1916); EVE Online's quarterly economic reports for
faucet/sink practice.
