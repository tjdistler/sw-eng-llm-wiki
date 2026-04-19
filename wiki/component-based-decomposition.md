# Component-Based Decomposition

**Summary**: Richards and Ford's preferred decomposition approach for monoliths that have *some* internal structure. Rather than cloning and deleting ([[tactical-forking]]), refactor the existing monolith to refine its [[components]], then extract those components into services — incrementally, in a controlled fashion (source: raw/software-architecture-the-hard-parts/chapter-04-architectural-decomposition.md). Chapter 5 of *The Hard Parts* catalogues six individual refactoring patterns that compose in sequence; this page is the **hub page** — when to choose this approach, what the whole trajectory looks like, and how the six patterns fit together.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-04-architectural-decomposition.md`, `raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md`

**Last updated**: 2026-04-19

---

## The approach in one sentence

> Refactor source code in the existing monolith to arrive at a set of well-defined components, then extract those components as services (typically first to a [[service-based-architecture]], and then — if needed — to [[microservices]]). (source: chapter-04-architectural-decomposition.md)

The emphasis is on **build services from components, not individual classes** (source: chapter-04-architectural-decomposition.md). A component — manifested in the codebase as a namespace or directory structure with a well-defined role and a stable set of operations — is the unit of decomposition. Extracting one class at a time produces a fine-grained mess; extracting whole components produces coherent services.

## When to choose it over tactical forking

Chapter 4 offers an explicit decision tree (source: chapter-04-architectural-decomposition.md):

1. **Is the codebase decomposable at all?** If not — because it is too degraded ([[big-ball-of-mud]]) or because metrics show systematic structural rot across most components — neither approach is tractable on its own; rewrite or retire may be the honest answer. Decomposability is assessed via the [[coupling-metrics]] from *Fundamentals* Chapter 3 (afferent/efferent coupling, abstractness, instability, distance from the main sequence) plus architect judgement.
2. **If decomposable, are there observable components?** The question is whether source files are organised so that *like functionality clusters inside well-defined (or even loosely defined) components* — typically visible in namespaces / directory structures. If **yes**, component-based decomposition is the right path. If **no**, fall through to [[tactical-forking]].

Put differently: component-based decomposition is the path the chapter *prefers*. Tactical forking is the pragmatic fallback when the codebase is too structurally weak for the preferred path.

## Why the migration runs *through* service-based architecture

Richards and Ford's recommended trajectory for most monolith-to-microservices migrations:

1. **Start with a monolith** (modular or not).
2. Apply the Chapter 5 component-based decomposition patterns to refine components inside the monolith.
3. Extract components into a **[[service-based-architecture]]** (4–12 coarse-grained domain services, single shared database, separately deployed UI).
4. Evaluate whether further granularity is needed (per Chapter 7). Some domains stay as coarse-grained domain services forever; others decompose further into [[microservices]] (source: chapter-04-architectural-decomposition.md).

The reason to stop at service-based architecture as an intermediate checkpoint:

- **No database decomposition required yet.** Service-based architecture keeps the shared database, so the architect can focus on *domain* and *functional* partitioning before tackling the hardest problem (data — Chapter 6).
- **No operational-automation requirement.** Domain services can be deployed using the same artifact format (EAR, WAR, assembly) as the original monolith. Containerisation, orchestration, service meshes are optional.
- **It's a technical migration, not an organisational one.** Service-based architecture doesn't require changing the IT org structure, the QA process, or the deployment environments. That makes the migration cheaper and less politically fraught than a direct monolith-to-microservices jump (source: chapter-04-architectural-decomposition.md).

The chapter's bottom line:

> When migrating monolithic applications to microservices, consider moving to a service-based architecture first as a stepping-stone to microservices. (source: chapter-04-architectural-decomposition.md)

See [[service-based-architecture]] for the style's full treatment.

## The six Chapter 5 patterns, in order

Chapter 5 decomposes the approach into six patterns that **compose**: each produces an input for the next, and together they transform a monolith into a [[service-based-architecture]] (source: raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md).

1. **[[identify-and-size-components-pattern]]** — Catalogue every component and measure its size (statements per namespace). Rebalance outliers — split the oversized ones, absorb the undersized ones. Outputs the **component inventory** everything downstream uses.
2. **[[gather-common-domain-components-pattern]]** — Find domain logic (notification, auditing, formatting, validation) duplicated across components and consolidate it. Distinguished carefully from *infrastructure* cross-cutting. Uses a root-namespace heuristic (`.shared`, `.common`).
3. **[[flatten-components-pattern]]** — Enforce that every class lives in a leaf-node namespace. Orphaned classes sitting in root namespaces get either pulled down into the root (making it a leaf) or pushed up into new leaf components. Every class ends up owned by exactly one component.
4. **[[determine-component-dependencies-pattern]]** — Visualise afferent/efferent coupling **between components** (not classes). The resulting graph answers the three CIO questions: is decomposition feasible, what's the effort (golfball / basketball / airliner), refactor or rewrite? An airliner graph is a "run in the opposite direction" signal.
5. **[[create-component-domains-pattern]]** — Group components into coarse-grained logical **domains** that share a namespace prefix (`ss.customer.*`, `ss.ticket.*`). Usually requires namespace renaming to align. Domains become service candidates in the next pattern.
6. **[[create-domain-services-pattern]]** — Physically extract each domain as its own separately deployed service. The output is a [[service-based-architecture]] — the "soft landing" recommended before deciding whether to go further into [[microservices]].

Each pattern has its own [[architecture-fitness-function|fitness functions]] for ongoing governance; the components keep drifting during the migration, and the governance keeps them in shape. See each pattern page for the specific fitness functions.

The **[[component-identification-cycle]]** from *Fundamentals* Chapter 8 is the closest analog at the concept level — the same iterative loop (identify → assign requirements → analyse roles → analyse characteristics → restructure) — but it is designed for greenfield component design. The Chapter 5 patterns are the *brownfield* counterpart, operating on an existing codebase.

## Contrast with tactical forking

| Dimension | Component-based decomposition | [[tactical-forking]] |
|---|---|---|
| Starting condition | Codebase has identifiable components | Codebase is a [[big-ball-of-mud]] |
| Strategy | Refactor in place, then extract | Clone, then delete |
| Up-front analysis | Substantial (months) | Minimal (days) |
| Resulting services | Clean, component-aligned | Coarse-grained, still carry latent mud |
| Typical granularity | Service-based architecture (4–12) → microservices | Two to four coarse services |
| When the architect picks it | Preferred path whenever the codebase permits | Pragmatic fallback |

## When it doesn't work

Component-based decomposition fails gracefully into tactical forking under two conditions:

1. **No component structure to work with.** If namespaces are meaningless, if shared state lives everywhere, if there are no namespaces at all — there's nothing to refine. The prerequisite for the approach doesn't exist.
2. **Organisational timeline is shorter than the refactor.** Even when components exist, the refactoring work can take months. Businesses with shorter runway (or a burning platform) may not be able to wait for the clean approach.

In either case, [[tactical-forking]] is the pragmatic second-best, and [[trade-off-analysis]] is how the architect justifies the switch rather than treating it as a failure mode.

## Relationship to Newman's patterns

Newman's [[monolith-to-microservices]] catalogue ([[strangler-fig-pattern]], [[branch-by-abstraction]], [[parallel-run-pattern]], etc.) overlaps with component-based decomposition but uses different vocabulary:

- Both assume a codebase with identifiable seams — Feathers's [[seams-and-legacy-code|seam]] concept and "components" are close siblings.
- Newman's patterns focus on *how to move the call-path* (perimeter interception, abstraction-swap, data-change triggers). The *Hard Parts* Chapter 5 patterns focus on *how to shape the codebase* before any extraction happens.
- The two are complementary: component-based decomposition prepares the monolith for an extraction; strangler fig / branch by abstraction is one way to execute the extraction itself. See [[migration-pattern-selection]] for the combined selection frame.

## Related pages

- [[identify-and-size-components-pattern]]
- [[gather-common-domain-components-pattern]]
- [[flatten-components-pattern]]
- [[determine-component-dependencies-pattern]]
- [[create-component-domains-pattern]]
- [[create-domain-services-pattern]]
- [[tactical-forking]]
- [[big-ball-of-mud]]
- [[coupling-metrics]]
- [[components]]
- [[component-identification-cycle]]
- [[service-based-architecture]]
- [[modular-monolith]]
- [[microservices]]
- [[strangler-fig-pattern]]
- [[branch-by-abstraction]]
- [[migration-pattern-selection]]
- [[seams-and-legacy-code]]
- [[trade-off-analysis]]
- [[architecture-fitness-function]]
- [[software-architecture-the-hard-parts]]
