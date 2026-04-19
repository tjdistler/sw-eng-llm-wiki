# Interservice Communication Pattern

**Summary**: The default and most common [[distributed-data-access]] pattern: when a service needs data it doesn't own, it calls the owning service over the network. Simple, always fresh, no sync machinery — but slow, fragile, and couples the caller's availability and scalability to the owner's.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md`

**Last updated**: 2026-04-19

---

## The mechanics

The Wishlist Service needs product descriptions held by the Catalog Service. On every wish-list display, it makes a synchronous remote call, passing a list of `item_id`s and receiving the corresponding descriptions (source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md).

The protocol (REST, gRPC, request-reply messaging) doesn't change the trade-off profile much. What matters is that **a read request on one service becomes a read request on another**.

## The three latencies

Chapter 10's taxonomy of cost for each remote read:

| Latency | Typical range | Source |
|---|---|---|
| **Network latency** | 30–300 ms | packet transmission to and from the target service |
| **Security latency** | 20–400 ms | endpoint authorization (higher with stricter security) |
| **Data latency** | 10–50 ms | extra DB calls the callee must make to service the request |

Summed, a single interservice read can approach **one second** before the caller gets its first byte back (source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md). A monolith's SQL join did this in microseconds.

## Coupling costs

The pattern inherits two forms of [[coupling]]:

- **Static coupling** — the Wishlist Service cannot be deployed in isolation; it requires the Catalog Service's contract and its availability. See [[synchronous-microservices]] for why sync fan-out amplifies this.
- **Semantic coupling** — the Wishlist Service is unavailable whenever the Catalog Service is. No circuit breaker makes this not-a-fact.

Second-order: as the Wishlist Service **scales** to meet demand, the Catalog Service must scale too, because every wish-list render still lands on it. Independent scalability — a headline benefit of microservices — is lost.

## Trade-offs summary (Table 10-1)

| Dimension | Rating |
|---|---|
| Service dependency | **High** (static + semantic) |
| Response time | **Poor** (up to ~1s) |
| Data currency | **Excellent** — always fresh |
| Fault tolerance | **Poor** — owner down ⇒ reader down |
| Data volume | Any |
| Scalability | Coupled to owner |
| Complexity | **Lowest of the four patterns** |
| Contract versioning | API contract, tightly scoped |

(source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md, Table 10-1)

## When to use it

Chapter 10's stance: this is the right default **unless** one of its weaknesses disqualifies it — high request rates, tight latency budgets, or fault-tolerance requirements that don't survive transitive outages (source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md).

When those matter, move up the ladder: [[replicated-caching-pattern]], [[column-schema-replication-pattern]], or [[data-domain-pattern]].

## Related pages

- [[distributed-data-access]]
- [[column-schema-replication-pattern]]
- [[replicated-caching-pattern]]
- [[data-domain-pattern]]
- [[synchronous-microservices]]
- [[coupling]]
- [[static-coupling]]
- [[dynamic-coupling]]
- [[service-mesh]]
- [[fault-tolerance]]
- [[software-architecture-the-hard-parts]]
