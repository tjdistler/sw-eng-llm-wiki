# Intra-Layer Communication

**Summary**: SRE Chapter 22's "Always Go Downward in the Stack" principle. When a backend tier communicates *within* itself — backends proxying requests to other backends, cross-cluster peer synchronisation, primary-to-hot-standby handoff — three cascading-failure risks arise: **distributed deadlock** (mutually waiting on each other's thread pools), **sudden mode switches** (low intra-layer traffic in healthy state, high intra-layer traffic under load), and **bootstrap complexity**. Chapter 22's prescription: let the *client* mediate any retry or alternate-backend routing. If a backend is wrong, tell the client to retry on the right backend; don't proxy.

**Sources**: `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`

**Last updated**: 2026-04-17

---

## The framing

From Chapter 22 (source: chapter-22-addressing-cascading-failures.md):

> In the example Shakespeare service, the frontend talks to a backend, which in turn talks to the storage layer. A problem that manifests in the storage layer can cause problems for servers that talk to it, but fixing the storage layer will usually repair both the backend and frontend layers. However, suppose the backends cross-communicate amongst each other. For example, the backends might proxy requests to one another to change who owns a user when the storage layer can't service a request. This intra-layer communication can be problematic for several reasons...

The specific scenarios the chapter calls out:

### 1. Distributed deadlock

> The communication is susceptible to a distributed deadlock. Backends may use the same thread pool to wait on RPCs sent to remote backends that are simultaneously receiving requests from remote backends. Suppose backend A's thread pool is full. Backend B sends a request to backend A and uses a thread in backend B until backend A's thread pool clears. This behavior can cause the thread pool saturation to spread.

If A and B both hold threads waiting on each other (directly or via a chain), the pool is deadlocked until a timeout fires. Under load this condition is almost inevitable because the same thread pool serves both incoming and outgoing calls.

The naval metaphor: every cross-backend call is a potential [[bulkhead]] breach. If A's threads can be consumed by B's calls, A is not isolated from B's problems.

### 2. Sudden mode switches

> If intra-layer communication increases in response to some kind of failure or heavy load condition (e.g., load rebalancing that is more active under high load), intra-layer communication can quickly switch from a low to high intra-layer request mode when the load increases enough.

The dangerous pattern: in steady state, backends almost never talk to each other. Under load, they start proxying — and the proxying itself is additional work. A small load increase triggers a large mode switch in the system's behaviour, which is exactly the kind of discontinuity that produces cascading failure.

The chapter's concrete example:

> Suppose a user has a primary backend and a predetermined hot standby secondary backend in a different cluster that can take over the user. The primary backend proxies requests to the secondary backend as a result of errors from the lower layer or in response to heavy load on the master. If the entire system is overloaded, primary to secondary proxying will likely increase and add even more load to the system, due to the additional cost of parsing and waiting on the request to the secondary in the primary.

The primary's "help under load" mechanism turns into a load multiplier when load increases. The parsing, waiting, and holding of thread state on the primary add work on top of the fundamental request — and the secondary is likely under similar pressure.

### 3. Bootstrap complexity

> Depending on the criticality of the cross-layer communication, bootstrapping the system may become more complex.

A system that depends on backends talking to each other has a chicken-and-egg problem when starting from scratch: no backend can make progress until enough of its peers are up and responsive. This is a cold-start failure mode that doesn't exist when backends are independent.

## The prescription

The chapter's two-sentence rule (source: chapter-22-addressing-cascading-failures.md):

> It's usually better to avoid intra-layer communication — i.e., possible cycles in the communication path — in the user request path. Instead, have the client do the communication. For example, if a frontend talks to a backend but guesses the wrong backend, the backend should not proxy to the correct backend. Instead, the backend should tell the frontend to retry its request on the correct backend.

The pattern: **return a redirect, don't proxy**. The client has the routing information and can decide what to do. The backend remains stateless with respect to cross-backend topology and doesn't carry the thread-level cost of waiting on peers.

The rule formalises a broader principle — **data flows in one direction**, from client through frontend to backend to storage. Cycles in the graph are cycles in the failure mode.

## When intra-layer is unavoidable

Not all intra-layer communication is bad. Some systems legitimately require it:

- **Consensus groups** (Paxos, Raft) — members must communicate to agree on state.
- **Leader election** — peers must coordinate to pick a leader.
- **Gossip protocols** — membership and health propagate through peer connections.
- **Shard-to-shard redistribution** — during rebalancing.

The distinguishing feature: these communications are *control-plane* — they happen out of band from user requests, are bounded in volume, and their failure degrades the system but doesn't amplify user-request load. Chapter 22's warning is specifically about intra-layer communication *in the user request path* — that's the pattern with the feedback-loop risk.

## Relationship to other wiki concepts

### Intra-layer communication and [[bulkhead]]

The cross-backend thread-sharing Chapter 22 warns about is a [[bulkhead]] violation. Isolating outgoing-call threads from incoming-request threads — the per-dependency thread pool pattern — would prevent the distributed deadlock. But the chapter argues for something stronger: don't make the outgoing call in the user request path at all.

### Intra-layer communication and [[saga]]

[[saga]] patterns can take two forms: orchestrated (one service coordinates all others) or choreographed (services react to each other's events). The chapter's "have the client do the communication" rule is the orchestration principle applied to intra-layer: the client is the orchestrator. Choreographed sagas with cross-service reactions are more vulnerable to the intra-layer cascading risks Chapter 22 names, unless the choreography uses asynchronous messaging (brokers, queues) that decouples temporal dependencies.

### Intra-layer communication and [[event-driven-architecture]]

An [[event-driven-architecture]] pattern sidesteps the synchronous intra-layer problem entirely: backends emit events, other backends consume them asynchronously. There is no thread held waiting on a peer, so the distributed-deadlock risk disappears. The trade-off is eventual consistency and added infrastructure. For workloads that can tolerate async, the Chapter 22 risks vanish.

### Intra-layer communication and [[smart-load-balancer]]

Bellemare's [[smart-load-balancer]] pattern routes requests to the specific instance that holds the relevant state, avoiding the need for the receiving instance to proxy to the owning instance. This is a partition-aware realisation of Chapter 22's "let the client do the routing" rule: the *load balancer* is where routing decisions are made, not inside the service tier.

### Intra-layer communication and [[failover]]

Kleppmann's [[failover]] discussion covers the specific case of leader handoff after a primary fails. The chapter's warning about primary-to-secondary proxying in the request path is a *specific* failover anti-pattern: rather than the client discovering the new leader and reconnecting, the old leader forwards to the new one. This works in steady state but becomes a load multiplier during the precise conditions the failover mechanism is meant to handle.

### Intra-layer communication and [[fallacies-of-distributed-computing]]

"The topology doesn't change" and "latency is zero" are the distributed-computing fallacies that intra-layer-proxy designs implicitly assume. Chapter 22's warning is the engineering restatement: topology changes (a backend doesn't know the right backend anymore), and proxying isn't free (the proxy thread holds resources until the downstream returns). Both fallacies produce cascading failures reliably.

### Intra-layer communication and [[service-mesh]]

A [[service-mesh]] sidecar proxy implements much of this discipline by default: when a service wants to call a peer, the sidecar decides where to route and handles retries without the application process holding thread state. This is the intra-layer communication pattern done right: the routing is outside the application's thread model, so the application doesn't pay the resource cost of cross-backend coordination.

## Related pages

- [[cascading-failure]]
- [[bulkhead]]
- [[saga]]
- [[event-driven-architecture]]
- [[smart-load-balancer]]
- [[failover]]
- [[fallacies-of-distributed-computing]]
- [[service-mesh]]
- [[slow-startup-and-cold-caching]]
- [[site-reliability-engineering]]
