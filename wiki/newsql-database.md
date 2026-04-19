# NewSQL Database

**Summary**: A family of databases that aim to combine the **scalability of [[nosql|NoSQL]]** with the **SQL and [[acid|ACID]] guarantees of a [[relational-model|relational database]]**. Coined by Matthew Aslett; the practical distinction from a classic RDBMS is **multiple active nodes** (horizontal scaling) while preserving transactional semantics.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md`

**Last updated**: 2026-04-19

---

## The positioning

Relational databases give strong consistency and SQL but scale vertically and rely on a single leader with passive followers. NoSQL stores scale horizontally but sacrifice ACID or SQL (or both). NewSQL picks a third way: **keep SQL, keep ACID, but also scale horizontally** by automating data partitioning / sharding across multiple active nodes (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md).

Common products: CockroachDB, VoltDB, TiDB, YugabyteDB, Google Spanner, NuoDB. Some (Spanner) are managed services; others (CockroachDB, TiDB) can run on-prem or in a cloud.

## Characteristics (Hard Parts ratings)

From Chapter 6's rating matrix (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md):

- **Learning curve — high.** Developers familiar with SQL and ACID pick it up quickly. Sharding design adds a new dimension.
- **Data modelling — familiar.** Relational-like; extra consideration for sharding key placement.
- **Scalability / throughput — high.** Multiple active nodes (the key differentiator from an RDBMS) mean horizontal scale.
- **Availability / partition tolerance — high.** Active-active topology tolerates node, disk, and even data-centre failure (CockroachDB's billing).
- **Consistency — strong.** ACID transactions, often with serialisable isolation. This is the headline feature vs NoSQL.
- **Community — growing.** Smaller than the RDBMS or document-store communities; many products are open source, some offer wire-compatible protocols for easy drop-in replacement (e.g., CockroachDB's PostgreSQL-compatible wire protocol).
- **Read/write priority — balanced.** Used similarly to an RDBMS with added geo-distribution for either read or write performance.

## Mechanics

The distinguishing trick is **transparent automated sharding** plus a distributed transaction protocol that keeps ACID across shards. Implementations vary:

- **Raft/Paxos-based consensus** over shard replicas (CockroachDB uses Raft per range).
- **TrueTime / hybrid logical clocks** for externally consistent ordering (Spanner uses GPS-and-atomic-clock-synchronised TrueTime; most others use HLC).
- **Automatic rebalancing** of shards as load or capacity changes.

Developers mostly see a single SQL endpoint — the complexity is below the surface.

## When to pick NewSQL

The book's Chapter 6 rationale (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md):

- You need ACID across a large dataset and can't fit it on one relational leader.
- You need multi-region active-active availability.
- You want SQL (for reporting, for developer familiarity, for tooling) but need NoSQL-scale writes.
- You want to replace an existing RDBMS without rewriting application code — wire-compatible NewSQL engines (CockroachDB vs PostgreSQL, YugabyteDB vs PostgreSQL) make the migration cheaper.

## Trade-offs

- **Latency tax for strong consistency.** A cross-region serialisable commit has a built-in round-trip cost. Ideal for high-value transactions, wasteful for high-volume low-value writes.
- **Operational maturity still catching up.** Most NewSQL products are a decade newer than mature RDBMS engines; community, tooling, and corner-case behaviour are less battle-tested.
- **Cost.** Multi-node active-active deployments cost more than a single RDBMS node.

## Where NewSQL sits in the family tree

In the [[database-type-selection]] matrix it occupies the "can scale horizontally AND be ACID" cell that used to be empty. It's not a replacement for [[relational-model|relational]] (most apps will keep using one); it's a choice for data domains whose scale exceeds an RDBMS's comfort zone but whose consistency needs exceed NoSQL's.

## Related pages

- [[database-type-selection]]
- [[relational-model]]
- [[nosql]]
- [[acid]]
- [[partitioning]]
- [[cap-theorem]]
- [[cloud-native-database]]
- [[database-decomposition]]
- [[software-architecture-the-hard-parts]]
