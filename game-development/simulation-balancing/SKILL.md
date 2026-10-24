---
name: simulation-balancing
description: "Use when balancing a game through bot, AI-vs-AI or self-play runs instead of (or before) human playtests — batch runners, seed sets, bot policy leagues, parameter sweeps, win-rate comparisons; when asking whether a mechanic matters or can be cut; when a rule change shows no effect in the sim; or when someone says 'the bots win every time so it's balanced', 'one strategy always wins' or 'nobody ever uses X'."
---

# Simulation Balancing

The simulation is a measuring instrument. A balance result is the number plus what
the instrument cannot see. Building the seat interface for bots is
`ai-playable-games`; the numeric methods (cost curves, payoff matrices, flows) are in
`game-balance-math`.

## 1. The instrument

- **Determinism test in CI.** Run the same seed and config twice and diff the full event log.
  Typical leaks: Perl hash key order and Python set order over strings (both vary per
  process), wall clock, a global RNG, threads, floats across platforms.
- **Run record.** Every run stores seed, config hash, rules commit and policy
  versions. Discard any result that lacks them, because nobody can reproduce it.
- **Mechanic toggles in config.** Anything you may want to switch off (§4) can be
  disabled without editing source. Edited source gets committed by accident, and a
  forgotten mutation silently changes the baseline.

## 2. The policy league

| Policy | What it reveals |
|---|---|
| Random-legal | The floor; whatever it achieves is not a challenge |
| Greedy (one-step best) | Dominant lines, fastest |
| Specialists, one per strategy (rush, economy, turtle, trade, …) | Whether counters actually counter |
| Conservative / risk-averse | Whether risk is ever rewarded |
| Exploit-seeker (search-tuned weights, or an LLM tasked to break the rules) | Degenerate loops nobody wrote a bot for |
| LLM seat | Exploratory, few games; human-like plans at high cost |

- **Depth signal.** If random-legal and greedy end up close together, the decisions in
  between barely matter.
- **League matrix.** Play every policy against every other with swapped seats on the
  same seeds. This win-rate matrix feeds the dominance analysis in
  `game-balance-math`.
- **Average over the league's Nash mixture, not over the policy list.** Three
  near-identical rush bots otherwise count rushing three times (Balduzzi et al. 2018,
  "Re-evaluating evaluation", Nash averaging).
- **Re-tune bots after rule changes.** A fixed-priority bot ignores new incentives;
  then you measured the bot, not the rule. Run the fixed and the re-tuned bots as
  separate arms, so the experiment still changes one thing per arm.
- **Tune on seed set A, confirm on a held-out set B.** Tuning that only holds on A
  fits the seeds, not the game.

## 3. The experiment

- **Write the hypothesis and the one primary metric down before the run.** Scanning 40
  metrics at 95 % confidence produces about two false alarms per run; treat
  everything beyond the primary metric as exploratory.
- **One change per experiment.** Run before and after on identical seeds and
  policies (common random numbers) and compare per seed. The paired difference has far
  less variance than two independent samples.
- **Sample size**, for a win rate near 50 %, 95 % CI half-width ≈ 1.96·√(p(1−p)/n):
  n = 100 → ±10 points, 400 → ±5, 1,000 → ±3.1, 2,500 → ±2. Unpaired, detecting a
  2-point edge (80 % power) takes about 10,000 games per arm.
- **Paired sample size:** n ≈ 7.85 · σ_d² / δ² seeds (95 % confidence, 80 % power),
  where σ_d is the standard deviation of the per-seed difference from a pilot run and
  δ the effect you need to see. With small σ_d, a few hundred seeds often suffice.
- **Report distributions** (median, p10, p90) per policy and per start position, not
  just means.

**N players and persistent worlds.** Win rates, league matrices and Nash averaging
assume two-player matches. With N empires, or an MMO that never ends, define the
outcome first: score or share at a fixed tick T, rank distribution, survival rate.
Evaluate each policy by its rank against mixed fields of the other policies, with field
composition drawn per seed.

Strategy-game metrics worth logging:

- Win rate per policy, start position and faction; first-mover or seat advantage.
- **Decisiveness tick**: from this tick on, the eventual winner leads continuously.
  Early decisiveness means a snowball.
- **Lead changes** per game and **comeback rate** (winner was behind at ⅓ of the game).
- Game length, stalemate rate, and strategy diversity (entropy of winning policies).
- Mechanic usage per policy, and the **binding-constraint share**: the fraction of
  ticks in which each resource was the limiting one.

## 4. Does this mechanic matter?

Run the stages in order and stop at the first stop condition. "No change" has four
causes, and only one of them is "the mechanic is inert".

1. **Exercise.** Count usage per policy. Zero everywhere → **UNEXERCISED**: a gap in
   the policy set. Write a policy that uses the mechanic and start again.
2. **Sensitivity.** Apply an absurd mutation (×10, ×0, free, sign flipped) on the
   standard seeds. Check the intermediate metrics first (tonnes mined, stock levels,
   binding constraint), then the outcomes. Nothing moves → **INVISIBLE**: the bots
   don't react, the metric is too coarse, or another bottleneck binds. Report the
   instrument gap and what would close it. If another bottleneck binds, that is also a
   balance finding: in the current tuning the mechanic cannot matter. The fix may lie
   at the bottleneck rather than at the mechanic.
3. **Ablate.** Disable the mechanic via its toggle. Disable it, don't tune it to zero:
   code that reads the mechanic must see it as absent. Use the same seeds and
   policies. Report deltas per metric and per seed: one seed in 24 changing
   drastically is a different finding from all seeds shifting slightly. Re-run the
   baseline afterwards and confirm it reproduces.
4. **Verdict**, exactly one:
   - **LIVE**: report the magnitude.
   - **DEAD**: the only verdict that is a claim about the mechanic itself. Cut it,
     or give it teeth; that is a design decision for whoever owns the design.
   - **UNEXERCISED** / **INVISIBLE**: findings about the apparatus, not about the
     mechanic.

Ablate displayed values too: a number shown to the player that no decision reads
misinforms the player. The same goes for a currency without a sink, and for a
variable that feeds several systems.

## 5. Report

```
Result:     <primary metric> <value> [95% CI], n=<games>, seeds <set>, policies <list>
Change:     <one parameter: old → new>, config <hash>, rules <commit>
Blind spot: <what these policies cannot express, e.g. "no policy retreats or trades">
Not seen:   legibility, fun, learning curve, social dynamics — needs humans
```

Bots read state directly and never tire, learn or feel betrayed. Readability, pacing,
surprise, trust in diplomacy and kingmaking among humans are design properties the
league cannot measure. Say so with every result.

The ablation stages follow the mechanic-ablation idea in the game-dev plugin of
rbergman/dark-matter-marketplace.
