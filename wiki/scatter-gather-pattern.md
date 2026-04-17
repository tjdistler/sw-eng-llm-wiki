# Scatter/Gather Pattern

**Summary**: The third serving pattern in Burns's catalogue. A **root** fans a single user request out to **many leaf nodes** simultaneously, each leaf computes a partial result, and the root combines the partials into one response before returning it to the client. Where the [[replicated-load-balanced-service]] replicates for request-throughput scaling and the [[sharded-service-pattern]] shards for state-size scaling, scatter/gather replicates for **time** — using parallelism to cut the latency of a single request.

**Sources**: `raw/designing-distributed-systems/chapter-07-scattergather.md`

**Last updated**: 2026-04-16

---

## The shape of the pattern

A scatter/gather system is a tree with a root and leaves (source: raw/designing-distributed-systems/chapter-07-scattergather.md):

```
                 ┌──────────┐
                 │   Root   │         1. Fan request out to all leaves
                 └─────┬────┘         2. Wait for every leaf to reply
        ┌────────┬────┴────┬────────┐ 3. Combine partials into one answer
        ▼        ▼         ▼        ▼
    ┌──────┐ ┌──────┐  ┌──────┐ ┌──────┐
    │ Leaf │ │ Leaf │  │ Leaf │ │ Leaf │
    └──────┘ └──────┘  └──────┘ └──────┘
```

Each leaf does a small fraction of the total work and returns a partial result; the root performs the combining step and returns the full answer to the client. Burns frames the pattern as **"sharding the computation rather than (or in addition to) sharding the data"** (source: raw/designing-distributed-systems/chapter-07-scattergather.md).

### What makes scatter/gather distinct

| Pattern | Root dispatches request to... | Purpose |
|---|---|---|
| [[replicated-load-balanced-service]] | one replica (any of them) | scale throughput |
| [[sharded-service-pattern]] | one shard (the owning one) | scale state size |
| Scatter/gather | **every leaf simultaneously** | scale request latency |

Scatter/gather shines when a single request needs a large amount of "mostly independent processing" — what Burns calls an **embarrassingly parallel problem** (source: raw/designing-distributed-systems/chapter-07-scattergather.md).

## Two variants

Burns presents two ways to partition the work across leaves. They can be combined.

### Variant 1: scatter/gather with root distribution (homogeneous leaves)

Every leaf is identical and holds the **same data**. The root splits the *work* of a single request across leaves and aggregates the partial results (source: raw/designing-distributed-systems/chapter-07-scattergather.md).

Burns's motivating example: a request that would take 60 seconds on one core can, in principle, be done in 2 seconds on 30 cores of one machine — but memory/network/disk bandwidth become the bottleneck before the CPU does. Scatter/gather escapes this by spreading the computation across *many* machines so each one's bandwidth is private.

Worked example in the chapter: **distributed document search for "cat" AND "dog"**. The root dispatches one leaf to look up documents containing "cat" and another to look up documents containing "dog"; each leaf returns a set; the root computes the **intersection** and returns it (source: raw/designing-distributed-systems/chapter-07-scattergather.md). Every leaf has the full index — the work being distributed is the two term-lookups.

Because every leaf can handle every request, the root can redistribute load dynamically when a particular leaf is responding slowly (noisy neighbour, etc.) — another flavour of what the [[replicated-load-balanced-service]] gets for free with round-robin.

### Variant 2: scatter/gather with leaf sharding (data-partitioned leaves)

The data is too large to fit on one machine, so the **documents themselves are sharded across leaves** — patents 0–100k on leaf 0, 100k–200k on leaf 1, and so on. A single query now has to consult *every* leaf, because any leaf might hold a matching document (source: raw/designing-distributed-systems/chapter-07-scattergather.md).

Worked example in the chapter: the same "cat AND dog" search, but each leaf only knows about its own document shard. Every leaf is asked for its hits; the root computes the **union** of all shards' matches and returns it.

> Burns notes in passing that partitioning patents by number range is a bad sharding scheme because new patents always land on the last shard — in practice you'd use `patent_id mod N`. See [[partitioning-strategies]], [[rebalancing-partitions]].

### Intersection vs union — why they differ

A subtlety easy to miss between the two variants:

- **Root-distributed variant**: each leaf handles *one term* against the full corpus. Leaves return complete per-term hit lists. Root computes **intersection** (for "AND" queries).
- **Leaf-sharded variant**: each leaf handles *all terms* against its own shard. Leaves return partial hit lists, each already filtered by "AND" locally. Root computes **union** across shards.

The two can be combined — a large system may shard by document and also dispatch per-term work — but the aggregation logic at the root depends on how you sliced things up.

## Why the leaf count is a design knob, not a free variable

It is tempting to push the leaf count arbitrarily high: more parallelism, less wall-clock time per request. Burns treats this in the chapter as a mistake, for two reasons (source: raw/designing-distributed-systems/chapter-07-scattergather.md):

### Per-request overhead scales with leaf count

Every fan-out call costs some fixed overhead — request parsing, network send, serialization. It is small compared to actual computation, but it scales **linearly with leaves**. Eventually the per-leaf overhead dominates the per-leaf useful work, and speedup becomes asymptotic. You do not get a meaningful speedup from the 1000th leaf.

### Tail latency gets worse at every request, by construction

This is the more consequential issue. In scatter/gather, the root must wait for **all** leaves to respond. The total request latency is bounded below by the **slowest** leaf's latency. See [[tail-latency-amplification]] for the full treatment — it is substantive enough to have its own page.

Quick sketch: if a leaf has a 2-second p99 (1 in 100 requests slow), scattering to 5 leaves makes the *overall system's* p99 actually a p95 (5 in 100 requests slow, because 0.99⁵ ≈ 0.95). Scattering to 100 leaves essentially guarantees that *every* user request hits a 2-second slow leaf. The 99th-percentile response time therefore **matters much more in scatter/gather than elsewhere**, because every user request becomes many subrequests (source: raw/designing-distributed-systems/chapter-07-scattergather.md).

### Availability compounds the same way

The same compounding applies to availability. A leaf failure probability of 1% with 100 leaves means every user request is practically guaranteed to fail — unless each leaf is itself replicated. See [[tail-latency-amplification]] and the next section.

## Reliability: replicate each leaf

A single-instance-per-leaf scatter/gather system has three failure modes Burns identifies (source: raw/designing-distributed-systems/chapter-07-scattergather.md):

1. A leaf failure takes the whole system down (because every request needs every leaf).
2. Rolling upgrades drop leaves temporarily — running under load is not possible.
3. Per-leaf compute ceiling caps the system's total throughput.

The answer is the same shape as [[replicated-sharded-service]] from the previous chapter: **replace each leaf with a [[replicated-load-balanced-service|replicated load-balanced sub-service]]**. The root's call to "leaf i" is now a load-balanced call to one of many replicas of that shard. Failures become degraded performance rather than outages, rolling upgrades proceed one replica at a time, and each shard's throughput can scale independently (source: raw/designing-distributed-systems/chapter-07-scattergather.md).

The resulting architecture combines all three serving patterns:

```
                         ┌──────────┐
                         │   Root   │
                         └─────┬────┘
               ┌───────────────┴───────────────┐
               ▼                               ▼
       ┌───────────────┐               ┌───────────────┐
       │ Leaf shard 0  │               │ Leaf shard 1  │
       │ (replicated   │               │ (replicated   │
       │  load-balanced│               │  load-balanced│
       │  sub-service) │               │  sub-service) │
       └───────────────┘               └───────────────┘
```

This is **scatter/gather over replicated shards** — the robust shape a real deployment takes.

## Relationship to existing wiki concepts

### Relationship to DDIA partitioning

The scatter/gather pattern already has deep coverage in the wiki from DDIA, but framed as a *database read path* rather than a named service pattern:

- **Document-partitioned secondary indexes** ([[partitioning-secondary-indexes]]): a query like "find all red cars" must be sent to every partition because any partition might hold a matching record. This is Burns's Variant 2 (leaf sharding) at the database layer.
- **MPP parallel query execution** ([[partitioning]], [[hadoop-vs-mpp-databases]]): complex analytical queries are broken into stages that execute in parallel across partitions, and results are aggregated. This is scatter/gather at the analytics layer.
- **MapReduce** ([[mapreduce]]): the shuffle + reduce phase performs exactly a union-style gather after mappers scatter per-key work — scatter/gather at batch-processing scale, asynchronously.
- **Dataflow engines** ([[dataflow-engines]]): generalise the scatter/gather idea to arbitrary DAGs, with pipelined execution between stages instead of materialising intermediates.

Burns's Chapter 7 contribution is to **name the shape** and treat it as a design pattern at the serving tier, complete with the operational consequences (leaf count, tail latency, leaf replication). The DDIA pages cover the mechanics; the serving-pattern page covers the deployment shape.

### Relationship to tail-latency amplification

[[tail-latency-amplification]] is the load-bearing performance concern for this pattern. DDIA's [[response-time-percentiles]] introduces the concept in the context of any fan-out system (microservices, page renders with many backend calls). Burns's Chapter 7 applies it specifically to scatter/gather, with concrete math. Both pages link to the amplification page as the detailed treatment.

### Relationship to sharded and replicated patterns

Scatter/gather is the third of the Part II serving patterns, and it composes with the first two:

- Each leaf can itself be a [[replicated-load-balanced-service]] (required for reliability — see above).
- Each leaf typically owns a subset of data, which is [[sharded-service-pattern|sharding]] applied to the leaf tier.
- The root is structurally the same as the sharded service's root, but with **fan-out-to-all** semantics instead of **route-to-one** semantics. It may be deployed either as a [[client-side-sharding|per-pod ambassador]] or as a shared routing tier — the same [[ambassador-pattern]] trade-off recurs.

### Relationship to the replicated-load-balanced pattern

Scatter/gather uses replication for latency; the replicated load-balanced pattern uses it for throughput and availability. The two are orthogonal — and both can stack on a single serving-tier design.

## When scatter/gather is (and isn't) the right pattern

The pattern fits when:

- A request decomposes into many mostly independent pieces.
- The individual pieces' aggregated latency would be unacceptable if served sequentially.
- The data or the work is large enough that splitting pays for the overhead.
- The aggregation step (intersection, union, sum, top-k) is cheap relative to the leaf work.

The pattern does **not** fit when:

- The leaf count would be so large that per-leaf overhead dominates useful work.
- The workload cannot tolerate tail-latency amplification — or the leaf tier cannot be made fast enough at high percentiles.
- The computation is sequential rather than parallel (leaf N's input depends on leaf N-1's output).
- The aggregation is itself expensive (moves the bottleneck rather than eliminating it).

## Related pages

- [[tail-latency-amplification]]
- [[replicated-load-balanced-service]]
- [[sharded-service-pattern]]
- [[replicated-sharded-service]]
- [[response-time-percentiles]]
- [[partitioning-secondary-indexes]]
- [[partitioning]]
- [[partitioning-strategies]]
- [[hadoop-vs-mpp-databases]]
- [[mapreduce]]
- [[dataflow-engines]]
- [[ambassador-pattern]]
- [[client-side-sharding]]
- [[request-routing]]
- [[fault-tolerance]]
- [[scalability]]
- [[designing-distributed-systems]]
