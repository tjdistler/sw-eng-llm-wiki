# Pod

**Summary**: An atomic container group that schedules multiple containers onto the same machine as a single unit and gives them shared Linux namespaces (filesystem paths, network, hostname, PID, etc.). The pod is the Kubernetes API object that makes single-node multi-container patterns like the [[sidecar-pattern]] possible.

**Sources**: `raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md`, `raw/designing-distributed-systems/chapter-03-ambassadors.md`, `raw/designing-distributed-systems/chapter-04-adapters.md`

**Last updated**: 2026-04-16

---

## What a pod provides

Burns introduces the pod as the mechanism that makes the sidecar pattern and the other single-node patterns work. Two properties are essential (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md):

1. **Atomic coscheduling** — all containers in the pod are scheduled onto the same machine, together. They start together and are moved or restarted together.
2. **Namespace sharing** — containers in the pod share parts of the filesystem, the hostname and network namespace, and other Linux namespaces (such as PID).

Atomic coscheduling is what distinguishes a pod from simply "two containers on the same host." If the container group is not atomic, the orchestrator might place the application container and its sidecar on different machines, and the sidecar could not reach the application via localhost or share its PID view.

## The shared resources that matter

The specific namespaces shared by pod containers are what make different single-node patterns possible (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md):

- **Network namespace** — a sidecar can reach the application on `127.0.0.1`, and external traffic to the pod's IP can be intercepted by the sidecar. This is how the nginx HTTPS sidecar terminates TLS and proxies cleartext to the app.
- **Filesystem paths (shared volumes)** — both containers read and write the same directory. This is how a configuration sidecar hands new config to the application, and how a git-pull sidecar feeds code into a Node.js server.
- **PID namespace** — a sidecar can see all processes in the application container. This is how a `topz` introspection sidecar reports on the application's resource usage without application-side instrumentation.

## Pod = the unit of deployment

Because a pod ties its containers together atomically, the pod is effectively the unit of deployment for single-node patterns. You deploy a pod; you get the application plus all its sidecars. Orchestration systems can inject standard sidecars (logging, metrics, mTLS) into every pod of an organization to deliver infrastructure capabilities uniformly (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md).

This uniform-injection capability is what elevates sidecars from a one-off trick to a piece of platform infrastructure — and it depends on the pod as the atomic boundary.

## Pods in relation to other concepts

### Pods and microservices

A pod is smaller than a [[microservices|microservice]]: it is the runtime packaging of one service's process (the application container) plus its local helpers (sidecars). Multiple replicas of the same pod can be run as a service. The microservice is the architectural unit; the pod is its on-node embodiment.

### Pods and independent deployability

Because the pod is atomic, the application container and its sidecar version together. Upgrading the sidecar — for example, rolling out a new mTLS proxy — is a pod redeploy. This is a mild tension with [[independent-deployability]]: the sidecar is now coupled to the application's deploy cadence, though it remains decoupled from the application's *source code*. In practice this trade is usually worth it, because sidecars tend to be general-purpose and upgraded less often than applications.

## Related pages

- [[sidecar-pattern]]
- [[ambassador-pattern]]
- [[adapter-pattern]]
- [[modular-reusable-containers]]
- [[designing-distributed-systems]]
- [[microservices]]
- [[independent-deployability]]
