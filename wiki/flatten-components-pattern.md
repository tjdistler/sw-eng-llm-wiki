# Flatten Components Pattern

**Summary**: The third [[component-based-decomposition]] pattern. A component is a **leaf-node namespace** containing source code; any source code sitting in a *root namespace* (a namespace extended by another namespace) is an **orphaned class** that doesn't belong to any definable component. Flatten Components moves orphans until every class belongs to exactly one component.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md`

**Last updated**: 2026-04-19

---

## The three definitions the pattern is built on

The chapter formalises three terms and hangs the whole pattern on them (source: raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md):

- **Component** — "a collection of classes grouped within a *leaf-node* namespace that performs some sort of specific functionality in the application."
- **Root namespace** — "a namespace node that has been extended by another namespace node." Given `ss.survey` and `ss.survey.templates`, `ss.survey` is a root namespace because `.templates` extends it. Root namespaces are also called **subdomains**.
- **Orphaned classes** — "classes contained within a root namespace, and hence have no definable component associated with them."

Under this rule, `ss.survey.templates` is a component and `ss.survey` is *not* — even though from a developer's perspective `ss.survey` looks like "the Survey component." The reason for the strict leaf-node rule: if both `ss.survey` and `ss.survey.templates` held code, there would be no principled answer to "should Survey Templates be its own service or part of Survey?" Forcing code to leaf nodes makes the eventual service boundary unambiguous.

## Two ways to flatten

Given a root namespace with orphaned classes, you either **push down** or **pull up**:

### Option A: pull orphans down into one component

Move the source code from extending namespaces *up* into the root, making the root itself a leaf. Example: move `ss.survey.templates` code into `ss.survey`, delete the `.templates` node, and `ss.survey` is now a single leaf-node component.

Used when the sub-namespace was cosmetic — an artefact of wanting to keep template code "separate" from processing code. If the two halves naturally cohere, collapse them.

### Option B: push orphans up into new components

Apply functional decomposition or [[domain-driven-design]] to the orphans in the root namespace; create new leaf components under the root for each distinct responsibility. Example: orphans in `ss.survey` split into `ss.survey.create` (creates and sends surveys) and `ss.survey.process` (handles submitted surveys). `ss.survey` becomes a subdomain with no direct code.

Used when the orphans *do* represent distinct responsibilities that should stay separable.

## The shared-orphan case

When common code (interfaces, abstract classes, utilities) lives in the root namespace because multiple sub-namespaces use it, those classes are still orphans. The fix: move them into their own leaf-node component, typically named `.shared`, `.sharedcode`, or `.commoncode`:

> Our advice when moving shared code to a separate component (leaf node namespace) is to pick a word that is not used in any existing codebase in the domain, such as `.sharedcode`, `.commoncode`, or some such unique name. This allows the architect to generate metrics based on the number of shared components in the codebase, as well as the percentage of source code that is shared in the application. (source: chapter-05-component-based-decomposition-patterns.md)

Two useful metrics fall out of a distinctive shared-code marker:

- **Percent of shared code.** If `.sharedcode` namespaces total 45% of the overall source, moving to a distributed architecture will generate a nightmare of shared-library dependencies. The pattern becomes a *feasibility signal* for the whole decomposition.
- **Count of shared components.** Approximates the number of shared libraries (JARs, DLLs) or shared services the distributed architecture will ship.

## Fitness function for governance

The canonical check (source: chapter-05-component-based-decomposition-patterns.md):

> **Fitness function: No source code should reside in a root namespace.**

Pseudocode walks each component, enumerates namespace nodes, and alerts if any non-leaf node contains source files. Atomic, triggered, static — runs on deployment via CI/CD. Keeps the codebase flat during ongoing maintenance on the monolith while the migration proceeds.

## The Sysops Squad walk-through

The chapter flattens two subsystems at once:

**Survey** — originally `ss.survey` (five orphan classes) + `ss.survey.templates` (seven class files). The seven template files were cosmetic — same author, same purpose as the survey-processing code. Solution: pull templates down into `ss.survey`. Result: a single flat `ss.survey` leaf-node component.

**Ticket** — originally `ss.ticket` (45 orphan classes) + `ss.ticket.assign` + `ss.ticket.route`. The 45 orphans represented three genuinely distinct responsibilities — ticket creation/maintenance, ticket completion, and shared code. Solution: push the orphans up into three new leaf components `ss.ticket.shared`, `ss.ticket.maintenance`, `ss.ticket.completion`. Result: `ss.ticket` becomes a subdomain containing five leaf components (source: chapter-05-component-based-decomposition-patterns.md).

Both directions of flattening are valid; the architect picks based on whether the orphans are cohesive or distinct.

## Where this pattern sits in the sequence

Runs **after** [[identify-and-size-components-pattern]] and [[gather-common-domain-components-pattern]] — the consolidated inventory is what gets flattened — and **before** [[determine-component-dependencies-pattern]] because a dependency graph over orphaned classes is meaningless.

Flattening is the pattern that most often gets skipped by architects in a hurry; skipping it produces ambiguous component boundaries that corrupt the domain grouping downstream.

## Related pages

- [[component-based-decomposition]]
- [[identify-and-size-components-pattern]]
- [[gather-common-domain-components-pattern]]
- [[determine-component-dependencies-pattern]]
- [[create-component-domains-pattern]]
- [[create-domain-services-pattern]]
- [[components]]
- [[architecture-fitness-function]]
- [[cohesion]]
- [[domain-driven-design]]
- [[software-architecture-the-hard-parts]]
