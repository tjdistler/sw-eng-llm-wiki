# Timeliness and Integrity

**Summary**: Two distinct requirements commonly conflated under "consistency" -- timeliness (users see up-to-date state) and integrity (no data corruption or contradiction) -- which can be decoupled in event-based systems to achieve scalable correctness without distributed transactions.

**Sources**: `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`

**Last updated**: 2026-04-15

---

## The distinction

"Consistency" conflates two separate requirements that are worth considering independently (source: chapter-12-the-future-of-data-systems.md):

### Timeliness

Users observe the system in an up-to-date state. A stale read is a timeliness violation -- temporary and self-healing (just wait and retry). [[linearizability]] is a strong way of achieving timeliness. Weaker forms include [[read-after-write-consistency]] (source: chapter-12-the-future-of-data-systems.md).

### Integrity

Absence of corruption: no data loss, no contradictory or false data. [[derived-data|Derived datasets]] must correctly reflect their underlying data (e.g., a database index must reflect the database contents). An integrity violation is **permanent** -- waiting won't fix it; explicit checking and repair is needed (source: chapter-12-the-future-of-data-systems.md).

### In slogan form

> Violations of timeliness are "[[eventual-consistency]]," whereas violations of integrity are "perpetual inconsistency." (source: chapter-12-the-future-of-data-systems.md)

## Why integrity matters more

In most applications, integrity is much more important than timeliness. A credit card statement that doesn't show the last 24 hours of transactions is normal (timeliness violation). A statement where the balance doesn't equal the sum of transactions is catastrophic (integrity violation) (source: chapter-12-the-future-of-data-systems.md).

## ACID conflates both

[[acid|ACID]] transactions typically provide both timeliness (linearizability) and integrity (atomic commit) together. When using ACID, the distinction is inconsequential. The distinction becomes critical when moving to event-based dataflow systems (source: chapter-12-the-future-of-data-systems.md).

## Correctness in dataflow systems

Event-based [[derived-data|dataflow systems]] naturally decouple timeliness and integrity (source: chapter-12-the-future-of-data-systems.md):

- **Timeliness**: not guaranteed by default (asynchronous processing), unless consumers explicitly wait for messages to arrive.
- **Integrity**: central to streaming systems. [[exactly-once-semantics]] preserves integrity by ensuring events are not lost or processed twice.

Integrity in dataflow systems is maintained through (source: chapter-12-the-future-of-data-systems.md):

1. **Atomic single-message writes** -- representing each write as one message (aligns with [[event-sourcing]])
2. **Deterministic derivation functions** -- deriving all other state from that single message
3. **End-to-end request IDs** -- enabling [[exactly-once-semantics|duplicate suppression and idempotence]] across all processing stages
4. **Immutable messages + reprocessing** -- making it easy to recover from bugs

This achieves comparable correctness to [[distributed-transactions]] with much better performance and operational robustness.

## Loosely interpreted constraints

Many real applications can accept **weaker constraint enforcement** than strict uniqueness or capacity limits (source: chapter-12-the-future-of-data-systems.md):

- **Username conflicts**: send an apology and ask the user to choose another (compensating transaction).
- **Overselling inventory**: order more stock, apologize, offer a discount. The apology workflow is needed anyway (e.g., a forklift runs over stock).
- **Overbooking**: airlines and hotels deliberately violate "one person per seat" for business reasons, with compensation processes in place.
- **Overdrafts**: the bank charges a fee and limits daily withdrawals to bound risk.

The cost of apology varies but is often low. If the cost is acceptable, checking constraints before writing is unnecessarily restrictive -- you can write optimistically and check after the fact. These applications require integrity (no lost reservations, no mismatched debits/credits) but not timeliness on constraint enforcement. See [[coordination-avoidance]] (source: chapter-12-the-future-of-data-systems.md).

## Related pages

- [[coordination-avoidance]]
- [[exactly-once-semantics]]
- [[end-to-end-argument]]
- [[acid]]
- [[linearizability]]
- [[eventual-consistency]]
- [[derived-data]]
- [[distributed-transactions]]
- [[event-sourcing]]
- [[transactions]]
