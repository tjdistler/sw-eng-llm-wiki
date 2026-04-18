# Intent-Based Capacity Planning

**Summary**: Chapter 18's proposed replacement for manual capacity planning: programmatically encode a service's **intent** (dependencies, performance metrics, prioritisation) and let a solver auto-generate an allocation plan. The approach turns capacity planning from a brittle spreadsheet-driven exercise into a computation that can be re-run on any change. [[auxon|Auxon]] is Google's implementation.

**Sources**: `raw/site-reliability-engineering/chapter-18-software-engineering-in-sre.md`

**Last updated**: 2026-04-17

---

## The motto

> Specify the requirements, not the implementation. (source: chapter-18-software-engineering-in-sre.md)

The shift is from **demand** ("I need 50 cores in cluster X") to **intent** ("I want my service to run at five nines of reliability"). Given the intent and the constraints, the implementation falls out of the optimisation; humans stop trying to pack bins by hand.

## The chain of abstraction

Chapter 18 walks up four rungs of a ladder, moving from concrete resource request to true intent (source: chapter-18-software-engineering-in-sre.md):

1. **"I want 50 cores in clusters X, Y, and Z for service Foo."** — An explicit resource request. No flexibility, no rationale.
2. **"I want a 50-core footprint in any 3 clusters in geographic region YYY for service Foo."** — Introduces degrees of freedom. Still doesn't explain why.
3. **"I want to meet service Foo's demand in each geographic region, and have N + 2 redundancy."** — Now the *reason* is visible; we can reason about what happens if the requirement can't be met.
4. **"I want to run service Foo at 5 nines of reliability."** — The abstract form. Ramification of missing the target is clear (reliability suffers). Maximum flexibility: the optimiser can choose the deployment shape, not just the bin-packing.

Google's experience: the sweet spot is around rung 3 — enough flexibility to matter, still human-understandable. Sophisticated services aim for rung 4. The system should support all rungs simultaneously; services benefit more as they move up.

## Precursors to intent

Three pieces of information must be captured to encode a service's intent (source: chapter-18-software-engineering-in-sre.md):

### Dependencies

Services depend on other services, with constraints on where dependencies can be placed relative to their consumers (for example "Bar must be within 30 ms network latency of Foo"). Dependencies are nested — placing Foo means jointly placing Bar, Baz (Bar's dependency), and Qux (Bar's other dependency). Shared dependencies can appear with different stipulations from different dependents.

### Performance metrics

The "glue" that converts demand in one resource into demand in another. How many CPU cores does Foo need to serve N queries per second? For every N queries of Foo, how many Mbps does Bar need? These are derived via load testing or resource-usage monitoring and are what makes the chain of dependencies quantitatively solvable.

### Prioritisation

Under resource scarcity, something must give — and intent-based planning forces the choice to be **transparent, open, and consistent**. Is N + 2 redundancy for Foo more important than N + 1 for Bar? Is the launch of X more important than Baz's N + 0 redundancy? Traditional capacity planning makes these trade-offs ad hoc and opaque; intent-based planning makes prioritisation an explicit input of whatever granularity the team wants.

## What the model delivers

Once intent is captured, the payoffs accumulate (source: chapter-18-software-engineering-in-sre.md):

- **Responsive to change** — if demand, supply, or requirements change, regenerate the plan. No manual propagation across quarters.
- **Optimal given constraints** — modern solvers can reach known-optimal solutions for many classes of what used to be intractable bin-packing problems. Bin packing is NP-hard in general but tractable in many specific cases.
- **Reduced human toil** — SREs stop spending their time scrounging for resources at the task level and start working at the SLO / production-dependency / infrastructure-requirement level.
- **Cost savings** — computational optimisation finds denser packings than human-by-hand, and decisions cascade automatically.

## Against the alternative

See [[traditional-capacity-planning]] for the problem this replaces — demand-driven, brittle, laborious, imprecise, and trapped in spreadsheets. Intent-based planning inverts every one of those properties.

## Cross-book connections

- [[capacity-planning]] — Chapter 1's one-page tenet gets its industrial-strength implementation in Chapter 18
- [[desired-state-management]] (Newman) — intent-as-specification + solver-produces-plan + automation-enacts-plan is the declarative-desired-state pattern applied to capacity. The *what* is intent; the *how* is computed; the *reconciliation* is someone else's job (Auxon is deliberately agnostic about who)
- [[architecture-fitness-function]] (Richards & Ford) — the intent constraints (latency bounds, redundancy levels, geographic requirements) are objective automatable integrity assessments; the unmet-requirements list in the allocation plan is a fitness-function failure report
- [[declarative-vs-imperative-queries]] (Kleppmann) — intent-based planning is the declarative end of the same distinction: say *what* you want, let the system figure out *how*

## Related pages

- [[auxon]]
- [[traditional-capacity-planning]]
- [[software-engineering-in-sre]]
- [[capacity-planning]]
- [[desired-state-management]]
