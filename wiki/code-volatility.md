# Code Volatility

**Summary**: The rate at which a piece of source code changes, measured from version-control history. Hard Parts Ch 7 names volatility-based decomposition as one of the six [[granularity-disintegrators|granularity disintegrators]]: high-volatility code mixed with low-volatility code in the same service drags the whole service onto the high-volatility deployment cadence, expanding test scope and deployment risk for code that didn't change.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md`

**Last updated**: 2026-04-19

---

## Why volatility matters at the service boundary

Every change to *any* part of a service forces the *whole* service to be retested and redeployed. If the service contains a function that changes weekly alongside functions that change every six months, then:

- **Testing scope** for the weekly change covers the entire service surface, not just the changed function.
- **Deployment risk** for the weekly change includes the risk of regressing the stable functions.
- **Availability** of the stable functions is interrupted by every weekly deploy.

Splitting along the volatility seam isolates the high-change code in its own service, shrinking testing scope and deployment risk for both sides (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md).

## The Notification Service example

Ford and Richards's worked case: one Notification Service handles SMS, email, and postal-letter notifications. Function-level change rates from version control:

- SMS: every six months (avg)
- Email: every six months (avg)
- Postal letter: weekly (avg)

The weekly postal-letter changes drag SMS and email through the test-and-deploy cycle every week. The honest split is **not** one service per notification method — it's two services grouped by volatility class:

- Electronic Notification Service (SMS + email; low change rate)
- Postal Letter Notification Service (high change rate)

Now the high-change code is isolated, and SMS/email functionality stays available during postal-letter deploys (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md).

The grouping shape is the key insight: **volatility-based decomposition cuts across functional cohesion when the change-rate signal is strong enough.** Two functions that differ in cohesion-by-purpose may belong together if their change cadence matches; two cohesive functions may belong apart if one churns and the other doesn't.

## Why this driver is unusually trustworthy

Most [[granularity-disintegrators]] involve subjective judgment. Volatility doesn't:

- It is **objectively measurable** from any modern source-control system. `git log --pretty=format:%H -- path/to/file | wc -l` is a one-liner.
- It is **historical**, not predictive — you're decomposing on what actually happened, not on what you guess will happen.
- It is **per-file or per-function**, so the signal is fine-grained enough to find the actual change boundary.

This makes volatility the disintegrator most useful for *suggesting* a split that other drivers (cohesion, scope) wouldn't have flagged on their own.

## Combining volatility with other disintegrators

Volatility rarely justifies a split alone, but it routinely tips a borderline case. The chapter's Notification Service walk-through shows volatility making the difference: cohesion alone said "don't split" (notification is one purpose), but volatility data revealed a clear seam.

Later in the chapter, [[fault-tolerance]] is added as a third driver, and the analysis converges on three services (SMS, Email, Letter). The compound conclusion comes from stacking the drivers: cohesion is OK with two services, volatility justifies two, fault tolerance + service-naming-test pushes to three. No single driver picked the final granularity; the trade-off across drivers did.

## Relation to instability metrics

Volatility is closely related to but distinct from the **instability** metric defined by Robert C. Martin (Ce / (Ce + Ca)) in [[coupling-metrics]]. Instability captures *structural* fragility — how exposed a module is to change in its dependencies. Volatility captures *behavioural* fragility — how often the module *actually* changes.

A module can be structurally stable (low Ce) but behaviourally volatile (frequent feature changes), or structurally unstable but rarely touched. Volatility-based decomposition uses the second signal; component-design metrics use the first. Both are useful; they answer different questions.

## Other places volatility shows up

- **Component decomposition** ([[component-based-decomposition]] / Hard Parts Ch 5): volatility helps identify components that should be sized down or moved to a different service.
- **[[architectural-checklists]]** (Fundamentals Ch 22): the software-release checklist is described as having "continuously growing volatility" — checklist content itself changes constantly as deployment surfaces evolve.
- **[[domain-driven-design]]**: high-volatility code often signals an emerging or splitting subdomain; the volatility seam may correspond to a yet-unrecognised [[bounded-context]] boundary.

## Related pages

- [[granularity-disintegrators]]
- [[service-granularity]]
- [[granularity-integrators]]
- [[architectural-modularity]]
- [[component-based-decomposition]]
- [[coupling-metrics]]
- [[deployability]]
- [[testability]]
- [[bounded-context]]
- [[software-architecture-the-hard-parts]]
