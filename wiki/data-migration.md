# Data Migration

**Summary**: Moving large volumes of data between databases, environments, or clouds — typically a one-time bulk operation, not an ongoing pipeline. Ch 7 of FoDE treats data migration as a special case of batch [[data-ingestion|ingestion]] with its own distinct considerations: hundreds-of-terabytes-or-more scale, schema subtleties between source and target systems, and the often-overlooked fact that moving the **pipeline connections** is harder than moving the data itself.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-07-ingestion.md`

**Last updated**: 2026-04-18

---

## When migration happens

Reis and Housley: "Migrating data to a new database or environment is not usually trivial, and data needs to be moved in bulk. Sometimes this means moving data sizes that are hundreds of terabytes or much larger, often involving the migration of specific tables and moving entire databases and systems" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

Typical triggers:

- Swapping database engines (e.g., SQL Server → Snowflake, Oracle → Postgres).
- Cloud transitions: on-prem → cloud, cloud → cloud.
- Consolidating multiple warehouses into one.
- Sunset of a legacy analytical system.

"Data migrations probably aren't a regular occurrence as a data engineer, but you should be familiar with them" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

## Key considerations

### Schema management

"No matter how closely the two databases resemble each other, subtle differences almost always exist in the way they handle schema." Migrations from SQL Server to Snowflake, for instance, are never one-to-one — data types, default-value semantics, case-sensitivity rules, and collation behaviours all vary (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

Mitigation: "it is generally easy to test ingestion of a sample of data and find schema issues before undertaking a complete table migration." Run a small sample first; surface the schema surprises before you're committed to the full load. See [[schema-evolution]] for the ongoing version of the problem.

### Move in bulk

"Most data systems perform best when data is moved in bulk rather than as individual rows or events. File or object storage is often an excellent intermediate stage for transferring data" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

The usual shape: source exports to [[object-storage]] as Parquet/Avro/CSV files; target ingests from object storage. This avoids the per-row overhead of JDBC/ODBC and lets both endpoints parallelize their sides of the move. See [[file-based-ingestion]].

### The pipeline-migration problem

"One of the biggest challenges of database migration is not the movement of the data itself but the movement of data pipeline connections from the old system to the new one" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

Every pipeline that reads from, writes to, or transforms data in the old system has to be cut over. Pipeline connections are scattered across orchestrators, dbt projects, BI tools, custom scripts, reverse-ETL jobs — and every one of them has its own test, deploy, and validation story. This is often where migrations actually fail or drag on.

### Use the right tools

"Many tools are available to automate various types of data migrations. Especially for large and complex migrations, we suggest looking at these options before doing this manually or writing your own migration solution" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

This parallels the broader FoDE advice: don't reinvent the data-ingestion wheel. See [[managed-connector]].

## For very large volumes: transfer appliances

Beyond roughly 100 TB, sending data over the internet becomes impractical; cloud vendors offer **physical transfer appliances** — devices that are shipped out, loaded with data, and shipped back to be uploaded into cloud storage. This is the standard approach for genuinely massive migrations and for multicloud moves where egress fees make wire transfers cost-prohibitive. See [[transfer-appliance]].

## Cross-book connections

- **[[change-data-capture]]** (DDIA, Newman) — once the initial bulk migration is done, CDC is the standard mechanism for catching up changes that occurred *during* the bulk copy (Newman's [[synchronize-data-in-application]] pattern does exactly this). Ongoing CDC can also be the "durable migration" pattern — moving data continuously until cutover.
- **[[legacy-modernization]]** / **[[strangler-fig-pattern]]** (Newman) — the analogous idea for application migration; the strangler pattern is how pipeline connections can be cut over incrementally rather than in a big-bang.
- **[[database-decomposition]]** (Newman) — the same engineering problems at a finer granularity, during monolith-to-microservices splits.

## Related pages

- [[data-ingestion]]
- [[snapshot-vs-differential-ingestion]]
- [[file-based-ingestion]]
- [[transfer-appliance]]
- [[managed-connector]]
- [[object-storage]]
- [[schema-evolution]]
- [[change-data-capture]]
- [[synchronize-data-in-application]]
- [[strangler-fig-pattern]]
