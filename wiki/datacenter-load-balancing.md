# Datacenter Load Balancing

**Summary**: SRE Chapter 20 (Alejandro Forero Cuervo) covers the *intra-datacenter* layer of Google's load-balancing stack: once [[frontend-load-balancing|DNS and VIP]] have delivered a user's packets to a datacenter, how does a client task choose which backend task inside that datacenter to send each request to? The chapter develops the story in three pieces: identify and avoid bad backends ([[backend-task-states]] and [[lame-duck-state]]), limit the connection pool ([[subsetting]] with [[deterministic-subsetting]]), and select one backend per request ([[load-balancing-policies]] culminating in [[weighted-round-robin]]).

**Sources**: `raw/site-reliability-engineering/chapter-20-load-balancing-in-the-datacenter.md`

**Last updated**: 2026-04-17

---

## The problem Chapter 20 solves

Chapter 19 ended with packets arriving at a specific machine inside the right datacenter. Chapter 20 picks up from the opposite direction: assume a stream of queries is arriving to the datacenter at a rate the fleet can handle, and that the service is implemented as many homogeneous **backend tasks** (typical fleet: 100-1,000 tasks; smallest: at least 3; largest: more than 10,000). Other tasks are **client tasks** that hold connections to the backends. For each incoming query, the client must decide which backend receives it (source: chapter-20-load-balancing-in-the-datacenter.md).

The chapter's thesis is that distribution quality matters: in the ideal case the most and least loaded backends consume exactly the same CPU, and the cross-datacenter balancer can keep sending traffic until the hottest task hits its ceiling. In a poorly-balanced datacenter, capacity is *wasted* — the sum over all tasks of `(CPU[most-loaded] - CPU[i])` is reserved but unused. A service with 1,000 reserved CPUs but poor balancing might only be able to use 700 (source: chapter-20-load-balancing-in-the-datacenter.md).

## Google's stack context

Chapter 20 explicitly situates itself in Google's real stack (source: chapter-20-load-balancing-in-the-datacenter.md):

- External HTTP requests reach an edge HTTP reverse-proxy tier via the [[frontend-load-balancing|DNS + VIP]] layers of Chapter 19.
- The reverse proxy uses the Chapter 20 algorithms (plus the Chapter 19 ones) to route request payloads to the individual application processes that can handle them, based on URL-pattern configuration.
- Those application processes use the same Chapter 20 algorithms in turn when they call their own infrastructure and dependency services.
- A single incoming HTTP request can trigger a *long transitive chain* of dependent requests, potentially with high fan-out at various points.

Communication between clients and backends is over TCP and UDP, via Google's internal [[rpc|RPC framework]]. Everything in Chapter 20 assumes that substrate.

## The three arcs of Chapter 20

### 1. Identifying bad tasks

Before picking which healthy backend gets a request, a client has to know which backends are *not* healthy. The chapter develops two mechanisms (source: chapter-20-load-balancing-in-the-datacenter.md):

- **Flow control via active-request limits** — a simple first line of defence where a client stops sending to a backend when it has too many outstanding requests. Works against extreme overload but not much else.
- **[[backend-task-states|Three explicit backend states]] and [[lame-duck-state]]** — healthy / refusing-connections / lame-duck, with a clean-shutdown protocol that avoids serving errors during deployments, maintenance, and machine failures.

### 2. Limiting the connection pool

Every client-backend connection costs memory and CPU at both ends; the naive "every client connects to every backend" model doesn't scale to large fleets. [[subsetting]] limits how many backends each client connects to. The chapter contrasts two selection algorithms:

- [[random-subsetting]] — naive random shuffle; spreads load very unevenly (least-loaded at 63% / most at 121% for the 30%-subset case; even worse for smaller subsets) and is not practical.
- [[deterministic-subsetting]] — Google's round-based algorithm that assigns backends uniformly, handles restarts and resizes with minimal churn, and produces near-perfect connection distribution.

### 3. Load balancing policies

Once a healthy, bounded subset is in place, the client picks a backend per request. The chapter walks up a ladder of increasing sophistication (source: chapter-20-load-balancing-in-the-datacenter.md):

- [[simple-round-robin]] — the long-standing default; up to 2x CPU spread in practice because of small-subsetting bias, varying query costs, machine diversity, and unpredictable performance factors (antagonistic neighbours, task restarts).
- [[least-loaded-round-robin]] — filter to backends with the fewest active requests, then round-robin; better but *sinkholes* traffic to unhealthy fast-failing backends unless errors are counted as active requests; still leaves a 2x spread in large services.
- [[weighted-round-robin]] — backends report QPS, errors, and utilisation in every response; clients maintain per-backend capability scores and weight the round-robin accordingly. Significantly reduced spread in Google's production data.

## The ideal case and why it matters

Chapter 20 opens with a formalisation of "ideal" that is worth keeping in mind as the chapter gets more complicated: in the ideal case, all backends consume the same CPU at every instant, and the datacenter can be driven to the edge of the most-loaded task's ceiling. Any deviation from that ideal is *wasted capacity* — reserved but unused (source: chapter-20-load-balancing-in-the-datacenter.md).

This is not just a theoretical concern: the whole Chapter 20 ladder (flow-control → subsetting → weighted round robin) is designed to close the gap between the reserved fleet size and what the fleet can actually serve. The same logic drives Chapter 18's [[intent-based-capacity-planning|intent-based capacity planning]]: the whole point of good balancing is that the capacity plan's numbers can be trusted.

## Relationship to existing wiki concepts

### Chapter 20 and Chapter 19

Chapter 19 handles the *outside* of the datacenter ([[dns-load-balancing|DNS]] and [[virtual-ip-address|VIP]]); Chapter 20 handles the *inside* ([[subsetting|subsetting]] and [[load-balancing-policies|policies]]). Together they make up Google's four-layer load-balancing stack — DNS, VIP, service, RPC — that [[gslb|GSLB]] exposes to application teams.

### Chapter 20 and Burns's patterns

The [[replicated-load-balanced-service]] pattern assumes a load balancer picks a replica; Chapter 20 is the content of that choice at Google scale, for stateful long-lived RPC connections rather than short-lived HTTP. The "round-robin is the default" default in Burns lines up with Chapter 20's admission that round-robin was Google's most common approach for years — and with Chapter 20's evidence that it is not good enough past a certain scale.

### Chapter 20 and the SRE fundamentals

- [[capacity-planning]] — bad balancing directly wastes planned capacity; weighted round robin is the runtime mechanism that lets the capacity plan be honest.
- [[change-management-sre]] — [[lame-duck-state]] is the protocol that makes *every* code push and maintenance restart non-disruptive; without it, rolling deployments would serve errors to in-flight requests.
- [[health-probes]] — Burns's readiness-vs-liveness split gives a binary signal; Chapter 20's three-state model with lame duck is the RPC-world richer version.

## Related pages

- [[backend-task-states]]
- [[lame-duck-state]]
- [[subsetting]]
- [[random-subsetting]]
- [[deterministic-subsetting]]
- [[load-balancing-policies]]
- [[simple-round-robin]]
- [[least-loaded-round-robin]]
- [[weighted-round-robin]]
- [[frontend-load-balancing]]
- [[network-load-balancer]]
- [[gslb]]
- [[site-reliability-engineering]]
