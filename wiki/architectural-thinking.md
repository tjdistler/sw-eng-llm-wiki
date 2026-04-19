# Architectural Thinking

**Summary**: Richards and Ford's name for the mindset that distinguishes an architect from a developer. It is not "thinking about the architecture" — it is seeing systems through an architectural eye. They decompose it into four aspects: knowing the line between [[architecture-versus-design|architecture and design]], favouring [[technical-breadth-vs-depth|technical breadth over depth]], [[trade-off-analysis|analysing trade-offs]] rather than seeking best answers, and translating business drivers into [[architecture-characteristics|architecture characteristics]].

**Sources**: `raw/fundamentals-of-software-architecture/chapter-02-architectural-thinking.md`, `raw/software-architecture-the-hard-parts/chapter-15-build-your-own-trade-off-analysis.md`

**Last updated**: 2026-04-19

---

## The framing

> An architect sees things differently from a developer's point of view, much in the same way a meteorologist might see clouds differently from an artist's point of view. (source: chapter-02-architectural-thinking.md)

Many architects believe architectural thinking is simply "thinking about the architecture." Richards and Ford argue it is much more than that — it is a specific cognitive stance with four identifiable components (source: chapter-02-architectural-thinking.md).

## The four aspects

### 1. Architecture versus design

Understanding the difference between architecture and design, and collaborating with development teams to keep the two in sync. See [[architecture-versus-design]]. The traditional waterfall separation — architect throws artefacts over the wall to developers — is why architecture rarely works; a bidirectional relationship is required.

### 2. Technical breadth over depth

A developer's career rewards depth; an architect's career shifts the knowledge portfolio toward breadth. See [[technical-breadth-vs-depth]]. Knowing that five solutions exist is more valuable to an architect than being the world expert in one of them.

### 3. Trade-off analysis

The architect's core skill. Every solution carries advantages *and* disadvantages, and "it depends" is the honest answer to most architecture questions. See [[trade-off-analysis]]. This is the applied form of the [[laws-of-software-architecture|First Law of Software Architecture]].

*Software Architecture: The Hard Parts* Chapter 15 turns this aspect into a **repeatable method** the architect can apply to any problem: (1) find what parts are entangled, (2) analyze how they are coupled, (3) assess trade-offs via iterative scenario modelling, then document in an [[architecture-decision-record|ADR]] (source: chapter-15-build-your-own-trade-off-analysis.md). The chapter also catalogues the **techniques** that make trade-off analysis honest — qualitative over quantitative comparison, [[mece-principle|MECE lists]], avoiding the out-of-context trap, modelling relevant domain cases, preferring the bottom line over overwhelming evidence, and resisting snake oil / evangelism. All of these live on [[trade-off-analysis]]. The corollary for architectural thinking: the architect's role is **objective arbiter of trade-offs**, not evangelist.

### 4. Understanding business drivers

Translating business goals (time-to-market, cost ceilings, compliance obligations, growth targets) into [[architecture-characteristics|architecture characteristics]] (scalability, availability, performance, security, and so on). Chapter 2 flags this as the fourth aspect but defers the full treatment to Chapters 4, 5, and 6 (source: chapter-02-architectural-thinking.md).

## The fifth theme: balancing architecture with hands-on coding

Chapter 2 closes with a section on how an architect maintains some level of technical depth while performing the architecture role — see [[balancing-architecture-and-coding]]. It is not one of the four named aspects of architectural thinking but it is the operational discipline that keeps the *first* aspect (architecture versus design) honest: without hands-on experience, the architect loses credibility with developers and cannot mentor them effectively.

## Relationship to the two laws

Architectural thinking is how the [[laws-of-software-architecture|two laws]] become daily practice:

- The **First Law** (everything is a trade-off) drives aspect #3 directly.
- The **Second Law** (why beats how) drives aspect #4 — the architect must understand *why* the business needs what it does, not just *how* to build it.
- Aspects #1 and #2 are the role-and-skill preconditions that make #3 and #4 performable at all.

## Relationship to the architect expectations

Chapter 1's eight [[architect-expectations]] and Chapter 2's architectural thinking cover overlapping territory but frame it differently. The expectations are *observable behaviours*; architectural thinking is the *cognitive stance* from which those behaviours emerge. Expectation #5 (diverse exposure) is the expectation form of aspect #2; expectation #6 (business domain knowledge) is the expectation form of aspect #4.

## Related pages

- [[architecture-versus-design]]
- [[technical-breadth-vs-depth]]
- [[trade-off-analysis]]
- [[balancing-architecture-and-coding]]
- [[architect-expectations]]
- [[laws-of-software-architecture]]
- [[software-architecture-definition]]
- [[architecture-characteristics]]
- [[fundamentals-of-software-architecture]]
- [[software-architecture-the-hard-parts]]
- [[mece-principle]]
- [[least-worst-trade-offs]]
