# Create Component Domains Pattern

**Summary**: The fifth [[component-based-decomposition]] pattern. Group components that perform related functionality into logical **component domains**, manifested as a shared prefix in the namespace (`ss.customer.*`, `ss.ticket.*`). Each resulting domain becomes a candidate [[service-based-architecture|service-based]] **domain service** in the next pattern. Often requires renaming namespaces to align with domains.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md`

**Last updated**: 2026-04-19

---

## Services are one-to-many with components

A key observation underwrites this pattern (source: raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md):

> In most cases the relationship between a service and components is a one-to-many relationship — that is, a single service may contain one or more components.

Treating every component as its own service produces fine-grained [[microservices]] prematurely — before the architect has evidence that the fine granularity is actually justified. The pattern instead groups components into **coarse-grained logical domains**, each of which will eventually become one domain service in a [[service-based-architecture]]. That's the recommended intermediate state before optionally going finer in Chapter 7.

## Domains live in the namespace

The chapter treats the namespace hierarchy as the physical carrier of the logical domain:

```
ss . customer . billing . payment . MonthlyBilling
│    │          │         │         │
root domain    subdomain  component  class
```

- Second node (`.customer`) — the **domain**.
- Third node (`.billing`) — a **subdomain** of the domain.
- Leaf node (`.payment`) — the **component**.
- After the leaf — **classes**.

Domains are visible because namespace nodes are hierarchical. A domain is just *the prefix shared by a coherent group of components*.

## Refactoring namespaces to reveal domains

Most monoliths pre-date explicit [[domain-driven-design]] and have namespaces that don't reflect the intended domain groupings. The pattern's main work is **renaming** components so the namespace prefix expresses the domain.

The chapter's Customer-domain walkthrough:

| Before | After |
|---|---|
| `ss.billing.payment` | `ss.customer.billing.payment` |
| `ss.billing.history` | `ss.customer.billing.history` |
| `ss.customer.profile` | `ss.customer.profile` (unchanged) |
| `ss.supportcontract` | `ss.customer.supportcontract` |

All four are customer-facing, but only one had `.customer` in its namespace. After the refactor, the Customer domain is an identifiable prefix `ss.customer.*` (source: chapter-05-component-based-decomposition-patterns.md).

## The Sysops Squad worked example — five domains

The book settles on five domains for Sysops Squad:

1. **`ss.ticket.*`** — ticket processing + customer surveys + knowledge base. The survey and KB components *had* to move under `.ticket` because they weren't originally ticket-prefixed (`ss.survey` → `ss.ticket.survey`, `ss.kb.*` → `ss.ticket.kb.*`).
2. **`ss.reporting.*`** — reporting components; already aligned from the earlier Reporting split in [[identify-and-size-components-pattern]].
3. **`ss.customer.*`** — customer profile, billing, support contracts.
4. **`ss.admin.*`** — administration of users and experts (`ss.users` → `ss.admin.users`; `ss.expert.profile` → `ss.admin.experts`).
5. **`ss.shared.*`** — login and notification used by the other domains (`ss.login` → `ss.shared.login`; `ss.notification` → `ss.shared.notification`).

Domain design is as much naming discipline as it is logical design — `ss.expert.profile` got renamed to `ss.admin.experts` purely to align with the Admin domain.

## Fitness function for governance

Once domains exist, govern the namespace constraint to prevent drift (source: chapter-05-component-based-decomposition-patterns.md):

> **Fitness function: All namespaces under <root> should be restricted to <list of domains>.**

[[architecture-fitness-function|ArchUnit]] example — allow only `ss.ticket.*`, `ss.customer.*`, `ss.admin.*`:

```java
public void restrict_domains() {
  classes().should().resideInAPackage("..ss.ticket..")
    .orShould().resideInAPackage("..ss.customer..")
    .orShould().resideInAPackage("..ss.admin..")
    .check(myClasses);
}
```

Catches a developer accidentally creating a new domain `ss.newthing.*` during maintenance — alerts the architect to discuss whether a new domain is actually warranted.

## Why this pattern runs before Create Domain Services

The physical extraction ([[create-domain-services-pattern]]) is a one-way door: once `ss.ticket.*` becomes its own deployable service, moving a component into or out of the Ticket domain becomes a cross-service change instead of a within-monolith refactor. The chapter is emphatic:

> Don't apply this pattern until all of the component domains have been identified and refactored. This helps reduce the amount of modification needed to each domain service when moving components (and hence source code) around. (source: chapter-05-component-based-decomposition-patterns.md, from Create Domain Services)

Shuffling components across domains is cheap while they're still in the same monolith. Get this pattern right *first*.

## Where this pattern sits in the sequence

Runs **after** [[determine-component-dependencies-pattern]] — the dependency graph informs which components cluster naturally — and **before** [[create-domain-services-pattern]] which extracts each domain into its own deployable unit.

## Related pages

- [[component-based-decomposition]]
- [[identify-and-size-components-pattern]]
- [[gather-common-domain-components-pattern]]
- [[flatten-components-pattern]]
- [[determine-component-dependencies-pattern]]
- [[create-domain-services-pattern]]
- [[service-based-architecture]]
- [[bounded-context]]
- [[domain-driven-design]]
- [[components]]
- [[architecture-fitness-function]]
- [[software-architecture-the-hard-parts]]
