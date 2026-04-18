# Distributed Barrier

**Summary**: A distributed-systems primitive that blocks a group of processes from proceeding until some condition is met — typically that all parts of one phase of a computation are completed. Implementable as a [[replicated-state-machine]] on top of [[consensus]]; exposed natively by [[zookeeper|ZooKeeper]]. The canonical use case is separating phases of a MapReduce computation.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## What a barrier does

"A barrier in a distributed computation is a primitive that blocks a group of processes from proceeding until some condition is met (for example, until all parts of one phase of a computation are completed). Use of a barrier effectively splits a distributed computation into logical phases" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

## MapReduce as the canonical case

A barrier can be used in implementing the [[mapreduce|MapReduce]] model to ensure that the entire **Map phase is completed** before the Reduce part of the computation proceeds (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). The barrier is the contract that makes the phased-computation mental model valid; without it, Reduce workers would have to tolerate partial Map outputs.

Chapter 23 points at this as an RSM-based alternative to the single-coordinator-process approach, which has an unacceptable single-point-of-failure problem. The same logic applies to other phased distributed computations — [[batch-processing|batch processing]] stages, [[coordinated-batch-pattern|coordinated batch workflows]], and any MPI-style collective operation.

## Implementation options

Chapter 23 explicitly names two options (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

1. **A single coordinator process** — the simplest implementation, but adds a single point of failure that is "usually unacceptable" for any production barrier.
2. **An RSM** — the barrier state (which processes have reported complete) is replicated via consensus; no single-coordinator failure mode. ZooKeeper can implement the barrier pattern natively.

## Relationship to [[join-pattern|join]] in batch workflows

Burns's [[join-pattern]] is the same abstract primitive at a higher level — barrier synchronisation in a batch computational pattern — realised over queues and orchestrator state rather than directly over consensus. Chapter 23's RSM-backed barrier is the primitive; Burns's `join` is the pattern-level shape built on top of an orchestrator that itself is (usually) backed by a consensus system like etcd.

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[replicated-state-machine]]
- [[zookeeper]]
- [[mapreduce]]
- [[coordinated-batch-pattern]]
- [[join-pattern]]
- [[reliable-distributed-queue]]
