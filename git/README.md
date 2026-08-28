![git](../assets/git.png)

# Git skills

How Getty's repositories are used, and how their commit messages are written — two
different concerns kept as two skills so either can be loaded without the other.

## [getty-git-usage](getty-git-usage/SKILL.md)

Short version: **keep the history linear.** A branch lands rebased, not merged, and
a force-push after a rebase is always `--force-with-lease`.

Covers why squash-merging is the wrong default where a release is cut from commit
prefixes (squashing replaces the individual `feat:`/`fix:` subjects with the PR
title, and a PR title without a prefix cuts no release at all), how stacked branches
behave when the lower one lands — GitHub closes the dependent PR and refuses to
reopen it — and which conventional prefixes drive which version bump. Merge commits
are not forbidden, just not the default.

It also states the cadence: **commit early and commit often**, one finished piece of
work per commit down to a typo fix, and wrapping up finished work needs no separate
go-ahead — pushing is the decision that waits. The linear, never-squashed history is
what carries those small commits into `main`, and with them `git bisect`, a one-commit
revert and the option to cherry-pick. A skill file that arrived under
`.claude/skills/` by hardlink gets a commit of its own: the edit was made in the repo
that owns it and merely surfaces here, so it never rides along in a code commit.

**Load when** landing a branch, cleaning up history before a PR, working with
stacked branches, or cutting a release.

## [getty-git-commit-style](getty-git-commit-style/SKILL.md)

The message format: an imperative summary line under ~72 characters, then a body
with one line per discrete change — no bullets, no prose, no "This commit…".

The rule that carries the most weight is completeness: every file-level change gets
named, nothing silently lumped together. State *what* changed, never why it matters
or how it works — the diff shows that. Includes the `@`-symbol trap (GitHub reads
`@word` as a user mention, so a bundle is written `[DBIO]`, never `[@DBIO]`), the
co-authorship trailer naming the model that actually did the work, and passing
messages via HEREDOC so the formatting survives the shell.

A `Changes`/`CHANGELOG` entry follows the same rules, plus three an ever-open
unreleased section needs: **one topic, one entry** — touching an area again rewrites
the bullet already there instead of appending a second; **describe the destination,
not the journey**, since the reader never saw the old behaviour and the reasoning
already has homes that keep it; and **reference only the tracker the repo
publishes** — an internal board number has no reader outside the workspace and, written
as `#254`, resolves against the platform's own issue 254, where it is a dead link or,
later, someone else's bug.

**Load when** writing or amending a commit message, including one that spans
several repos — each repo gets its own commit, with no cross-references.
