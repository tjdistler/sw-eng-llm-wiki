# Principles of Good Data Architecture

**Summary**: Reis and Housley's nine principles for evaluating major architectural decisions in data systems. Drawn from AWS Well-Architected ([[well-architected-framework]]) and Google Cloud's Five Principles for Cloud-Native Architecture ([[cloud-native-principles]]), then adapted and extended for data engineering.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`

**Last updated**: 2026-04-18

---

## The nine principles

Chapter 3 enumerates nine principles (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

1. Choose common components wisely
2. Plan for failure
3. Architect for scalability
4. Architecture is leadership
5. Always be architecting
6. Build loosely coupled systems
7. Make reversible decisions
8. Prioritize security
9. Embrace FinOps

The principles sit on top of the two external frameworks Reis and Housley recommend studying in full: the AWS [[well-architected-framework]] (six pillars) and Google Cloud's [[cloud-native-principles]] (five principles).

## Principle 1: Choose common components wisely

Select widely reusable components that cross teams and projects — object storage, version control, observability, monitoring, orchestration, processing engines. Common components become the fabric that enables collaboration and breaks down silos (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

It is a **balancing act**: common components must not become one-size-fits-all mandates that block domain-specific work. Cloud platforms make this easier — storage-compute separation lets teams share the storage layer while picking their own query engine.

## Principle 2: Plan for failure

> Everything fails, all the time. — Werner Vogels

Hardware is robust but not infallible. Chapter 3 names four metrics the architect has to think about (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- **Availability** — the percentage of time a service is operable (see [[availability-measurement]]).
- **Reliability** — the probability the system meets defined standards during a specified interval (see [[reliability]]).
- **Recovery time objective (RTO)** — maximum acceptable outage duration. One day is fine for an internal reporting system; five minutes could kill an online retailer.
- **Recovery point objective (RPO)** — maximum acceptable data loss (how far back you're willing to roll the state back to).

Every architecture decision should be evaluated against plausible failure scenarios.

## Principle 3: Architect for scalability

Two directions (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- **Scale up** — spin up the cluster big enough to train the petabyte model, or absorb a transient load spike
- **Scale down** — once the spike passes, shed capacity to cut cost (ties directly to Principle 9)

An **elastic** system scales dynamically in response to load, ideally automatically. Some can **scale to zero** — shut down when idle (serverless functions, serverless OLAP). See [[scalability]] and [[elasticity]].

Reis and Housley warn: **inappropriate scaling strategies cost more than they save**. A relational database with one failover node may be the right answer, not a complex cluster. Measure current load, estimate growth, then choose.

## Principle 4: Architecture is leadership

> The best data architects take [leadership plus technical competence] seriously.

Data architects must be technically competent but delegate the individual-contributor work. Leadership here is **not** command-and-control (the old model of mandating one proprietary database). The [[data-architect]] page covers this role in depth. Chapter 3 cites Martin Fowler's *Architectus Oryzus* archetype: the most important activity is to mentor the team and raise their level — running the risk of being an architectural bottleneck is worse than being less directly in control (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

## Principle 5: Always be architecting

Borrowed directly from [[cloud-native-principles|Google Cloud's fifth principle]]. Data architects do not maintain the existing state — they constantly redesign in response to business and technology change (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

Per EABOK, the architect's job is to:

1. Develop deep knowledge of the **baseline architecture** (current state)
2. Develop a **target architecture** (future state)
3. Map out a **sequencing plan** to get from one to the other

Modern architecture is collaborative and agile, not command-and-control or waterfall. The target architecture is a moving target; the sequencing plan determines immediate priorities. See [[evolutionary-architecture]].

## Principle 6: Build loosely coupled systems

From the Google DevOps Tech Architecture Guide: *loosely coupled architecture enables teams to test, deploy, and change systems without dependencies on other teams*.

Chapter 3 tells the story of the **Bezos API Mandate** (2002) — all Amazon teams must expose functionality through service interfaces; no direct reads of another team's data store; every interface must be externalizable from the ground up. This mandate is widely viewed as the moment that made AWS possible (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

Technical properties of loose coupling:

1. Systems are broken into many small components
2. Components interface through abstraction layers (messaging bus, API) that hide internal details
3. Internal changes don't require changes elsewhere
4. No waterfall global release cycle — each component releases independently

**Organisational translation** (the point Chapter 3 hammers): these are not just technical properties. Many small teams own components; teams publish their interfaces to each other; each team evolves independently; releases are continuous during regular working hours.

See [[loose-coupling]], [[microservices]], [[event-driven-architecture]].

## Principle 7: Make reversible decisions

> One of an architect's most important tasks is to remove architecture by finding ways to eliminate irreversibility in software designs. — Martin Fowler

The [[reversible-vs-irreversible-decisions|two-way-door framing]] (Bezos) — prefer reversible decisions because the data landscape changes rapidly and today's hot stack is tomorrow's afterthought. Pick best-of-breed solutions for **today**, and be prepared to upgrade as the landscape evolves (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

This principle directly depends on Principle 6: loose coupling is what makes decisions reversible in practice.

## Principle 8: Prioritize security

Two sub-concepts that Chapter 3 elevates (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- **[[zero-trust-security]]** — the cloud-native replacement for the traditional hardened-perimeter model. Perimeters are an illusion once every asset is internet-connected.
- **[[shared-responsibility-model]]** — AWS's framing of who secures what: the provider secures "the cloud"; the customer secures "in the cloud."

A stronger thesis: **all data engineers should consider themselves security engineers**. The cloud pushes security responsibility out of the central security team and into the hands of every engineer who configures an S3 bucket. Failure to accept this responsibility produces the Leaky Buckets-style breaches that have filled the news for a decade.

See [[data-security]], [[least-privilege]].

## Principle 9: Embrace FinOps

**FinOps** is the cultural practice of bringing engineering, finance, and business together around data-driven cloud spending decisions (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md). See [[finops]].

The cost structure of data has fundamentally changed. On-prem meant a capital expenditure every few years and performance engineering against a fixed resource budget. Cloud means pay-as-you-go — systems charge per query, per processing second, per byte stored. This is more efficient on average, but **spending is dynamic** and requires active management.

FinOps implications for the architect:

- Monitor cost **as an operational signal** alongside latency and errors
- Build hard spending limits with graceful failure modes
- Defend against **cost attacks** — a malicious bulk download of an S3 bucket can bankrupt a small startup overnight; use requester-pays, monitor for anomalous spending
- Know the cost-performance curves of different options (spot instances, reserved capacity, pay-per-query)

FinOps is a young discipline — the FinOps Foundation was founded only in 2019. The principle says: start early, before the bill teaches you the hard way.

## How the principles compose

The principles lean on each other:

- Principle 6 (loose coupling) makes Principle 7 (reversibility) possible
- Principle 3 (scalability) interacts with Principle 9 (FinOps) — scale-to-zero is FinOps made operational
- Principle 2 (plan for failure) and Principle 8 (prioritise security) both assume a distributed world where [[fallacies-of-distributed-computing|the network is unreliable]] and adversaries are present
- Principle 4 (leadership) is what makes the other eight actually happen across an organisation
- Principles 1 and 5 together express the tension between standardisation and constant change

## Related pages

- [[data-architecture]]
- [[well-architected-framework]]
- [[cloud-native-principles]]
- [[reversible-vs-irreversible-decisions]]
- [[loose-coupling]]
- [[finops]]
- [[zero-trust-security]]
- [[shared-responsibility-model]]
- [[scalability]]
- [[elasticity]]
- [[reliability]]
- [[availability-measurement]]
- [[data-architect]]
- [[evolutionary-architecture]]
- [[trade-off-analysis]]
