# Create Domain Services Pattern

**Summary**: The sixth and final [[component-based-decomposition]] pattern. Physically extract each logical domain from [[create-component-domains-pattern]] into its own separately deployed coarse-grained service. The output *is* a [[service-based-architecture]] — the "soft landing" Richards and Ford recommend as the intermediate checkpoint before deciding whether to go further into [[microservices]].

**Sources**: `raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md`

**Last updated**: 2026-04-19

---

## What a domain service is

A **domain service** is (source: raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md):

> A coarse-grained, separately deployed unit of software containing all of the functionality for a particular domain (such as Ticketing, Customer, Reporting, and so on).

It is the runtime manifestation of a component domain. The pattern simply takes everything under `ss.ticket.*`, builds it as its own deployment artefact, and runs it as its own process — while everything under `ss.customer.*`, `ss.admin.*`, etc. does the same.

## The target shape: basic service-based architecture

The simplest valid output of this pattern is the canonical [[service-based-architecture]] topology:

```
    [ User Interface (monolithic) ]
               |
    --------------------------------
    |       |        |        |    |
 [Ticket][Customer][Admin][Shared][Reporting]     <- 4 to 12 domain services
    |       |        |        |    |
    +-------+---+----+---+----+----+
               |
          [ Shared DB ]
```

Remote UI, remote domain services, shared monolithic database. The chapter explicitly recommends this as the migration target:

> Once components have been properly sized, flattened, and grouped into domains, those domains can then be moved to separately deployed domain services, creating what is known as a service-based architecture. (source: chapter-05-component-based-decomposition-patterns.md)

More elaborate [[service-based-architecture]] topologies — split UI, split DB, API gateway — are topology variants the architect can adopt later; the basic topology is a safe default.

## Why service-based architecture is the "soft landing"

The chapter's argument for stopping here first rather than jumping straight to [[microservices]] (source: chapter-05-component-based-decomposition-patterns.md):

1. **It gives the architect learning time.** Running each domain as a service under production traffic reveals whether that domain really needs finer granularity — or whether a coarse-grained domain service is sufficient forever.
2. **Most teams mistakenly start fine-grained.** Going directly to microservices forces the team to solve data decomposition, distributed workflows, distributed transactions, operational automation, and containerisation *simultaneously* — "without the need for all of those fine-grained microservices." Service-based architecture defers those costs until evidence justifies them.
3. **No database decomposition required yet.** The shared monolithic database stays intact; data separation (Chapter 6) is the hardest problem and can be deferred.
4. **No operational-automation requirement yet.** Domain services can ship as EAR/WAR/assembly, the same format as the original monolith. Kubernetes, service meshes, observability platforms are optional.
5. **Technical migration only.** No reorg, no QA-process change, no deployment-environment overhaul.

## Do all the component work first

The pattern has one load-bearing sequencing rule:

> Don't apply this pattern until all of the component domains have been identified and refactored. This helps reduce the amount of modification needed to each domain service when moving components (and hence source code) around. (source: chapter-05-component-based-decomposition-patterns.md)

Worked scenario from the chapter: if the Ticket service is extracted first and then the team decides the customer-survey component belongs in Ticket, the survey has to be migrated *into a running service* instead of shuffled within the monolith. Get [[create-component-domains-pattern]] right first; then extract.

## Fitness function for governance

Once domain services are running, keep them from drifting into their own unstructured monoliths (source: chapter-05-component-based-decomposition-patterns.md):

> **Fitness function: All components in <some domain service> should start with the same namespace.**

Example [[architecture-fitness-function|ArchUnit]] rule for the Ticket domain service:

```java
public void restrict_domain_within_ticket_service() {
  classes().should().resideInAPackage("..ss.ticket..")
    .check(myClasses);
}
```

One such rule per domain service. This prevents the kind of silent reintroduction-of-coupling that turns a clean service-based architecture into a badly-packaged [[distributed-monolith]] — someone adds a `ss.admin.*` class to the Ticket service; the rule fires on the next build.

This matters especially if the domain service will later decompose into microservices — the next step needs the domain boundary to be clean.

## The Sysops Squad outcome

After the full six-pattern sequence, the Sysops Squad monolith becomes a distributed application consisting of separately deployed domain services (one per domain identified in [[create-component-domains-pattern]]) all sharing a single database. The result is the Figure 5-22 topology in the chapter — a [[service-based-architecture]] in the exact shape described in [[service-based-architecture|its own page]] (source: chapter-05-component-based-decomposition-patterns.md).

## What happens after this pattern

Chapter 5 is explicit about the follow-ons:

- **Decompose the data** — the shared database is now the biggest remaining coupling point. Chapter 6 addresses [[database-decomposition]].
- **Refine granularity** — Chapter 7 defines the **integrator/disintegrator forces** that tell the architect whether a given domain service should decompose further into [[microservices]] or stay coarse-grained.

A domain service is not automatically a stepping stone — it may be the final shape for some domains and an intermediate shape for others. The point of landing here first is that the architect now has the evidence to tell the difference.

## Where this pattern sits in the sequence

The **last** pattern. All five earlier patterns produce inputs; this one converts the refined monolith into a distributed architecture.

1. [[identify-and-size-components-pattern]]
2. [[gather-common-domain-components-pattern]]
3. [[flatten-components-pattern]]
4. [[determine-component-dependencies-pattern]]
5. [[create-component-domains-pattern]]
6. **Create Domain Services** (this page)

## Related pages

- [[component-based-decomposition]]
- [[create-component-domains-pattern]]
- [[identify-and-size-components-pattern]]
- [[gather-common-domain-components-pattern]]
- [[flatten-components-pattern]]
- [[determine-component-dependencies-pattern]]
- [[service-based-architecture]]
- [[microservices]]
- [[monolith-to-microservices]]
- [[distributed-monolith]]
- [[database-decomposition]]
- [[architecture-fitness-function]]
- [[software-architecture-the-hard-parts]]
