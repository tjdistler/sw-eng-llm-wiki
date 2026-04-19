# Monolith vs Modular (Data Systems)

**Summary**: Chapter 4's framing of the long-running architectural debate for **data** stacks. **Monolithic** data systems are self-contained and simple to reason about. **Modular** stacks compose decoupled best-of-breed tools via open formats and APIs. Reis and Housley come down firmly on the modular side for today's data world, while acknowledging monoliths are still a valid choice in specific cases.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## The tension

Chapter 4 frames the classic architectural debate specifically for data stacks (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- **Monolithic systems** are self-contained, often performing multiple functions under one system. "Simplicity of having everything in one place. It's easier to reason about a single entity, and you can move faster because there are fewer moving parts."
- **Modular systems** lean toward **decoupled, best-of-breed technologies** performing tasks at which they're uniquely great. Interoperability among an ever-changing array of solutions.

## Monolithic data systems

Examples Chapter 4 cites: Informatica (older commercial), **Apache Spark** (OSS framework) (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md).

### Pros

- Easy to reason about.
- Lower cognitive burden and context-switching.
- One technology, one principal programming language.
- Simpler developer workflow and debugging.

### Cons

- **Brittle.** Vast number of moving parts means updates and releases take longer and "bake in the kitchen sink." A bug can harm the entire system.
- **User-induced problems.** Chapter 4's example: a 48-hour monolithic ETL pipeline where any failure anywhere restarts the whole thing. Breakages became common enough that the system was eventually thrown out.
- **[[multitenancy-in-streaming-clusters|Multitenancy is hard]].** Hard to isolate workloads — one user's UDF consumes enough CPU to slow everyone else. Dependency and resource conflicts are chronic.
- **High switching cost** if the vendor or project dies. All processes are entangled; extraction is expensive.

## Modular data systems

Chapter 4 (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Modularity is an old concept in software engineering, but modular distributed systems truly came into vogue with the rise of microservices.

Modern data systems increasingly lean modular via:

- **Open storage formats** — data in object storage as **Parquet** (lakes, lakehouses). Any tool that supports the format can read/write.
- **External tables and import/export** — cloud data warehouses can query data in lakes directly.
- **API-mediated services** — microservice principles applied at the data-platform layer.

Reis and Housley's view (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> We view data modularity as a more powerful paradigm than monolithic data engineering. Modularity allows engineers to choose the best technology for each job or step along the pipeline.

### Cons of modularity

- **More systems to understand and operate.**
- **[[interoperability|Interoperability]] becomes a potential headache** — hopefully these systems all play nicely together. This is exactly why Chapter 4 breaks [[orchestration]] out as its own undercurrent: orchestrating five or ten tools is dramatically more complex than one.

## The [[distributed-monolith|distributed monolith]] pattern

Chapter 4 warns of an anti-pattern between the two (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md): distributed services that share a **common codebase or dependency set**. A traditional Hadoop cluster is the exemplar — Hive, Pig, Spark all coexist but all share Hadoop common libraries, HDFS, YARN, Java versions. You pay distribution costs without gaining independence.

Some Python-based orchestration tools have the same problem: decoupled execution but a single dependency set where every client library for any task must be installed cluster-wide.

**Two mitigations Chapter 4 names:**

1. **Ephemeral infrastructure.** Each job runs on a temporary cluster installed with its own dependencies. Amazon EMR, Google Cloud Dataproc do this for Spark.
2. **[[containers|Containers]].** Properly decompose the distributed monolith into multiple software environments using containerisation. See [[serverless-vs-servers]].

See [[distributed-monolith]] for the full anti-pattern.

## Chapter 4's advice

Things to weigh when evaluating monolith vs modular (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- **[[interoperability|Interoperability]]** — architect for sharing and interoperability.
- **Avoiding the "bear trap"** — something easy to get into might be impossible to escape.
- **Flexibility** — committing to a monolith reduces flexibility and reversibility, and the data space is moving fast.

The verdict: default to modular; use a monolith when the simplicity it offers is a clear win and you're confident the scope will stay bounded.

## Cross-book framing

- [[monolith]], [[modular-monolith]], [[microservices]] (Newman) — the equivalent debate for application services.
- [[monolithic-vs-distributed]] (Richards and Ford) — the top-level architecture-style split.
- [[loose-coupling]] (Principle 6) and the Bezos API Mandate — the organisational root of modularity.
- [[unbundling-databases]] (Kleppmann) — why modern data platforms tend to dis-aggregate storage, compute, and query.

## Related pages

- [[distributed-monolith]]
- [[monolith]]
- [[microservices]]
- [[interoperability]]
- [[orchestration]]
- [[loose-coupling]]
- [[modern-data-stack]]
- [[containers]]
- [[serverless-vs-servers]]
- [[technology-selection]]
- [[principles-of-good-data-architecture]]
