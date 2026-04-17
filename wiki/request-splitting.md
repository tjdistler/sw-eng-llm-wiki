# Request Splitting

**Summary**: A use of the [[ambassador-pattern]] in which the ambassador container diverts a fraction of requests from the main production backend to an alternative (experimental or new) backend. Supports canary experiments, dark launches, and traffic teeing — the [[progressive-delivery]] techniques — at the pod level without changing application code. Most commonly implemented with an off-the-shelf proxy like nginx.

**Sources**: `raw/designing-distributed-systems/chapter-03-ambassadors.md`

**Last updated**: 2026-04-16

---

## What it is

In a production system it is often useful to route some fraction of requests away from the main implementation and toward a different one (source: raw/designing-distributed-systems/chapter-03-ambassadors.md). Common motivations:

- **Experimentation.** Evaluate a beta version of the service in real production traffic to check reliability and performance against the current version.
- **Teeing / shadow traffic.** Send every request to the production system *and* to the new service. Return the production system's response to the user; discard or separately log the new service's response. The new service is exercised with real load without risking impact to production users.

Both fit naturally into the ambassador shape: the application connects to `localhost`, the ambassador applies the splitting rule and proxies accordingly, and the application never knows which backend actually served any given request.

## How the ambassador version works

The chapter's mechanics (source: raw/designing-distributed-systems/chapter-03-ambassadors.md):

- The application issues requests to a backend at `localhost`.
- A request-splitting ambassador in the same [[pod]] receives those requests.
- Based on a configured rule, the ambassador routes each request to either production, an experimental backend, or both.
- The ambassador returns the production response to the application (or the appropriate response for the splitting mode), and the application proceeds as if it had spoken to a single backend.

The separation of concerns keeps each container slim and focused, and the modular factoring means the same request-splitting ambassador can be reused across many applications and settings.

## Hands-on: 10% experiments with nginx

Burns's worked example uses nginx as a weighted reverse proxy (source: raw/designing-distributed-systems/chapter-03-ambassadors.md):

```nginx
upstream backend {
    ip_hash;
    server web weight=9;
    server experiment;
}
server {
    listen localhost:80;
    location / {
        proxy_pass http://backend;
    }
}
```

Two rules do the work:

- **`weight=9`** on the production `web` server vs unweighted `experiment` server sends ~90% of traffic to production and ~10% to the experiment.
- **`ip_hash`** pins each user's IP to one upstream so that the user doesn't flip-flop between the experiment and production across requests. Burns flags this as important for ensuring every user has a consistent experience.

Deployment: the config is mounted into the pod via a `ConfigMap`; the ambassador is an `nginx` container in the pod with the production application alongside. Upstream services `web` and `experiment` must exist before the ambassador starts — nginx refuses to start if it can't resolve its proxies.

## The client-side / server-side trade-off

As with other ambassador uses, the splitting logic can live client-side (as an ambassador in each pod) or server-side (as a standalone proxy tier in front of the application). Burns's guidance (source: raw/designing-distributed-systems/chapter-03-ambassadors.md):

- If experimentation is **occasional**, a client-side ambassador is usually right — zero ongoing operational cost when it's not in use.
- If experimentation is a **longstanding component** of the architecture, it may be worthwhile to run it as a separate microservice in front of the application despite the extra service to maintain, scale, and monitor.

A [[service-mesh]] with traffic-shifting policy is the industrialized form of the server-side option.

## Relationship to existing wiki concepts

### Relationship to progressive delivery

Request splitting is one of the most direct implementations of [[progressive-delivery]] techniques. The same ambassador mechanism can realize all three variants catalogued on the progressive-delivery page:

- **Canary release** — a fraction of real users hit the new code; the rest hit production. Burns's 10% nginx example is a canary.
- **Dark launch** — the new backend is exercised but invisible to users. A request-splitting ambassador that tees traffic and discards the experimental response implements dark launching.
- **[[parallel-run-pattern|Parallel run]]** — both backends run on every call and their results are compared. The tee-and-compare variant of request splitting implements a parallel run at the pod level.

### Relationship to parallel run

Newman's [[parallel-run-pattern]] describes the technique at the migration-architecture level: run both implementations on every call, compare results, and treat one as authoritative. A teeing ambassador is one concrete mechanism for doing that; GitHub's Scientist library is an in-process alternative. The ambassador lets the same behaviour be applied to *any* application without language-specific code.

### Relationship to feature toggles

[[feature-toggle|Feature toggles]] are an alternative mechanism for controlling exposure to new behaviour: a runtime switch inside the application code. Request splitting at the ambassador level is complementary — it operates at the transport layer and needs no cooperation from the application. Organizations often use both.

### Relationship to service mesh

Modern service meshes ([[service-mesh]]) industrialize the request-splitting ambassador. Envoy and Linkerd-proxy support weighted routing and traffic mirroring as first-class features, configured centrally via the control plane. The ambassador pattern as Burns describes it is the hand-rolled, single-service version of the same capability.

## Related pages

- [[ambassador-pattern]]
- [[progressive-delivery]]
- [[parallel-run-pattern]]
- [[feature-toggle]]
- [[service-mesh]]
- [[deployment-vs-release]]
- [[pod]]
- [[sidecar-pattern]]
- [[designing-distributed-systems]]
