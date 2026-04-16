# Local Developer Experience

**Summary**: As the number of services grows, running enough of them on a developer's laptop to make changes becomes painful or impossible. Mitigations include stubbing, hybrid local/remote setups, lightweight runtimes, and serverless — but the underlying tension never goes away and demands ongoing investment.

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Last updated**: 2026-04-16

---

## The squeeze

Newman's framing: he can run four or five JVM-based microservices on his laptop. Could he run ten or twenty? Probably not (source: chapter-05-growing-pains.md). Even with lighter-weight runtimes there's a ceiling — and once you hit it, the entire conversation about how to develop changes locally has to start.

Symptoms (source: chapter-05-growing-pains.md):

- Local builds and execution slow down as more services have to be stood up.
- Developers ask for bigger machines. That buys time, but only that.

## What makes it worse, and what makes it better

(source: chapter-05-growing-pains.md)

- **Heavyweight runtimes** (the JVM is the canonical example) hit the ceiling earlier. Lighter runtimes — Go, Node, Python — fit more services on a laptop.
- **Collective ownership** ([[code-ownership-models]]) makes it worse. Developers move across many services as part of normal work, so they need many services running. **Strong ownership** of a few services makes it easier — developers focus on their few services and stub out the rest.
- **The strength of stubbing infrastructure** is decisive. If stubbing services you don't own is easy and low-fidelity stubs are sufficient, the local box stays manageable.

## Mitigations Newman names

### Stub the rest

Run the few services you're actively changing. Replace everything else with a stub — local lightweight fake or a recorded replay (source: chapter-05-growing-pains.md). Strong-ownership teams tend to invest in this naturally.

### Point at remote instances

Run nothing locally; point your local development against shared remote instances (a dev or staging cluster). Eliminates the laptop ceiling entirely.

### Pure remote development

The whole environment lives on more capable infrastructure (source: chapter-05-growing-pains.md). Trade-offs:

- Requires connectivity. Remote workers and frequent travellers suffer.
- Slower feedback cycle if you have to push to the remote box on every change.
- Resource cost — every developer needs their own remote environment.

### Hybrid local/remote

Develop one service locally; let it talk to a remote cluster for everything else. Newman's named example: **Telepresence** for Kubernetes, which proxies calls between the local process and the remote cluster (source: chapter-05-growing-pains.md). **Azure Functions** offers a local-with-cloud-resources mode for serverless workflows.

## Newman's bigger point

> "Seeing how the developer experience changes as the number of services increases is important — so you need feedback mechanisms put in place. You'll need to continually invest to ensure that developers remain as productive as possible as the number of services they are working with increases." (source: chapter-05-growing-pains.md)

This isn't a one-time fix. As the architecture grows, the local-developer-experience problem will keep mutating. Treat it as something that needs ongoing investment and continuous measurement, not a problem you "solve" once.

## Connection to other Chapter 5 pains

- **[[code-ownership-models]]**: strong ownership reduces how many services any one developer needs to run, easing the squeeze.
- **[[end-to-end-testing]]**: large local test environments are partly the same problem in test clothing.
- **[[running-too-many-things]]**: the operational equivalent — at production scale, you need [[desired-state-management]] tools like Kubernetes; at developer scale, you need stubs and remote setups.

## Related pages

- [[code-ownership-models]]
- [[end-to-end-testing]]
- [[desired-state-management]]
- [[microservices]]
