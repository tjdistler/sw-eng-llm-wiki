# Stream-Processing Cluster

**Summary**: The dedicated pool of processing resources that a [[heavyweight-framework-microservice|heavyweight streaming framework]] (Spark, Flink, Storm, Heron) uses to run jobs. A stream-processing cluster is organized around two primary roles — **master nodes** that schedule, prioritize, and coordinate, and **executor/worker nodes** that actually run tasks — typically with Apache Zookeeper (or similar) providing distributed coordination for master leader election and HA (source: chapter-11-heavyweight-framework-microservices.md).

**Sources**: `raw/building-event-driven-microservices/chapter-11-heavyweight-framework-microservices.md`

**Last updated**: 2026-04-17

---

## Roles

Bellemare's generic cluster picture (source: chapter-11-heavyweight-framework-microservices.md):

- **Master node.** Prioritizes, assigns, and manages executors and the tasks they run. A **task manager** on the master monitors task progress and restarts failed work elsewhere. Task managers are usually deployed with high-availability so that a master-node failure does not halt running jobs.
- **Executor / worker node.** Hosts tasks, which use the worker's CPU, memory, local disk, and remote disk to do the real work. In an EDM context, each task connects to the [[event-broker]] and consumes events from one or more partitions.
- **Distributed coordination (Zookeeper or equivalent).** Elects the active master, detects master failures, and brokers the leader transition. Historically a mandatory sidekick to Apache Hadoop-family frameworks; newer frameworks may or may not require it, but some form of distributed coordination is essential for reliable distributed operation.

## From job to tasks

A **job** is a stream-processing topology built with the framework's SDK and designed to solve a bounded-context problem. Unlike a batch job, it runs **indefinitely**, processing events as they arrive — just like any other [[event-driven-microservices|EDM]] (source: chapter-11-heavyweight-framework-microservices.md).

On submission:

1. The master accepts the job and decomposes its topology into **tasks**.
2. Tasks are assigned to available worker nodes.
3. Each task opens long-lived connections to the broker and starts consuming events from assigned stream partitions.
4. The task manager monitors progress; on task failure, the work is rescheduled on another worker.

Parallelism is configurable. The typical case is a 1:1 mapping between tasks and stream partitions, but one task can consume from all partitions (no parallelism), or many tasks can share a single partition (useful for queue-style consumption).

## Cluster resource management vs application resource management

Historically the cluster is responsible for allocating worker resources to jobs. Under CMS-native deployment modes (Spark on Kubernetes, Flink session clusters on Kubernetes), the CMS takes over much of that role — the framework requests resources from the CMS on demand, and the CMS owns the underlying scheduler. See [[heavyweight-framework-microservice]] for the four deployment options (source: chapter-11-heavyweight-framework-microservices.md).

In either mode, **application scaling is distinct from cluster scaling**: an application can only scale up as far as the cluster has free resources to offer (source: chapter-11-heavyweight-framework-microservices.md).

## Failure semantics

- **Worker failure.** Tasks on the failed worker are restarted elsewhere, reloading state from the last checkpoint and picking up their assigned partitions. See [[checkpointing-stream-processing]].
- **Master failure.** Running jobs continue unaffected; new job submissions may be blocked until a backup master takes over. HA mode with Zookeeper makes this transition automatic.
- **Zookeeper failure.** Because Zookeeper is itself a distributed quorum, minority-node failures are tolerated. Loss of Zookeeper quorum affects the cluster's ability to detect leader failure and elect new leaders.

Monitoring matters: a single surviving master after a failure is one failure away from a full coordination outage. Alert before you have to recover (source: chapter-11-heavyweight-framework-microservices.md).

## Related pages

- [[heavyweight-framework-microservice]]
- [[application-submission-modes]]
- [[checkpointing-stream-processing]]
- [[stream-processing-scaling-strategies]]
- [[multitenancy-in-streaming-clusters]]
- [[container-management-system]]
- [[event-broker]]
- [[zookeeper]]
- [[consensus]]
- [[microservice-topology]]
