# skill-mining — Design

**Status:** approved 2026-08-19 · **Archetype:** workflow · **Home:** `authoring/skill-mining/`

## Problem

Getty's skill library is written top-down: someone decides what the house rule
is and writes it into a SKILL.md. That misses everything the house already
decided in code but never articulated — eleven years of Perl carry hundreds of
settled choices that no one has ever put into words. Meanwhile an agent editing
that same code re-derives its own defaults and writes Perl that looks nothing
like the surrounding file.

The knowledge exists. It is just trapped in the code, and nobody has read it
back out.

## Goal

A repeatable procedure that reads a curated body of hand-written code, extracts
the decisions embedded in it, presents them for a human verdict, and folds the
approved ones into the existing skills.

**End state of one run:** a verdict file where every candidate carries its rule,
its evidence, and Getty's judgement — and every approved candidate has landed in
a skill.

## Non-goals

- **Not code documentation.** The output is "always do it this way", not "this
  is what this module does".
- **Not a linter.** Nothing is enforced mechanically; the skills are the product.
- **Not automatic.** No candidate reaches a skill without an explicit verdict.

## The corpus problem

Mining a codebase an agent wrote produces a self-confirming loop: the agent's
own guesses come back as house rules and get canonised. So evidence is
restricted to hand-written code, declared per run.

**Filter:** a line counts as evidence when its commit carries no
`Co-Authored-By: Claude|noreply@anthropic` trailer. Authorship is *not*
filtered — Getty's position is that code is code, and a contributor's Perl is
as valid a specimen as his own.

**Declared, never assumed.** The corpus is a list Getty ticks off at the start
of a run, recorded in the verdict file's header with each repo's HEAD SHA. The
frequency numbers next to a candidate refer to that list and nothing else —
counting "whatever is on the machine" would count AI repos and call it canon.

## Extraction

Three mechanisms, in fixed roles:

1. **Contrast (motor).** Hold the code against how an average Perl developer
   would write the same thing; every deviation is a candidate. This mirrors
   `skill-authoring`'s "no observed failure, no skill" at the candidate level:
   what an agent would have written anyway does not belong in a skill.
2. **Axis catalogue (net).** After the contrast pass, walk a fixed list of
   decision axes — object system, types, error handling, async, tests, dist
   config, docs, naming, file layout — and check each for silence. A quiet axis
   is either genuinely absent or a blind spot; both are worth a look.
3. **Frequency and span (evidence).** Count occurrences across the declared
   corpus and record the years they span. Decides nothing; informs the verdict.

Span matters as much as count. Over an eleven-year corpus, "all evidence from
2014" and "consistent through 2025" are different findings, and only Getty can
tell obsolete from settled.

## Verdict file

One file per domain (`mining/perl.md`), growing across runs — never rewritten.

```markdown
### <one-line rule title>
Rule:        <imperative, one sentence — the form it would take in a skill>
Evidence:    <repo/path:line> · <repo/path:line>
Spread:      <n> occurrences, <m> counter-examples, <year>–<year>
Axis:        <decision axis>
Target:      <skill it would land in>
verdict:
```

Getty fills `verdict:` with `ja`, `nein`, or free text. Free text is the most
valuable outcome — "yes but only in modules" is knowledge that exists nowhere
in the code.

**Rejected candidates stay in the file** with their verdict. Without that
record every later run re-proposes the same rejects.

## Landing the yield

Approved rules are folded into the skill named in `Target:` — in place, with a
truncating write, preserving the inode (CLAUDE.md). A new skill is created only
for rules that fit no existing one. The verdict file stays as the audit trail:
every rule in a skill can be traced back to the lines that justified it.

## First run

Corpus: `sunriser` (3,921 Perl lines, 2014–2024) and `amigaevent` (10,522 Perl
lines, 2022–2025). Both carry zero AI commits. Target skills: `getty-perl-core`,
`getty-perl-moose`, `getty-perl-moo`, `perl-io-async-future`,
`perl-release-dist-ini`, `getty-perl-distribution`.
