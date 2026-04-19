# Determine Component Dependencies Pattern

**Summary**: The fourth [[component-based-decomposition]] pattern. Visualise the afferent/efferent coupling *between components* (not between classes) to answer three questions a CIO actually asks: is the migration feasible, how much work is it, and is it a refactor or a rewrite. Outputs a component-dependency graph that predicts what the resulting service-dependency graph will look like.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md`

**Last updated**: 2026-04-19

---

## The three CIO questions

The chapter opens with a story about an architect engaged on a microservices migration whose CIO asked a single question: *"is this a golfball, a basketball, or an airliner?"* The Determine Component Dependencies pattern is how that question gets answered in hours instead of weeks. The three questions it addresses (source: raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md):

1. **Is the migration feasible?**
2. **What is the rough level of effort?**
3. **Is this a refactor, a rewrite, or a combination?**

## Component dependencies, not class dependencies

The pattern operates at one level of abstraction up from [[coupling-metrics]]: **a component dependency exists when any class in component A calls any class in component B**. Internal class-to-class coupling inside a component doesn't count. From the chapter's worked snippet:

```
namespace ss.survey
class CustomerSurvey {
  function sendSurvey {
    ss.notification.CustomerNotification.send(customer_id, survey)
  }
}
```

This creates one edge: `ss.survey` has an **efferent** (outgoing) dependency on `ss.notification`, and `ss.notification` has an **afferent** (incoming) dependency on `ss.survey` (source: chapter-05-component-based-decomposition-patterns.md). Fifty class-level calls between the two components still count as one component-level edge.

Why the coarsening matters: the chapter is blunt — "the classes within a particular component may be a highly coupled mess of numerous dependencies, but that doesn't matter when applying this pattern — what matters is only those dependencies between components."

## Reading the dependency diagram

Every component is a box; every inter-component edge is a line. The chapter defines three topologies that map directly onto CIO answers:

### Golfball — sparse graph

Minimal edges; components mostly stand alone.

- **Feasible?** Yes.
- **Effort?** Small.
- **Refactor or rewrite?** Refactor — move existing code into separately deployed services.

### Basketball — dense but asymmetric graph

Some tight clusters, some cleanly separable. Typical of most real-world business applications.

- **Feasible?** Maybe.
- **Effort?** Significant.
- **Refactor or rewrite?** Combination — refactor the clean side, rewrite the hairball side.

### Airliner — fully saturated graph

Every component depends on nearly every other component. The chapter's advice on seeing this shape: "the architect should turn around and run in the opposite direction as fast as they can."

- **Feasible?** No.
- **Effort?** Enormous.
- **Refactor or rewrite?** Full rewrite.

An airliner graph is close to a [[big-ball-of-mud]] diagnosis — the case where the precondition for [[component-based-decomposition]] fails and [[tactical-forking]] or a greenfield rewrite may be the honest call.

## Afferent, efferent, and total coupling

The pattern reuses the standard [[coupling-metrics|coupling metrics]] at component granularity:

- **Ca** — afferent (incoming) coupling.
- **Ce** — efferent (outgoing) coupling.
- **CT** — total coupling = Ca + Ce.

Most dependency-visualisation tools (JDepend, NDepend, Structure101, IntelliJ's Dependency Matrix, Visual Studio Architecture Explorer) produce these counts at the namespace level for free.

## Decomposition as a way to reduce coupling

The pattern is not just diagnostic — it's **prescriptive**. High afferent coupling on a component often means the component is overloaded: 20 other components depend on it, but maybe only 14 need one part and the other 6 need another part. Splitting the component into A1 and A2 drops each piece's Ca below the original threshold:

> Assume component A has an afferent coupling level of 20… Maybe 14 of the other components require only a small part of the functionality contained in component A. Breaking component A into two different components (A1 containing the smaller, coupled functionality, and A2 containing the majority of the functionality) reduces the afferent coupling in component A2 to 6, with component A1 having an afferent coupling level of 14. (source: chapter-05-component-based-decomposition-patterns.md)

This is the step where dependency analysis feeds back into resizing — effectively looping back to [[identify-and-size-components-pattern]] with new information.

## Fitness functions for governance

Two fitness functions govern component coupling once it's under control (source: chapter-05-component-based-decomposition-patterns.md):

1. **No component shall have more than *N* total dependencies.** Example pseudocode uses `15` as a total-coupling ceiling. Can be split into incoming-only, outgoing-only, or combined variants. Alerts on threshold crossings.
2. **Component X should not have a dependency on component Y.** Enforced with [[architecture-fitness-function|ArchUnit]] or equivalent — one rule per restricted pair. The chapter's example forbids `ss.ticket.maintenance` from touching `ss.expert.profile`:

```java
public void ticket_maintenance_cannot_access_expert_profile() {
  noClasses().that().resideInAPackage("..ss.ticket.maintenance..")
    .should().accessClassesThat().resideInAPackage("..ss.expert.profile..")
    .check(myClasses);
}
```

This second fitness function scales to the number of architectural rules, not the number of components — each deliberate dependency *prohibition* gets its own rule.

## Why architects keep skipping this pattern

The chapter's editorial:

> All too often we see teams jump straight into breaking a monolithic application into microservices without having any analysis or visuals into what the monolithic application even looks like. And not surprisingly, those teams struggle to break apart their monolithic applications. (source: chapter-05-component-based-decomposition-patterns.md)

The dependency graph functions as a **radar**: it tells the architect where the enemy (high coupling) sits before battle plans are made. Skipping it is why "seat-of-the-pants migrations rarely produce positive results."

## Where this pattern sits in the sequence

Runs **after** the first three patterns — you need a clean, sized, de-orphaned inventory to get a meaningful graph — and **before** [[create-component-domains-pattern]], which uses the dependency graph to decide which components naturally cluster.

If the graph looks like an airliner, the chapter advises stopping here: the remaining patterns assume decomposability, and an airliner graph has disproven that precondition.

## Related pages

- [[component-based-decomposition]]
- [[identify-and-size-components-pattern]]
- [[gather-common-domain-components-pattern]]
- [[flatten-components-pattern]]
- [[create-component-domains-pattern]]
- [[create-domain-services-pattern]]
- [[coupling-metrics]]
- [[coupling]]
- [[architecture-fitness-function]]
- [[big-ball-of-mud]]
- [[tactical-forking]]
- [[components]]
- [[software-architecture-the-hard-parts]]
