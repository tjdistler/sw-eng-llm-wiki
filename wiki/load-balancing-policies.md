# Load Balancing Policies

**Summary**: SRE Chapter 20's term for the *per-request* decision a client makes about which backend in its [[subsetting|subset]] receives the next request. The chapter walks up a ladder of three policies: [[simple-round-robin]] (no backend information; up to 2x CPU spread in practice), [[least-loaded-round-robin]] (tracks active-request count per backend; better but prone to sinkholing traffic to fast-failing unhealthy backends), and [[weighted-round-robin]] (backends self-report utilisation and error rates; clients maintain capability scores and pick proportionally). The distributed nature of the decision — many clients making choices in real time from stale partial state — is the root of most of the complexity.

**Sources**: `raw/site-reliability-engineering/chapter-20-load-balancing-in-the-datacenter.md`

**Last updated**: 2026-04-17

---

## The decision problem

Once [[backend-task-states|state management]] has eliminated unhealthy backends from consideration and [[subsetting]] has narrowed the pool to a bounded set, the client still has to pick *one* backend per request. Chapter 20 frames this as the load-balancing-policies question (source: chapter-20-load-balancing-in-the-datacenter.md).

What makes it hard:

- **Distribution.** Many clients are making choices in parallel, each with only its own view of its own backends.
- **Staleness.** Any information a client has about backend state is inherently a bit out of date.
- **Partiality.** A client sees only the traffic *it* sends; it doesn't see what other clients are doing.
- **Real-time.** The decision has to be fast — per-request, on the hot path.

Policies range from no information at all ([[simple-round-robin]], no backend state) to rich closed-loop feedback ([[weighted-round-robin]], backend-reported utilisation).

## The three-rung ladder

### Rung 1: Simple Round Robin

Each client round-robins through its healthy, non-[[lame-duck-state|lame-duck]] backends. No information; no state beyond a pointer (source: chapter-20-load-balancing-in-the-datacenter.md).

- **Pros:** dead simple; better than random.
- **Cons:** Chapter 20 reports **up to 2x spread** in CPU from least to most loaded task in practice. Causes: small subsetting (uneven client request rates), varying query cost (up to 1000x in Google), machine diversity (different CPUs), unpredictable performance (antagonistic neighbours, task restarts).

Google used Simple Round Robin as its most common policy *for years* and many services still do (source: chapter-20-load-balancing-in-the-datacenter.md). It is the pragmatic baseline.

### Rung 2: Least-Loaded Round Robin

Each client tracks the number of active requests per backend and round-robins among backends tied for the minimum (source: chapter-20-load-balancing-in-the-datacenter.md). The motivation: loaded backends should have higher latency, which accumulates as more active requests, which the filter then avoids.

- **Pros:** self-correcting for backends that are genuinely slow.
- **Cons (the big one):** **sinkholing traffic.** An unhealthy backend that serves fast `500` errors has *low* active-request counts and attracts *more* traffic, not less. Fixable by counting recent errors as active requests — which [[least-loaded-round-robin]] now always does.
- **Residual cons:** active-request count is a poor proxy for *capability* (most of a request's life is I/O waiting, which costs little); and each client sees only its own requests, not the aggregate load on the backend. In practice still around 2x spread at large services.

### Rung 3: Weighted Round Robin

Backends include QPS, errors/s, and CPU utilisation in *every response* (including responses to health checks). Clients maintain per-backend *capability scores* and distribute requests round-robin but weighted by score; failed requests are penalised (source: chapter-20-load-balancing-in-the-datacenter.md).

- **Pros:** the balancer sees the backend's *actual* load, including traffic from other clients, because the backend is reporting it directly. Figure 20-6 shows the CPU-distribution spread dropping sharply at the moment Google flipped a service from Least-Loaded to Weighted.
- **Cons:** more machinery; backends have to measure and report; clients have to maintain and adjust scores.

## Why information beats algorithmic cleverness

The progression from Simple → Least-Loaded → Weighted Round Robin is mostly about *getting more information into the decision*, not about smarter math. Simple Round Robin uses none. Least-Loaded uses active-request count, which the client can measure locally. Weighted Round Robin uses utilisation + error rate from the backend itself, which is the richest signal available.

This mirrors the general pattern of distributed-system decisions: with perfect information the decision is easy, and the engineering is mostly about how to get information out of the backends and into the clients cheaply. Chapter 20's specific mechanism — piggybacking metrics on every response, including responses to periodic UDP health checks ([[backend-task-states|state management]]) — means the signal is free of extra round trips.

## What the ladder doesn't solve

Chapter 20 is honest that even Weighted Round Robin has limitations. The underlying problems it lists for Simple Round Robin — **varying query cost** and **unpredictable performance factors** — are fundamentally about the workload and the environment, not the policy. Weighted Round Robin reduces their impact by reacting to observed utilisation, but it can't predict an expensive query before dispatching it, and it can't prevent an antagonistic neighbour from degrading a backend.

The chapter's other levers — capping per-request work (pagination), using `GCU` (Google Compute Units) to normalise across CPU types in the scheduler, and [[lame-duck-state|prewarming servers]] after restart — sit on the workload or platform side rather than in the policy itself.

## Relationship to existing wiki concepts

### Policies and the three-state model

The policies apply *only* to backends in the healthy state. Backends in "refusing connections" or [[lame-duck-state|lame duck]] are removed from consideration before the policy runs. The policies can still get into trouble on healthy-but-silently-broken backends (the Least-Loaded sinkhole case) — Chapter 20's solution is to teach the policy about errors as a proxy for load, which is a policy-internal fix rather than a state-model extension.

### Policies and subsetting

Subsetting determines the *candidate pool* the policy picks from. The interaction matters: Simple Round Robin works worst with small subsets (one client's hot traffic hits a small number of unlucky backends), which is one of Chapter 20's explicit reasons Simple is weak. Weighted Round Robin is less sensitive because it responds to observed load.

### Policies and Burns's load balancer

Burns's [[replicated-load-balanced-service]] mentions round-robin as the default. Chapter 20 is the detailed why-it's-not-enough argument: the 2x CPU spread Burns's default produces is what Chapter 20 is explicitly trying to avoid.

### Policies and the network-layer balancer

The [[network-load-balancer|Chapter 19 packet-level balancer]] also picks backends (least-loaded, hash-mod-N, consistent-hashing); the mechanisms are different because they operate on packets rather than RPCs. Chapter 20's policies are the *application-layer* balancer, running inside each client task in the [[rpc|RPC framework]].

### Policies and Weighted Round Robin as a closed loop

The capability-score-update cycle is a [[architecture-fitness-function|fitness-function-like]] control loop: observe backend utilisation, adjust weights, observe again. It is also the RPC-level instance of the pattern [[desired-state-management|desired-state management]] uses at the orchestration level: continuous reconciliation of observed against desired.

## Related pages

- [[simple-round-robin]]
- [[least-loaded-round-robin]]
- [[weighted-round-robin]]
- [[datacenter-load-balancing]]
- [[subsetting]]
- [[backend-task-states]]
- [[lame-duck-state]]
- [[network-load-balancer]]
- [[replicated-load-balanced-service]]
- [[site-reliability-engineering]]
