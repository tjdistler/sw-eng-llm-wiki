# Semantic Coupling

**Summary**: The **inherent coupling in a problem domain** — the parts of a business workflow that must relate to one another because the domain requires them to, independent of any implementation choice. Introduced in Chapter 11 of *Software Architecture: The Hard Parts* to distinguish the coupling architects *must* live with from the [[static-coupling|structural]] and [[dynamic-coupling|runtime]] coupling their implementation choices create on top. The key property: **architects can never reduce semantic coupling through implementation — they can only increase it.**

**Sources**: `raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md`

**Last updated**: 2026-04-19

---

## Definition

> Every workflow that architects need to model in software has a certain amount of semantic coupling — the inherent coupling that exists in the problem domain. (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md)

Chapter 11's worked example: assigning a ticket to a Sysops Squad member. The domain *requires* that a client must request service, skills must match specialists, schedules and locations must cross-reference. Those dependencies exist before any code is written. They are properties of the problem, not the solution.

> However clever an architect is, they cannot reduce the amount of semantic coupling, but their implementation choices may increase it. (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md)

## Semantic versus implementation coupling

Chapter 11 names the counterpart: **implementation coupling** is the coupling an architect's design choices introduce. Where semantic coupling is the *floor*, implementation coupling is what the architect adds on top. The architect's job is to keep implementation coupling as close to the semantic floor as possible.

### Not the same as static or dynamic coupling

Semantic coupling sits **above** both [[static-coupling]] and [[dynamic-coupling]]. It is not about deployment dependencies or runtime calls — it is about **domain concepts**. Two services can be statically and dynamically decoupled but still share semantic coupling because the domain they both serve has inherent relationships between their concepts.

| Coupling | Question it answers | Source |
|---|---|---|
| Semantic | Does the problem domain require these concepts to relate? | The business |
| [[static-coupling]] | Do these components share wiring, contracts, or deployment fate? | The architect's structural choices |
| [[dynamic-coupling]] | Do these components call one another at runtime to complete a workflow? | The architect's runtime choices |

## How implementation coupling can make it worse

Chapter 11's canonical example: the **technically partitioned** layered monolith versus the **domain-partitioned** modular monolith (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md).

In a technically partitioned architecture (presentation / business rules / persistence), a domain concept like **Catalog Checkout** is "smeared across" every layer — a bit of UI, a bit of business logic, a bit of persistence. To change the domain concept the architect must modify components in several layers. The semantic coupling (the domain relationships around Catalog Checkout) is the same in both architectures, but the technical partitioning **imposes additional implementation coupling** that semantic coupling didn't require.

In a domain-partitioned architecture, Catalog Checkout lives in one component with its own database. The implementation's coupling matches the domain's coupling. This is the lesson of the last decade of architecture design, Chapter 11 claims:

> The major lesson of the last decade of architecture design is to model the semantics of the workflow as closely as possible with the implementation. An architect can never reduce semantic coupling via implementation, but they can make it worse. (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md)

This is the architectural motivation for [[technical-vs-domain-partitioning|domain partitioning]] and for the [[bounded-context]] pattern from domain-driven design: align implementation boundaries with domain boundaries to avoid introducing coupling the problem didn't demand.

### When technical partitioning is still worth it

Chapter 11 acknowledges exceptions. Layered architectures historically arose from desires like consolidating database connection pooling across components. The architect weighed the extra implementation coupling against cost savings and chose technical partitioning. The point isn't that implementation coupling is always bad — it's that **implementation coupling is a real cost**, and the architect should know they're paying it.

## Coupling floor and workflow complexity

Chapter 11 ties semantic coupling to the coordination trade-off it frames (orchestration vs choreography):

> We can establish a relationship between the semantic coupling and the need for coordination — the more steps required by the workflow, the more potential error and other optional paths appear. (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md)

The higher the workflow's intrinsic semantic coupling, the more valuable a [[workflow-orchestration|workflow orchestrator]] becomes — a single place to hold all the domain relationships that can't be reduced away. [[workflow-choreography]] works best when semantic coupling is *low* — a simple linear chain — because the event graph and the domain graph stay close to each other.

## Relation to connascence

Page-Jones's [[connascence]] framework uses "static" and "dynamic" to classify kinds of connascence (entanglement between code elements). Semantic coupling sits at a higher level: it is about domain entities and business rules, not about code. A domain workflow can have zero connascence between its code components (services never call each other) and still have high semantic coupling (the business requires the steps to happen in a particular order with particular dependencies).

The connascence vocabulary helps describe the *implementation* coupling that an architect adds on top; semantic coupling describes what the domain demanded before the implementation was chosen.

## Practical use of the concept

Three places the semantic-coupling frame becomes a tool (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md):

- **Granularity decisions.** If two proposed services have high semantic coupling in the domain, pulling them apart increases implementation coupling above the semantic floor. [[service-granularity|Granularity integrators]] include this force.
- **Orchestration-vs-choreography decisions.** Complex semantic coupling → orchestration pays off. Thin semantic coupling → choreography can stay close to the floor.
- **Architect push-back.** Chapter 11 is explicit that architects may sometimes push back on **impractical or impossible semantics** proposed by business users — some domain requirements create intractable architecture problems. The concept names what the architect is pushing back against: unreduceable coupling that the proposed architecture cannot absorb.

## Related pages

- [[static-coupling]]
- [[dynamic-coupling]]
- [[coupling]]
- [[connascence]]
- [[workflow-orchestration]]
- [[workflow-choreography]]
- [[distributed-workflow-patterns]]
- [[service-granularity]]
- [[bounded-context]]
- [[technical-vs-domain-partitioning]]
- [[software-architecture-the-hard-parts]]
