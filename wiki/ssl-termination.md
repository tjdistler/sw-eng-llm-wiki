# SSL Termination

**Summary**: Decrypting HTTPS at a dedicated edge tier — typically a replicated nginx layer — and forwarding plaintext (or re-encrypted) traffic inward. Burns positions this as the outermost of three stacked [[replicated-load-balanced-service]] tiers: nginx SSL → Varnish cache → application. Each layer should use its own certificate so layers can be rolled independently.

**Sources**: `raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md`

**Last updated**: 2026-04-16

---

## Why terminate at the edge

Handling TLS inside every application replica is possible but unattractive: certificates and key material proliferate, rotation is harder, and many application servers have weaker TLS stacks than a dedicated proxy. Terminating TLS at a small edge tier centralises certificate management and lets the inside of the cluster run simpler, plaintext (or re-encrypted with internal certs) traffic (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md).

In Burns's Chapter 5 stack, the cache tier (Varnish) cannot itself terminate TLS — Varnish does not speak SSL. A third tier is added in front of the cache: a replicated nginx tier dedicated to SSL termination, forwarding plaintext HTTP to Varnish.

## The complete stacked pattern

Chapter 5's closing figure shows the full three-tier composition (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md):

1. **nginx SSL tier** — external-facing; terminates HTTPS; forwards plaintext HTTP to the cache service.
2. **Varnish cache tier** ([[caching-layer]]) — absorbs repeated reads; forwards misses to the application tier.
3. **Application tier** — the original stateless dictionary-server replicas.

Each tier is itself a [[replicated-load-balanced-service]] — replicas + Kubernetes `Service` + [[health-probes|readiness probes]]. The three compose by pointing each tier's backend at the next tier's service DNS name. Only the outermost tier is exposed externally; the inner two are cluster-internal.

## Kubernetes mechanics

Burns's example (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md):

- **Certificate secret.** `kubectl create secret tls ssl --cert=server.crt --key=server.key` uploads the key and cert as a Kubernetes `Secret`.
- **nginx configuration.** An `nginx.conf` (stored in a `ConfigMap`) listens on `:443`, references the cert/key paths (mounted from the secret), and proxies to `http://varnish-service:80` — the DNS name of the cache-tier `Service`. Standard forwarding headers (`X-Forwarded-For`, `X-Forwarded-Proto`, `X-Real-IP`, `Host`) are set explicitly so the downstream tiers see the right values.
- **Deployment.** 4 nginx replicas, each mounting both the `ConfigMap` (config) and the `Secret` (certs) as volumes.
- **Service.** Exposed with `type: LoadBalancer` so the cloud provides an external IP. This is the only externally-routable piece of the stack.

## Separate certificates per layer

Burns's specific operational guidance: **even if you plan to use TLS between tiers, each tier should use its own certificate** (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md).

Why: shared certificates couple deploy cadences. Rotating a cert or swapping an algorithm in a shared cert forces every tier to redeploy in lockstep. Independent certs let each tier roll on its own schedule and recover from certificate incidents (expiry, compromise, rotation) without stopping the world.

This is a concrete instance of [[independent-deployability]] applied to cryptographic material: anything shared between services reintroduces deployment coupling.

## Self-signed certs and production

The chapter walks through self-signed certs with openssl for local testing but cautions explicitly that these cause security alerts in modern browsers and should never be used for production (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md). Let's Encrypt is the default recommendation for real certificates.

## Relationship to existing wiki concepts

### SSL termination and the sidecar HTTPS example

In Chapter 2, Burns's first [[sidecar-pattern]] worked example is an nginx sidecar adding HTTPS to a legacy HTTP service (see [[legacy-modernization]]). That is the same mechanism — nginx terminating TLS and proxying plaintext to a backend — applied at a different scope:

| Scope | Sidecar HTTPS (Chapter 2) | SSL termination tier (Chapter 5) |
|---|---|---|
| Unit | One pod, one legacy app | A fleet-wide edge |
| Backend hop | `localhost` | Cluster DNS to a downstream `Service` |
| Replication | 1:1 with the app | Its own independently-scaled tier |

Both are valid. The sidecar version fits retrofits and single-service deployments; the tier version fits whole-site serving stacks where the TLS tier scales differently than the cache or application.

### SSL termination and the service mesh

A [[service-mesh]] pushes mTLS into every pod's data-plane proxy — terminating and re-encrypting at each hop. That subsumes edge SSL termination for internal traffic but doesn't replace it at the true network perimeter: external clients still hit a public TLS endpoint first. In most mesh deployments, an edge tier (or cloud-managed L7 load balancer) still handles external TLS; the mesh handles TLS between services.

### SSL termination and the base pattern

The SSL tier is a third instance of [[replicated-load-balanced-service]] in the Chapter 5 stack. The same pattern — Deployment + Service + readiness probes + rolling upgrades — applies unchanged.

### SSL termination and rate limiting

The edge tier is a natural place to colocate [[rate-limiting]]. nginx can enforce rate limits directly (or pass through to Varnish's throttle module). Both features benefit from the same "parse HTTP at the edge, reject cheaply" property.

## Related pages

- [[replicated-load-balanced-service]]
- [[caching-layer]]
- [[rate-limiting]]
- [[sidecar-pattern]]
- [[legacy-modernization]]
- [[service-mesh]]
- [[independent-deployability]]
- [[designing-distributed-systems]]
