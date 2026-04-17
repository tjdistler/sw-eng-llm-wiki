# Service Brokering

**Summary**: A use of the [[ambassador-pattern]] in which an ambassador container introspects its deployment environment and brokers an appropriate connection to a dependency on the application's behalf. Makes applications portable across public cloud, private cloud, and on-premises environments without knowledge of the local binding mechanism. The system that performs the discovery-and-linking is called a **service broker**.

**Sources**: `raw/designing-distributed-systems/chapter-03-ambassadors.md`

**Last updated**: 2026-04-16

---

## The problem

Applications often need to connect to ambient services like MySQL, Redis, or a message queue. The *way* to connect to each of these varies across environments (source: raw/designing-distributed-systems/chapter-03-ambassadors.md):

- In a public cloud, MySQL may be offered as a managed SaaS (RDS, Cloud SQL) — find the SaaS endpoint and provide credentials.
- In a private cloud, MySQL might be provided by dynamically spinning up a virtual machine or container running MySQL — launch the VM/container, wait for readiness, learn its address.
- In an on-premises datacenter, it may be a pre-existing hostname provisioned through change-control processes.

A portable application would need to introspect its environment, choose the right strategy, and bind to the right endpoint. Baking all of that into the application couples it to every target environment's quirks.

## Service discovery and the service broker

Burns names this problem **[[service-discovery|service discovery]]** and the system that performs it a **service broker** (source: raw/designing-distributed-systems/chapter-03-ambassadors.md). The ambassador pattern separates the application from the service broker:

- The application always connects to an instance of the dependency running on `localhost` — `localhost:3306` for MySQL, for example.
- A **service-broker ambassador** in the same [[pod]] is responsible for introspecting the environment and brokering the appropriate connection. It listens on the expected localhost port and proxies the application's traffic to the real backend, wherever that is.

The application never knows whether today's MySQL is a SaaS instance, a freshly-launched private-cloud VM, or a legacy on-prem cluster. This lets the same application image run in all three environments unchanged.

## Why ambassadors fit

The pattern's win: the application container is free of environment-specific binding logic. The ambassador container encapsulates the variable part — how to find and connect to the dependency — and exposes the stable part — a local-protocol endpoint — to the application.

This is the same "separation of application logic from brokerage logic" argument Burns applies to sharding and request splitting. The ambassador is effectively a per-pod service-discovery client, factored out of the application process and into reusable container form (source: raw/designing-distributed-systems/chapter-03-ambassadors.md).

Because the ambassador is a separate container, it can also be reused across many different applications that all need MySQL (or Redis, or whatever the ambient dependency is). A single well-tested service-broker image can front every application in an organization.

## Relationship to existing wiki concepts

### Relationship to service discovery

This is exactly the [[service-discovery]] problem from DDIA's Chapter 6 — locating the right network endpoint for a given service across redundant or dynamically-provisioned machines — but implemented as a container-level pattern. The ambassador container is a per-pod service-discovery client whose output is a stable local endpoint rather than a returned IP address.

### Relationship to service mesh

A [[service-mesh]] data-plane proxy (Envoy, Linkerd-proxy) generalizes this: the local proxy handles service discovery, load balancing, and mTLS for *every* outbound dependency, not just one. A bespoke service-broker ambassador is the single-dependency, hand-rolled version of the same idea.

### Relationship to legacy modernization

A service-broker ambassador is a close cousin of the sidecar-style [[legacy-modernization]] pattern. Both take a deployment-time concern that the application cannot easily handle itself (TLS termination for a legacy HTTP service; environment-specific service discovery for a legacy hard-coded connection string) and externalise it into a coresident container.

### Relationship to RPC

Traditional [[rpc]] frameworks bundled service discovery into client libraries (gRPC in particular supports service discovery directly). The ambassador pattern is a language-agnostic alternative: the discovery logic runs in a container, not in every supported client language.

## Related pages

- [[ambassador-pattern]]
- [[service-discovery]]
- [[service-mesh]]
- [[pod]]
- [[legacy-modernization]]
- [[rpc]]
- [[information-hiding]]
- [[designing-distributed-systems]]
