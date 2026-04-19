# Gather Common Domain Components Pattern

**Summary**: The second [[component-based-decomposition]] pattern. Find cross-cutting *domain* logic duplicated across components (notification, auditing, formatting, validation) and consolidate it into a single shared component. Reduces the number of duplicate services that would otherwise appear in the resulting distributed architecture.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md`

**Last updated**: 2026-04-19

---

## Domain functionality vs infrastructure functionality

The chapter draws a sharp line between two flavours of cross-cutting code (source: raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md):

| | **Domain functionality** | **Infrastructure functionality** |
|---|---|---|
| Role | Business processing logic | Operational concerns |
| Examples | Notification, data formatting, data validation, auditing | Logging, metrics gathering, security |
| Scope | Common to *some* processes, not all | Common to *all* processes |
| Fate | Consolidate via this pattern | Handled elsewhere (platform, sidecar, library) |

This pattern targets *domain* commonalities only. Infrastructure cross-cutting is out of scope — it already has its own mechanisms ([[sidecar-pattern]], shared platform libraries, [[service-mesh]]).

## How to find it

Identification is mostly **manual** — the chapter is explicit that fully automating this is hard because of the subjectivity of "common". But two heuristics help:

### Heuristic 1: shared classes across namespaces

If a single class is imported by multiple unrelated namespaces, there's a strong chance the surrounding functionality is duplicated. The chapter's illustration:

> Take a class file named `SMTPConnection` in a large codebase that is used by five classes, all contained within different namespaces (components). This scenario is a good indication that common email notification functionality is spread throughout the application. (source: chapter-05-component-based-decomposition-patterns.md)

### Heuristic 2: common leaf-node names

When multiple components share the **same final namespace node**, that's a signal the same kind of work is being done in different places. The chapter's example:

- `penultimate.ss.ticket.audit`
- `penultimate.ss.billing.audit`
- `penultimate.ss.survey.audit`

Three different audit implementations, each "writing the action performed and the user requesting the action to an audit table." Consolidate into `penultimate.ss.shared.audit` (source: chapter-05-component-based-decomposition-patterns.md).

The **root-namespace heuristic** here is the mirror image: a shared `.shared`, `.common`, or equivalent root namespace emerges as the home for consolidated components.

## Output path: shared component or shared library?

Not all common domain functionality becomes a shared service. The two options:

1. **Shared component → [[shared-service-pattern|shared service]]** — independent deployment, network-callable from any domain that needs it.
2. **Shared component → [[shared-library-pattern|shared library]]** — bound at compile time to consumers.

The trade-off is worked through in Chapter 8 of the book — see [[reuse-patterns]] for the full decision matrix, including the [[code-replication-pattern]] (rarely applicable here) and [[sidecar-pattern|sidecar / service mesh]] (for *infrastructure* cross-cutting, explicitly out of scope for this pattern).

The two-step relationship is important: **Chapter 5 identifies candidates; Chapter 8 decides what shape they take.** Pulling ten scattered notification implementations into one shared library makes JAR/DLL dependency hygiene important; pulling them into one shared service creates a new distributed-coupling edge. The decision hinges on whether the environment is polyglot and how fast the shared logic changes — see [[shared-library-pattern]] vs [[shared-service-pattern]].

## Fitness functions for governance

Automation here is *assistive*, not deterministic — the pattern's subjectivity means the fitness functions produce candidate lists for human review, not hard pass/fail (source: chapter-05-component-based-decomposition-patterns.md):

1. **Find common names in leaf nodes of component namespace.** Walk component namespaces, collect the last node of each path (`.audit`, `.notify`, `.validate`), and alert when the same leaf name appears in more than one component. An **exclusion list** suppresses known false positives (`.calculate`, `.validate` that are genuinely distinct implementations).
2. **Find common code across components.** Collect source-file names per component, alert when the same file name appears in multiple components — again with an exclusion list.

Both are atomic, triggered, static, assistive fitness functions. They surface candidates to an architect, who then decides manually.

## The Sysops Squad worked example

The chapter's illustration consolidates three scattered notification components:

- `ss.customer.notification`
- `ss.ticket.notify`
- `ss.survey.notify`

All three send outbound messages. They collapse into a single `ss.notification` component. Coupling analysis improves (fewer redundant afferent edges), the component inventory shrinks, and the eventual distributed architecture won't ship three duplicate Notification services (source: chapter-05-component-based-decomposition-patterns.md).

## Where this pattern sits in the sequence

Runs **after** [[identify-and-size-components-pattern]] has produced the component inventory — you need the inventory to know what you're looking across — and **before** [[flatten-components-pattern]] tidies up orphaned classes. The consolidated components produced here feed [[determine-component-dependencies-pattern]]'s dependency analysis with materially fewer (and cleaner) edges.

## Related pages

- [[component-based-decomposition]]
- [[identify-and-size-components-pattern]]
- [[flatten-components-pattern]]
- [[determine-component-dependencies-pattern]]
- [[create-component-domains-pattern]]
- [[create-domain-services-pattern]]
- [[components]]
- [[architecture-fitness-function]]
- [[coupling-metrics]]
- [[domain-driven-design]]
- [[service-based-architecture]]
- [[software-architecture-the-hard-parts]]
- [[reuse-patterns]]
- [[shared-library-pattern]]
- [[shared-service-pattern]]
