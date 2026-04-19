# Shared Library Pattern

**Summary**: The most common [[reuse-patterns|code-reuse pattern]] in distributed architectures. Common code lives in a versioned external artifact (JAR, DLL, NuGet package, gem, etc.) bound into each consuming service at compile time. Adds [[static-coupling|compile-time static coupling]]; pays its price in granularity choices, dependency-management complexity, and versioning discipline.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md`

**Last updated**: 2026-04-19

---

## The pattern

A shared library is an external build artifact (JAR / DLL / NuGet / gem / pip package, etc.) containing source consumed by multiple services and bound at compile time (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md). The library lives in an artifact repository (Artifactory, Nexus, npm registry, etc.); each service's build pulls the version it depends on.

Conceptually simple. The complexity lives in two questions: **how granular?** and **how versioned?**

## Dependency management vs change control: granularity

The two opposing forces (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md):

| Coarse-grained library (one big `SharedStuff.jar`) | Fine-grained libraries (`Security.jar`, `Formatters.jar`, `Calculators.jar`, etc.) |
|---|---|
| Dependency graph is simple — every service depends on one thing | Dependency graph is a tangle — services depend on a partial set |
| **Any** change forces every service to retest and redeploy on next deprecation | Changes only impact services that depend on that specific library |
| Easy to govern, terrible to change | Better change control, harder to govern |

With 200 services and 40 libraries, the dependency matrix becomes a "big ball of distributed mud" — what some call a [[distributed-monolith]] (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md).

The chapter's recommendation: **prefer fine-grained, functionally partitioned libraries**. Carve relatively static functionality (formatters, security) into its own library so it isolates from churn elsewhere. Accept the dependency-management overhead in exchange for far less unnecessary retesting.

## Versioning is the ninth fallacy

The chapter quips that *"versioning is simple"* deserves a place alongside Deutsch's [[fallacies-of-distributed-computing|fallacies of distributed computing]] (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md). Why versioning matters and where it gets hard:

### Always version

The example: a `Validation.jar` used by 10 services. One service needs an urgent change. With versioning, that service bumps to the new version and ships immediately; the other nine are unaffected. Without versioning, *all ten* must be retested and redeployed for one service's change. **Versioning is the agility lever.**

### Communicating version changes

In a multi-team distributed architecture, knowing "Validation.jar bumped to 1.5 — what changed and who's impacted?" is non-trivial. Tools (Artifactory etc.) help but don't replace deliberate communication.

### Deprecation strategy: custom vs global

| Strategy | How it works | Trade-off |
|---|---|---|
| **Custom (per-library)** | Each library declares its own supported-version count based on its own change rate | Best fit (`Security.jar` keeps 2-3, `Calculators.jar` keeps 10), but someone must track and govern each |
| **Global** | One rule: "no library supports more than N back-versions" | Easy to govern, but causes constant *churn* — every service forced to upgrade frequently to keep up with the most-volatile library |

The book recommends **custom** strategies despite the tracking cost: matching deprecation cadence to actual change rate is what keeps total churn low.

### Breaking changes blow up any deprecation strategy

A serious defect or breaking change forces *all* consumers to take the latest version immediately. This is another argument for **fine-grained** libraries — a security defect in `Security.jar` only forces a fleet-wide redeploy of `Security.jar` consumers, not of everything.

### Avoid `LATEST`

Specifying `LATEST` for a library version "saves time" until a quick-fix or hot-deploy fails because *something in `LATEST` is incompatible*. Always pin a specific version in production builds.

## Trade-offs

| Pro | Con |
|---|---|
| No runtime overhead — no network call, no extra hop | Compile-time [[static-coupling|static coupling]] adds to the dependency envelope |
| No fault-tolerance / availability impact | Versioning, deprecation, and dependency management add ongoing operational tax |
| Versioning gives controlled, opt-in change | Polyglot environments multiply effort — one library per language stack |
| Good for low-to-moderate change rates | Coarse-grained libraries cause widespread unnecessary retest/redeploy |

## When to use

Default choice for **homogeneous** environments where shared code change is **low to moderate** (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md). Compile-time binding means operational characteristics (performance, scalability, fault tolerance) are unaffected, and versioning controls the risk of breaking other services with a change.

Pivot to [[shared-service-pattern]] when:

- The environment is **polyglot** (would require parallel libraries per language).
- The shared logic **changes frequently** and rapid fleet-wide propagation matters more than runtime safety.

Pivot to [[code-replication-pattern]] only when the code is so trivial and static that even a versioned library is overkill.

## Cross-link to component decomposition

[[gather-common-domain-components-pattern]] (Chapter 5) identifies *domain* reuse candidates while a system is still a monolith. The Chapter 8 question — "should each consolidated component become a shared library or a shared service?" — is exactly the question this page answers from the library side.

## Related pages

- [[reuse-patterns]]
- [[code-replication-pattern]]
- [[shared-service-pattern]]
- [[sidecar-pattern]]
- [[static-coupling]]
- [[gather-common-domain-components-pattern]]
- [[fallacies-of-distributed-computing]]
- [[distributed-monolith]]
- [[software-architecture-the-hard-parts]]
