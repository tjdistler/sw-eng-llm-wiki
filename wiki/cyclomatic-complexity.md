# Cyclomatic Complexity

**Summary**: A code-level metric developed by Thomas McCabe in 1976 that counts the number of linearly independent execution paths through a function. It is one of the few objective, tool-computable measures available for the structural dimension of [[architecture-characteristics|architecture characteristics]] — in particular for maintainability, testability, and modularity — and is therefore a natural input to an [[architecture-fitness-function|architecture fitness function]].

**Sources**: `raw/fundamentals-of-software-architecture/chapter-06-measuring-and-governing-architecture-characteristics.md`

**Last updated**: 2026-04-16

---

## Definition

Cyclomatic Complexity (CC) applies graph theory to source code. Treat the control-flow graph of a function as a graph; CC counts the decision points that cause divergent execution paths (source: chapter-06-measuring-and-governing-architecture-characteristics.md).

For a single function or method:

> **CC = E − N + 2**

Where `N` is the number of nodes (code statements) and `E` is the number of edges (possible transfers of control).

The generalised form for a function that fans out to other methods (connected components in graph theory):

> **CC = E − N + 2P**

Where `P` is the number of connected components.

Intuitively, CC is one plus the number of decision points (`if`, `else if`, `case`, `&&`, `||`, loop predicates). A function with no conditionals has CC = 1. One `if` yields CC = 2. Two nested `else if` branches yield CC = 3.

## Worked example from Chapter 6

```
public void decision(int c1, int c2) {
  if (c1 < 100)
    return 0;
  else if (c1 + c2 > 500)
    return 1;
  else
    return -1;
}
```

CC = 3 (three possible paths through the function) (source: chapter-06-measuring-and-governing-architecture-characteristics.md).

## What's a good threshold?

Richards and Ford note the industry convention: **CC < 10 is acceptable**, barring domain reasons for higher complexity (source: chapter-06-measuring-and-governing-architecture-characteristics.md). They consider that threshold too permissive and prefer **CC < 5** as an indication of cohesive, well-factored code.

Crucial qualifier: domain complexity matters. An algorithmically complex problem (pricing engine, chess evaluator, compiler) will yield genuinely complex functions. The architect's job is to ask:

- **Is the function complex because the problem is?** If yes, that's essential complexity — leave it.
- **Or is the function complex because the code is badly partitioned?** If yes, that's [[accidental-complexity|accidental complexity]] — extract helpers, split responsibilities, refactor.

This is the same essential-vs-accidental distinction that underlies every structural metric — CC cannot make the judgement for you (source: chapter-06-measuring-and-governing-architecture-characteristics.md; see also the same warning on [[coupling-metrics]]).

## Crap4J and the CC × coverage grid

The Java tool Crap4J combines CC with code coverage to produce a "crap score" (source: chapter-06-measuring-and-governing-architecture-characteristics.md). The rule the tool implements: if CC exceeds ~50, no amount of test coverage redeems the code. High CC means too many paths to meaningfully test.

Neal Ford's horror story in the chapter: a single commercial-software C function with CC > 800, over 4,000 lines of code, with liberal `GOTO` statements to escape deeply nested loops. The number is a memorable anchor for what "too high" really looks like.

## Relationship to TDD

Richards and Ford observe a side effect of test-driven development: it produces **smaller, less complex methods on average** for a given problem domain (source: chapter-06-measuring-and-governing-architecture-characteristics.md).

The mechanism: TDD's red-green-refactor cadence encourages writing the smallest amount of code to pass the test, then refactoring. Tests drive methods toward single, discrete behaviours with clean boundaries. That structural pressure is orthogonal to the practice's stated goal of correctness but produces low-CC code as a by-product.

## As a fitness function

CC is directly actionable as an [[architecture-fitness-function|architecture fitness function]]. Typical shapes:

- **Absolute threshold** — fail CI if any function exceeds CC = N (pick N for the project).
- **Drift alarm** — baseline the current distribution and fail CI if a commit introduces a function over the 95th percentile, or if the mean rises.
- **Hotspot monitor** — warn on the top ten highest-CC functions and require a comment explaining why each is unavoidable.

The attraction is that every mainstream language has CC tooling (SonarQube, ESLint plugins, Checkstyle, Radon, gocyclo), so the fitness function is cheap to wire in. The cost is that CC alone is coarse — it doesn't catch coupling issues or architectural-layer violations.

## Limits

CC measures **local** complexity only. A 5-line function with CC = 2 can still be disastrous if it's at the centre of a massive dependency web. That's why CC is typically paired with [[coupling-metrics|afferent/efferent coupling]] and distance-from-the-main-sequence for a fuller structural picture. Richards and Ford's "unifying coupling and connascence" argument applies here too: metrics cooperate; none is sufficient alone.

CC is also language-level, not architecture-level. It says nothing about whether the presentation layer depends on the persistence layer — that's what [[architecture-governance|architectural governance]] via tools like ArchUnit and NetArchTest is for.

## Related pages

- [[architecture-fitness-function]]
- [[architecture-governance]]
- [[measuring-architecture-characteristics]]
- [[coupling-metrics]]
- [[modularity]]
- [[maintainability]]
- [[accidental-complexity]]
- [[architecture-characteristics]]
- [[fundamentals-of-software-architecture]]
