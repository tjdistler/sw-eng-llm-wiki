# Coupling Metrics

**Summary**: The quantitative metrics Richards and Ford collect in Chapter 3 of *Fundamentals of Software Architecture* for reasoning about code-level coupling. Afferent and efferent coupling (Yourdon & Constantine, 1979) count incoming and outgoing dependencies; Robert Martin's derived metrics — abstractness, instability, and distance from the main sequence — combine those raw counts into holistic judgments about whether a module is balanced, too abstract, or too concrete.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-03-modularity.md`, `raw/fundamentals-of-software-architecture/chapter-06-measuring-and-governing-architecture-characteristics.md`, `raw/software-architecture-the-hard-parts/chapter-04-architectural-decomposition.md`, `raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md`

**Last updated**: 2026-04-19
---

## Afferent and efferent coupling

Edward Yourdon and Larry Constantine defined these in *Structured Design: Fundamentals of a Discipline of Computer Program and Systems Design* (Prentice-Hall, 1979), borrowing the adjectives from anatomy:

- **Afferent coupling (Ca)** — the number of **incoming** connections to a code artifact (component, class, function). How many other things depend on *this*?
- **Efferent coupling (Ce)** — the number of **outgoing** connections to other code artifacts. How many other things does *this* depend on?

Tooling for these metrics exists for virtually every platform and is routinely used by architects during restructuring, migration, or technical-debt assessment (source: chapter-03-modularity.md).

### Why the names are terrible

Richards and Ford flag the obvious usability problem: *afferent* and *efferent* differ only in the vowels that sound most alike. Yourdon and Constantine borrowed the terms from mathematics for symmetry rather than clarity. The mnemonics offered in the chapter (source: chapter-03-modularity.md):

- **a** comes before **e** in the alphabet — corresponding to *incoming* before *outgoing*.
- The **e** in *efferent* matches the initial letter of *exit* — corresponding to outgoing.

A saner reading is: just say "incoming" and "outgoing." The literature uses Ca and Ce.

## Martin's derived metrics

Robert Martin introduced three derived metrics in a C++ book; Richards and Ford note they generalise well to other object-oriented languages (source: chapter-03-modularity.md).

### Abstractness (A)

> A = Σ(ma) / Σ(mc)

Where `ma` = abstract artifacts (interfaces, abstract classes) and `mc` = concrete artifacts (implementation classes) (source: chapter-03-modularity.md).

This is the ratio of abstractions to concrete elements. The worked illustration: an application of 5,000 lines, all in one `main()`, has `ma = 0` (actually the numerator is tiny) and `mc ≈ 5000`, so abstractness ≈ 0. The opposite extreme is a codebase so abstract that an `AbstractSingletonProxyFactoryBean` is indistinguishable from parody.

### Instability (I)

> I = Ce / (Ce + Ca)

The ratio of efferent coupling to total coupling (source: chapter-03-modularity.md). Instability captures **volatility**: a module with high efferent coupling (many outgoing calls) breaks easily when any of its dependencies change. A module that only receives calls (Ca > 0, Ce = 0) has I = 0 — it is stable, because no dependency it makes can pull the rug out.

The word "instability" here is *descriptive*, not pejorative. A code base needs both stable and unstable components — stable utilities at the bottom, unstable orchestrators at the top.

### Distance from the main sequence (D)

> D = |A + I − 1|

The metric derives from plotting abstractness on one axis and instability on the other. Both are fractions between 0 and 1, so their sum ranges from 0 to 2. The **main sequence** is the line where A + I = 1 — the ideal balance point (source: chapter-03-modularity.md).

Two named regions sit on opposite corners of the plot:

- **Zone of uselessness** (upper-right, A ≈ 1 and I ≈ 1): the code is highly abstract and highly unstable. Abstract things that nothing depends on — abstractions for their own sake. "Code that is too abstract becomes difficult to use" (source: chapter-03-modularity.md).
- **Zone of pain** (lower-left, A ≈ 0 and I ≈ 0): concrete implementation that many things depend on. Hard to change without breaking the world. "Code with too much implementation and not enough abstraction becomes brittle and hard to maintain" (source: chapter-03-modularity.md).

A class falling near the main sequence (A + I ≈ 1) balances abstraction against how many things it exposes to change.

D is one of the few **holistic** metrics available for architectural structure (source: chapter-03-modularity.md). Most architecture metrics are local: cyclomatic complexity, LCOM, Ca, Ce. D combines them into a single number per module, which makes it useful for flagging outliers during migrations or technical-debt assessments.

## Limits of code-level metrics

Richards and Ford are blunt about the state of the art (source: chapter-03-modularity.md):

- Software-engineering metrics are **extremely blunt** compared to tools in other engineering disciplines.
- Even structural metrics require **interpretation**. Cyclomatic complexity can't distinguish *essential* complexity (the problem is hard) from *accidental* complexity (the code is harder than the problem — see [[accidental-complexity]]).
- Everything above predates the popularity of object-oriented languages and targets structured-programming constructs. Other coupling types defined in *Structured Design* have been **supplanted by [[connascence]]**, which Richards and Ford treat as the modern complement to these metrics.

The metrics earn their keep by establishing **baselines**. Once you know your codebase's current Ca/Ce/A/I/D distribution, a [[architecture-fitness-function|fitness function]] can assert that new commits don't push any module further from the main sequence, or that no module exceeds a Ca threshold. The metrics aren't for grading code; they're for preventing drift.

Chapter 6 makes this concrete with a JDepend-based fitness function that fails CI when any package's distance metric exceeds a project-specific tolerance (source: chapter-06-measuring-and-governing-architecture-characteristics.md; see [[architecture-fitness-function]] for the full example). Richards and Ford note the same example also illustrates a caveat: distance-from-the-main-sequence is an esoteric metric, and developers must understand why it matters before the check is imposed, or the failure will seem arbitrary and be bypassed. This is the **no-ivory-tower** rule for [[architecture-governance]].

## Using the metrics as a decomposability check

*The Hard Parts* Chapter 4 repurposes the whole metric suite for a specific question: **is this monolith even decomposable?** Before an architect picks between [[component-based-decomposition]] and [[tactical-forking]], they need to know whether the codebase has enough internal structure to support a disciplined decomposition at all (source: chapter-04-architectural-decomposition.md).

Richards and Ford are explicit that no single metric answers this — the judgement remains the architect's. But the metrics above give the architect an evidence base:

- **Ca / Ce matrices** (via JDepend on the JVM, NDepend for .NET, or equivalent) surface the topology of the monolith. A codebase where every package depends on every other package is the quantitative signature of a [[big-ball-of-mud]]; one where dependency clusters are visible is a candidate for component refinement.
- **Abstractness / instability per component** reveals whether the monolith has a coherent stable-utility / unstable-orchestrator layering, or whether components are uniformly concrete and uniformly coupled (a mud-ball indicator).
- **Distance from the main sequence** applied across components is the holistic read. If most components fall near the line, the architect can refine them into service candidates. If most fall into the zones of pain or uselessness, component-based decomposition is not worth the effort — [[tactical-forking]] or a rewrite is the honest call.

The metrics don't decide the decomposition approach on their own; they inform the Chapter 4 decision tree. See [[component-based-decomposition]] for the full selection rubric.

### The JDepend-style tool chain

The chapter names the tooling category explicitly (source: chapter-04-architectural-decomposition.md). Every major platform has a coupling-analysis tool that produces the Ca/Ce matrix and derived metrics an architect needs for the readiness assessment:

- **JDepend / Eclipse plugins** — JVM, the chapter's illustrated example.
- **NDepend** — .NET.
- **Structure101, Sonargraph, Lattix** — multi-platform.
- **IDE built-ins** (IntelliJ's Dependency Matrix, Visual Studio's Architecture Explorer) — quick reads without setting up a separate tool.

These tools produce the *same* metrics Chapter 3 of *Fundamentals* defines. The difference in *Hard Parts* Ch 4 is the **use-case**: not monitoring drift in a living codebase, but *assessing* a legacy codebase for migration feasibility.

## Component-granularity use: the Chapter 5 dependency pattern

Chapter 5 of *The Hard Parts* applies Ca and Ce **at the component level**, not the class level — a component dependency exists when any class in component A references any class in component B, regardless of how many class-to-class edges underlie it (source: raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md). This coarsening is deliberate: internal class-level coupling inside a component is the developer's problem; inter-component coupling is the architect's problem and the predictor of inter-service coupling after extraction.

The resulting **component dependency graph** is the radar used by [[determine-component-dependencies-pattern]] to answer three migration questions:

- **Sparse graph (golfball)** — feasible, low effort, pure refactor.
- **Dense asymmetric graph (basketball)** — partially feasible, significant effort, refactor + rewrite.
- **Saturated graph (airliner)** — not feasible as a decomposition; full rewrite territory.

The chapter further notes that **decomposition itself can reduce coupling**: splitting a high-Ca component into A1 (carrying the small, coupled slice) and A2 (carrying the majority) can cut each piece's afferent count below threshold. This turns the metric into a prescriptive signal, not just a descriptive one (source: chapter-05-component-based-decomposition-patterns.md).

[[architecture-fitness-function|Fitness functions]] paired with the pattern: a total-coupling ceiling per component (the chapter's pseudocode uses 15), and ArchUnit-based "component X must not depend on component Y" rules — one per deliberate architectural prohibition.

## Unifying coupling and connascence

The chapter's "Unifying Coupling and Connascence" section makes the relationship explicit (source: chapter-03-modularity.md):

- Afferent/efferent coupling tells you **how much** coupling exists and in which direction.
- Static [[connascence]] refines that into **what kind** — CoN, CoT, CoM, CoP, CoA — ordered by how easy to refactor.
- Dynamic connascence covers runtime territory (execution order, timing, shared identity, coordinated values) that structured-programming coupling never addressed.

An architect in practice uses both. The metrics flag outliers; connascence tells you what to do about them. The modern architectural quantum concept introduced in Chapter 7 extends this further to distributed-system coupling.

## Related pages

- [[coupling]]
- [[connascence]]
- [[modularity]]
- [[cohesion]]
- [[accidental-complexity]]
- [[architecture-fitness-function]]
- [[architecture-governance]]
- [[cyclomatic-complexity]]
- [[measuring-architecture-characteristics]]
- [[big-ball-of-mud]]
- [[component-based-decomposition]]
- [[determine-component-dependencies-pattern]]
- [[tactical-forking]]
- [[fundamentals-of-software-architecture]]
- [[software-architecture-the-hard-parts]]
