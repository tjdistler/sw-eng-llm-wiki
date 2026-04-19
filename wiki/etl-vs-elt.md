# ETL vs ELT

**Summary**: Two data-integration patterns that differ in when transformation happens relative to loading into the destination. **ETL** — extract, transform, then load — transforms data *before* it reaches the warehouse. **ELT** — extract, load, then transform — loads raw data first and transforms inside the warehouse. ELT has risen with cloud warehouses where storage is cheap and the query engine is powerful enough to transform at scale.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-07-ingestion.md`

**Last updated**: 2026-04-18

---

## ETL

Chapter 2's brief description: in traditional batch-oriented ingestion, **"ETL's extract (E) part clarifies that we're dealing with a pull ingestion model. In traditional ETL, the ingestion system queries a current source table snapshot on a fixed schedule"** (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

The sequence:

1. **Extract** from the source system (usually via pull).
2. **Transform** into the warehouse's target schema, outside the warehouse.
3. **Load** the transformed result into the warehouse.

See [[data-warehousing]] for the classic ETL flow into a star/snowflake schema.

## ELT

Chapter 2 only mentions ELT in passing ("extract, load, transform"), but the pattern it names is the modern default with cloud data warehouses: **load raw data first, transform inside the warehouse with SQL**.

The sequence:

1. **Extract** from the source system.
2. **Load** raw data into the warehouse or [[data-lake|lake]] / [[data-lakehouse|lakehouse]].
3. **Transform** inside the warehouse/lake using the query engine (e.g., dbt on BigQuery/Snowflake/Redshift).

Tools like **Fivetran, Airbyte, Singer** (named elsewhere in Chapter 2) handle extract-and-load, leaving transform to the warehouse-native stack.

## Why ELT won for cloud warehouses

Several forces (implicit in Chapter 2's broader framing about the rising capability of cloud warehouses) push toward ELT:

- **Storage is cheap.** Keeping raw extracts costs little.
- **Warehouse compute is scalable and on-demand.** Transforms that once needed a dedicated ETL cluster can now run as SQL inside the warehouse.
- **Schema-on-read flexibility.** Keeping raw data means later analysts can re-derive differently without re-extracting.

See [[hadoop-vs-mpp-databases]] for the earlier "Hadoop as ETL staging + MPP warehouse as target" pattern that prefigured ELT.

## Trade-offs

| | ETL | ELT |
|---|---|---|
| Transform location | External process | Inside warehouse |
| Raw data retained? | Usually not | Yes — enables re-derivation |
| Compute cost model | Dedicated ETL infra | Warehouse consumption |
| Schema coupling at load time | Tight | Loose (can transform later) |
| Suited for | On-prem / appliance warehouses | Cloud warehouses |

## Ch 7 framing — ETL/ELT as the E and L of ingestion

Chapter 7 of *Fundamentals of Data Engineering* treats the **extract (E)** and **load (L)** specifically as parts of the ingestion stage; the **transform (T)** is reserved for Chapter 8 (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

### Extract

"Means getting data from a source system. While extract seems to imply pulling data, it can also be push based." Extraction "may also require reading metadata and schema changes" — the schema is first-class ingestion concern, not a downstream-transform concern. See [[push-vs-pull-vs-poll]] and [[ingestion-payload]] for the metadata/schema dimension.

### Load

"Once data is extracted, it can either be transformed (ETL) before loading it into a storage destination or simply loaded into storage for future transformation." Ch 7's three load-time awarenesses (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- **Type of destination system.** What does it accept? Columnar formats into a columnar DB? JSON into a document store?
- **Schema of the data.** Does it match or need mapping?
- **Performance impact of loading.** Will the load spike contention on the destination?

### Inserts, updates, and batch size

Ch 7 devotes a section specifically to how load operations interact with destination behaviour (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- Batch-oriented systems perform badly on many small writes. Columnar databases create many small suboptimal files; in-place updates force scans of whole column files.
- Purpose-built tools matter: Apache Druid and Apache Pinot handle high insert rates; SingleStore manages hybrid OLAP+OLTP; BigQuery performs poorly on row-by-row inserts but extremely well via its streaming buffer.
- The lesson: "Know the limits and characteristics of your tools" — batch size and insert pattern must match the destination's physics.

## Cross-book connections

- [[data-warehousing]] (DDIA) gives the classic ETL flow.
- [[hadoop-vs-mpp-databases]] (DDIA) — the data-lake/enterprise-data-hub pattern is the conceptual ancestor of ELT: schema-on-read, producer writes raw, consumer decides interpretation.
- [[change-data-capture]] — the extract mechanism increasingly used in both patterns for low-latency extract.

## Related pages

- [[data-ingestion]]
- [[data-transformation]]
- [[data-warehousing]]
- [[data-lake]]
- [[data-lakehouse]]
- [[hadoop-vs-mpp-databases]]
- [[change-data-capture]]
- [[reverse-etl]]
- [[push-vs-pull-vs-poll]]
- [[ingestion-payload]]
- [[managed-connector]]
- [[file-based-ingestion]]
