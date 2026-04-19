# MapReduce

**Summary**: MapReduce is a programming framework for processing large datasets across a distributed cluster. It provides a simple abstraction — write a mapper and a reducer — while the framework handles partitioning, sorting, data movement, and fault tolerance. Reis & Housley call it "the defining batch data transformation pattern of the big data era" — the ancestor to every modern distributed processing framework, even though data engineers rarely write raw MapReduce today.

**Sources**: `raw/designing-data-intensive-applications/chapter-10-batch-processing.md`, `raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md`, `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`, `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## How it works

A MapReduce job has four steps (source: designing-data-intensive-applications, chapter 10):

1. **Break input into records** — Handled by the input format parser. In HDFS, each file block is a separate partition assigned to a map task.
2. **Map** — Call the mapper function on each record. It extracts a key-value pair from the input. Each record is handled independently (no state carried between records).
3. **Sort** — The framework sorts all key-value pairs by key. This is implicit — you don't write it.
4. **Reduce** — Call the reducer with all values for a given key. The reducer produces output records.

The mapper prepares data into a form suitable for sorting; the reducer processes the sorted data (source: designing-data-intensive-applications, chapter 10).

## Distributed execution

Parallelization is based on [[partitioning]] (source: designing-data-intensive-applications, chapter 10):

- **Map tasks**: The number is determined by input file blocks. The scheduler tries to run each mapper on a machine that stores a replica of its input file — **putting computation near the data** to reduce network load.
- **Reduce tasks**: Configured by the job author (can differ from map task count). A hash of the key determines which reducer receives each key-value pair.

The **shuffle** process connects mappers to reducers:
1. Each mapper partitions its output by reducer (hash of key).
2. Each partition is written as a sorted file on the mapper's local disk (using a technique similar to [[sstables-and-lsm-trees]]).
3. Reducers fetch sorted files from all mappers and merge them, preserving sort order.

## MapReduce workflows

A single MapReduce job is limited in what it can compute. Complex tasks require chaining jobs into workflows where the output directory of one job is the input directory of the next (source: designing-data-intensive-applications, chapter 10).

Chained jobs are more like a sequence of commands writing to temporary files than Unix pipes — each job must complete fully before the next begins. Workflow schedulers (Oozie, Azkaban, Luigi, Airflow, Pinball) manage job dependencies (source: designing-data-intensive-applications, chapter 10).

Workflows of 50–100 MapReduce jobs are common in recommendation systems. Higher-level tools (Pig, Hive, Cascading, Crunch, FlumeJava) automatically wire together multi-stage workflows (source: designing-data-intensive-applications, chapter 10).

## Join algorithms

MapReduce supports several join strategies:

- **[[sort-merge-joins]]** (reduce-side joins) — Both datasets go through mappers that extract the join key. The shuffle brings all records with the same key to the same reducer.
- **[[map-side-joins]]** — Bypass reducers entirely when assumptions about input data hold (small dataset fits in memory, or inputs are co-partitioned).

## Fault tolerance

MapReduce is designed for environments where task failure is common. At Google, a MapReduce task running for an hour has approximately a 5% chance of being preempted by a higher-priority process (source: designing-data-intensive-applications, chapter 10).

- If a map or reduce task fails, the framework retries it on another machine using the same input.
- Automatic retry is safe because inputs are immutable and outputs from failed tasks are discarded.
- The all-or-nothing output guarantee: if the job succeeds, the result is as if every task ran exactly once. If the job fails, no output is produced.

This design is expensive in the failure-free case (eager disk writes) but tolerates frequent task termination. It was designed for Google's mixed-use datacenters where batch jobs run at low priority and are preempted to free resources for production services (source: designing-data-intensive-applications, chapter 10).

## Limitations

MapReduce has significant drawbacks that motivated the development of [[dataflow-engines]] (source: designing-data-intensive-applications, chapter 10):

- **[[materialization-of-intermediate-state]]**: Every job writes complete output to HDFS before the next job starts. This means jobs can't pipeline, redundant mapper stages read back what reducers just wrote, and intermediate data is replicated across nodes unnecessarily.
- **Straggler tasks**: A workflow waits for the slowest task in the preceding job before the next job can start.
- **Low-level API**: Implementing joins and complex processing from scratch is laborious.
- **Always sorts**: Sorting happens between every map and reduce stage, even when it's not needed.

## Container-level perspective: map = sharder, reduce = reduce-pattern

Burns's *Designing Distributed Systems* Chapter 12 ([[coordinated-batch-pattern]]) names the two halves of MapReduce as standalone container-level patterns (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md):

> "It's easy to see that the map step is an example of sharding a work queue, and the reduce step is an example of coordinated processing that eventually reduces a large number of outputs down to a single aggregate response."

The correspondence is exact:

| MapReduce step | Burns pattern |
|---|---|
| Input split + scheduled map tasks | [[work-queue-pattern]] |
| Shuffle / partition-by-key | [[sharder-pattern]] |
| "Wait for all mappers" barrier before reduce | [[join-pattern]] |
| Reduce | [[reduce-pattern]] |

MapReduce's framework-level guarantee that every mapper completes before any reducer starts is a [[join-pattern|join]] in Burns's vocabulary — a barrier synchronization point that costs the straggler latency. [[dataflow-engines|Spark, Flink, Tez]] relax that barrier where the reduce is associative, which is the operator-level form of preferring Burns's [[reduce-pattern|reduce]] (streaming, pipelined) over his [[join-pattern|join]] (blocking, completeness-guaranteeing). So the pattern-level distinction Burns draws at container granularity echoes the engine-level distinction DDIA draws between MapReduce and dataflow execution.

## At Google: the production MapReduce

The SRE book's Chapter 2 refers to MapReduce alongside indefinitely-running servers as one of the two kinds of job [[borg]] runs — framing MapReduce as a first-class citizen of Google's cluster OS rather than a separate system (source: site-reliability-engineering, chapter 2). The Chapter 2 Shakespeare example (see [[life-of-a-request]]) uses MapReduce as the batch indexer that writes per-word location tuples into [[bigtable]]:

- Map: split Shakespeare's texts into words.
- Shuffle: sort tuples by word.
- Reduce: emit `(word, list-of-locations)`, one Bigtable row per word.

It is the textbook three-phase MapReduce with [[bigtable]] as the sink instead of HDFS. The preempt-at-5% observation above is from Google's mixed-use datacenters in the same era, when batch MapReduce runs were scheduled at low priority and preempted to free resources for production serving jobs.

## SRE Chapter 25: MapReduce as the framework periodic pipelines are written in

SRE Chapter 25 (Dan Dennison) names MapReduce as one of the two frameworks Google uses to write [[periodic-pipeline|periodic data pipelines]] (the other is Flume) (source: raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md). The chapter is not a critique of MapReduce per se — it credits MapReduce as useful and stable when sized for the workload — but it catalogues the operational failure modes that emerge when MapReduce-based pipelines grow into deep multi-phase chains:

- Cycle-aligned worker spawn produces [[pipeline-thundering-herd|thundering herds]] on the cluster scheduler. Ch 25 frames the canonical case as "a daily cron at midnight spawning thousands of MapReduce workers" — exactly Ch 24's [[cron-thundering-herd]] but at the application layer.
- The straggler problem named under Limitations above (a workflow waits for the slowest task in the preceding job) is what Ch 25 calls the [[pipeline-uneven-work-distribution|hanging chunk problem]], with the additional observation that the standard kill-and-restart response wastes all completed work because periodic pipelines lack checkpointing.
- The [[pipeline-batch-scheduling-drawbacks|execution-frequency floor]] from running at batch priority limits how fresh MapReduce-pipeline outputs can be.

The chapter's recommendation is not to fix MapReduce but to **adopt a different shape** for workloads where the failure modes matter: continuous data processing via [[google-workflow|Workflow]] with its long-running workers and exactly-once guarantees. Modern open-source [[dataflow-engines]] (Spark, Flink) sit between the two — they retain MapReduce's per-job submission model but pipeline through stages so the straggler-amplification problem is reduced, and Flink in particular offers continuous-streaming modes that approach Workflow's shape.

## Chapter 8 — the post-MapReduce world

Reis & Housley frame the modern landscape as a relaxation of MapReduce's rigidity rather than a replacement (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

> Post-MapReduce processing does not truly discard MapReduce; it still includes the elements of map, shuffle, and reduce, but it relaxes the constraints of MapReduce to allow for in-memory caching.

The diagnosis is concrete: Google's original MapReduce runs numerous short-lived ephemeral tasks that read from and write to disk. No intermediate state is preserved in memory; all data transfers between tasks via disk or network. This simplifies state and workflow management and minimizes memory consumption — **but** drives high disk-bandwidth use and increases processing time.

The fix: frameworks like Spark, BigQuery, and others treat data as a distributed set that lives in memory, spilling to disk only when it overflows. The disk becomes a second-class data-storage layer. **RAM is much faster than SSD/HDD in transfer and seek; persisting even a tiny amount of judiciously chosen data in memory can dramatically speed up processing and utterly crush MapReduce's performance.**

The cloud accelerates this: "it is much more effective to lease memory during a specific processing job than to own it 24 hours a day" (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md). The old MapReduce assumption — cheap disk, so throw disk at the problem — inverted once memory became rentable by the minute.

## Chapter 8 — the map/shuffle/reduce worked example

Chapter 8 uses a concrete SQL to illustrate (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

```sql
SELECT COUNT(*), user_id
FROM user_events
GROUP BY user_id;
```

- The table is spread across nodes in data blocks; MapReduce creates one map task per block.
- Each map task generates a count per user ID present in its block.
- The **shuffle** redistributes tuples by key via a hash so that each key ends up on exactly one reducer node.
- Reducers sum the counts per key. Key/count pairs are written to local disk on the owning node.
- Full results are collected across nodes at the end.

The map phase is a near-perfect example of **embarrassing parallelism** — data scan rate scales linearly with node count. Real-world jobs add `WHERE` clauses, three-table joins, and window functions, which expand into many stacked map + reduce stages.

## Relationship to MPP databases

The parallel join algorithms in MapReduce were not new — MPP databases (Teradata, Tandem NonStop SQL, Gamma) had them a decade earlier. MapReduce's contribution was making general-purpose distributed computation accessible on commodity hardware via [[distributed-filesystems]]. See [[hadoop-vs-mpp-databases]] (source: designing-data-intensive-applications, chapter 10).

## Related pages

- [[batch-processing]]
- [[unix-philosophy]]
- [[distributed-filesystems]]
- [[sort-merge-joins]]
- [[map-side-joins]]
- [[dataflow-engines]]
- [[materialization-of-intermediate-state]]
- [[hadoop-vs-mpp-databases]]
- [[batch-workflow-outputs]]
- [[partitioning]]
- [[declarative-vs-imperative-queries]]
- [[coordinated-batch-pattern]]
- [[join-pattern]]
- [[reduce-pattern]]
- [[sharder-pattern]]
- [[work-queue-pattern]]
- [[graph-batch-processing]]
- [[periodic-pipeline]]
- [[pipeline-thundering-herd]]
- [[pipeline-uneven-work-distribution]]
- [[google-workflow]]
- [[data-processing-pipelines]]
