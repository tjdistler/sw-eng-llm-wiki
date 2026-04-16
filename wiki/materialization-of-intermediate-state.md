# Materialization of Intermediate State

**Summary**: Materialization means eagerly computing and writing out the result of an operation, rather than streaming it to the next stage. MapReduce fully materializes intermediate state to HDFS between jobs, which enables fault tolerance but causes significant performance overhead.

**Sources**: `raw/designing-data-intensive-applications/chapter-10-batch-processing.md`

**Last updated**: 2026-04-15

---

## What materialization means

To **materialize** is to eagerly compute a result and write it out (to disk or distributed filesystem), rather than computing it on demand or streaming it incrementally. The term also appears in the context of materialized views in databases (see [[column-oriented-storage]]) (source: designing-data-intensive-applications, chapter 10).

In [[mapreduce]], each job writes its complete output to [[distributed-filesystems|HDFS]] before any downstream job can begin. When the output of one job is only used as input to the next job (not published for broader use), these files are **intermediate state** — temporary data passing between stages of a workflow (source: designing-data-intensive-applications, chapter 10).

## The problem with full materialization

Compared to Unix pipes, which stream data incrementally between processes, MapReduce's full materialization has three downsides (source: designing-data-intensive-applications, chapter 10):

1. **No pipelining**: A downstream job cannot start until all tasks in the upstream job complete. Straggler tasks in the upstream job delay the entire workflow.
2. **Redundant mappers**: Mappers in the downstream job often just read back what the upstream reducer wrote and re-partition it. This work could have been folded into the upstream reducer.
3. **Unnecessary replication**: Writing intermediate files to HDFS means replicating them across multiple nodes — overkill for temporary data that will be discarded after the next job reads it.

## Unix pipes: the alternative model

Unix pipes do **not** materialize intermediate state. The output of one process streams directly into the input of the next through a small in-memory buffer. Both processes run concurrently. This is the model that [[dataflow-engines]] approximate (source: designing-data-intensive-applications, chapter 10).

## How dataflow engines improve on this

[[dataflow-engines|Spark, Tez, and Flink]] treat an entire workflow as one job and keep intermediate state in memory or on local disk rather than HDFS. Operators can begin executing as soon as their input is available, enabling pipelined execution (source: designing-data-intensive-applications, chapter 10).

Flink is especially built around pipelined execution — incrementally passing output between operators without waiting for complete input. However, any operation that requires sorting must still accumulate its full input before producing output (source: designing-data-intensive-applications, chapter 10).

## The tradeoff: fault tolerance

Full materialization has one major advantage: **durability**. If a MapReduce task fails, it can restart on another machine and re-read its input from HDFS. Dataflow engines that skip materialization must **recompute** lost intermediate state from earlier stages or from the original HDFS input, which requires tracking data lineage (source: designing-data-intensive-applications, chapter 10).

## When materialization is still appropriate

- The output is intended for broad consumption (published dataset, not just intermediate state).
- The intermediate data is much smaller than the source data (cheaper to write than to recompute).
- The computation is very CPU-intensive (recomputation would be expensive).
- Final inputs and outputs of a workflow are still typically materialized to HDFS, even with dataflow engines.

(source: designing-data-intensive-applications, chapter 10)

## Related pages

- [[mapreduce]]
- [[dataflow-engines]]
- [[batch-processing]]
- [[distributed-filesystems]]
- [[unix-philosophy]]
