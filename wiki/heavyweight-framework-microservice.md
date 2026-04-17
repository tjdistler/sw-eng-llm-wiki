# Heavyweight Framework Microservice

**Summary**: An [[event-driven-microservices|EDM]] built on top of a **full-featured streaming framework** — Apache Spark, Apache Flink, Apache Storm, Apache Heron, Apache Beam — that runs on its own dedicated [[stream-processing-cluster|cluster]] of worker and master nodes and provides its own failure recovery, resource allocation, task distribution, shuffling, and coordination. "Heavyweight" names the fact that the framework duplicates many responsibilities already handled by the [[container-management-system|CMS]] and [[event-broker]]; the trade is a mature, battle-tested analytics stack against significant operational overhead (source: chapter-11-heavyweight-framework-microservices.md).

**Sources**: `raw/building-event-driven-microservices/chapter-11-heavyweight-framework-microservices.md`

**Last updated**: 2026-04-17

---

## What makes a framework "heavyweight"

Two defining characteristics (source: chapter-11-heavyweight-framework-microservices.md):

1. **Requires an independent cluster of processing resources.** Shareable worker nodes plus coordinating master nodes, typically backed by Apache Zookeeper (or a similar distributed-coordination service) for high availability and leader election.
2. **Uses its own internal mechanisms** for failures, recovery, resource allocation, task distribution, data storage, inter-task communication, and coordination — rather than leaning on the [[container-management-system|CMS]] and [[event-broker]].

This contrasts with [[basic-producer-consumer-microservice|BPC]], [[functions-as-a-service|FaaS]], and lightweight-framework implementations, which delegate most of those responsibilities to the broker and the CMS. The cluster is the weight.

See [[stream-processing-cluster]] for the master/executor architecture.

## Lineage: big-data, not microservices

Heavyweight stream frameworks descend directly from their heavyweight **batch-processing** predecessors (source: chapter-11-heavyweight-framework-microservices.md):

- Hadoop (2006) bundled distributed storage, [[mapreduce]], and failure recovery for commodity hardware.
- As workloads grew from gigabytes to petabytes and demand shifted toward near-real-time, Spark, Flink, Storm, Heron, and Beam emerged.
- Spark and Flink unify batch and streaming; Storm and Heron are streaming-only.

This lineage matters: these frameworks were designed for **large-scale analytics workloads** (ETL, sessionization, anomaly detection, aggregation), not microservice-style deployment. That shapes both their strengths and their awkward edges. See [[dataflow-engines]] for the batch-era framing.

## Fit with EDM

Heavyweight frameworks are excellent at (source: chapter-11-heavyweight-framework-microservices.md):

- ETL pipelines across large event streams.
- Session- and window-based analysis — see [[windowing]].
- Abnormal-pattern detection over streams.
- Running aggregations with materialized state — see [[stateful-stream-processing]].
- Arbitrary [[stateless-stream-processing]].

They are less well suited to (source: chapter-11-heavyweight-framework-microservices.md):

- **Microservice-style deployment.** Historically required a dedicated cluster on top of the broker and CMS. Recent CMS-integration modes mitigate this — see below.
- **Non-JVM languages.** Most are Java/Scala-only for application code, though Python APIs and SQL dialects are expanding. A common workaround: use the framework to **transform** data into a materialized state store and serve business logic from another microservice in a different language.
- **Indefinite stream materialization.** Not every framework supports keeping an entity stream materialized as a table forever out of the box, which constrains [[stream-joins|stream-table]] and table-table joins and patterns like the gating pattern. Global windows can often provide this, but are poorly documented.

Bellemare's warning: **a heavyweight streaming framework is not a reasonable implementation for every event-driven microservice.** Verify fit before committing.

## Deployment options

Four ways to obtain a cluster (source: chapter-11-heavyweight-framework-microservices.md):

1. **Hosted service.** Pay Amazon, Google, Microsoft, Databricks, or Confluent to run it. Highest dollar cost, lowest operational cost, possible trend toward full serverless with reduced control.
2. **Build your own full cluster.** The historical Hadoop-style norm. Appropriate when hundreds or thousands of worker nodes are needed.
3. **Cluster on CMS-provisioned resources.** Run the master, worker, and Zookeeper nodes as CMS-managed containers — gaining CMS monitoring, logging, and scaling primitives — but otherwise operating a traditional long-lived cluster.
4. **Per-job CMS-native deployment.** Let the CMS itself play the role of master and dedicate worker resources per application (Spark-on-Kubernetes, Flink session clusters on Kubernetes). This mode *merges lightweight, BPC, and heavyweight deployment strategies*: each streaming job is a first-class microservice at the CMS level, with its own isolated workers.

Option 4 is where heavyweight frameworks are heading. It gives complete isolation between jobs, lets different frameworks/versions coexist, and lets the team's ordinary deployment pipeline ship streaming applications. The trade-offs: not every framework/CMS combination is supported, and some full-cluster features (e.g. advanced autoscaling) may not yet work under CMS-native deployment.

## Application submission modes

Independent of cluster shape, a job is submitted in one of two modes — see [[application-submission-modes]] (source: chapter-11-heavyweight-framework-microservices.md):

- **Driver mode** (Spark, Flink) — a local driver process coordinates the cluster-hosted job; killing the driver stops the job. Fits normal microservice deploy/terminate pipelines.
- **Cluster mode** (Spark, Flink, and the default for Storm and Heron) — the entire application is submitted and managed by the cluster, identified by a returned job ID. Requires cluster-API commands for deploy/terminate.

## State and checkpoints

Most heavyweight frameworks favor [[internal-state-store|internal state]] for performance — in-memory with spill to local disk — and protect durability with **checkpoints** written to external storage (HDFS, cloud object storage, highly-available KV stores). See [[checkpointing-stream-processing]] for the operator-state / key-state model and for how checkpointing is the analogue of snapshotting an [[external-state-store]] (source: chapter-11-heavyweight-framework-microservices.md).

## Scaling

Heavyweight stateful applications are tricky to scale because state must follow partition assignments. Two strategies, covered in [[stream-processing-scaling-strategies]] (source: chapter-11-heavyweight-framework-microservices.md):

- **Scale while running** — add/remove instances without stopping the job. Requires careful shuffle handling; typically depends on an [[external-shuffle-service]] (or, in Spark 3.0+, source-side shuffle-file management).
- **Scale by restart** — pause, checkpoint, stop, restart with new parallelism, reload state from checkpoint.

**Autoscaling** is built in for some frameworks (Google Dataflow, Heron's Health Manager, Spark Streaming's dynamic allocation) and wire-your-own for others.

**Application scaling is separate from cluster scaling** — the cluster must have resources available before an application can claim more.

## Recovery

Master-node, worker-node, and Zookeeper failures are all designed to be tolerable. On worker failure, tasks migrate to other workers and reload state from the latest checkpoint. Master failures are transparent to running jobs but may block new deployments; Zookeeper-backed HA restores the master role on failure. Monitoring both master and worker nodes is essential: a single failure may degrade performance and remove the headroom needed to recover from a subsequent one (source: chapter-11-heavyweight-framework-microservices.md).

## Multitenancy

As the number of applications on a cluster grows, **resource contention** becomes a real risk — for instance, a new job replaying from the beginning of time can starve running jobs by grabbing all spare cluster resources (source: chapter-11-heavyweight-framework-microservices.md). Two mitigations:

- **Many smaller clusters**, per team or business unit. Strong isolation; higher aggregate overhead from duplicated coordinator/Zookeeper nodes.
- **Namespacing within one cluster**, each team with reserved resources. Shared overhead; potential for fragmented unused capacity in idle namespaces.

See [[multitenancy-in-streaming-clusters]].

## Languages and syntax

JVM-centric: Java is most common, Scala second, Python increasingly represented. MapReduce-style chained-operator APIs dominate. SQL-like dialects (Spark SQL, Flink SQL, KSQL, Beam SQL) lower the learning curve at the cost of feature coverage (source: chapter-11-heavyweight-framework-microservices.md).

## Choosing a framework

Bellemare frames this the same way as choosing a CMS or event broker: pick the one your organization can operate at scale, not the one with the most interesting benchmarks. Inputs: available hosted offerings, team's familiarity with the JVM stack, required operations, and popularity (Spark dominant, Flink/Storm active, Heron least). Beam is an option if you want to keep the runner pluggable (source: chapter-11-heavyweight-framework-microservices.md).

## How this page fits the EDM family

| Implementation style | Summary | Chapter |
|---|---|---|
| [[basic-producer-consumer-microservice]] | Raw broker clients; external state the default; language-flexible | 10 |
| [[functions-as-a-service]] | Ephemeral per-event functions; managed runtime | 9 |
| [[lightweight-framework-microservice]] | Library-based (Kafka Streams, Samza embedded); leverages broker + CMS directly | 12 |
| **Heavyweight framework** (this page) | Full streaming cluster; Spark/Flink/Storm/Heron/Beam | 11 |

The recurring theme: each style differs in how much of the state, coordination, shuffling, scaling, and recovery work is done by the framework versus by the [[event-broker|broker]] plus [[container-management-system|CMS]] plus your own code. Heavyweight frameworks sit at the most-framework end of that axis.

## Related pages

- [[event-driven-microservices]]
- [[stream-processing-cluster]]
- [[application-submission-modes]]
- [[checkpointing-stream-processing]]
- [[external-shuffle-service]]
- [[stream-processing-scaling-strategies]]
- [[multitenancy-in-streaming-clusters]]
- [[stateful-stream-processing]]
- [[stateless-stream-processing]]
- [[internal-state-store]]
- [[external-state-store]]
- [[basic-producer-consumer-microservice]]
- [[functions-as-a-service]]
- [[hybrid-bpc-stream-processing]]
- [[container-management-system]]
- [[event-broker]]
- [[microservice-tax]]
- [[dataflow-engines]]
- [[mapreduce]]
- [[windowing]]
- [[stream-joins]]
- [[lightweight-framework-microservice]]
- [[broker-as-shuffle-service]]
