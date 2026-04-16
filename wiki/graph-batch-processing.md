# Graph Batch Processing

**Summary**: Graph batch processing applies offline algorithms (like PageRank) to entire graphs. The Pregel/BSP model provides an efficient vertex-centric programming abstraction where vertices exchange messages in synchronized rounds, avoiding the inefficiencies of iterative MapReduce.

**Sources**: `raw/designing-data-intensive-applications/chapter-10-batch-processing.md`

**Last updated**: 2026-04-15

---

## Graph processing vs graph databases

[[graph-data-models|Graph databases]] focus on OLTP-style queries — quickly finding a small number of vertices matching specific criteria. Graph batch processing performs offline analysis on an **entire graph**: machine learning, recommendation engines, ranking algorithms like PageRank (source: designing-data-intensive-applications, chapter 10).

This is also distinct from the DAG (directed acyclic graph) that [[dataflow-engines]] use to structure operator flow — there, the data flow is a graph but the data itself is relational-style tuples. In graph batch processing, the data itself has the form of a graph (source: designing-data-intensive-applications, chapter 10).

## Iterative algorithms on graphs

Many graph algorithms work by traversing edges one at a time, propagating information between adjacent vertices, and repeating until convergence. Examples include transitive closure and PageRank (source: designing-data-intensive-applications, chapter 10).

This "repeat until done" pattern cannot be expressed in a single [[mapreduce]] pass. The naive approach uses an external scheduler to run MapReduce iterations:

1. Run a batch job for one step of the algorithm.
2. Check the completion condition (e.g., convergence below a threshold).
3. If not done, run another iteration.

This is very inefficient: MapReduce reads the entire graph and writes a complete new copy on every iteration, even if only a small part changed (source: designing-data-intensive-applications, chapter 10).

## The Pregel model (Bulk Synchronous Parallel)

The **Bulk Synchronous Parallel (BSP)** model, popularized by Google's Pregel paper, provides a better abstraction. Implementations include Apache Giraph, Spark's GraphX, and Flink's Gelly (source: designing-data-intensive-applications, chapter 10).

### How it works

- Each **vertex** can send messages to other vertices (typically along edges).
- In each **iteration**, a function is called for each vertex, receiving all messages sent to it in the previous iteration.
- A vertex **remembers its state** between iterations — the function only processes new incoming messages.
- If no messages are sent to a part of the graph, no work is done there.

This is similar to the actor model: each vertex is like an actor. But unlike actors, communication proceeds in **fixed rounds** — all messages from iteration N are delivered in iteration N+1. There is no timing ambiguity (source: designing-data-intensive-applications, chapter 10).

### Fault tolerance

Pregel implementations periodically **checkpoint** the state of all vertices to durable storage. On failure, the simplest recovery is to roll back the entire computation to the last checkpoint. If the algorithm is deterministic and messages are logged, selective partition recovery is possible (source: designing-data-intensive-applications, chapter 10).

### Parallel execution

A vertex doesn't know which physical machine it runs on — it sends messages to vertex IDs, and the framework handles routing. The framework partitions the graph across machines, ideally co-locating vertices that communicate heavily. In practice, finding such optimal partitioning is hard, so the graph is often partitioned by arbitrary vertex ID (source: designing-data-intensive-applications, chapter 10).

## Performance considerations

Graph algorithms often incur heavy cross-machine communication. The intermediate state (messages between vertices) is often larger than the original graph. This overhead can significantly slow distributed graph algorithms (source: designing-data-intensive-applications, chapter 10).

**Rule of thumb**: If the graph fits in memory on a single machine, a single-machine algorithm will likely outperform a distributed approach. Even if it doesn't fit in memory, single-machine processing with frameworks like GraphChi (disk-based) may be viable. Distributed approaches like Pregel are only necessary when the graph is too large for a single machine (source: designing-data-intensive-applications, chapter 10).

## Related pages

- [[batch-processing]]
- [[graph-data-models]]
- [[mapreduce]]
- [[dataflow-engines]]
- [[partitioning]]
- [[message-brokers]]
