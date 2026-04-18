# Feature Flag Framework

**Summary**: SRE Chapter 27's infrastructure for rolling out individual features independently of binary releases. Not all changes warrant a full launch process — a UI tweak, a small A/B experiment, or an early-prototype feature preview shouldn't carry thousands-of-lines-of-code overhead. Feature flag frameworks let many changes roll out in parallel, each to a subset of servers/users/entities, and be reverted independently. Two general classes: UI-rewriter frameworks and request-routing frameworks for server-side business logic.

**Sources**: `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`

**Last updated**: 2026-04-17

---

## The case for feature flags

Not all launches are equal (source: chapter-27-reliable-product-launches-at-scale.md):

- Sometimes you want a small UI tweak; it shouldn't involve a heavyweight launch process.
- You may want to test hundreds of small changes in parallel.
- You may want to find out whether a sample of users enjoys an early prototype before investing months of engineering to harden it.

Pre-launch testing alone can't answer these questions — realistic test environments are impractical for many complex launches, and user response is inherently empirical. Feature flag frameworks complement pre-launch testing by letting observation of real behaviour under real workloads substitute for tests that would be infeasible.

## Framework requirements

Google's feature-flag frameworks meet a common set of requirements (source: chapter-27-reliable-product-launches-at-scale.md):

- **Parallel change rollout** — many changes in flight simultaneously, each to a few servers, users, entities, or datacenters.
- **Gradual expansion** — from 0 to a larger-but-limited group (usually 1–10%).
- **Routing by attribute** — direct traffic through different servers depending on users, sessions, objects, or locations.
- **Failure containment by design** — automatic handling of failure in new code paths, without affecting users.
- **Independent revert** — each change can be immediately reverted in the event of serious bugs or side effects.
- **Measurement** — the extent to which each change improves the user experience must be observable.

Each framework is itself hardened so that most of its applications need no [[launch-coordination-engineering|LCE]] involvement. The framework *is* the launch process for flag-gated changes.

## Two general classes

Chapter 27 splits Google's feature-flag frameworks into two classes (source: chapter-27-reliable-product-launches-at-scale.md):

### UI-rewriter frameworks

For user-interface changes in stateless services, the simplest realisation is an **HTTP payload rewriter at the frontend application servers**, limited to a subset of cookies or an equivalent request/response attribute. A configuration mechanism names:

- The identifier associated with the new code paths
- The scope of the change — cookie-hash-mod ranges, whitelists, blacklists

This covers the "does this small UI change improve things" class of experiments without touching server code paths.

### Server-side business-logic frameworks

For stateful services, feature flags are limited to a subset of **unique logged-in user identifiers** or to the actual **product entities accessed** — document IDs, spreadsheet IDs, storage object IDs. Rather than rewriting HTTP payloads, stateful services **proxy or reroute requests** to different servers depending on the change. This lets the change extend to improved business logic and more complex features, not just UI.

The difference between the two classes is where the fork lives in the stack:

| Class | Fork location | Change type it supports |
|---|---|---|
| UI rewriter | HTTP payload at frontend | UI changes in stateless services |
| Request routing | Traffic routing to a different backend | Business-logic, stateful, or complex features |

## Relationship to Newman's feature toggles

Newman's [[feature-toggle|feature toggle]] is the same idea framed from a microservices migration perspective — runtime switches for cutover and rollback. Chapter 27 adds:

- The explicit *framework* framing — the mechanism is infrastructure, not per-service code
- The distinction between UI-rewriter and request-routing styles
- The "hardened enough to not need LCE" rule — the framework absorbs the launch process for the changes that use it
- The **dormant functionality** pattern (see [[abusive-client-behavior]]): code for new functionality is hosted in the client before activation; activating it doesn't require shipping a new client version

See also [[progressive-delivery]] — the umbrella term.

## Why frameworks, not ad hoc flags

The chapter is deliberate: ad hoc feature flags sprinkled across services produce a governance mess — each one is a mini launch that needs its own rollout, its own monitoring, its own revert mechanism, its own review. A framework consolidates these into infrastructure, which:

- Concentrates the hardening investment
- Makes flag rollouts predictable and observable
- Removes the per-flag launch review

This is the feature-flag form of the **driving-convergence-on-common-infrastructure** principle [[launch-coordination-engineering|LCE]] applies throughout the chapter: one well-hardened framework beats many per-team reinventions.

## Related pages

- [[feature-toggle]]
- [[progressive-delivery]]
- [[gradual-rollout]]
- [[canary-test]]
- [[reliable-product-launches]]
- [[launch-coordination-engineering]]
- [[launch-checklist-themes]]
- [[abusive-client-behavior]]
- [[change-management-sre]]
- [[site-reliability-engineering]]
