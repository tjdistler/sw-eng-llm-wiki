# Client-Side Sharding

**Summary**: A specific use of the [[ambassador-pattern]] in which the logic that maps requests to shards of a [[partitioning|sharded]] backend lives in an ambassador container coresident with the client. The application connects to what it believes is a single backend on `localhost`; the ambassador proxy translates each request to the correct shard. An alternative to building the sharding logic into a server-side load balancer.

**Sources**: `raw/designing-distributed-systems/chapter-03-ambassadors.md`, `raw/designing-distributed-systems/chapter-06-sharded-services.md`

**Last updated**: 2026-04-16

---

## The problem

When storage outgrows a single machine, the data layer is split across machines into disjoint [[partitioning|shards]]. Somewhere in the system there must be logic that routes each request to the correct shard (source: raw/designing-distributed-systems/chapter-03-ambassadors.md).

Two common difficulties:

- **Retrofitting clients.** Existing application code was written for a single storage backend. Teaching every client to be shard-aware — via a library change, connection-pool change, or query rewrite — is invasive and error-prone.
- **Dev/prod parity.** Development environments often have one shard; production has many. Sharing a single configuration between the two is awkward when the client is shard-aware.

## Two deployment options for the sharding logic

Burns is explicit that the sharding logic can live in either place (source: raw/designing-distributed-systems/chapter-03-ambassadors.md):

1. **Server-side load balancer** — a stateless load balancer fronts the shards and routes each request. Burns describes this as "a distributed ambassador as a service." Clients stay simple but the sharded service has a more complex deployment.
2. **Client-side ambassador** — a sharding proxy runs as an ambassador container in each client's [[pod]]. The client connects to `localhost`; the ambassador routes to the correct shard. Deployment of the sharded service is simpler; deployment of the client is more complex.

Burns stresses that "either choice is valid" and that the selection depends on team boundaries, whether you are writing code or deploying off-the-shelf software, and other particulars (source: raw/designing-distributed-systems/chapter-03-ambassadors.md). This page focuses on the client-side option.

## How the ambassador version works

The chapter's mechanics (source: raw/designing-distributed-systems/chapter-03-ambassadors.md):

- The application frontend or middleware is unchanged: it opens a TCP connection to, say, `localhost:6379` (for Redis) and issues protocol-level commands.
- In the same pod, a sharding-proxy container listens on that port. The "single backend" that the application sees is this ambassador.
- The ambassador knows the shard topology and the hash function. For each command, it picks a shard, sends the command, awaits the reply, and returns it to the application.

Net effect: the application container's code only knows it needs to talk to a storage service and discovers that service on `localhost`. The sharding ambassador contains only the sharding logic. The two can evolve independently.

Like all good single-node patterns, this ambassador can be reused across many different applications, or an off-the-shelf open-source implementation can be dropped in (source: raw/designing-distributed-systems/chapter-03-ambassadors.md).

## Hands-on: sharded Redis via twemproxy

The chapter's worked example deploys Redis as a three-replica sharded service behind a twemproxy ambassador (source: raw/designing-distributed-systems/chapter-03-ambassadors.md):

- **Sharded backend.** A Kubernetes `StatefulSet` runs three Redis replicas (`sharded-redis-0`, `-1`, `-2`). A headless `Service` exposes per-replica DNS names (`sharded-redis-0.redis`, etc.).
- **Ambassador config.** A `nutcracker.yaml` configuration tells twemproxy to listen on `127.0.0.1:6379`, hash keys with `fnv1a_64`, distribute via `ketama` (a form of [[consistent-hashing]] originally associated with memcached), and route to the three DNS names as shard servers. The config is mounted into the pod via a `ConfigMap`.
- **Ambassador pod.** A pod defines a `twemproxy` container from the `ganomede/twemproxy` image running the `nutcracker` binary with the mounted config. The application container slot is left open — the pod spec is designed so that any application container can be dropped in alongside the ambassador.

**twemproxy** is a lightweight, high-performance proxy for memcached and Redis originally developed at Twitter and open-sourced on GitHub (source: raw/designing-distributed-systems/chapter-03-ambassadors.md). It is a ready-made off-the-shelf sharding ambassador.

Once deployed, the application's Redis client sees `127.0.0.1:6379` and speaks the Redis protocol normally. twemproxy hashes each key, picks one of the three backends, forwards the command, and returns the reply.

## Separation of concerns

The pattern's payoff (source: raw/designing-distributed-systems/chapter-03-ambassadors.md):

- **Application container** — knows only that it needs a storage service on `localhost`. It carries zero sharding code.
- **Sharding ambassador** — contains only the sharding logic. No business logic intrudes.

Either container can be swapped, upgraded, or reused without affecting the other. This is [[information-hiding]] at the deployment layer: the sharding scheme's internals are hidden behind a stable `localhost` protocol.

## Relationship to existing wiki concepts

### Relationship to request routing

DDIA's [[request-routing]] chapter enumerates three approaches for finding the right partition for a key: contact any node (node forwarding), a dedicated routing tier, or client-side awareness. A client-side sharding ambassador is a particular implementation of **client-side awareness**, except the awareness is factored out of the application process and into a coresident container — so the application itself stays routing-agnostic. The ambassador is, in effect, a per-pod routing tier.

### Relationship to consistent hashing

The twemproxy example uses the `ketama` distribution, which is a form of [[consistent-hashing]]. The ambassador applies the hash function to each key and maps the hash to one of the configured shard servers. Adding or removing a shard redistributes only a small fraction of keys — the usual consistent-hashing property — without requiring coordination through the application.

### Relationship to sharded services (Chapter 6)

Chapter 3 is explicit that it does not discuss *how* the sharded service came to exist — only how a client connects to one (source: raw/designing-distributed-systems/chapter-03-ambassadors.md). Burns's [[sharded-service-pattern|Chapter 6]] covers sharded services as a multi-node serving pattern; the ambassador is the single-node counterpart on the client side.

Chapter 6's hands-on deploys the sharded backend as a Kubernetes `StatefulSet` of memcached pods with stable per-replica DNS names, and then explicitly contrasts two deployment options for the sharding proxy (source: raw/designing-distributed-systems/chapter-06-sharded-services.md):

- **Per-pod twemproxy ambassador.** This page's subject; `localhost` endpoint, one ambassador per client pod.
- **Shared shard-router service.** A [[replicated-load-balanced-service]] of twemproxy pods fronted by a service name that clients resolve. Reduces per-client complexity at the cost of an extra network hop and another scalable service to operate. See [[sharded-service-pattern#Deployment variants: ambassador vs shared routing service]].

Both are valid; the choice depends on how permanent the sharding logic is, how tight the latency budget is, and where team boundaries fall. The trade-off mirrors the client-side-vs-server-side discussion in [[ambassador-pattern]].

## Related pages

- [[ambassador-pattern]]
- [[partitioning]]
- [[partitioning-strategies]]
- [[consistent-hashing]]
- [[request-routing]]
- [[service-discovery]]
- [[pod]]
- [[service-mesh]]
- [[information-hiding]]
- [[sharded-service-pattern]]
- [[sharded-cache]]
- [[designing-distributed-systems]]
