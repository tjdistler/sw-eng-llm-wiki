# End-to-End Argument

**Summary**: A systems design principle (Saltzer, Reed, Clark, 1984) stating that correctness guarantees can only be fully implemented at the application endpoints, not by intermediate infrastructure alone -- applied to databases, it means that application-level measures like end-to-end operation identifiers are needed for true correctness, even when using strong infrastructure like serializable transactions.

**Sources**: `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`

**Last updated**: 2026-04-15

---

## The principle

"The function in question can completely and correctly be implemented only with the knowledge and help of the application standing at the endpoints of the communication system." Providing the function within the communication system itself is not possible, though an incomplete version may be useful as a performance optimization (source: chapter-12-the-future-of-data-systems.md).

## Application to duplicate suppression

TCP suppresses duplicate packets at the connection level, and stream processors provide [[exactly-once-semantics]] at the message processing level. But neither prevents a user from submitting a duplicate request when the first one times out. The user retries, the web server sees a separate HTTP request, the database sees a separate transaction -- and the usual deduplication mechanisms don't help (source: chapter-12-the-future-of-data-systems.md).

### The money transfer example

A simple `UPDATE accounts SET balance = balance + 11.00` transaction is not idempotent. If the client doesn't receive the COMMIT acknowledgment and retries, $22 is transferred instead of $11. Even [[two-phase-commit]] doesn't fully solve this, because duplicate requests can originate between the end-user device and the application server (source: chapter-12-the-future-of-data-systems.md).

### Solution: operation identifiers

Generate a unique ID (e.g., UUID) at the client and pass it end-to-end through every hop (source: chapter-12-the-future-of-data-systems.md):

1. Include the operation ID as a hidden form field in the client.
2. Pass it through the application server to the database.
3. Use a uniqueness constraint on the operation ID to ensure exactly-once execution.

The requests table with a unique operation ID also acts as a kind of event log, hinting toward [[event-sourcing]] (source: chapter-12-the-future-of-data-systems.md).

## Application to data integrity

The end-to-end argument applies to multiple domains (source: chapter-12-the-future-of-data-systems.md):

| Domain | Low-level mechanism | End-to-end mechanism |
|---|---|---|
| Duplicate suppression | TCP sequence numbers | Application-level operation IDs |
| Data integrity | Ethernet/TCP/TLS checksums | End-to-end checksums |
| Encryption | WiFi WPA, TLS | End-to-end encryption |

Low-level mechanisms reduce the probability of problems at higher levels but are not sufficient by themselves. HTTP would be unusable without TCP packet ordering, but TCP doesn't protect against application-level bugs or disk corruption (source: chapter-12-the-future-of-data-systems.md).

## Implications for database design

Just because an application uses serializable [[transactions]] does not mean it is free from data loss or corruption. The application itself must take end-to-end measures. This is inconvenient -- fault-tolerance mechanisms are hard to get right -- but necessary (source: chapter-12-the-future-of-data-systems.md).

Transactions simplify the programming model (collapsing many failure modes into commit/abort), but they may not be enough. When [[distributed-transactions]] are too expensive and applications implement their own fault-tolerance logic, bugs are likely. Better fault-tolerance abstractions are needed that provide application-specific end-to-end correctness while maintaining good performance at scale (source: chapter-12-the-future-of-data-systems.md).

## End-to-end integrity checking

The more systems included in an integrity check, the fewer opportunities for undetected corruption. Continuous end-to-end integrity checks enable confident, fast evolution of the system -- similar to how automated testing reduces the risk of regressions. See [[timeliness-and-integrity]] for how this relates to the broader correctness story (source: chapter-12-the-future-of-data-systems.md).

## Related pages

- [[exactly-once-semantics]]
- [[timeliness-and-integrity]]
- [[transactions]]
- [[distributed-transactions]]
- [[two-phase-commit]]
- [[event-sourcing]]
- [[data-integration]]
- [[coordination-avoidance]]
