# Decision axes

The net for step 4. Walk it after the contrast pass and note every axis no
candidate touched — a silent axis is either genuinely absent from the corpus
(itself a finding) or a blind spot in the reading.

Each axis is phrased as the question to put to the code. Examples are Perl
because that is where the catalogue was first used; the questions are not.

## Structure

| Axis | Ask the code |
|---|---|
| **File skeleton** | What does every file open and close with? Is there a required header comment, a version line, a trailing truth value? |
| **Import block** | What order do imports come in, and does anything non-import sit among them (role composition, pragma, class declaration)? |
| **Module layout** | What lives in its own file versus inline? How deep does the namespace go before it splits? |
| **Section markers** | How is a long file divided — banners, rules, blank lines, not at all? |

## Code

| Axis | Ask the code |
|---|---|
| **Object system** | Which one, and is it the same everywhere? What happens at the boundary where a framework imposes another? |
| **Attributes** | Mutable or read-only by default? Lazy or eager? Where does construction logic live — inline or in a named builder? |
| **Type constraints** | Present at all? Where is input validated instead? |
| **Function signatures** | How are arguments unpacked, and on which line? What does a trivial one-liner do differently? |
| **Return conventions** | Explicit or implicit? Bare return or an explicit undef? Copies or references? |
| **Visibility** | How is "private" marked, and is it enforced or by convention? |
| **Control flow** | Postfix conditions or blocks? Negation via `unless`/`if not`? Guard clauses or nesting? |
| **Sugar** | Are there hand-built helpers that wrap the framework's own declarations? |

## Behaviour

| Axis | Ask the code |
|---|---|
| **Error raising** | Which function, imported or qualified? Do messages name their origin? Are there error classes? |
| **Error handling** | Caught where — at the call site, at a boundary, not at all? |
| **Logging** | Through what, with which levels, and how does a class declare its category? |
| **Strings** | Interpolation or concatenation? Which quote by default? |
| **Serialisation** | Which library, and is deterministic output configured? |
| **Filesystem and paths** | Which abstraction, or bare built-ins? |
| **Configuration** | Environment, file, or constants? How are defaults expressed and where do they live? |
| **Concurrency** | Which model, and what is the shape of an asynchronous call? |

## Around the code

| Axis | Ask the code |
|---|---|
| **Tests** | Present at all, and for which kind of project? What opens and closes a test file? Plan or dynamic count? |
| **Test data** | Fixtures, factories, temp dirs, live services? |
| **Build and release** | What produces a release, and what is hooked into it? |
| **Dependencies** | Pinned or floating? Sorted? Which houses' libraries recur — and which obvious ones are conspicuously absent? |
| **Documentation** | Inline docs required? What is always documented, what never? |
| **Naming** | What do files, classes, methods, variables look like — and what marks the exceptions? |
| **Comments** | What earns one? Does disabled code stay or go? |
| **Version control** | Anything visible in the tree that implies a workflow — changelogs, tag formats, generated files committed? |
