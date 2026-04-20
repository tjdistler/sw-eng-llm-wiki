# Subsetting

**Summary**: SRE Chapter 20's technique for limiting the set of backend tasks each client task talks to. Without subsetting, every client holds long-lived connections to every backend — a resource waste that grows quadratically with fleet size. Subsetting caps the pool at a small *subset size* (typically 20-100 backends per client) and uses a selection algorithm to decide which backends each client picks. Random selection spreads load badly ([[random-subsetting]]); Google's [[deterministic-subsetting]] algorithm distributes connections uniformly and handles restarts, failures, and fleet resizes with minimal churn.

**Sources**: `raw/site-reliability-engineering/chapter-20-load-balancing-in-the-datacenter.md`

**Last updated**: 2026-04-17

---

## The problem subsetting solves

Every client-to-backend connection in Google's internal [[rpc|RPC system]] is long-lived: it is established when the client starts and usually remains open, with requests flowing through it, until the client dies. Tearing down and reopening a connection per request has significant resource and latency cost, so the long-lived model is the default (source: chapter-20-load-balancing-in-the-datacenter.md).

Each connection costs memory and CPU at *both* ends, chiefly because of periodic health checks. In theory the overhead is small; across many machines it can become significant. Two pathological cases the chapter wants to avoid:

- **A single client connects to a very large number of backend tasks** (e.g. every backend in a 10,000-task service), wasting connection state proportional to the fleet size.
- **A single backend task receives connections from a very large number of client tasks**, paying health-check overhead on all of them.

Subsetting is the technique that avoids both: each client connects to only a bounded subset of the backend pool.

### An idle-connection optimisation

Chapter 20 mentions in passing that Google's RPC implementation also handles the corner case of a connection that stays idle for a long time: it switches to a cheap *inactive mode* with reduced health-check frequency, drops the underlying TCP connection in favour of UDP, and keeps just enough state to re-activate when a request arrives (source: chapter-20-load-balancing-in-the-datacenter.md). This is complementary to subsetting — it reduces the cost of the *bounded* set of connections a subset produces — but does not replace it. A very large set of idle connections still costs more than a small set.

## The two design knobs

A subsetting scheme has two independent design decisions (source: chapter-20-load-balancing-in-the-datacenter.md):

1. **Subset size** — how many backend tasks each client connects to.
2. **Selection algorithm** — which specific backends land in each client's subset.

### Picking the subset size

Typical Google subset sizes are **20 to 100 backends per client**. The right size depends on service behaviour (source: chapter-20-load-balancing-in-the-datacenter.md):

- **If there are significantly fewer clients than backends**, the subset has to be large enough that every backend is picked by at least some client; otherwise some backends receive no traffic.
- **If client load is unbalanced** — one client sends many more requests than its peers, or receives bursty fan-out traffic — the subset needs to be large enough that the bursts from a single client spread across many backends rather than hammering the small subset that one client happens to own.

The fan-out case is the archetypal problem: a social-network client receiving a "fetch information for all followers of user X" request will suddenly generate a huge burst of backend queries, all confined to that client's subset. If the subset is small, the burst is concentrated; if the subset is larger, the concentration dilutes across more backends.

### Requirements on the selection algorithm

The algorithm must satisfy several properties simultaneously (source: chapter-20-load-balancing-in-the-datacenter.md):

1. **Uniform backend load.** If the algorithm overloads one backend by 10%, the *whole* fleet has to be overprovisioned by 10% to accommodate it. Non-uniformity is paid for globally.
2. **Low churn on restart and failure.** When a backend fails, clients need to route around it; when a client restarts, it reopens connections. Either event creates connection churn, and churn costs CPU and introduces transient latency. The algorithm should minimise both.
3. **Graceful handling of resizes.** As the client or backend count grows or shrinks (e.g. during a progressive rollout of a new version, one task at a time), the subset assignment should change as little as possible. Critically, the algorithm must do this *without knowing the counts in advance* — the fleet can be scaled at any time.

Requirement 3 is especially tricky during one-at-a-time restarts for version pushes: clients should continue serving with minimal churn while the fleet on either side churns through.

## The two algorithms Chapter 20 compares

### Random subsetting

[[random-subsetting]] is the naive approach: each client shuffles the backend list once at startup and picks the first *subset_size* entries. The shuffle gives each client a stable subset (low restart churn), but the distribution is awful — with 300 clients × 300 backends at a 30% subset, the least-loaded backend gets 63% of the average load and the most-loaded gets 121%. Smaller subsets make it worse. Chapter 20 concludes that random subsetting needs subsets of 75% or more to spread load decently, which defeats the point of subsetting.

### Deterministic subsetting

[[deterministic-subsetting]] is Google's solution. Clients are grouped into *rounds*, where each round's clients collectively cover every backend exactly once. Within a round, the backend list is shuffled with a round-specific seed and partitioned into equal-size subsets; each client takes the subset corresponding to its position in the round. Different rounds use different seeds, so the subsets don't align across rounds — a failing backend's load redistributes across *all* remaining backends, not just within one subset.

For the same 300 × 300 × 10% case that random subsetting handles badly, deterministic subsetting gives each backend *exactly* the same number of connections.

## Relationship to existing wiki concepts

### Subsetting vs sharding

Subsetting is *not* the same as [[partitioning|sharding]] or [[sharded-service-pattern|sharded services]]. Sharding partitions *data* (or responsibility for data) across backends; different shards handle different data. Subsetting partitions *connections* across clients; every client-subset pair could in principle serve the same data. The analogue on the data side would be "every shard is replicated on every backend, and subsetting picks which replicas each client talks to."

### Subsetting and consistent hashing

[[consistent-hashing]] is another technique for achieving the third requirement (minimum disruption on fleet change), used extensively in CDN and packet-level load balancing. Chapter 20 does not use it for subsetting — the deterministic-subsetting algorithm achieves the same goal through a different mechanism (rounds with shared seeds) that also satisfies the first two requirements. Consistent hashing solves "which backend does this *key* go to"; deterministic subsetting solves "which backends does this *client* connect to." The design spaces overlap but don't coincide.

### Subsetting and the SRE tenets

- [[capacity-planning]] — the 10% overprovisioning Chapter 20 flags as the price of poor subsetting is exactly what the capacity plan has to absorb; good subsetting is a direct capacity savings.
- [[change-management-sre]] — one-at-a-time client/backend restarts during a push are the torture test for the selection algorithm; low churn is what makes progressive rollouts cheap.

## Related pages

- [[random-subsetting]]
- [[deterministic-subsetting]]
- [[datacenter-load-balancing]]
- [[load-balancing-policies]]
- [[capacity-planning]]
- [[consistent-hashing]]
- [[site-reliability-engineering]]
