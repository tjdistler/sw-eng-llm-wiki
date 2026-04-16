# Consistent Prefix Reads

**Summary**: A consistency guarantee that ensures if a sequence of writes happened in a certain order, anyone reading those writes sees them in the same order — preventing observers from seeing effects before their causes.

**Sources**: `raw/designing-data-intensive-applications/chapter-05-replication.md`

**Last updated**: 2026-04-15

---

## The problem

In a partitioned or multi-replica system, different writes may replicate at different speeds. An observer reading from multiple replicas may see a *reply* before the *question* it answers — because the reply's partition replicated faster than the question's.

This violates causality. The observer sees an effect without its cause, which is confusing and can break application logic that depends on order. This is the third anomaly caused by [[replication-lag]].

Example from the book: Mrs. Cake answers Mr. Poons's question, but an observer on lagging replicas hears the answer first, then the question — as if Mrs. Cake can see the future.

## The guarantee

Consistent prefix reads says:

> If a sequence of writes happens in a certain order, any read of those writes will see them appear in the same order.

This is specifically about **causality** — writes that are causally dependent on each other must appear in causal order to all readers.

## Where this is hardest

This anomaly is particularly problematic in **partitioned (sharded) databases** where different partitions operate independently with no global ordering of writes. A user's reads may span multiple partitions, each at a different point in time.

If a database applies all writes in a single total order (as in single-node systems), consistent prefix reads are automatic. The problem arises when writes are distributed across nodes with no coordination.

## Solutions

**Route causally-related writes to the same partition**: if writes that depend on each other always go to the same partition, they are ordered within that partition. This isn't always possible efficiently.

**Causal dependency tracking**: algorithms can explicitly track which writes depend on which other writes, and ensure dependent writes are applied in order across replicas. [[version-vectors]] are one tool for tracking these dependencies.

## Related pages

- [[replication-lag]]
- [[read-after-write-consistency]]
- [[monotonic-reads]]
- [[version-vectors]]
- [[replication]]
- [[eventual-consistency]]
- [[causal-consistency]]
