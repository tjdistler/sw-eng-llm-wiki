# Google Frontend (GFE)

**Summary**: The HTTP server that terminates the TCP connection from a browser to Google. It is a **reverse proxy**: it inspects the requested service (web search, Maps, Shakespeare, etc.) and forwards the request to that service's frontend over [[stubby|Stubby]] RPC.

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`

**Last updated**: 2026-04-17

---

## Role in the request path

In the Chapter 2 Shakespeare walkthrough (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

1. The user's browser resolves `shakespeare.google.com` via DNS → [[gslb|GSLB]] picks a frontend IP.
2. The browser opens a TCP connection to that IP; a **Google Frontend (GFE)** terminates it.
3. The GFE looks up which service is required and uses [[gslb|GSLB]] to find an available service frontend.
4. The GFE sends the service frontend a Stubby RPC containing the HTML request.

GFE is therefore the edge proxy fronting every Google product. It is the equivalent of the dedicated edge tier that Burns's wiki pages split into [[ssl-termination]], [[caching-layer]], and [[rate-limiting]] — but collapsed into a single reverse-proxy binary and replicated globally via GSLB.

## Structural parallels

- [[ssl-termination]] (Burns) — GFE terminates TCP (and in practice TLS) at the edge, just like Burns's dedicated nginx tier.
- [[replicated-load-balanced-service]] (Burns) — GFE is a replicated stateless frontend behind a global load balancer.
- [[smart-load-balancer]] (Bellemare) — similar idea, but GFE routes by *service name* rather than by *partition-to-instance ownership*.

## Related pages

- [[gslb]]
- [[life-of-a-request]]
- [[stubby]]
- [[ssl-termination]]
- [[replicated-load-balanced-service]]
- [[site-reliability-engineering]]
