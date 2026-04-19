# Elasticity

**Summary**: The ability of a scalable system to scale dynamically — automatically up and down — based on current workload. Distinct from raw [[scalability]]: scalability is whether the system **can** grow; elasticity is whether it grows **by itself**. Chapter 3 of *Fundamentals of Data Engineering* lists elasticity among the four characteristics of distributed data systems the data engineer must think about.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`

**Last updated**: 2026-04-18

---

## The four characteristics

Chapter 3 names four closely related characteristics of data systems (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- **[[scalability]]** — can the capacity grow?
- **Elasticity** — does it grow dynamically and automatically?
- **[[availability-measurement|Availability]]** — percentage of time in an operable state
- **[[reliability]]** — probability of meeting defined standards during a specified interval

Dynamic scaling improves reliability: elasticity ensures adequate performance without manual intervention, and performance failures under load lead to unavailability.

## Scale to zero

A property of some elastic systems: when idle, they can shut down entirely (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md). Serverless functions and serverless OLAP databases are the canonical examples. Scale-to-zero is where elasticity meets [[finops]] — cost goes to zero while capacity is not needed, then scales with demand.

## Warning: inappropriate scaling costs money

Chapter 3 warns that deploying elaborate scaling machinery where it isn't warranted produces **overcomplicated systems and high costs** (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md). A single relational database with a failover node is often the right answer for an application. Measure current load, approximate load spikes, and estimate near-term growth — then decide.

## Cross-book framing

- Kleppmann's treatment of [[scalability]] and [[load-parameters]] is the theoretical foundation
- Burns's [[dynamic-worker-scaling]] is elasticity implemented at the batch-worker layer
- [[cold-start-warm-start]] (Burns, FaaS) names the latency tax elasticity imposes at scale-to-zero boundaries
- [[capacity-planning]] and [[intent-based-capacity-planning]] (SRE) are the Google operational counterparts

## Related pages

- [[scalability]]
- [[reliability]]
- [[availability-measurement]]
- [[principles-of-good-data-architecture]]
- [[finops]]
- [[dynamic-worker-scaling]]
- [[cold-start-warm-start]]
- [[data-architecture]]
