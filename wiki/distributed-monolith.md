# Distributed Monolith

**Summary**: A distributed architecture that still suffers from the limitations of a monolith — multiple services, but with shared dependencies or a common codebase that forces them to evolve together. Chapter 4 of *Fundamentals of Data Engineering* names Hadoop clusters and some Python orchestration frameworks as canonical data-world examples.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`, `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`, `raw/software-architecture-the-hard-parts/chapter-01-what-happens-when-there-are-no-best-practices.md`

**Last updated**: 2026-04-19

---

## The pattern (Chapter 4's framing)

Chapter 4's data-engineering description (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> The distributed monolith pattern is a distributed architecture that still suffers from many of the limitations of monolithic architecture. The basic idea is that one runs a distributed system with different services to perform different tasks. Still, services and nodes share a common set of dependencies or a common codebase.

## Canonical examples

### Traditional Hadoop cluster

Can simultaneously host Hive, Pig, Spark — all as separate frameworks — but shares (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- Hadoop common libraries
- HDFS
- YARN
- Java

In practice a cluster runs one version of each component. Managing a common environment that works for all users and all jobs is hard. Upgrades risk breaking jobs; maintaining two versions of a framework adds complexity.

### Some Python-based orchestration

> Some modern Python-based orchestration technologies also suffer from this problem. While they utilize a highly decoupled and asynchronous architecture, every service runs the same codebase with the same dependencies. Any executor can execute any task, so a client library for a single task run in one DAG must be installed on the whole cluster. (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md)

Orchestrating many tools means installing client libraries for many APIs. **Dependency conflicts are a constant problem.**

## Mitigations Chapter 4 names

1. **Ephemeral infrastructure.** Each job gets its own temporary server or cluster installed only with its dependencies. Amazon EMR, Google Cloud Dataproc for Spark. Each cluster is still monolithic, but separating jobs dramatically reduces conflicts.
2. **[[containers|Containers]].** Properly decompose the distributed monolith into multiple software environments using containers — see [[serverless-vs-servers]].

## Newman's original framing

Newman (Chapter 1 of *Monolith to Microservices*) identified the same pattern in application services (source: raw/monolith-to-microservices/chapter-01-just-enough-microservices.md):

> A distributed monolith has all the disadvantages of a distributed system, and the disadvantages of a single-process monolith, without enough upsides of either.

The root cause in Newman's account is lack of [[information-hiding]] and [[cohesion]] — services are built but remain so tightly coupled that any change ripples across boundaries. See [[monolith]] for the full three-way split Newman uses (single-process, distributed, third-party black-box).

## Why the pattern matters for data engineering

Chapter 4's treatment adds the data-specific angle: the distributed monolith is especially common in data because data frameworks historically shipped as large dependency graphs (Hadoop) or single-runtime environments (Python with one interpreter/dependency set). The modern mitigations — ephemeral clusters, containers, isolated runtimes — are what make the [[monolith-vs-modular-data|modular]] data stack actually achievable.

## The Sysops Squad pathology (*Hard Parts* Ch 1)

Ford, Richards, Sadalage, and Dehghani open *Software Architecture: The Hard Parts* with a fictional brownfield case — *Penultimate Electronics'* Sysops Squad ticketing application — that exhibits the full distributed-monolith symptom pattern (source: raw/software-architecture-the-hard-parts/chapter-01-what-happens-when-there-are-no-best-practices.md):

- **Lost and misrouted tickets** — the ticket-assignment component can't reliably pick the right expert, and tickets are dropped altogether when the system "freezes up."
- **Availability failures** — the system frequently crashes for 5 minutes to 2 hours at a time; the whole application goes dark because there is no real isolation between components.
- **Change risk** — every change ships the whole monolith; something unrelated to the change typically breaks in production.
- **Scalability pressure** — the customer-facing ticket-entry flow cannot be scaled independently of the administrative or reporting components.

Despite being called "the monolithic system" in the book, the application is structurally distributed in several senses — multiple component namespaces (ticket, customer, expert, billing, survey, reporting), a shared schema, cross-component views and stored procedures — that make it rhyme with the distributed-monolith pathology as experienced in production. The book uses it to motivate the decomposition exercises in the rest of Part I: this is the system the authors walk through pulling apart.

The Sysops Squad saga itself is pedagogical context, not a concept; it recurs throughout the book as the running worked example for migration, decomposition, saga coordination, and data-ownership decisions.

## Cross-book framing

- [[monolith]] — Newman's three monolith types, including the distributed variant.
- [[microservices]] — the "proper" distributed alternative.
- [[monolith-vs-modular-data]] — Chapter 4's top-level debate.
- [[containers]], [[serverless-vs-servers]] — the concrete escape routes.
- [[orchestration]] — the undercurrent that makes modular data stacks operable.

## Related pages

- [[monolith]]
- [[monolith-vs-modular-data]]
- [[microservices]]
- [[containers]]
- [[serverless-vs-servers]]
- [[orchestration]]
- [[information-hiding]]
- [[cohesion]]
- [[coupling]]
- [[software-architecture-the-hard-parts]]
- [[brownfield-vs-greenfield]]
