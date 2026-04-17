# Architecture Characteristics

**Summary**: The "-ilities" a system must support — availability, scalability, performance, reliability, security, elasticity, and so on. Architecture characteristics are the concerns critical to a system's success that are independent of the problem domain; they define the success criteria of a system orthogonally to its functionality.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-01-introduction.md`, `raw/fundamentals-of-software-architecture/chapter-04-architecture-characteristics-defined.md`, `raw/fundamentals-of-software-architecture/chapter-05-identifying-architectural-characteristics.md`, `raw/fundamentals-of-software-architecture/chapter-06-measuring-and-governing-architecture-characteristics.md`, `raw/fundamentals-of-software-architecture/chapter-07-scope-of-architecture-characteristics.md`

**Last updated**: 2026-04-16 (Chapter 7 ingested)

---

## Definition (Chapter 4)

Richards and Ford define an architecture characteristic as anything that meets **three criteria** (source: chapter-04-architecture-characteristics-defined.md):

1. **Specifies a non-domain design consideration.** Domain requirements say *what* the application does; characteristics specify *how* well and *why* certain choices were made. Performance, for instance, rarely appears in a requirements document, yet it constrains nearly every structural decision. "Prevent technical debt" is the archetype — no requirement document ever states it, but every architect designs for it.
2. **Influences some structural aspect of the design.** A characteristic rises above "default hygiene" only when it forces the architect to design something special. The chapter's worked example: if payment is delegated to a third-party processor, security is routine engineering hygiene (encryption, hashing); if payment is processed in-application, security becomes an architecture characteristic because it demands a dedicated module/component/service to isolate the risk structurally.
3. **Is critical or important to application success.** The job is to choose the **fewest** characteristics, not the most, because each one adds design complexity and interacts with the others. This is a recurring theme across the chapter and the book.

These three criteria interlock: drop any one and the term loses meaning. A concern can be non-domain and important but require no structural support (then it's a coding concern); it can be structural and non-domain but unimportant (then it's not worth the complexity); it can be structural and critical but domain-specific (then it's a requirement, not a characteristic).

Richards and Ford reject two popular alternative terms (source: chapter-04-architecture-characteristics-defined.md):

- **Non-functional requirements** — self-denigrating; "how do you get teams to pay attention to something explicitly labelled non-functional?"
- **Quality attributes** — implies after-the-fact assessment rather than up-front design.

The book's ubiquitous language is **architecture characteristics**.

## Explicit vs implicit characteristics

Characteristics split along whether they're named in the requirements:

- **Explicit characteristics** appear in requirements documents or other specific instructions ("the system must sustain 10,000 concurrent users").
- **Implicit characteristics** are rarely stated yet necessary for project success. Availability, reliability, security, and [[modularity]] underpin virtually every application. A high-frequency trading firm doesn't write "low latency" in every spec — the architects know. Uncovering implicit characteristics from domain knowledge is one of the architect's core analytical skills (and the subject of Chapter 5).

This is why [[modularity]] is filed in the wiki as an implicit characteristic: no one ever writes "the codebase should be modular" in a requirements document, yet without it no sustainable system exists.

## The three categories

Chapter 4 partitions characteristics into three broad, deliberately non-exhaustive categories (source: chapter-04-architecture-characteristics-defined.md). The book lists them in tables (4-1, 4-2, 4-3) without elaborate definitions, since each category is conventional.

### Operational

Run-time and production concerns that heavily overlap with operations and DevOps — the intersection of architecture and ops in most software projects. Typical entries:

- **Availability** — how long the system needs to be up (relates to [[architect-role-intersections|ops/DevOps]]).
- **Continuity** — disaster recovery capability.
- **Performance** — response, throughput, capacity; ISO calls this *performance efficiency*.
- **Recoverability** — time to restore after an outage.
- **[[reliability]]** — safety-critical behaviour under fault.
- **Robustness** — handling unexpected errors and boundary conditions. (See [[robustness-vs-resilience]] for Woods's distinction.)
- **[[scalability]]** — ability to grow with load; elasticity is the burstable variant.

### Structural

Code-quality and internal-organisation concerns. The architect has sole or shared responsibility for these. Typical entries:

- **Configurability** — ease of changing configuration without redeployment.
- **Extensibility** — ease of plugging in new capabilities.
- **Installability** — ease of install across target platforms.
- **Leverageability/reuse** — ability to share common components across products.
- **Localization** — i18n/l10n support.
- **[[maintainability]]** — ease of applying changes and enhancements (ISO subcategories: modularity, reusability, analyzability, modifiability, testability).
- **Portability** — running on multiple platforms (ISO subcategories: adaptability, installability, replaceability).
- **Supportability** — logging, debugging, ops diagnostics.
- **Upgradeability** — in-place version upgrades without data loss.

### Cross-cutting

Important design constraints that don't fit cleanly in either bucket and often span the whole system:

- Accessibility, archivability, authentication, authorization, legal, privacy, security, usability, and others.

Any list will be incomplete; projects routinely invent their own.

### The ISO list and "functional suitability"

Chapter 4 includes the ISO quality model as a reference point (performance efficiency, compatibility, usability, reliability, security, maintainability, portability). Richards and Ford **reject** the ISO category of *functional suitability* (completeness, correctness, appropriateness) — those are the motivational requirements to build the software, not characteristics of the architecture (source: chapter-04-architecture-characteristics-defined.md).

## Italy-ility: custom characteristics

The chapter tells the story of a client whose first question for every proposed design was "but what happens if we lose Italy?" — a reaction to an outage that had organisationally traumatised the head office. The team eventually called the resulting requirement **Italy-ility**, a custom mix of availability, recoverability, and resilience. The point: characteristics are **not a closed taxonomy**. Every project may invent important architecture characteristics based on unique factors, and these custom characteristics can be just as load-bearing as the canonical ones.

The chapter also notes that many terms overlap or contradict across definitions — interoperability vs compatibility, the two distinct meanings of learnability (users learning the system vs the system learning via ML), availability vs reliability (UDP is available but not reliable) — and recommends domain-driven design's [[domain-driven-design|ubiquitous language]] discipline to prevent term-based misunderstanding within a team.

## Trade-offs and the "least worst" principle

The chapter ends with the strongest formulation in the book so far of the [[laws-of-software-architecture|First Law]] as it applies to characteristics. Two forces make it impossible to maximise them all (source: chapter-04-architecture-characteristics-defined.md):

1. **Each supported characteristic adds design effort and structural support.**
2. **Characteristics interact.** Improving security almost certainly degrades performance (encryption, secrets indirection). Improving availability often costs consistency (see [[cap-theorem]]). Improving one almost always costs another.

The authors' helicopter metaphor: each hand and each foot has a control, and every input disturbs the others — flying a helicopter is a balancing exercise, and so is choosing architecture characteristics.

> **Never shoot for the best architecture, but rather the least worst architecture.**

Supporting too many characteristics produces generic solutions that try to solve every business problem and fail under their own weight. The architect's job is to pick the **fewest** that matter. This is why the concrete deliverable of early architectural work is a **short, ranked list** of characteristics — not an exhaustive scorecard.

Because characteristics will be wrong in the first pass, the chapter closes on an iteration argument: if the architecture can be changed cheaply, you don't need to discover the exact right set of characteristics on the first attempt. This is the connective tissue to [[evolutionary-architecture]] and [[architecture-fitness-function|fitness functions]] — the mechanism that makes iteration on characteristics safe.

## Why they are central

The book's recurring argument is that architectural styles differ mostly in which characteristics they favour. The "star rating" per style in Part II (microservices vs layered vs event-driven vs space-based) is a characteristic-by-characteristic scorecard: high scores on deployability and scalability, low scores on simplicity, etc. Choosing a style is choosing which characteristics to optimise and which to sacrifice — an instance of the [[laws-of-software-architecture|First Law]].

Naming which characteristics are required is the first concrete deliverable of architectural work — without that list, no subsequent decision can be evaluated.

## Characteristics already in the wiki

Several architecture characteristics have their own pages, drawn from multiple sources:

- [[reliability]] — correct behaviour under faults (operational)
- [[scalability]] — coping with increased load (operational)
- [[fault-tolerance]] — preventing faults from becoming failures (operational; ISO files this under reliability)
- [[maintainability]] — keeping the system workable over time; includes operability, simplicity, evolvability (structural)
- [[modularity]] — the implicit structural characteristic; the theoretical underpinning via [[cohesion]], [[coupling]], [[connascence]]
- [[independent-deployability]] — the central microservice characteristic (structural; closest fit is upgradeability/deployability)
- [[robustness-vs-resilience]] — Woods's distinction between two operational characteristics
- [[accidental-complexity]] — the enemy of several characteristics at once

## Relation to Chapter 1's worked examples

- The [[strangler-fig-pattern]] and [[feature-toggle]] discussion in Chapter 1 is about supporting **evolvability** as a structural characteristic.
- The Pets.com story is about the cost of ignoring **elasticity** as an operational characteristic (source: chapter-01-introduction.md).
- The layered-architecture example (presentation layer cannot access the database) is an [[architecture-decisions-vs-design-principles|architecture decision]] made to preserve the **modifiability** structural characteristic.

## How to identify them (Chapter 5)

Chapter 5 — covered in full on [[identifying-architecture-characteristics]] — answers *where the list comes from*. Characteristics have three sources (source: chapter-05-identifying-architectural-characteristics.md):

1. **Domain concerns** — stakeholder vocabulary (mergers, user satisfaction, time to market, competitive advantage), translated into -ilities. The translation is non-trivial: *agility ≠ time to market*; time to market is agility + testability + deployability. One domain concern typically maps to multiple characteristics, not one.
2. **Explicit requirements** — stated outright, often as numbers ("10,000 concurrent users" → scalability).
3. **Implicit domain knowledge** — never written down, inferred from knowing the domain. A sandwich shop has lunch rushes (→ elasticity); a university registration system sees procrastination spikes in the last 10 minutes (→ burst handling).

Chapter 5 also names two techniques for keeping the list short: **have stakeholders pick the top three in any order** (much easier consensus than full ranking), and **try to drop one** (which characteristic could you cut? the answer sharpens the rest). Both techniques operationalise the "fewest, not most" rule.

The chapter's two case studies are worth reading together: **the Vasa** (a Swedish warship over-specified into capsizing) as the cautionary tale for over-specification, and the **Silicon Sandwiches** [[architecture-katas|architecture kata]] as the worked example for deriving a short list from requirements + domain knowledge.

## Measuring and governing (Chapter 6)

Chapter 6 argues that a characteristic has to be **objectively defined** before it can be governed, because vague definitions ("agility", "deployability") vary across teams and defeat ubiquitous language. It sorts measurement into three axes — operational (performance budgets, statistical models over metrics), structural ([[cyclomatic-complexity]], [[coupling-metrics|coupling metrics]]), and process (testability, deployability) — detailed on [[measuring-architecture-characteristics]]. Composite characteristics like *agility* have to be decomposed into measurable leaves (modularity, deployability, testability) before they can anchor a [[architecture-fitness-function|fitness function]].

Once objectively defined, characteristics are preserved via [[architecture-governance]] — the umbrella practice of steering the project so declared characteristics hold. The modern form is automated: fitness functions encode invariants as CI-time or runtime checks (ArchUnit layer rules, JDepend cyclic-dependency gates, Netflix's Simian Army as holistic runtime fitness functions). Chapter 6 is the deep treatment that Chapter 1 only sketched.

## Scope: the architectural quantum (Chapter 7)

Chapter 7 closes out the characteristics arc by answering a question the earlier chapters left open: **at what scope do these characteristics apply?** The traditional axiomatic answer was "the system" — when architects said "scalability", they meant the scalability of the entire system. That assumption was safe when systems were monolithic; modern styles like microservices have narrowed the scope considerably (source: chapter-07-scope-of-architecture-characteristics.md).

Richards and Ford's replacement unit is the **[[architectural-quantum]]**: an independently deployable artifact with high functional cohesion and synchronous [[connascence]]. The definition has three parts — independently deployable (includes the database and any dependent components), high functional cohesion (one business-meaningful thing), and synchronous connascence (components locked into the same operational characteristics by blocking calls). See the dedicated page for the full treatment.

The headline consequence for this page:

> Architects define architecture characteristics at the quantum level rather than system level. (source: chapter-07-scope-of-architecture-characteristics.md)

**A monolith with one shared database is one quantum; characteristics are system-wide.** The Payment quantum and the Catalog quantum cannot, in a pure monolith, have different availability or security profiles — there's only one deployable and everyone lives with whatever characteristics it has.

**Microservices with per-service databases are many quanta; characteristics are per-quantum.** Different quanta can legitimately have different -ilities. The Payment quantum can be high-security, low-throughput; the Catalog quantum can be high-performance, eventually consistent; the Notification quantum can be fire-and-forget asynchronous. This is the design foundation for *hybrid architectures* — different styles per quantum, each matching its own characteristics.

The **Going, Going, Gone** kata in Chapter 7 makes this vivid: an online auction system decomposes into three quanta (Bidder feedback, Auctioneer, Bidder) with materially different characteristic lists — the Auctioneer quantum needs security and reliability that the Bidder feedback quantum doesn't; the Bidder feedback quantum needs streaming performance the Auctioneer quantum doesn't care about. A single system-level characteristic list would be wrong in both directions.

The quantum lens also lets architects identify cross-quantum synchronous calls as a design smell: two services locked in a synchronous call share operational characteristics for the duration of the call whether the architect intended it or not. See [[connascence]] for the updated (Chapter 7) communication-connascence axis.

## Related pages

- [[identifying-architecture-characteristics]]
- [[measuring-architecture-characteristics]]
- [[architecture-governance]]
- [[architectural-quantum]]
- [[cyclomatic-complexity]]
- [[architecture-katas]]
- [[software-architecture-definition]]
- [[architecture-decisions-vs-design-principles]]
- [[architecture-fitness-function]]
- [[evolutionary-architecture]]
- [[architect-expectations]]
- [[laws-of-software-architecture]]
- [[trade-off-analysis]]
- [[architectural-thinking]]
- [[modularity]]
- [[reliability]]
- [[scalability]]
- [[maintainability]]
- [[fault-tolerance]]
- [[independent-deployability]]
- [[robustness-vs-resilience]]
- [[accidental-complexity]]
- [[cap-theorem]]
- [[fundamentals-of-software-architecture]]
