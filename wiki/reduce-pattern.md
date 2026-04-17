# Reduce Pattern

**Summary**: Burns's second coordinated-batch primitive and the container-level naming of the reduce half of MapReduce. A **reduce** combines two or more parallel outputs into a single output of the same shape, repeatedly, until one aggregate remains. Unlike the [[join-pattern|join]]'s barrier semantics, reduce is optimistic and streaming: each reduction step can start as soon as two outputs exist, so the reduce phase pipelines in parallel with the upstream map/shard phase and the whole pipeline is substantially faster.

**Sources**: `raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md`

**Last updated**: 2026-04-16

---

## What it does

"With the reduce pattern, each step in the reduce merges several different outputs into a single output. This stage is called 'reduce' because it reduces the total number of outputs. Additionally, it reduces the data from a complete data item to simply the representative data necessary for producing the answer to a specific batch computation" (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md).

The pattern has three defining properties (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md):

1. **Associative / repeatable.** "The reduce phase can be repeated as many or as few times as necessary in order to successfully reduce the output down to a single output for the entire data set." A reduce stage's output has the same shape as its input, so reduce steps can be stacked arbitrarily.
2. **Parallel.** Because the operation is associative, multiple reduce workers can process disjoint pairs of inputs in parallel, producing intermediate aggregates that are themselves reducible.
3. **Pipelined with upstream work.** "Reduce can be started in parallel while there is still processing going on as part of the map/shard phase." This is the fundamental advantage over [[join-pattern|join]]: the workflow does not block on the slowest upstream shard — it begins draining into the reduce tree as soon as two outputs exist.

## Identity with MapReduce's reduce step

Burns is explicit that the reduce pattern **is** the reduce half of the canonical map/reduce algorithm, named at container granularity (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md):

> "If sharding a work queue is an example of the map phase of the canonical map/reduce algorithm, then what remains is the reduce phase. Reduce is an example of a coordinated batch processing pattern because it can happen regardless of how the input is split up, and it is used similar to join; that is, to group together the parallel output of a number of different batch operations on different pieces of data."

See [[mapreduce]] for the framework-level treatment. The identity is exact: a [[sharder-pattern|sharder]] feeding parallel [[work-queue-pattern|work queues]] is the map phase; a reduce-pattern container draining their outputs into one aggregate is the reduce phase. Burns's contribution is container-level naming of a primitive that MapReduce bakes into the framework.

## Hands on: word count (Burns's example)

The worked example is a distributed word count over a book (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md). Pages are sharded across ten worker queues by page-number modulo; each worker emits a partial histogram:

```
a: 50
the: 17
cat: 2
airplane: 1
```

A reduce container takes two such histograms and sums them key by key:

```
a: 80
the: 42
dog: 4
cat: 2
airplane: 3
```

The resulting histogram has the same shape as each input, so it can be fed into another reduce step with another partial histogram — repeatedly, in parallel, in any order — until one histogram remains.

This is the canonical example because the required algebraic structure is visible: integer addition is associative and commutative, so any pairing and any ordering of reduce steps gives the same final answer. That structure is what lets the reduce phase be pipelined and parallel.

## Burns's three worked examples

Chapter 12 walks through three reductions in increasing complexity (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md):

| Example | Per-worker output | Reduce operation |
|---|---|---|
| Count | `word -> integer` map (per page) | Sum counts per word |
| Sum | `(town, population)` tuples | Sum populations, label with the union of town names |
| Histogram | Per-town percentage histogram of family size | Population-weighted average: multiply each histogram by its town's population, sum, then divide by merged populations |

The histogram example is the subtle one: naively averaging percentage histograms would be wrong because small towns would count equally with large ones. The correct combine requires carrying the population as a weight, reconstructing counts, summing, and redividing. Burns's message is that **what makes a reducer correct is the algebraic structure of the combine, not the pattern's container shape** — if the combine is wrong (e.g., averaging percentages), the whole aggregate is wrong. The pattern provides the pipelining; the programmer provides the associativity.

## The shape of the reduce container

A reduce container implements a narrow interface:

- **Input**: two (or more) outputs from either an upstream worker or a previous reduce step. They share a schema (word-count map, population tuple, weighted histogram).
- **Output**: one output in the same schema, representing the combined aggregate.
- **Invariant**: the operation is associative — `reduce(a, reduce(b, c)) == reduce(reduce(a, b), c)` — so the reduce tree can be built in any order.

The [[work-queue-pattern|queue manager]] arranges the reduce tree: it feeds pairs of ready outputs into reduce workers, whose outputs become inputs to the next level of the tree, until one output remains.

## Relationship to other patterns

### Join vs reduce

The comparison with [[join-pattern|join]] is Burns's central framing (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md):

| Property | [[join-pattern]] | Reduce (this page) |
|---|---|---|
| Waits for all upstream work? | Yes | No — starts pairwise as soon as outputs exist |
| Combines values? | No | Yes, associatively |
| Pipelined with upstream? | No | Yes |
| Latency cost | Max of all upstream paths | Closer to average of upstream paths + reduce-tree depth |

Reduce is strictly more parallel than join. When the aggregation can be expressed associatively, reduce is the right answer; when the downstream step requires a completeness fence that is not a combine, join is the right answer.

### Merger vs reduce

A [[merger-pattern|merger]] concatenates streams; a reduce **combines values**. The reduce's shape is N-to-1 in the value-space, not N-to-1 in the stream-space.

### Scatter/gather at the serving tier

[[scatter-gather-pattern|Scatter/gather]]'s gather step is a reduce in the online request/response setting: partial responses from leaves are combined into one response to the client. The algebraic requirement is the same — the gather combine must be associative (or at least commutative + idempotent) for the pattern to work. Burns does not name the parallel in Chapter 12, but the identity is structural.

### Dataflow engines

[[dataflow-engines|Spark, Flink, Tez]] treat reduction as a first-class operator (`reduce`, `aggregateByKey`, `fold`) with the same pipelining story: the optimizer starts the reduce tree as soon as partial outputs are available rather than materialising the full map output to disk. Burns's container-level reduce pattern is the coarse-grained echo of that operator-level capability.

### Stream aggregation

Stream processing engines implement running reductions over windows ([[windowing]]) using the same associativity requirement. A batch reduce is the bounded-input form; a windowed stream reduce is the unbounded form.

## When the pattern fits

Use reduce when:

- The aggregation can be expressed as an associative (ideally commutative) pairwise combine.
- Upstream work has high parallelism and stragglers would otherwise dominate wall-clock time.
- The per-item output is significantly smaller than the full dataset (so the reduce tree usefully compresses).

Prefer alternatives when:

- The aggregation is not associative and requires a global view — use a [[join-pattern|join]] before a single-shot aggregator.
- The operation preserves every input without combining — use a [[merger-pattern|merger]].
- The reduction logic is complex enough that a dedicated framework helps — use [[mapreduce]] or [[dataflow-engines]] directly.

## Related pages

- [[coordinated-batch-pattern]]
- [[join-pattern]]
- [[merger-pattern]]
- [[sharder-pattern]]
- [[work-queue-pattern]]
- [[event-driven-batch-pattern]]
- [[mapreduce]]
- [[dataflow-engines]]
- [[scatter-gather-pattern]]
- [[windowing]]
- [[batch-processing]]
- [[idempotence]]
- [[designing-distributed-systems]]
