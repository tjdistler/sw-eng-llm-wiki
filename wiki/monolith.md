# Monolith

**Summary**: A unit of deployment in which all functionality must be deployed together. Newman identifies three variants — the single-process monolith (and its modular subtype), the distributed monolith, and third-party black-box systems — and argues the monolith is a valid architectural choice, not a synonym for legacy.

**Sources**: `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`, `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`, `raw/fundamentals-of-software-architecture/chapter-07-scope-of-architecture-characteristics.md`, `raw/fundamentals-of-software-architecture/chapter-09-foundations.md`

**Last updated**: 2026-04-16 (Chapter 9 ingested)

---

## What counts as a monolith

When Newman uses the term, he means primarily a *unit of deployment*: a system in which all functionality has to be deployed together is a monolith (source: chapter-01-just-enough-microservices.md). Three types fit this definition.

## 1. The single-process monolith

All code is packaged into a single process. There may be multiple instances of the process for robustness or scaling, but fundamentally all code is in one binary (source: chapter-01-just-enough-microservices.md).

These systems are often themselves simple distributed systems — they read from a database that runs on a different machine. This is the most common form Newman encounters, and the primary focus of *Monolith to Microservices*.

### The modular monolith (subtype)

A single-process monolith whose code is broken into independent modules that still combine into one deployable artifact (source: chapter-01-just-enough-microservices.md). Modular monoliths can be excellent: well-defined module boundaries allow parallel work while sidestepping the operational complexity of distribution. **Shopify** is cited as a successful example.

A common challenge is that the database typically lacks the same decomposition as the code, making future extraction harder. Some teams push further by decomposing the database along module lines.

## 2. The distributed monolith

A system that consists of multiple services but where the entire system has to be deployed together (source: chapter-01-just-enough-microservices.md). Distributed monoliths often meet the formal definition of SOA but fail to deliver its benefits.

> "A distributed monolith has all the disadvantages of a distributed system, and the disadvantages of a single-process monolith, without enough upsides of either" (source: chapter-01-just-enough-microservices.md).

They typically arise when teams build services without enough focus on [[information-hiding]] and [[cohesion]], producing highly coupled architectures where changes ripple across boundaries. Encountering distributed monoliths motivated much of Newman's interest in microservices.

## 3. Third-party black-box systems

Off-the-shelf or SaaS software you cannot modify — payroll, CRM, HR systems — can also be treated as monoliths to decompose around. The decomposition patterns discussed later in the book apply even when the underlying code cannot be changed (source: chapter-01-just-enough-microservices.md).

## Challenges of monoliths

The primary challenge is *delivery contention*: as more people work in the same place, they get in each other's way. Different developers want to change the same code; different teams want to push features at different times (or delay deployments). Lines of ownership get confused (source: chapter-01-just-enough-microservices.md).

Monoliths are particularly vulnerable to [[coupling|implementation and deployment coupling]]. A microservice architecture does not eliminate delivery contention, but it provides concrete boundaries around which ownership lines can be drawn.

## Advantages of monoliths

The single-process monolith has real strengths (source: chapter-01-just-enough-microservices.md):

- **Simpler deployment topology** — avoids many distributed-systems pitfalls.
- **Simpler developer workflow** — one process, one debugger.
- **Simpler monitoring, troubleshooting, and end-to-end testing.**
- **Code reuse is trivial** — no need to copy code, extract libraries, or push functionality into a service. The code is just there.

> "A monolithic architecture is a choice, and a valid one at that. It may not be the right choice in all circumstances, any more than microservices are — but it's a choice nonetheless" (source: chapter-01-just-enough-microservices.md).

Newman warns against treating "monolith" as synonymous with "legacy."

## When the monolith is the right choice

Chapter 2 reinforces several scenarios where a monolith — typically a [[modular-monolith]] — is the better answer (source: chapter-02-planning-a-migration.md):

- **Unclear domain.** Premature decomposition is expensive. The SnapCI team at ThoughtWorks merged their microservices back into one monolith to learn the domain before re-decomposing a year later.
- **Real startups** (pre-product/market-fit). The product itself is shifting; service boundaries laid down now will be wrong. See [[when-microservices-are-a-bad-idea]].
- **Customer-installed software.** Pushing operational complexity onto customers who don't have your skills or platform breaks the contract they bought into.
- **Many of microservices' stated benefits** (autonomy, parallel development, even some scaling) can be achieved by a [[modular-monolith]] at a fraction of the cost. See [[why-microservices]].

## A monolith is a quantum of one

Richards and Ford (Chapter 7 of *Fundamentals of Software Architecture*) frame the monolith / microservices distinction in terms of the [[architectural-quantum]] — the unit at which [[architecture-characteristics]] are scoped. A single-process monolith backed by a single shared database satisfies the three-part quantum definition exactly once: there's one independently deployable artifact, its cohesion is whatever the architect made of it, and all its communication is in-process (synchronous by construction) (source: chapter-07-scope-of-architecture-characteristics.md).

> Virtually all legacy systems deployed using a single database by definition form a quantum of one. (source: chapter-07-scope-of-architecture-characteristics.md)

The practical consequence is that **characteristics in a monolith are system-wide** — you cannot give the Payment code a different availability SLA from the Catalog code because there's no quantum boundary between them. The Payment and Catalog code share the process, the database, and every -ility. This is not by itself a problem (it's often an advantage — one consistent operational profile is much simpler to reason about) but it constrains the kinds of architectures a monolith can represent. Heterogeneous characteristics (different availability, scalability, or security per domain) require multiple quanta, which means extracting services — the subject of Newman's [[incremental-migration]].

The distributed-monolith anti-pattern looks the same under the quantum lens: multiple deployables that are synchronously and deeply coupled are *operationally* one quantum even though they're packaged as several. You pay the distribution tax without gaining the ability to scope characteristics independently — which is exactly Newman's complaint that the distributed monolith has all the downsides of both worlds.

## Monolithic vs distributed as the top-level style split

Chapter 9 of *Fundamentals of Software Architecture* uses **monolithic vs distributed** as the primary classification for every architecture style in Part II — layered, pipeline, and microkernel on the monolithic side; service-based, event-driven, space-based, SOA, and microservices on the distributed side (source: chapter-09-foundations.md). The split is load-bearing because distributed architectures all share a common cost structure — the [[fallacies-of-distributed-computing|eight fallacies of distributed computing]], plus distributed logging, distributed transactions, and contract-maintenance overheads — that monolithic architectures avoid by construction.

A monolith in this scheme dodges every fallacy: no network on the business-request path means reliability, latency, bandwidth, and topology concerns don't apply. That's the main reason Richards and Ford treat *monolithic* as a legitimate first choice rather than a legacy label. See [[monolithic-vs-distributed]] for the full Chapter 9 framing.

## Brownfield is easier than greenfield

A counter-intuitive corollary: an existing monolith you want to decompose is easier to work with than a greenfield microservice design (source: chapter-02-planning-a-migration.md). You have running code to inspect, users to talk to, a working baseline to compare against, and a production performance profile. Newman's advice: most of the time, start with the monolith.

## Related pages

- [[microservices]]
- [[modular-monolith]]
- [[independent-deployability]]
- [[coupling]]
- [[cohesion]]
- [[information-hiding]]
- [[conways-law]]
- [[when-microservices-are-a-bad-idea]]
- [[incremental-migration]]
- [[architectural-quantum]]
- [[architecture-characteristics]]
- [[monolithic-vs-distributed]]
- [[fallacies-of-distributed-computing]]
