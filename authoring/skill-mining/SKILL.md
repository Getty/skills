---
name: skill-mining
description: "Use when a skill's content should come from existing code — mining house conventions out of a codebase, or checking whether a skill states real practice or an invented convention."
---

# Skill Mining

Turns settled decisions that live only in code into skill content. The output of
one run is a verdict file in which every candidate carries its rule, its
evidence, and a human judgement — and every approved candidate has landed in a
skill.

A codebase records what was done. It never records "always do it this way" —
that lives in the author's head. Mining reads the first and proposes the second;
only the author can confirm it.

## Step 0 — preconditions

Mining code an agent wrote produces a self-confirming loop: the agent's own
guesses come back as house rules and get canonised. Before anything else,
establish that hand-written code exists and can be identified.

**Date is the primary filter, not the trailer.** `Co-Authored-By: Claude` proves
a commit was AI-assisted; its absence proves nothing, because the trailer was not
always set. Find the earliest AI commit anywhere in the author's estate and treat
that date as the boundary — everything after it is suspect until shown otherwise.

```bash
# the boundary: earliest AI-attributed commit across all repos
for d in */; do git -C "$d" log --format='%ad %H %(trailers:key=Co-Authored-By)' --date=short 2>/dev/null \
  | grep -i 'claude\|anthropic' | tail -1; done | sort | head -1
```

Then read the repo's own history for what the trailer misses:

| Signal | What it looks like |
|---|---|
| Repo born after the boundary | first commit postdates the estate's first AI commit |
| The author says so | commit messages mentioning AI, the model, or fixing its output |
| Agent infrastructure committed | `CLAUDE.md`, `AGENTS.md`, `.claude/`, skill files in the tree |
| Implausible cadence | a whole distribution from "initial commit" to complete in one day |

Any one of these outweighs a missing trailer. A repo that trips several is
AI-written no matter how clean its trailers look.

**Ask the author.** They know which projects they typed by hand, and the answer
costs one question — cheaper than a run built on the wrong corpus. Do this even
when the signals look unambiguous.

## Step 1 — declare the corpus

Present the candidate repos as a table — commits, AI-commit count, line count,
year span — and have the human tick off which ones count. **Never assume the
corpus.** Frequency claims are only as good as the list they are counted over,
and "everything on the machine" counts AI repos as canon.

Then subtract, inside each chosen repo:

- **AI-written lines** — commits carrying `Co-Authored-By: Claude`, plus
  everything after the boundary date that the author has not vouched for.
- **Vendored third-party code** — patched CPAN modules under `docker/`, `local/`,
  `vendor/`, or a `lib/` namespace that is not the distribution's own. This is
  the easiest way to ruin a run: a vendored module is a *different author's*
  style, mined as if it were the house's.

Record the surviving file list and each repo's HEAD SHA in the verdict file's
header, so a later run can tell what the numbers were counted over.

**Done when:** every path in the corpus is one a human ticked off, and the
excluded paths are named in the header.

If subtracting leaves too little to mine, **say so and stop**. A topic the
hand-written record cannot describe is a case for `skill-authoring` — writing the
rule as a decision — not for mining a corpus that does not exist. Reporting an
empty corpus is a successful run; presenting AI-written code as house practice is
the one failure this skill exists to prevent.

## Step 2 — read for candidates

Read whole files, not greps — a convention is visible in the shape of a file and
invisible in a line of context. Three or four substantial files per repo is
usually enough; the same patterns start repeating.

Hold each file against how an average developer in that language would write the
same thing, and note every deviation. **The deviation is the candidate.** What an
agent would have produced anyway does not belong in a skill (`skill-authoring`:
delete every sentence the agent would do anyway) — and this is where that test
gets applied, before the candidate exists rather than after.

Absences are candidates too — no type constraints anywhere, no test directory, no
exception class — because an agent silently reverses them by adding what it
thinks is missing. But an absence is **the weakest evidence there is**: it shows
what that code did not need at that time, which is not what the house wants now.
Two things follow. Look outside the corpus before proposing one — the thing may
be established in the author's other work and simply absent here. And put it as a
question, never as a prohibition: "nothing is typed here — policy or
circumstance?" Both answers occur, and only the author can tell them apart.

**Done when:** reading a further file produces no candidate that is not already
on the list.

## Step 3 — count both sides

Every candidate gets counted across the whole corpus, **together with its
counter-form**. A bare number proves nothing; `402 spaced vs 8 unspaced` is a
finding, and `9 concatenations` alone is not.

```bash
grep -rEc 'my \( \$' $(git ls-files 'lib/*.pm')  | awk -F: '{n+=$2} END{print n}'
grep -rEc 'my \(\$'  $(git ls-files 'lib/*.pm')  | awk -F: '{n+=$2} END{print n}'
```

Record the span of years alongside the count. Over a long corpus "all evidence
from 2014" and "consistent through 2025" are different findings, and only the
author can tell obsolete from settled.

Where two repos disagree — one uses Moo, the other Moose; one imports `croak`,
the other qualifies it — **present the disagreement as the candidate**. A
contradiction is the most valuable thing a run can surface: it is exactly the
question the code cannot answer.

**Done when:** every candidate carries a count, a counter-count, and a year span.

## Step 4 — check the axes for silence

Walk [references/axes.md](references/axes.md) and note every axis no candidate
touched. A silent axis is either genuinely absent from the corpus or a blind
spot in step 2; look before deciding which. Silence that turns out to be real
becomes a candidate in its own right (C10 "no type constraints" came from this).

**Done when:** every axis is either represented by a candidate or explicitly
noted as absent.

## Step 4b — subtract what is already canon

Read the target skills before presenting anything, and drop every candidate they
already state. A human asked to judge a rule that has been house policy for years
learns nothing and spends attention for nothing — in the first run, ten of
forty-eight candidates were already written down.

What survives this pass is worth more than the count suggests: where a candidate
*contradicts* an existing skill, or sharpens a rule the skill states too broadly,
that is a finding in its own right. Present it as a correction, not as a new rule.

**Done when:** every remaining candidate is absent from its target skill, or
marked as a correction to what that skill currently says.

## Step 5 — present for judgement

One verdict file per domain (`mining/<language>.md`), appended to across runs,
never rewritten. Per candidate:

```markdown
### C07 — is => 'lazy' plus a separate _build_*, never an inline default
Rule:     <imperative, one sentence — the exact form it would take in a skill>
Evidence: <repo/path:line> · <repo/path:line>
Spread:   <count> vs <counter-count>, <year>–<year>
Target:   <skill it would land in>
verdict:
```

`Rule:` is written as skill content, not as an observation — "declare X and write
Y below it", never "the code tends to declare X". The verdict then approves a
sentence that is ready to move.

`Target:` is decided now, while the evidence is in view. Deciding it later, in
front of forty rules, is a second research task.

**Read every line reference back out of the file before writing it down.**
Recalled line numbers are wrong about half the time, and a verdict file whose
references do not land teaches the reader to distrust all of them. Verify the
finished file mechanically, not by sampling:

```bash
grep -o '<repo>/[A-Za-z0-9_./-]*:[0-9]\+' mining/<lang>.md | sort -u |
  while IFS=: read -r f l; do printf '%-50s %s\n' "$f:$l" "$(sed -n "${l}p" "$f")"; done
```

Mark weak evidence as weak. A candidate with one occurrence and a candidate with
four hundred must not look alike on the page.

**Done when:** every candidate has a rule, evidence, a target skill, and an empty
`verdict:`; and the human has been handed the file.

## Step 6 — land the yield

Only after verdicts are filled in. Approved rules move into the skill named in
`Target:`; free-text verdicts ("yes, but only in modules") move as written — that
qualifier is knowledge the code did not contain and the whole reason to ask.

Rules that fit no existing skill become a new one — via `skill-authoring`, not
by dumping the leftovers into a file.

**Rejected candidates stay in the verdict file with their verdict.** Without that
record every later run re-proposes the same rejects, and the human re-judges
work already done.

Shared skills are hardlinked: edit them in place with a truncating write and
verify the inode survived (`getty-skill-library`).

**Done when:** every `yes` verdict is present in a skill, and the verdict file
still lists every `no`.

## Related

- `skill-authoring` — what a skill looks like once the content exists.
- `getty-skill-library` — where it lives, what it is named, how to edit it safely.
