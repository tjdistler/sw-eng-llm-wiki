# Batch Workflow Outputs

**Summary**: The output of a batch processing workflow is typically not a report but a derived data structure — search indexes, precomputed key-value databases, or input to further batch jobs — built following the philosophy of immutable inputs and replaceable outputs.

**Sources**: `raw/designing-data-intensive-applications/chapter-10-batch-processing.md`, `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`

**Last updated**: 2026-04-15

---

## Search indexes

Google's original use of MapReduce was building indexes for its search engine — a workflow of 5–10 MapReduce jobs. Hadoop MapReduce remains a good way to build Lucene/Solr indexes (source: designing-data-intensive-applications, chapter 10).

The approach: mappers partition the document set, each reducer builds the index for its partition, and index files are written to the [[distributed-filesystems|distributed filesystem]]. This parallelizes very well as a document-partitioned index (see [[partitioning]]) (source: designing-data-intensive-applications, chapter 10).

Index files are **immutable** once created. If the document set changes, you can either:
- **Full rebuild**: Rerun the entire indexing workflow and replace old indexes wholesale.
- **Incremental**: Build new index segments and merge/compact in the background (as [[sstables-and-lsm-trees|LSM-trees]] do).

## Key-value stores

Batch jobs commonly build databases for serving systems — recommendation databases (suggested friends, related products), machine learning classifiers (spam filters, anomaly detection), and precomputed query results (source: designing-data-intensive-applications, chapter 10).

### Why not write directly to a database?

Writing from a batch job directly to a database server is a bad idea for several reasons (source: designing-data-intensive-applications, chapter 10):

- **Performance**: Network round-trips per record are orders of magnitude slower than batch throughput.
- **Overload**: All mappers/reducers writing concurrently can overwhelm the database and degrade its query performance.
- **Broken guarantees**: MapReduce provides all-or-nothing output guarantees (the result of running every task exactly once). Writing to an external database introduces visible side effects from partially completed or speculatively executed tasks.

### The better approach: build database files in the batch job

Build a brand-new read-only database as files in the job's output directory on [[distributed-filesystems|HDFS]]. These files are then bulk-loaded into serving systems. Tools that support this include Voldemort, Terrapin, ElephantDB, and HBase bulk loading (source: designing-data-intensive-applications, chapter 10).

Since these key-value stores are **read-only** (immutable files written once by the batch job), the data structures are simple — no write-ahead log needed (unlike [[storage-engines]] that handle concurrent writes) (source: designing-data-intensive-applications, chapter 10).

**Atomic switchover**: When loading data into Voldemort, the server continues serving from old files while new files are copied from HDFS to local disk. Once copying completes, the server atomically switches to the new files. If anything goes wrong, it switches back to the old (still-intact) files (source: designing-data-intensive-applications, chapter 10).

## Philosophy

This follows the [[unix-philosophy]] of batch processing (source: designing-data-intensive-applications, chapter 10):

- Inputs are immutable — rerun the job without corrupting state.
- Previous output is completely replaced — no partial mutations.
- No externally visible side effects during processing.
- Failed tasks are automatically retried because their partial output is discarded.
- The same input files can feed multiple jobs (monitoring, validation, different analyses).
- Logic is separated from wiring — teams implement jobs that do one thing well; other teams decide when and where to run them.

This enables **human fault tolerance**: if buggy code produces wrong output, roll back and rerun. Feature development proceeds more quickly when mistakes are reversible (source: designing-data-intensive-applications, chapter 10).

## Write path and read path

Chapter 12 generalizes the batch output concept into a model of **write path** (eager precomputation) and **read path** (lazy on-demand computation). Batch and stream outputs are the write path: they precompute [[derived-data|derived datasets]] (search indexes, caches, ML models) as data arrives. The read path happens when a user queries the derived dataset. Indexes, caches, and materialized views shift work from the read path to the write path. The derived dataset is where the two meet (source: chapter-12-the-future-of-data-systems.md).

See [[derived-data]] for the full treatment of this concept.

## Related pages

- [[batch-processing]]
- [[mapreduce]]
- [[distributed-filesystems]]
- [[unix-philosophy]]
- [[storage-engines]]
- [[indexes]]
- [[sstables-and-lsm-trees]]
- [[derived-data]]
- [[stream-processing]]
