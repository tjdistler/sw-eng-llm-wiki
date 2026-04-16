# Monolith

**Summary**: A unit of deployment in which all functionality must be deployed together. Newman identifies three variants — the single-process monolith (and its modular subtype), the distributed monolith, and third-party black-box systems — and argues the monolith is a valid architectural choice, not a synonym for legacy.

**Sources**: `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`, `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`

**Last updated**: 2026-04-16

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
