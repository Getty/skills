# Writing Posts

Mechanics of the individual post. Strategy (what to post at all) is in `content-strategy.md`;
distribution mechanics in `algorithm-and-distribution.md`.

## Structure

```
HOOK          1–2 lines. Must survive the fold alone (~140 chars mobile).
              A number, a story opening, or a claim someone could argue with.
CONTEXT       2–4 lines. Why this, why now, why you.
BODY          The substance: what you did, measured, found. Short paragraphs,
              one idea each. Lists and tables where they earn their place.
TURN          The thing the reader did not expect. The reason to have read it.
CTA           A specific question, a counterpoint invitation, or a resource offer.
              Never "thoughts?" — ask something only your reader can answer.
```

## Hooks

Hook type materially changes performance. One 2026 analysis of 30,360 posts across 968
creators measured these relative lifts (see `sources.md` — one dataset, treat as directional
and re-test on your own account):

| Hook type | Relative lift | Share of posts |
|---|---|---|
| **Statistic** — a concrete number in the first line | **1.67×** | small |
| **Story** — "Three years ago I …" | **1.51×** | small |
| **Direct** — states the topic plainly | 1.45× | **77.8 %** |
| **Contrarian** — "Everyone says X. They are wrong." | 1.03× | small |
| **Imperative** — "Stop doing X." | 0.02× | small |

Two readings of that table matter more than the numbers:
1. The best-performing hooks are the **least used** — the field is not competitive there.
2. The imperative hook, beloved of LinkedIn advice, is catastrophic.

**Hook patterns that work in practice:**
- `4 GB of RAM. 11,000 tokens. One laptop.`
- `I was wrong about local models. Here is the measurement that changed my mind.`
- `A customer asked for X. What they needed was Y. The difference cost €0 and six weeks.`
- `Everyone benchmarks tokens per second. That metric is meaningless without error rates.`

**Hook patterns to avoid:** "In today's fast-paced world", "I'm excited to announce",
"Let that sink in", "Unpopular opinion:" (it is always a popular opinion), any question that
answers itself.

## Length

3,000 characters available. Published analyses converge on roughly **900–1,900 characters**
as the productive range, with 1,300–1,900 cited most often for engagement. Shorter (under
600) works for a single sharp thesis. Length is not the variable to optimise — **density is.**
Cut every sentence that does not add information.

## Formatting

- **Short paragraphs**, one idea each, separated by a blank line (see the Braille-blank note
  in `post-formats-and-limits.md`).
- **No bold/italic** — LinkedIn has no native rich text in posts; Unicode pseudo-bold breaks
  screen readers and search. Do not use it.
- **Lists** for parallel items; a table as an image when the structure is the point.
- **Emoji** sparingly and functionally (as list markers at most). Emoji-heavy posts read as
  marketing.
- **No blockquote or leading `>`** in a delivered draft — the post body must be paste-ready.

## The CTA

| Weak | Strong |
|---|---|
| "Thoughts?" | "If you've run this on ARM, what did you see?" |
| "Let me know!" | "Which of these two would you have shipped, and why?" |
| "DM me" | "I wrote the full teardown — link in the first comment" |
| "Follow for more" | (nothing; earn it) |

## Never invent specifics

Numbers, anecdotes, quotes, dates, customer stories, claims about what you do — every one must
come from a real facts base. If something is missing, the draft ships with a **visible
placeholder** (`{{NUMBER}}`, `[INSERT REAL EXAMPLE]`) and a question, never a plausible
invention. This is not a stylistic preference: an invented specific in a professional post is
a reputational and sometimes legal problem.

## Editing pass

1. Does line 1 survive alone? Would *you* click "see more"?
2. Is there a number, a name, or a concrete artefact in the first three lines?
3. Can any sentence be deleted without loss? Delete it.
4. Is the honest one-line summary "here is something true I found out" — or "buy my thing"?
   If the latter, rewrite (see `content-strategy.md` §3).
5. Any invented specific? Any bare domain in the body?
6. Read it aloud. Anything you would not say out loud, cut.
