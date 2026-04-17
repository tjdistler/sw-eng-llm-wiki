# Measuring Architecture Characteristics

**Summary**: Before an [[architecture-characteristics|architecture characteristic]] can be governed, it has to be objectively measurable. Richards and Ford's Chapter 6 argues for replacing vague organisational definitions ("agility", "deployability", "performance") with concrete metrics along three axes: operational, structural, and process. Only objective definitions can anchor a [[architecture-fitness-function|fitness function]].

**Sources**: `raw/fundamentals-of-software-architecture/chapter-06-measuring-and-governing-architecture-characteristics.md`

**Last updated**: 2026-04-16

---

## Why objective definition comes first

Richards and Ford open Chapter 6 with three problems endemic to how organisations talk about characteristics (source: chapter-06-measuring-and-governing-architecture-characteristics.md):

1. **They aren't physics.** Terms like *agility* and *deployability* have no universal definition; the industry uses them inconsistently, sometimes for legitimate context reasons and sometimes accidentally.
2. **Wildly varying definitions within one org.** Dev, architecture, and ops may each mean something different by "performance". Until they unify on a concrete definition, no productive conversation is possible.
3. **Too composite.** Many desirable characteristics decompose into smaller ones. Agility = modularity + deployability + testability, for example.

The fix is the same in all three cases: pick an **objective, measurable definition**. That creates a [[domain-driven-design|ubiquitous language]] across teams and forces composite characteristics to be unpacked into measurable pieces. Without this step, fitness functions cannot exist because there's nothing concrete to assess.

This is distinct from the Chapter 4 categorisation of characteristics themselves (operational / structural / cross-cutting — see [[architecture-characteristics]]). Chapter 4 classifies *what* a characteristic is; Chapter 6 classifies *how to measure* it. The two trichotomies have overlapping vocabulary but different purposes.

## The three measurement categories

### Operational measures

Runtime and production concerns — performance, scalability, elasticity, availability, recoverability (source: chapter-06-measuring-and-governing-architecture-characteristics.md). These are the measurements most directly supported by monitoring and observability infrastructure.

Even "obvious" operational measures hide subtleties. The chapter's examples:

- **Average response time** catches the common case but misses the 1% of requests that take 10× longer. Always measure max and tail percentiles alongside the average.
- **Performance budgets** carve general performance into specific slices: first-page render, first contentful paint, first CPU idle. Mature orgs set targets like the well-known 500 ms first-visible-progress budget derived from user-behaviour research.
- **K-weight page budgets** — a maximum number of bytes of libraries/frameworks on a page, driven by physics: only so many bytes cross a high-latency mobile link before the user abandons.
- **Statistical alerting over fixed thresholds** — a video service models its scale-over-time and alarms when real-time metrics diverge from the model. Divergence means either the model is wrong (useful) or something is broken (also useful).

The measurement surface evolves with tooling. Metrics like first contentful paint didn't exist a decade ago; architects should expect new operational measures to appear.

### Structural measures

Code-quality and internal-organisation concerns (source: chapter-06-measuring-and-governing-architecture-characteristics.md). Richards and Ford are candid: comprehensive metrics for internal code quality **don't yet exist** as a field. But a few narrow, well-understood metrics carry most of the weight:

- **[[cyclomatic-complexity|Cyclomatic complexity]]** — McCabe 1976; the canonical local-complexity metric.
- **[[coupling-metrics|Afferent/efferent coupling]]** — Yourdon & Constantine 1979; incoming and outgoing dependency counts.
- **Abstractness, instability, distance from the main sequence** — Robert Martin's derived metrics; the closest software has to a holistic structural metric.
- **LCOM (lack of cohesion of methods)** — Chidamber & Kemerer; see [[cohesion]].

None of these is sufficient alone. Cyclomatic complexity can't distinguish essential from [[accidental-complexity|accidental]] complexity. Afferent/efferent coupling can't tell you whether the coupling is semantically correct. The architect's job is to pick a small combination that catches drift for the specific codebase.

### Process measures

Software-process characteristics — agility, testability, deployability (source: chapter-06-measuring-and-governing-architecture-characteristics.md). These overlap with DevOps metrics:

- **Testability** — measured via code-coverage tools on every major platform. The chapter's caveat: 100% coverage with weak assertions still provides poor confidence; the metric cannot replace intent.
- **Deployability** — measured via success/failure ratio of deployments, time-to-deploy, bugs-per-deployment, and similar indicators. Each team picks a set that captures what matters locally.

Process measures matter structurally because they often drive the architecture. If deployability and testability are priorities, the architect invests in modularity and isolation at the structural level — an operational priority shaping a structural decision.

## Why this matters for governance

The whole point of objective measurement is that it lets you write a [[architecture-fitness-function|fitness function]]. "Performance is important" is unenforceable; "p95 page load time must stay under 300 ms on every CI run" is a fitness function.

Richards and Ford's closing of the section restates the Chapter 4 three-criteria test:

> Virtually anything within the scope of a software project may rise to the level of an architecture characteristic if it manages to meet our three criteria, forcing an architect to make design decisions to account for it. (source: chapter-06-measuring-and-governing-architecture-characteristics.md)

Plus a Chapter-6 corollary: and anything that rises to the level of an architecture characteristic must be defined objectively enough to measure, or it cannot be governed.

## Composite characteristics and decomposition

The chapter's other load-bearing point: **decompose before you measure**. "Agility" is not measurable. But its components — modularity (measurable via coupling metrics), testability (measurable via coverage + mutation testing), deployability (measurable via pipeline metrics) — are each individually measurable. Decomposition is how you turn a composite wish into a set of enforceable checks.

This is also why Richards-Ford's broader argument connects: the Chapter 5 technique of picking the **fewest** characteristics that matter (see [[identifying-architecture-characteristics]]) is essentially a request to stop specifying composites and start specifying measurable leaves.

## Related pages

- [[architecture-characteristics]]
- [[architecture-fitness-function]]
- [[architecture-governance]]
- [[cyclomatic-complexity]]
- [[coupling-metrics]]
- [[cohesion]]
- [[response-time-percentiles]]
- [[monitoring-and-observability]]
- [[accidental-complexity]]
- [[identifying-architecture-characteristics]]
- [[fundamentals-of-software-architecture]]
