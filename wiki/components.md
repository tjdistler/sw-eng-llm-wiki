# Components

**Summary**: Richards and Ford define a **component** as the physical packaging of a [[modularity|module]] — the building block an architect actually manipulates. Components are the generic structural unit that threads through every architecture style in the book: layers of a monolith, services in microservices, plug-ins in a microkernel, subsystems in a pipeline. Identifying and partitioning components is one of the first things an architect does on a new project.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-08-component-based-thinking.md`, `raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md`

**Last updated**: 2026-04-19

---

## Module vs component

Chapter 3 introduced [[modularity|modules]] as a **logical** grouping of related code. Chapter 8 steps from the logical to the physical: a **component is the physical manifestation of a module** (source: chapter-08-component-based-thinking.md). Most languages have a concrete mechanism for this packaging — `jar` in Java, `dll` in .NET, `gem` in Ruby, `wheel` in Python, and so on.

The relationship:

- **Module** (Chapter 3) — the abstract, logical unit. "The customer code."
- **Component** (Chapter 8) — the packaged, concrete unit. "The customer library / layer / service."

Components are *the lowest level of the system an architect interacts with directly*. Classes and functions below that are the tech-lead and developer's domain (source: chapter-08-component-based-thinking.md).

## Varieties of components

A component is a generic containership mechanism. It shows up in several forms depending on the style (source: chapter-08-component-based-thinking.md):

| Form | Runtime | Communication |
|---|---|---|
| **Library** | Same process, same address space | Function calls (compile-time dependency, occasionally dynamic — DLLs) |
| **Layer / subsystem** | Same process, conceptual grouping | Function calls across layer boundaries |
| **Event processor** | Deployable unit in an event-driven style | Messages |
| **Service** | Own process, own address space | TCP/IP, REST, message queues (microservices) |

Nothing *requires* an architect to use components — in a sufficiently simple microservice, the whole service may be a single file of code and components would be overhead. Components are just useful when the natural grouping level is above what the language offers (classes, functions) but below the whole system.

## The architect's job: identify and partition

The primary Chapter 8 teaching point is that **identifying top-level components is one of the architect's first acts on a project** (source: chapter-08-component-based-thinking.md). Architects define, refine, manage, and govern components; developers take that partitioning and subdivide it further into classes, functions, and sub-components. The boundary is not rigid — architects stay involved in class design when design patterns matter, and developers refine the component design through implementation feedback — but the initial top-level partition is the architect's call.

Before components can be identified, the architect must pick a **partitioning strategy**. See [[technical-vs-domain-partitioning]] for the axis and its trade-offs.

## The component identification cycle

Component design is iterative, not up-front. The chapter's five-step loop:

1. Identify initial components (based on the chosen partitioning).
2. Assign requirements (user stories) to components.
3. Analyse roles and responsibilities.
4. Analyse [[architecture-characteristics]] per component.
5. Restructure components based on feedback.

See [[component-identification-cycle]] for the full treatment, including why step 4 is the step that often turns a monolith-shaped design into a distributed one.

## Component granularity

Finding the right component granularity is "one of an architect's most difficult tasks" (source: chapter-08-component-based-thinking.md):

- **Too fine-grained**: communication overhead between components dominates; coupling at the boundary becomes a tax on every feature.
- **Too coarse-grained**: internal coupling grows, which harms [[cohesion]], deployability, and testability.

There is no formula. The iterative cycle exists precisely because granularity emerges from use — assigning requirements reveals which components are underpopulated and which are overloaded.

## Component discovery techniques

Richards and Ford catalogue three approaches (source: chapter-08-component-based-thinking.md):

- **Actor/actions** — identify the actors (types of user, plus "the system") and the actions each performs, then build components around actor-action groupings. Originates in the Rational Unified Process; works for any development process; the Chapter 8 *Going, Going, Gone* walk-through uses it.
- **[[event-storming]]** — Brandolini's DDD technique. Identify domain events; components handle those events. Natural fit for microservices and event-driven styles.
- **Workflow** — model around the end-to-end workflows the roles perform. Like event storming without the messaging assumption; works when the team isn't using DDD.

None is superior. They're different lenses on the same problem — the fit depends on the process and style the team is using.

### The entity trap

The standing anti-pattern: one component per database entity. See [[entity-trap]] for the full treatment and why it's a sign the architect skipped the workflow analysis.

## From components to the monolith-vs-distributed decision

The component analysis closes back onto the [[architectural-quantum]]. Once components have architecture characteristics attached (cycle step 4), the architect can see whether the whole system can live within a single quantum (one set of characteristics → monolith) or whether differing characteristics across components force a distributed architecture (multiple quanta → distributed) (source: chapter-08-component-based-thinking.md).

The *Going, Going, Gone* worked example makes this concrete: Richards and Ford split a single `BidCapture` component into `BidCapture` and `AuctioneerCapture` specifically because the two have different scalability, reliability, and availability needs — and that split is part of the argument for making GGG distributed rather than monolithic. See [[architectural-quantum]] for the three-quantum decomposition.

## The Hard Parts sharpening: leaf-node rule and statements-per-namespace

*The Hard Parts* Chapter 5 makes the component definition operationally strict for migration work. A **component is the classes contained in a *leaf-node namespace*** — any source code sitting in a namespace that has been extended by another namespace is an **orphaned class** belonging to no component (source: raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md). This disambiguates "is `ss.survey` the Survey component or a subdomain?" — if `ss.survey.templates` exists, `ss.survey` is not a component, and its classes need to be flattened. See [[flatten-components-pattern]] for the resolution.

The chapter also recommends **statements per namespace** (not files or lines of code) as the useful size metric — programmer style variance makes file counts unreliable, but statements reflect actual work being done (source: chapter-05-component-based-decomposition-patterns.md). See [[identify-and-size-components-pattern]].

Together, the leaf-node rule and the statements metric make components *measurable* in a monolith migration — the prerequisite for the six [[component-based-decomposition]] patterns.

## Why this is a hub page

Every architecture style in Part II of the book (Chapters 10–17) answers the question "what do components look like in *this* style?" — layers, pipes-and-filters, microkernel + plug-ins, services, events, grid+cloud, and so on. Chapter 8's abstract treatment sets up the vocabulary those chapters re-use. This page is intended to grow inbound links as the style chapters are ingested.

## Related pages

- [[modularity]]
- [[technical-vs-domain-partitioning]]
- [[component-identification-cycle]]
- [[entity-trap]]
- [[event-storming]]
- [[architectural-quantum]]
- [[cohesion]]
- [[coupling]]
- [[bounded-context]]
- [[domain-driven-design]]
- [[conways-law]]
- [[component-based-decomposition]]
- [[identify-and-size-components-pattern]]
- [[flatten-components-pattern]]
- [[fundamentals-of-software-architecture]]
- [[software-architecture-the-hard-parts]]
