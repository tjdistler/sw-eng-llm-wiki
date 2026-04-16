# MapReduce

**Summary**: MapReduce is a programming framework for processing large datasets across a distributed cluster. It provides a simple abstraction — write a mapper and a reducer — while the framework handles partitioning, sorting, data movement, and fault tolerance.

**Sources**: `raw/designing-data-intensive-applications/chapter-10-batch-processing.md`

**Last updated**: 2026-04-15

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
