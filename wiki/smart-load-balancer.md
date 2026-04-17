# Smart Load Balancer

**Summary**: A load balancer that applies the stream [[partitioning-strategies|partitioner]] to a request's key and consults the current [[consumer-group]] assignment table, so it can route the request directly to the microservice instance that owns that partition's [[internal-state-store|internal state]]. A latency optimization for [[serving-state-from-edm|serving state from an EDM]] that avoids the per-request redirect tax of round-robin balancing.

**Sources**: `raw/building-event-driven-microservices/chapter-13-integrating-event-driven-and-request-response-microservices.md`

**Last updated**: 2026-04-17

---

## The problem it solves

When an EDM serves materialized state from an [[internal-state-store]], each instance holds only its assigned partitions. A round-robin load balancer gets the request to the right instance with probability `1/N` for N instances (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). Every miss requires the receiving instance to redirect to the correct peer — adding a network hop and latency.

## How it works

The smart load balancer (source: chapter-13-integrating-event-driven-and-request-response-microservices.md):

1. Extracts the routing key from the request.
2. Applies the **same partitioner logic** used by the input streams to compute the partition ID.
3. Cross-references the partition ID against its internal view of **consumer-group assignments** (which partition is owned by which instance).
4. Forwards the request to the owning instance.

The partition-assignment data usually comes from the internal [[repartitioning|repartition streams]] or the [[changelog-stream]] of the relevant state store.

## The redirect fallback is still required

Smart load-balancer routing is **best effort, not correctness** (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). Between the balancer's last refresh and the request's arrival:

- The [[consumer-group]] may have rebalanced (instance added, removed, crashed).
- Partition ownership may have moved.

Each microservice instance must still be able to detect that an incoming request is for a partition it does not own and redirect to the current owner. The smart balancer just makes the redirect rare.

## The coupling cost

The balancer has to know the microservice's partitioner and topology. Renaming state stores, changing the partitioner, or reorganizing the topology can silently break routing (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). Bellemare's recommendation: **build the smart load balancer into the microservice's single deployable** — test and ship it alongside the service so topology changes are caught before production.

This is in contrast to a generic network-level load balancer that treats the backend as opaque.

## When it's worth it

- Large instance counts (`1/N` miss rate gets painful fast).
- Latency-sensitive user-facing reads.
- Stable topologies where the partition-to-instance mapping changes infrequently enough to be worth caching.

For small fleets the redirect cost is trivial and a plain round-robin balancer plus in-service redirects is simpler.

## Relationship to other routing patterns

This is a specific instance of the [[request-routing]] problem for partitioned databases, specialized for EDM. The mechanism mirrors client-side routing in Dynamo-style systems: the client (here, the load balancer) knows the hash function and the membership table and routes accordingly.

## Related pages

- [[serving-state-from-edm]]
- [[internal-state-store]]
- [[consumer-group]]
- [[partition-assignor]]
- [[partitioning-strategies]]
- [[request-routing]]
- [[changelog-stream]]
- [[repartitioning]]
- [[hot-replicas]]
