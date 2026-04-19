# Identify and Size Components Pattern

**Summary**: The first of Chapter 5's [[component-based-decomposition]] patterns. Catalogue every component in the monolith, measure each one's size, and balance outliers — components that are too big get split; components that are too small get absorbed. Outputs a **component inventory** that every subsequent pattern consumes.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md`

**Last updated**: 2026-04-19

---

## Why sizing matters

Services are built from [[components|components]], so if the components are wrong the services will be wrong. Richards and Ford argue that **size asymmetry is a coupling hazard**: a component that is too big is almost always coupled to many other components, harder to extract into a service, and an obstacle to modularity (source: raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md). Too-small components generate their own tax — chatter, needless indirection — so both tails matter.

## Measuring component size

**Statements is the recommended metric.** The chapter explicitly rejects file counts, class counts, and raw lines of code — programmer style varies too much to make those reliable. A *statement* is a single complete action (terminated by `;` in Java/C/C#/Go/JS; by newline in F#/Python/Ruby). Summing statements within a namespace is "not a perfect metric" but "a good indicator of how much the component is doing and how complex the component is" (source: chapter-05-component-based-decomposition-patterns.md).

Most static-analysis tools count statements per file, not per component. The architect usually does a manual or scripted roll-up to accumulate totals per namespace.

## The component inventory

Every row in the inventory captures:

| Field | Meaning |
|---|---|
| **Component name** | Human-readable identifier; self-describing (`Billing History`, not `Ticket Manager`). |
| **Namespace** | Physical path, typically `dotted.lower.case` mapped from directory structure. |
| **Percent** | `component_statements / total_statements`. Identifies outliers on both tails. |
| **Statements** | Sum of statements across all files in the namespace. |
| **Files** | Source-file count. Useful secondary signal — 18,000 statements in 2 files flags internal refactoring needs. |

Example rows from the Sysops Squad walkthrough: `ss.billing.payment`, `ss.billing.history`, `ss.customer.notification` (source: chapter-05-component-based-decomposition-patterns.md).

## The balancing rule of thumb

> Generally speaking, the size of components in an application should fall between one to two standard deviations from the average (or mean) component size. (source: chapter-05-component-based-decomposition-patterns.md)

Percent of code per component should also be roughly even. The threshold is application-dependent:

- Small application (~10 components) — alert when any component exceeds **30%** of the codebase.
- Large application (~50 components) — alert when any exceeds **10%**.

## Resizing large components

When a component exceeds the threshold, apply functional decomposition or [[domain-driven-design]] to find subdomains:

> Assume the Sysops Squad application has a Trouble Ticket component containing 22% of the codebase … break [it] into four separate components (Ticket Creation, Ticket Assignment, Ticket Routing, and Ticket Completion). (source: chapter-05-component-based-decomposition-patterns.md)

The chapter's worked example is Reporting — a single `ss.reporting` at **33%** of the codebase, split into `ss.reporting.shared` / `ss.reporting.tickets` / `ss.reporting.experts` / `ss.reporting.financial`. After the split, `ss.reporting` becomes a subdomain, not a component. This distinction matters for [[flatten-components-pattern]] next.

If no subdomains exist, leave the component as-is — a large component with a genuinely single purpose is valid.

## Fitness functions for governance

Three [[architecture-fitness-function|fitness functions]] govern this pattern, all usually triggered at deployment via CI/CD (source: chapter-05-component-based-decomposition-patterns.md):

1. **Maintain component inventory.** Walk the directory tree, compute current namespaces, diff against the previously stored list, alert on additions and removals. Keeps the inventory current and surfaces rogue new components during ongoing maintenance.
2. **No component shall exceed *X*% of the overall codebase.** Project-specific threshold; pseudocode uses `0.10` as the illustration. Alerts when percent metric crosses the line.
3. **No component shall exceed *N* standard deviations from the mean.** The statistical version; pseudocode uses `3σ`. Catches outliers even when no absolute threshold has been set.

All three are atomic, triggered, static fitness functions. They feed the architect an alert, not a hard block — human judgement still decides whether a flagged component needs splitting.

## Where this pattern sits in the sequence

This is the **first** pattern applied. It produces the component inventory that [[gather-common-domain-components-pattern]] operates on (looking for cross-cutting duplication) and that [[flatten-components-pattern]] refines (resolving orphans). Subsequent patterns — [[determine-component-dependencies-pattern]], [[create-component-domains-pattern]], [[create-domain-services-pattern]] — all take the inventory as given (source: chapter-05-component-based-decomposition-patterns.md).

## Related pages

- [[component-based-decomposition]]
- [[gather-common-domain-components-pattern]]
- [[flatten-components-pattern]]
- [[determine-component-dependencies-pattern]]
- [[create-component-domains-pattern]]
- [[create-domain-services-pattern]]
- [[components]]
- [[component-identification-cycle]]
- [[architecture-fitness-function]]
- [[coupling-metrics]]
- [[domain-driven-design]]
- [[software-architecture-the-hard-parts]]
