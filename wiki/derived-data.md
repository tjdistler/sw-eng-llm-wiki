# Derived Data

**Summary**: Data that is created by transforming or processing some underlying dataset, such as search indexes, caches, materialized views, and ML models -- maintained through deterministic derivation functions applied to a system of record, enabling fault tolerance, evolution, and auditability.

**Sources**: `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`

**Last updated**: 2026-04-15

---

## Systems of record vs derived data

A **system of record** (source of truth) holds the authoritative version of data, typically captured through user input. **Derived data** is the result of transforming the system of record into another form for a specific access pattern. If derived data is lost, it can be rebuilt from the source. Examples: search indexes, materialized views, caches, analytics aggregates, ML models (source: chapter-12-the-future-of-data-systems.md).

The distinction is not about the tool but about the role: the same database might be a system of record for one dataset and hold derived data for another.

## Write path vs read path

All data follows a journey from collection to consumption, divided into two phases (source: chapter-12-the-future-of-data-systems.md):

- **Write path** (eager evaluation): precomputation that happens as soon as data arrives, regardless of whether anyone queries it. [[batch-processing]] and [[stream-processing]] pipelines are the write path, pushing data through derivation functions to update indexes, caches, and views.
- **Read path** (lazy evaluation): work done only when a user makes a request -- reading from the derived dataset and constructing a response.

The derived dataset is where the write path and read path **meet**. It represents a trade-off between work at write time and work at read time (source: chapter-12-the-future-of-data-systems.md).

### Shifting the boundary

Indexes, caches, and materialized views shift work from the read path to the write path by precomputing results. A full-text search index does work at write time (update index entries for all terms) to save work at read time (avoid scanning all documents). You could precompute results for all possible queries (maximum write-path work, zero read-path work), but the set of possible queries is infinite. A cache of common queries is a middle ground -- a materialized view for frequent queries (source: chapter-12-the-future-of-data-systems.md).

## Maintaining derived state

[[batch-processing|Batch processing]] encourages deterministic, pure functions: immutable inputs, append-only outputs, no side effects. [[stream-processing]] extends this with managed, fault-tolerant state. This functional flavor simplifies reasoning about organizational dataflows (source: chapter-12-the-future-of-data-systems.md).

Key principles:

- Think in terms of **data pipelines** that derive one thing from another
- Push state changes through deterministic application code
- Prefer asynchronous derivation (contained failures) over synchronous updates (amplified failures via [[distributed-transactions]])

## Pushing state to clients

The write path can extend all the way to end-user devices. Rather than clients polling for changes, servers can push state changes via WebSockets or server-sent events. The client device becomes a small subscriber to a stream of events, maintaining a local replica of the relevant derived state (source: chapter-12-the-future-of-data-systems.md).

Technologies like Elm, React/Redux, and Flux already manage client-side state by subscribing to event streams. Extending this to server-pushed events creates **end-to-end event streams**: state changes flow from one user's interaction, through event logs and stream processors, all the way to another user's display (source: chapter-12-the-future-of-data-systems.md).

## Reads are events too

Read requests can also be represented as events in a stream. Routing both reads and writes through the same stream operator is equivalent to a [[stream-joins|stream-table join]]. This enables (source: chapter-12-the-future-of-data-systems.md):

- **Multi-partition query execution**: combining data from several partitions using existing stream infrastructure for message routing, partitioning, and joining.
- **Causal dependency tracking**: recording what the user saw before making a decision, enabling better audit trails and [[causal-consistency|causal reasoning]].

## Application code as a derivation function

Unlike standard derivations (secondary indexes), many derivations require custom application code -- full-text indexing with domain-specific NLP, ML feature engineering, or UI-specific cache population. The [[unbundling-databases]] approach lets application code serve as the derivation function, running as a stream operator rather than a database stored procedure (source: chapter-12-the-future-of-data-systems.md).

## Related pages

- [[data-integration]]
- [[unbundling-databases]]
- [[lambda-architecture]]
- [[batch-processing]]
- [[stream-processing]]
- [[batch-workflow-outputs]]
- [[change-data-capture]]
- [[event-sourcing]]
- [[timeliness-and-integrity]]
- [[exactly-once-semantics]]
