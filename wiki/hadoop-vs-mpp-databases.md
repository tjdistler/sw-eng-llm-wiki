# Hadoop vs MPP Databases

**Summary**: Hadoop (MapReduce + HDFS) and massively parallel processing (MPP) databases both run computations across clusters, but they differ fundamentally in philosophy: MPP databases are monolithic systems optimized for SQL analytics, while Hadoop is a general-purpose platform supporting diverse processing models and storage formats.

**Sources**: `raw/designing-data-intensive-applications/chapter-10-batch-processing.md`

**Last updated**: 2026-04-15

---

## Historical context

All the parallel join algorithms used by MapReduce (sort-merge, broadcast hash, partitioned hash) were implemented in MPP databases more than a decade earlier — Gamma database machine, Teradata, and Tandem NonStop SQL were pioneers. MapReduce was not algorithmically novel; its contribution was making distributed computation accessible on commodity hardware (source: designing-data-intensive-applications, chapter 10).

## Key differences

### Diversity of storage

**MPP databases** require data to be structured according to a particular model (relational or document) and imported into a proprietary storage format. This requires careful up-front modeling of data and query patterns (source: designing-data-intensive-applications, chapter 10).

**Hadoop/HDFS** stores arbitrary byte sequences — database records, text, images, videos, sensor readings, genome sequences. Data can be dumped first and structured later. This is the **"sushi principle": raw data is better** (source: designing-data-intensive-applications, chapter 10).

This approach is sometimes called a **data lake** or **enterprise data hub**. It shifts the burden of interpretation from the data producer to the consumer — a **schema-on-read** approach (see [[data-models]]). The careful schema design required by MPP databases slows down centralized data collection; Hadoop's schema-on-read speeds it up (source: designing-data-intensive-applications, chapter 10).

Hadoop has often been used for ETL: dump raw data from OLTP systems into HDFS, then clean and transform it with MapReduce jobs before loading into an MPP data warehouse for analytics. Data modeling still happens, but it is decoupled from data collection (source: designing-data-intensive-applications, chapter 10). See [[data-warehousing]].

### Diversity of processing models

**MPP databases** are monolithic — storage, query planning, scheduling, and execution are tightly integrated and optimized for SQL analytics. SQL is expressive and accessible to business analysts via tools like Tableau (source: designing-data-intensive-applications, chapter 10).

**Hadoop** supports multiple processing models on the same cluster and the same files (source: designing-data-intensive-applications, chapter 10):

- [[mapreduce]] for general batch processing
- SQL engines (Hive, Impala) for analytics
- Machine learning frameworks (Mahout)
- Full-text search index building
- Image analysis, NLP, statistical algorithms
- HBase for random-access OLTP
- [[dataflow-engines]] (Spark, Tez, Flink)

Not having to move data between specialized systems makes it much easier to derive value from data and to experiment with new processing approaches (source: designing-data-intensive-applications, chapter 10).

### Fault tolerance design

**MPP databases** abort the entire query on node failure and resubmit it. Queries typically run for seconds to minutes, so this is acceptable. They prefer keeping data in memory (e.g., hash joins) to avoid disk I/O (source: designing-data-intensive-applications, chapter 10).

**MapReduce** retries individual failed tasks without affecting the rest of the job. It eagerly writes data to disk for fault tolerance. This approach is appropriate for jobs that run for hours and are statistically likely to experience at least one failure (source: designing-data-intensive-applications, chapter 10).

MapReduce's design was motivated by Google's mixed-use datacenters, where batch jobs run at low priority and are frequently preempted by higher-priority production services. A one-hour task has roughly a 5% chance of preemption. In environments without preemption, MapReduce's design makes less sense — which is part of why [[dataflow-engines]] have gained favor (source: designing-data-intensive-applications, chapter 10).

## Convergence

The two approaches are converging (source: designing-data-intensive-applications, chapter 10):

- **Batch frameworks** are gaining declarative query languages, cost-based optimizers, and [[column-oriented-storage]] support (vectorized execution). Hive, Spark DataFrames, and Impala generate optimized native code for inner loops.
- **MPP databases** are becoming more programmable, supporting user-defined functions and non-SQL processing models.

In the end, both are systems for storing and processing data. The distinction is blurring (source: designing-data-intensive-applications, chapter 10).

## Related pages

- [[batch-processing]]
- [[mapreduce]]
- [[dataflow-engines]]
- [[distributed-filesystems]]
- [[data-warehousing]]
- [[column-oriented-storage]]
- [[declarative-vs-imperative-queries]]
- [[data-models]]
