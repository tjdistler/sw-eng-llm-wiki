# Cloud-Native Database

**Summary**: Databases designed for and usually delivered only via a specific cloud platform, built on decoupled compute-and-storage architectures that wouldn't be practical on-prem. Examples include Snowflake, Amazon Redshift, Google BigQuery, Azure Cosmos DB, and Datomic.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md`

**Last updated**: 2026-04-19

---

## The positioning

Cloud-native databases are engineered to take advantage of the elastic, pay-as-you-go nature of cloud infrastructure. Their design assumes:

- **Separation of compute and storage.** Data lives in object storage (S3, GCS, Azure Blob); compute is spun up, paid for, and spun down per query.
- **Elastic scaling.** More compute arrives when needed, not via hardware procurement.
- **Managed operations.** No DBA installs or patches the engine; the cloud operator does.
- **Pay-per-use economics.** Cost scales with workload rather than provisioned capacity.

Chapter 6 of *Software Architecture: The Hard Parts* groups Snowflake, Amazon Redshift, Azure Cosmos DB, and Datomic into this family (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md). The family is heterogeneous — Snowflake and Redshift are warehouse-like, Cosmos DB is a multi-model OLTP store, and Datomic is a totally different paradigm (immutable facts, EAVT indexes). The unifying property is "cloud-only delivery model," not a shared data model.

## Characteristics (Hard Parts ratings)

The book's star ratings are the most *variable* of any family — different products within the group score very differently:

- **Learning curve — varies.** Redshift feels like an RDBMS (familiar). Snowflake has familiar SQL but unusual storage/compute separation (some practice). Datomic uses immutable atomic facts and Clojure-heavy APIs (steep learning curve).
- **Data modelling — varies.** Redshift and Snowflake: relational, with data-warehouse-shaped designs. Datomic: no tables, no predefined attributes — entities can have any attribute; individual attribute properties are defined instead.
- **Scalability / throughput — very high.** Cloud-native means scaling is a configuration change (and a bill). The trade-off is dollars, not capacity planning.
- **Availability / partition tolerance — very high.** Snowflake replicates across regions; Cosmos DB offers multi-region writes; Datomic Production Topology has no single point of failure. Redshift is cluster-in-one-AZ by default and needs explicit multi-cluster setup for HA.
- **Consistency — varies.** Redshift and Snowflake: ACID transactions. Datomic: ACID via immutable-fact storage. Cosmos DB: tunable consistency levels (five of them).
- **Community — often immature.** These databases are newer and cloud-specific; the user community is smaller than relational/document stores and finding experienced help is harder. Clojure-specific needs (Datomic) narrow the talent pool further.
- **Read/write priority — varies.** Snowflake/Redshift lean toward read-heavy analytical workloads; Datomic and Cosmos DB handle both.

## The cost shape

The pay-per-use model is the most consequential non-technical property. Costs are (often) per-query-second on compute, per-GB-month on storage, per-GB on egress, and per-API-call on some engines. The same workload can cost dramatically more or less depending on how it's shaped:

- **Full scans on document-like cloud stores** can be expensive enough that the book flags them explicitly in the [[document-model]] source-system section — full-scan extraction "can charge a significant fee for each full scan."
- **Compute autoscaling** means a runaway query can rack up a real bill before the guard-rails kick in.
- **Long-running idle compute** on the warehouse models is effectively free compared to provisioned clusters — you pay when queries run.

[[finops|FinOps]] practices exist to make these cost shapes visible and governable.

## When to pick a cloud-native database

The book's Chapter 6 rationale (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md):

- You're already committed to the cloud vendor and want managed operations.
- Your workload is intrinsically bursty (occasional big analytics queries; experimental workloads; variable-load apps).
- You want to experiment without up-front infrastructure investment.
- The specific engine solves your problem better than any non-cloud-native alternative (Snowflake's concurrency model for analytics; Cosmos DB's global distribution).

## Trade-offs

- **Lock-in.** Most cloud-native databases run only on one cloud.
- **Migration cost.** Getting data out can be as painful as getting data in was easy.
- **Community depth.** Smaller than established databases; fewer Stack Overflow answers, fewer blog posts, fewer experienced hires.
- **Opaque internals.** You can't profile the engine, only the SQL.

## Related pages

- [[database-type-selection]]
- [[cloud]]
- [[cloud-native-principles]]
- [[finops]]
- [[relational-model]]
- [[nosql]]
- [[acid]]
- [[newsql-database]]
- [[software-architecture-the-hard-parts]]
