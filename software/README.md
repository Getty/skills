![software](../assets/software.png)

# Software skills

Creating and structuring software projects, independent of language. Language-
specific depth lives in the language groups; this is the common ground and the
router into them.

## [getty-create-software](getty-create-software/SKILL.md)

Scaffolds a new project: detect the type from the signals present (a `Foo::Bar`
name or a `dist.ini` means Perl, `package.json` means Node, and so on), lay down
the structure and the right `.gitignore`, initialise git and make the first commit.

Ships `.gitignore` templates for Perl/Dist::Zilla, Node.js, Python, Go and a
generic one, plus a `claude.gitignore` block for repos that carry a `.claude/`
directory — merged into an existing file rather than overwriting custom patterns.
Perl distributions are routed onwards to `getty-perl-distribution`, which owns the
full CPAN scaffold.

The skill is deliberately conservative about guessing: an ambiguous type, an
existing `.gitignore` that would lose custom patterns, or missing author metadata
all stop and ask rather than inventing something.

**Load when** creating a new project or module — "create", "new", "scaffold",
"init" plus a name.
