# Column-Oriented Storage

**Summary**: Column-oriented storage keeps all values for each column together on disk rather than all values for each row. This dramatically reduces the data read for analytic queries that access only a few columns across millions of rows.

**Sources**: `raw/designing-data-intensive-applications/chapter-03-storage-and-retrieval.md`

**Last updated**: 2026-04-15

---

## The problem with row-oriented storage for analytics

In row-oriented storage, all columns of a row are stored contiguously. To answer an analytic query that reads 3 columns from a 100-column fact table, the database must load every row's full 100-column block into memory, then discard 97 columns — wasting almost all disk I/O.

[[Data-warehousing|Data warehouse]] queries typically access 4–5 columns from tables with hundreds. Row-oriented storage is the wrong layout.

## Column storage

Store all values of each column in a separate file, in the same row order across all column files. To reconstruct a row, take the Nth entry from each column file.

A query accessing 3 columns only reads and parses those 3 column files. Disk I/O is proportional to the number of columns accessed, not the total width of the table.

Parquet is a widely-used columnar storage format that supports document data models (based on Google's Dremel).

**Clarification on Cassandra/HBase "column families"**: These are often mischaracterized as column-oriented. Within each column family, all columns for a row are stored together — this is still row-oriented. The Bigtable model is mostly row-oriented.

## Column compression

Column values are often highly repetitive (e.g., a sales fact table might have billions of rows but only 100,000 distinct products). This repetition compresses extremely well.

**Bitmap encoding**: For a column with n distinct values, create n bitmaps — one per distinct value, one bit per row (1 if the row has that value, 0 otherwise). For low-cardinality columns, this is very compact.

**Run-length encoding**: If a sorted column has long runs of the same value, encode it as `(value, count)` pairs instead of storing every bit. Especially effective when the table is sorted by that column (see Sort Order below).

**Bitwise operations on bitmaps**: Bitmap encoding enables extremely fast query execution. For example:
- `WHERE product_sk IN (30, 68, 69)` → load three bitmaps, compute bitwise OR
- `WHERE product_sk = 31 AND store_sk = 3` → load two bitmaps, compute bitwise AND

These operations work because all column files preserve the same row order, so the kth bit in any column's bitmap corresponds to the same row.

## Vectorized processing

Compressed column data that fits in the CPU's L1 cache can be iterated in a tight loop with no function calls. The CPU executes such loops much faster than code requiring per-record branching. Operations like bitwise AND and OR can operate directly on chunks of compressed data.

This technique is called **vectorized processing**. It reduces not just disk I/O but also CPU cycles — an important bottleneck in analytical queries that scan millions of rows already cached in memory.

## Sort order in column storage

Rows don't need to be stored in insertion order. The database administrator can choose sort keys based on common query patterns:

- If queries often filter by date range, sort by `date_key` first. Only rows from the queried dates need to be scanned.
- A second sort key (e.g., `product_sk`) breaks ties and helps queries that group by product within a date range.

Sorting also improves compression: after sorting by the primary key, long runs of identical values appear, compressing extremely well with run-length encoding. Secondary and tertiary sort keys are more jumbled and compress less, but the first key alone provides a big win.

**Multiple sort orders**: C-Store (adopted commercially by Vertica) stores the same data sorted in several different ways on different replicas. Since data must be replicated for durability anyway, different replicas can be sorted for different query patterns. A query can use whichever sort order fits it best — similar in spirit to secondary indexes in row-oriented stores, but without heap-file pointers.

## Writing to column-oriented storage

Column storage's read optimizations make writes harder. An update-in-place approach (as B-trees use) is impossible for compressed columns: inserting a row in the middle of a sorted table would require rewriting every column file.

The solution: use [[sstables-and-lsm-trees|LSM-trees]]. All writes go to an in-memory store (row-oriented or column-oriented). When enough writes accumulate, they're merged with the on-disk column files and written to new files in bulk. This is what Vertica does. The query optimizer combines disk column data with recent in-memory writes transparently.

## Materialized views and OLAP cubes

Analytic queries frequently compute aggregates (COUNT, SUM, AVG, MIN, MAX) over large scans. When the same aggregations are needed repeatedly, it's wasteful to recompute them every time.

**Materialized view**: A precomputed query result stored on disk (unlike a virtual view, which is just a stored query definition). When underlying data changes, the materialized view must be updated — making writes more expensive. Used sparingly in OLTP, but common in read-heavy data warehouses.

**OLAP cube** (data cube): A common special case of a materialized view. A grid of aggregates across multiple dimensions. For example, with dimensions date and product: each cell contains the aggregate (e.g., total sales) for that date-product combination. Summing along a row gives total sales by product across all dates; summing along a column gives total sales by date across all products.

Real fact tables have many more dimensions (date, product, store, promotion, customer, ...). An OLAP cube precomputes all combinations.

**Advantage**: Some queries become instant lookups rather than scans.

**Disadvantage**: No flexibility beyond the precomputed dimensions. You can't answer "what proportion of sales came from items over $100?" unless price is one of the cube's dimensions. Most warehouses keep raw data and use cubes only as performance boosts for known query patterns.

## Column storage in batch processing

[[dataflow-engines]] like Spark and Impala take advantage of column-oriented storage during batch processing. When simple filtering and mapping operations are expressed declaratively (rather than as opaque callback functions), the query optimizer can read only the required columns from columnar formats like Parquet. Combined with vectorized execution — tight inner loops that are friendly to CPU caches — this allows batch processing engines to achieve performance comparable to MPP databases. Spark generates JVM bytecode and Impala uses LLVM to generate native code for these inner loops (source: designing-data-intensive-applications, chapter 10).

The structured file formats commonly used in the Hadoop ecosystem — Avro for row-oriented encoding and Parquet for columnar encoding — replace the ad hoc text parsing required by Unix tools, while supporting [[schema-evolution]] (source: designing-data-intensive-applications, chapter 10).

## Related pages

- [[storage-engines]]
- [[oltp-vs-olap]]
- [[data-warehousing]]
- [[sstables-and-lsm-trees]]
- [[indexes]]
- [[dataflow-engines]]
- [[batch-processing]]
- [[encoding-formats]]
