# Software Architecture: The Hard Parts

**Summary**: Ford, Richards, Sadalage, and Dehghani's follow-up to *Fundamentals of Software Architecture*, focused on the class of architecture problems that *have no good general answer* — only trade-offs. Where *Fundamentals* surveys the discipline, *The Hard Parts* is a trade-off analysis textbook: identify coupling, analyze the trade-offs on each side, document the decision.

**Sources**: `raw/software-architecture-the-hard-parts/`

**Last updated**: 2026-04-19


---

## About the book

*Software Architecture: The Hard Parts: Modern Trade-Off Analyses for Distributed Architectures* (O'Reilly, 2021). Co-authored with Pramod Sadalage (data) and Zhamak Dehghani (data mesh), it extends the *Fundamentals* frame into the problem space where no universal best practice exists.

The title is a double entendre. *Hard* connotes **difficult** — architects face problems no one has faced before, entangled with the particular organization, team, and political environment. And *hard* connotes **solidity** — the foundational, hard-to-change parts of architecture, contrasted with the softer design layer that sits on top (source: raw/software-architecture-the-hard-parts/chapter-01-what-happens-when-there-are-no-best-practices.md). A favorite tongue-in-cheek definition quoted in Chapter 1: *"software architecture is the stuff that's hard to change later."*

## The thesis

> Don't try to find the best design in software architecture; instead, strive for the least worst combination of trade-offs. (source: chapter-01-what-happens-when-there-are-no-best-practices.md)

For architects, every problem is a snowflake — the exact combination of environment, business, team, and constraints is usually unique in the world. Books, blogs, and Stack Overflow cannot help. The architect's job is therefore not to search for a silver bullet (Fred Brooks, 1986: there isn't one) but to enumerate the trade-offs on either side of a consequential decision and resolve it as well as the context allows. See [[least-worst-trade-offs]] and [[trade-off-analysis]].

The two *Fundamentals* laws carry over unchanged:

- **First Law**: everything in software architecture is a trade-off.
- **Second Law**: *why* is more important than *how*. The Second Law is the motivation for [[architecture-decision-record|ADRs]], which the book uses extensively to document decisions.

## The method

The book's trade-off analysis method, introduced in Chapter 1 and used throughout:

1. **Identify [[coupling]]** — find the architectural parts that are entangled. Page-Jones's static/dynamic split (referenced in Chapter 1 and developed in Chapter 2) is the primary lens — see [[coupling]].
2. **Analyze trade-offs** — enumerate the benefits *and* costs on each side, as [[trade-off-analysis]] requires.
3. **Document decisions** — capture each one in an [[architecture-decision-record|ADR]], whose Consequences section carries the trade-off analysis itself.

The book also leans on [[architecture-fitness-function|fitness functions]] as the governance mechanism that keeps decisions from quietly eroding.

## Data as a first-class architectural concern

Unlike most architecture books, *The Hard Parts* treats data as a load-bearing architectural concern from Chapter 1. Tim Berners-Lee: *"Data is a precious thing and will last longer than the systems themselves."* Modern distributed architectures (especially [[microservices]]) forced data to become an architectural concern because bounded-context decomposition requires breaking up historically shared data (source: chapter-01-what-happens-when-there-are-no-best-practices.md).

Chapter 1 introduces the [[operational-vs-analytical-data]] split — OLTP data (the business runs on it) versus analytical data (data scientists and analysts derive insight from it) — that the rest of the book returns to repeatedly. See [[data-outlives-code]] for the asymmetry that makes data decisions structurally expensive, and [[big-ball-of-mud]] for the data-coupling antipattern the book warns against.

## The Sysops Squad saga

The book's recurring worked example is *Penultimate Electronics'* **Sysops Squad ticketing system** — a large monolithic ticketing application suffering from lost tickets, wrong-expert assignment, frequent crashes, and risky changes. The system handles four user roles (administrator, customer, expert, manager) across nonticketing workflows (customer registration, billing, reporting) and ticketing workflows (ticket creation → expert routing → mobile dispatch → completion → survey) (source: chapter-01-what-happens-when-there-are-no-best-practices.md).

The Sysops Squad is **brownfield** — the book uses it specifically because most real-world architecture work is brownfield, not greenfield (see [[brownfield-vs-greenfield]]). The [[distributed-monolith]] pathology the Sysops Squad exhibits is the starting point for the book's exercises in decomposition, granularity, data ownership, and distributed-transaction management.

The saga is a pedagogical device, not a concept. The pattern is referenced in passing on wiki pages that pick up specific Hard Parts examples.

## Structure

The book is organized around the method:

- **Part I: Pulling Things Apart** — how to decompose a system. Covers static and dynamic [[coupling]], [[modularity]], codebase evaluation, decomposition patterns, data-and-architecture tensions, and the [[service-granularity|integrator/disintegrator]] forces that set service size.
- **Part II: Putting Things Back Together** — how to recompose. Workflow coordination, transaction management ([[saga]]), contract design, [[coupling|dynamic coupling]] trade-offs.

## Ingestion status

**Fully ingested — all chapters (1–15) complete as of 2026-04-19.**

| Chapter | Title | Status |
|---|---|---|
| 1 | What Happens When There Are No "Best Practices"? | Ingested 2026-04-19 |
| 2 | Discerning Coupling in Software Architecture | Ingested 2026-04-19 |
| 3 | Architectural Modularity | Ingested 2026-04-19 |
| 4 | Architectural Decomposition | Ingested 2026-04-19 |
| 5 | Component-Based Decomposition Patterns | Ingested 2026-04-19 |
| 6 | Pulling Apart Operational Data | Ingested 2026-04-19 |
| 7 | Service Granularity | Ingested 2026-04-19 |
| 8 | Reuse Patterns | Ingested 2026-04-19 |
| 9 | Data Ownership and Distributed Transactions | Ingested 2026-04-19 |
| 10 | Distributed Data Access | Ingested 2026-04-19 |
| 11 | Managing Distributed Workflows | Ingested 2026-04-19 |
| 12 | Transactional Sagas | Ingested 2026-04-19 |
| 13 | Contracts | Ingested 2026-04-19 |
| 14 | Managing Analytical Data | Ingested 2026-04-19 |
| 15 | Build Your Own Trade-Off Analysis | Ingested 2026-04-19 |

## Relation to other books in the wiki

- [[fundamentals-of-software-architecture]] — the prerequisite; *Hard Parts* assumes its vocabulary (architecture characteristics, quanta, fitness functions, ADRs, laws) and pushes into the decision-heavy territory.
- [[monolith-to-microservices]] — Newman's migration-focused companion; *Hard Parts* overlaps on decomposition patterns and data-separation techniques.
- [[designing-data-intensive-applications]] — Kleppmann's data-engineering perspective on many of the same trade-offs the book confronts.
- [[building-event-driven-microservices]] — Bellemare's event-first lens on the dynamic-coupling choices the book dissects.

## Related pages

- [[trade-off-analysis]]
- [[least-worst-trade-offs]]
- [[laws-of-software-architecture]]
- [[architecture-decision-record]]
- [[architecture-fitness-function]]
- [[architecture-versus-design]]
- [[coupling]]
- [[static-coupling]]
- [[dynamic-coupling]]
- [[architectural-quantum]]
- [[choreography]]
- [[operational-vs-analytical-data]]
- [[distributed-monolith]]
- [[brownfield-vs-greenfield]]
- [[fundamentals-of-software-architecture]]
- [[architectural-modularity]]
- [[agility]]
- [[testability]]
- [[deployability]]
- [[maintainability]]
- [[scalability]]
- [[elasticity]]
- [[fault-tolerance]]
- [[speed-to-market]]
- [[big-ball-of-mud]]
- [[tactical-forking]]
- [[component-based-decomposition]]
- [[identify-and-size-components-pattern]]
- [[gather-common-domain-components-pattern]]
- [[flatten-components-pattern]]
- [[determine-component-dependencies-pattern]]
- [[create-component-domains-pattern]]
- [[create-domain-services-pattern]]
- [[coupling-metrics]]
- [[migration-pattern-selection]]
- [[service-based-architecture]]
- [[database-decomposition]]
- [[data-decomposition-drivers-and-integrators]]
- [[data-domain]]
- [[data-sovereignty]]
- [[database-type-selection]]
- [[polyglot-persistence]]
- [[newsql-database]]
- [[cloud-native-database]]
- [[service-granularity]]
- [[granularity-disintegrators]]
- [[granularity-integrators]]
- [[code-volatility]]
- [[reuse-patterns]]
- [[code-replication-pattern]]
- [[shared-library-pattern]]
- [[shared-service-pattern]]
- [[orthogonal-coupling]]
- [[sidecar-pattern]]
- [[service-mesh]]
- [[data-ownership]]
- [[joint-ownership-techniques]]
- [[table-split-technique]]
- [[delegate-technique]]
- [[base-properties]]
- [[compensating-update]]
- [[background-synchronization-pattern]]
- [[orchestrated-request-based-pattern]]
- [[event-based-consistency-pattern]]
- [[distributed-data-access]]
- [[interservice-communication-pattern]]
- [[column-schema-replication-pattern]]
- [[replicated-caching-pattern]]
- [[data-domain-pattern]]
- [[distributed-workflow-patterns]]
- [[workflow-orchestration]]
- [[workflow-choreography]]
- [[semantic-coupling]]
- [[saga]]
- [[epic-saga]]
- [[phone-tag-saga]]
- [[fairy-tale-saga]]
- [[time-travel-saga]]
- [[fantasy-fiction-saga]]
- [[horror-story-saga]]
- [[parallel-saga]]
- [[anthology-saga]]
- [[contracts]]
- [[strict-contract]]
- [[loose-contract]]
- [[stamp-coupling]]
- [[consumer-driven-contracts]]
- [[data-mesh]]
- [[data-product-quantum]]
- [[data-as-a-product]]
- [[data-governance]]
- [[mece-principle]]
