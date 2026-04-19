# Strangler Fig Pattern

**Summary**: Newman's signature migration pattern, named after the strangler fig vine that envelops a host tree. A new microservice grows alongside the [[monolith]], intercepting calls at the perimeter and gradually replacing functionality, while the original system keeps running until each slice is migrated.

**Sources**: `raw/monolith-to-microservices/chapter-03-splitting-the-monolith.md`, `raw/fundamentals-of-software-architecture/chapter-01-introduction.md`, `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`

**Last updated**: 2026-04-18

---

## The metaphor

Martin Fowler captured the pattern in 2004, inspired by a fig vine that seeds itself in the upper branches of a tree, descends to take root, and gradually envelops the host. The original tree initially supports the fig; eventually it dies and rots away, leaving a self-supporting fig in its place (source: chapter-03-splitting-the-monolith.md).

In software, the new system initially wraps and is supported by the existing system; old and new coexist; the new gradually replaces the old. The big benefit is that migration is incremental and **each step is reversible** — you can pause or even abandon the migration and still keep the value of what's been done so far (source: chapter-03-splitting-the-monolith.md).

## Three steps

1. **Identify** the part of the existing system you want to migrate. Use [[extraction-prioritization|effort-vs-benefit prioritisation]].
2. **Implement** the functionality in a new microservice — possibly copying code from the monolith, possibly reimplementing.
3. **Reroute** calls from the monolith to the new service.

Until calls are redirected, the new functionality isn't *technically* live, even when deployed to production. This separation of [[deployment-vs-release|deployment from release]] is essential — you can deploy and exercise the new service in production while the monolith still handles all real traffic.

## When to use it

The strangler fig is Newman's first port of call (source: chapter-03-splitting-the-monolith.md). It works particularly well when:

- The monolith is a black-box (vendor product, SaaS, legacy system) you cannot or do not want to change.
- The monolith is being actively worked on by other teams and you want to avoid contention.
- The functionality to be migrated has a clear inbound entry point that can be intercepted at the system's perimeter.

It works less well when:

- Functionality is **deep inside** the monolith and triggered by multiple inbound calls (e.g. notifications fired from many places). Then [[branch-by-abstraction]] is usually better (source: chapter-03-splitting-the-monolith.md).
- The protocol between callers and the monolith is hard to intercept or transform.

## End-to-end vs shallow extractions

Some extractions are clean end-to-end slices (e.g. all of Inventory Management). Others are *shallow* — the extracted service still depends on functionality remaining in the monolith (e.g. Payroll still needs to call User Notifications). The shallow case requires exposing monolith functionality to the new service, which means changes to the monolith itself (source: chapter-03-splitting-the-monolith.md).

## Examples

### HTTP reverse proxy

The classic implementation. Insert a proxy (Newman suggests NGINX) between callers and the monolith and roll out in three sub-steps:

1. **Insert the proxy** that just passes calls through. Verify latency overhead and observability before going further. If latency is unacceptable, stop here.
2. **Build the new service** behind the proxy, deployed to production but not yet receiving redirected traffic. Initially it can return 501 Not Implemented.
3. **Redirect** the matching calls from monolith to service. Most proxies make this fast and easily reversible.

URL/resource-based redirection (e.g. moving the entire `/invoice` resource) is straightforward. Switching on a parameter inside a request body is harder and may require richer proxy capabilities (source: chapter-03-splitting-the-monolith.md).

### FTP (Homegate)

The Swiss real estate company Homegate intercepted FTP uploads by detecting changes in the FTP server log, then routed newly uploaded files to an adapter that translated them into REST calls to a new microservice. Customers continued to upload via FTP unchanged, but the new service published listings much faster. Both upload mechanisms ran in parallel during the cutover — a [[parallel-run-pattern|parallel run]] (source: chapter-03-splitting-the-monolith.md).

### Message interception

For monoliths driven by a message broker, two options:

- **Content-based router**: intercept all messages and filter them to the right consumer. Adds a "smart pipe" — Newman cautions against overuse.
- **Selective consumption**: the new service and the monolith share a queue, each filtering for the messages it cares about (e.g. via a JMS Message Selector). Avoids an extra hop but requires coordinated changes when redirecting.

Newman recommends selective consumption for small numbers of consumers with simple rules; content-based routing scales better but tends toward "smart pipes" (source: chapter-03-splitting-the-monolith.md).

## Changing protocols at the proxy: usually a bad idea

You *can* use the proxy to translate protocols (e.g. SOAP to gRPC). But complexity in shared middleware becomes contention across teams and undermines [[independent-deployability]]. Newman's advice — **"keep the pipes dumb, the endpoints smart"** — points to having the new service expose both the old and new protocols itself, then retire the old once consumers migrate (source: chapter-03-splitting-the-monolith.md).

A [[service-mesh]] is a hybrid that gives each service its own dedicated local proxy, avoiding a shared smart pipe.

## Other protocols and creative interception

The pattern generalises. If the monolith is driven by a batch file upload, intercept the file, extract calls you care about, forward the remainder. With creativity the strangler fig works in surprising places — Paul Hammant's blog has a list of ThoughtWorks projects that used it for a trading blotter, an airline booking system, a rail ticketing system, a classifieds portal, and more (source: chapter-03-splitting-the-monolith.md).

## Data is the missing piece

The strangler fig elegantly handles code migration but not data. If the new service needs data currently in the monolith's database, you need additional patterns covered in Chapter 4.

## Why Agile makes this pattern practical

Richards and Ford call out the strangler fig (alongside [[feature-toggle]]s) as a restructuring technique that Agile methodologies enable: "Agile methodologies support these kinds of changes better than planning-heavy processes because of the tight feedback loop and encouragement of techniques like the Strangler Pattern and feature toggles" (source: chapter-01-introduction.md). The pattern's step-by-step reversibility assumes that each step can be deployed, observed, and reverted quickly — a short-feedback-loop delivery pipeline is the substrate. On a Waterfall cadence the pattern's main advantage evaporates.

## In data architecture ([[brownfield-vs-greenfield|brownfield]] data projects)

Reis and Housley's Chapter 3 of *Fundamentals of Data Engineering* picks up the strangler pattern as the preferred tool for **brownfield data-architecture projects** — replacing a legacy data architecture with a new one (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md). The book contrasts it with big-bang overhauls, which they explicitly warn against: big-bang rewrites "often lead to disaster, with many irreversible and costly decisions."

The strangler pattern's attractions in a data setting are the same as in the original microservices setting: targeted surgical replacement; each step flexibly reversible; you can assess the impact of deprecating each old component on dependent systems before committing.

The caveat Chapter 3 adds: deprecation is sometimes impossible in practice — "legacy is a condescending way to describe something that makes money." When it *is* possible, demonstrate value on the new platform first, grow maturity gradually, then follow a planned exit.

## Related pages

- [[brownfield-vs-greenfield]]
- [[data-architecture]]
- [[incremental-migration]]
- [[deployment-vs-release]]
- [[parallel-run-pattern]]
- [[branch-by-abstraction]]
- [[decorating-collaborator-pattern]]
- [[feature-toggle]]
- [[service-mesh]]
- [[progressive-delivery]]
- [[migration-pattern-selection]]
