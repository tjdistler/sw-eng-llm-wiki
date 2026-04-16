---
name: Scaling Approaches
description: Strategies for handling increased load — vertical vs horizontal scaling, elastic vs manual, stateless vs stateful
type: concept
---

# Scaling Approaches

**Summary**: There is no one-size-fits-all scaling strategy. The right approach depends on a system's specific [[load-parameters]], and good architectures usually combine several techniques.

**Sources**: `raw/designing-data-intensive-applications/chapter-01-reliable-scalable-and-maintainable-applications.md`

**Last updated**: 2026-04-15

---

## Vertical scaling (scale up)

Move to a more powerful machine with more CPU, memory, and I/O. Simpler operationally — no distribution complexity. But high-end machines become very expensive, and there is an upper limit to what a single machine can provide. (source: chapter-01)

## Horizontal scaling (scale out)

Distribute load across many smaller machines. Also called a **shared-nothing architecture** — nodes do not share memory or disk; they coordinate only via a network. More complex to implement, but commodity machines are cheap and there is no theoretical upper bound on capacity. (source: chapter-01)

In practice, good architectures mix both: several moderately powerful machines is often simpler and cheaper than a large fleet of tiny VMs.

## Elastic vs manual scaling

- **Elastic scaling**: the system automatically adds or removes resources in response to detected load changes. Useful when load is highly unpredictable.
- **Manual scaling**: a human analyzes capacity and provisions machines deliberately. Simpler to reason about and avoids operational surprises from unexpected auto-scaling behavior.

Neither is universally better; the right choice depends on load predictability and operational maturity. (source: chapter-01)

## Stateless vs stateful scaling

Scaling stateless services (e.g. web servers, API handlers) across multiple machines is relatively straightforward — any node can handle any request. Stateful systems (especially databases) are much harder to distribute: moving from a single-node database to a distributed setup introduces significant complexity around consistency, coordination, and failure handling.

The conventional wisdom has historically been: scale your database up (single node) until cost or availability requirements force distribution. As distributed systems tooling matures, this threshold is shifting. (source: chapter-01)

## Architecture is application-specific

There is no "magic scaling sauce" — a generic architecture that works for all problems. A system handling 100,000 × 1 kB requests/sec looks completely different from one handling 3 × 2 GB requests/min, even though both have the same total throughput. The bottleneck may be read volume, write volume, storage volume, data complexity, response time requirements, access patterns, or some combination. (source: chapter-01)

Scalable architectures are built around assumptions about which operations are common and which are rare. If those assumptions are wrong, the engineering investment is wasted — or worse, counterproductive. This is why quantifying [[load-parameters]] correctly is the prerequisite for any scaling decision.

For early-stage products, the ability to iterate quickly on features typically matters more than scaling for hypothetical future load.

## Related pages

- [[scalability]]
- [[load-parameters]]
- [[response-time-percentiles]]
- [[maintainability]]
