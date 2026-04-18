# Spanner

**Summary**: Google's globally distributed database offering an SQL-like interface and real consistency across the world. The counterpart to [[bigtable]]: pick Spanner when you need cross-datacenter consistency, pick Bigtable when eventual consistency is fine.

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`, `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## What Spanner offers

Spanner offers "an SQL-like interface for users that require real consistency across the world" (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md). Two properties stand out:

- **SQL-like interface** — unusual for a globally distributed database and distinct from [[bigtable]]'s sparse-sorted-map model.
- **Real (globally strong) consistency** — linearizable reads and writes across datacenters.

This is the extreme opposite end of the consistency spectrum from Bigtable's [[eventual-consistency]].

## How strong consistency is possible at scale

Spanner achieves linearizable ordering across datacenters using **TrueTime**, an API backed by GPS and atomic clocks that bounds clock skew. With a known `ε` of clock error, a transaction can wait out its uncertainty interval before committing, giving a globally-agreed linearisation order.

See [[clock-synchronization]] (Kleppmann) for the wiki's existing discussion of TrueTime as an engineering response to the [[unreliable-clocks|unreliable-clocks]] problem. Chapter 2 of the SRE book doesn't drill into TrueTime itself, but Spanner is the concrete product that the mechanism exists for.

## Where it fits in the storage stack

Spanner sits alongside [[bigtable]] and Blobstore as a database-like service layered on top of [[colossus]] (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md). Chapter 26 of the SRE book treats the consistency trade-offs in more detail.

## TrueTime as the answer to "timestamps are dangerous"

Chapter 23 uses Spanner as its canonical counter-example to the rule that wall-clock timestamps are unsafe for ordering in distributed systems: "Spanner addresses this problem by modeling the worst-case uncertainty involved and slowing down processing where necessary to resolve that uncertainty" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

The argument is important because Chapter 23 elsewhere warns that "Timestamps are highly problematic in distributed systems because it's impossible to guarantee that clocks are synchronized across multiple machines" — Spanner is the exception that proves the rule, and it costs GPS-and-atomic-clock infrastructure plus explicit wait-out-the-uncertainty-interval logic on commits. Most systems can't afford that infrastructure; they use [[consensus]] instead.

## Cross-book connections

- [[linearizability]] — what Spanner provides globally.
- [[cap-theorem]] — Spanner is the canonical "we'll sacrifice availability during extreme partitions to keep linearizability" system; it is the standard counter-example to "NoSQL means giving up consistency."
- [[clock-synchronization]] — TrueTime is the mechanism.
- [[distributed-transactions]] — Spanner extends serializable distributed transactions globally, where [[two-phase-commit]] alone would not be viable.

## Related pages

- [[bigtable]]
- [[colossus]]
- [[linearizability]]
- [[clock-synchronization]]
- [[distributed-transactions]]
- [[site-reliability-engineering]]
- [[managing-critical-state]]
- [[reliable-replicated-datastore]]
- [[consensus]]
