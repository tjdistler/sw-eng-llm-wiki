# Architecture Fitness Function

**Summary**: An objective, automatable integrity assessment of one or more [[architecture-characteristics]]. Borrowed from evolutionary-computing vocabulary by Neal Ford's *Building Evolutionary Architectures* and treated in depth in Chapter 6 of *Fundamentals of Software Architecture*. Fitness functions turn architectural invariants into executable checks that run on a cadence fast enough to catch regressions before they compound.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-01-introduction.md`, `raw/fundamentals-of-software-architecture/chapter-06-measuring-and-governing-architecture-characteristics.md`, `raw/software-architecture-the-hard-parts/chapter-01-what-happens-when-there-are-no-best-practices.md`, `raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md`

**Last updated**: 2026-04-19
---

## Where the term comes from

In evolutionary computing, a genetic algorithm mutates candidate solutions and selects the fittest via a *fitness function* that measures how close each candidate is to the optimum. For the travelling-salesperson problem, fitness is the path length — or the total cost, or the total travel time, depending on what the designer wants to optimise for (source: chapter-01-introduction.md; chapter-06-measuring-and-governing-architecture-characteristics.md). Rebecca Parsons (one of the *Building Evolutionary Architectures* authors) spent part of her career in the evolutionary-computing space; the vocabulary migrated to architecture from her work.

Richards and Ford's Chapter 6 recasts the book's original definition:

> Architecture fitness function: any mechanism that provides an objective integrity assessment of some architecture characteristic or combination of architecture characteristics. (source: chapter-06-measuring-and-governing-architecture-characteristics.md)

And emphasises the key phrase:

> Fitness functions are not some new framework for architects to download, but rather a new perspective on many existing tools. (source: chapter-06-measuring-and-governing-architecture-characteristics.md)

## Defining properties

- **Objective** — no subjective judgement; a run either passes or fails (or emits a numeric score that's compared against a threshold).
- **Integrity assessment** — measures that a [[architecture-characteristics|characteristic]] holds, not that a feature works.
- **Automatable** — runnable as part of a pipeline or a continuous monitor, not as an expert-review step.
- **Attached to a named characteristic** — a failure must be interpretable as "characteristic X regressed", not as a generic bug.

## The categories

*Building Evolutionary Architectures* catalogues fitness-function types along several orthogonal axes. The chapter's sweep introduces or implies each:

- **Atomic vs holistic** — atomic fitness functions check one characteristic in isolation (a cyclic-dependency test); holistic ones check the emergent behaviour of several characteristics interacting (Chaos Monkey verifies availability + recoverability + fault tolerance simultaneously).
- **Triggered vs continual** — triggered functions run in response to an event (a commit, a deployment); continual functions run constantly in production (a monitor, a [[synthetic-transactions|synthetic transaction]]).
- **Static vs dynamic** — static functions inspect the artefact (source code, bytecode, infrastructure-as-code); dynamic ones exercise it at runtime.
- **Automated vs manual** — automated is the default and preferred; manual exists for things that genuinely cannot be automated yet (legal review, UX assessment).
- **Temporal** — time-bound fitness functions like deprecation-countdown timers that begin failing once a grace period expires.
- **Domain-specific** — bespoke checks for project-specific characteristics (the "Italy-ility" variant from [[architecture-characteristics]]).

Most real-world fitness functions combine several of these axes — ArchUnit's layer rule is atomic, triggered, static, and automated; Chaos Monkey is holistic, continual, dynamic, and automated.

## Concrete examples from Chapter 6

### Cyclic-dependency check (JDepend)

Modularity is the canonical important-but-not-urgent concern (source: chapter-06-measuring-and-governing-architecture-characteristics.md). IDEs for Java and .NET aggressively auto-import classes, and developers reflexively accept, which over time produces a web of cycles. Code review catches this too late. The chapter's fitness function:

```java
public class CycleTest {
  private JDepend jdepend;

  @BeforeEach
  void init() {
    jdepend = new JDepend();
    jdepend.addDirectory("/path/to/project/persistence/classes");
    jdepend.addDirectory("/path/to/project/web/classes");
    jdepend.addDirectory("/path/to/project/thirdpartyjars");
  }

  @Test
  void testAllPackages() {
    Collection packages = jdepend.analyze();
    assertEquals("Cycles exist", false, jdepend.containsCycles());
  }
}
```

Wired into the continuous build, this kills accidental cycle introduction at commit time.

### Distance from the main sequence

Using JDepend to enforce the [[coupling-metrics|distance-from-the-main-sequence]] metric (source: chapter-06-measuring-and-governing-architecture-characteristics.md):

```java
@Test
void AllPackages() {
  double ideal = 0.0;
  double tolerance = 0.5; // project-dependent
  Collection packages = jdepend.analyze();
  Iterator iter = packages.iterator();
  while (iter.hasNext()) {
    JavaPackage p = (JavaPackage) iter.next();
    assertEquals("Distance exceeded: " + p.getName(),
                 ideal, p.distance(), tolerance);
  }
}
```

The chapter uses this example to make an editorial point: **architects must ensure developers understand the purpose of a fitness function before imposing it**. Distance-from-the-main-sequence is an esoteric metric; enforcing it without explanation creates incomprehensible CI failures. This applies generally — see [[architecture-governance]] on ivory-tower governance.

### Layered-architecture enforcement (ArchUnit)

ArchUnit is a Java testing framework built on JUnit for architectural assertions (source: chapter-06-measuring-and-governing-architecture-characteristics.md). Example: enforcing the classical three-layer discipline where presentation may not skip the service layer:

```java
layeredArchitecture()
  .layer("Controller").definedBy("..controller..")
  .layer("Service").definedBy("..service..")
  .layer("Persistence").definedBy("..persistence..")
  .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
  .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
  .whereLayer("Persistence").mayOnlyBeAccessedByLayers("Service")
```

The architect defines the intended layer relationships once; ArchUnit fails the build whenever a developer introduces a disallowed dependency. Without this check, "better to ask forgiveness than permission" pressure — usually justified by some local performance concern — silently erodes the layer discipline until the architecture is a [[modularity|Big Ball of Mud]].

### Layered-architecture enforcement (NetArchTest)

The .NET analogue (source: chapter-06-measuring-and-governing-architecture-characteristics.md):

```csharp
// Classes in the presentation should not directly reference repositories
var result = Types.InCurrentDomain()
  .That()
  .ResideInNamespace("NetArchTest.SampleLibrary.Presentation")
  .ShouldNot()
  .HaveDependencyOn("NetArchTest.SampleLibrary.Data")
  .GetResult()
  .IsSuccessful;
```

### Chaos Monkey and the Simian Army (Netflix)

Chapter 6 frames Netflix's Chaos Monkey as a **holistic fitness function** running in production (source: chapter-06-measuring-and-governing-architecture-characteristics.md). The Simian Army extensions each govern a different architectural characteristic:

- **Chaos Monkey** — terminates instances at random to verify fault tolerance.
- **Latency Monkey** — simulates slow AWS instances to verify the system survives degraded dependencies.
- **Chaos Kong** — simulates an entire AWS region failing; Netflix credits this with preventing real regional outages.
- **Conformity Monkey** — fails a service that violates architect-defined governance rules (e.g. "every service must respond usefully to all RESTful verbs").
- **Security Monkey** — scans services for well-known security defects (open ports, config errors).
- **Janitor Monkey** — finds orphaned services no one routes to anymore and disintegrates them; Netflix's evolutionary architecture means services are routinely superseded, and cloud-billing makes old services expensive.

These are [[architecture-governance|governance]] mechanisms codified as running processes. See also [[fault-tolerance]] for more on chaos engineering as a discipline and [[reliability]] for the deliberate-fault-injection rationale.

### Other shapes

Beyond the chapter's worked examples, fitness functions built on common tooling include:

- **Unit and integration tests** — hard pass/fail on decisions like "presentation may not depend on persistence."
- **[[cyclomatic-complexity|Cyclomatic-complexity]] ceilings** — static-analysis gates in CI.
- **Linters and style checkers** — Checkstyle, ESLint, RuboCop, golangci-lint; architectural rules live alongside style rules.
- **Performance-budget tests** — CI-level assertions that p95 page load time stays under a threshold, or that the frontend bundle stays under a K-weight budget (see [[measuring-architecture-characteristics]]).
- **Monitors and runtime assertions** — p95 latency, error rate, saturation, queue depth; continuous fitness functions on operational characteristics.
- **[[synthetic-transactions|Synthetic transactions]]** — end-to-end probes that exercise a user journey continuously.
- **Deprecation timers** — temporal fitness functions that begin failing once a grace period elapses.
- **Zero-tolerance policies** — "no new warnings" or "no new cycles" rules that prevent backsliding without requiring a full cleanup first.
- **Chaos experiments** — holistic, continual, dynamic fitness functions verifying availability and fault tolerance under adverse conditions.

## The Checklist Manifesto framing

Richards and Ford lean on Atul Gawande's *The Checklist Manifesto* to explain how fitness functions should feel (source: chapter-06-measuring-and-governing-architecture-characteristics.md):

> Rather than a heavyweight governance mechanism, fitness functions provide a mechanism for architects to express important architectural principles and automatically verify them. Developers know that they shouldn't release insecure code, but that priority competes with dozens or hundreds of other priorities for busy developers.

The point: pilots and surgeons use checklists not because they're incompetent but because high-repetition expert work makes details easy to miss. Fitness functions are the same discipline for software. See [[architecture-governance]] for more on this framing.

## Cadence matters

Richards and Ford insist on the link between how often a fitness function runs and how useful it is:

> Note the correlation between how often fitness functions execute and the feedback they provide. (source: chapter-01-introduction.md)

A fitness function that runs monthly is ~30× less useful than one that runs on every commit. The feedback cadence of the fitness function is capped by the cadence of the delivery pipeline — which is why fitness functions are entwined with continuous integration, automated provisioning, and the rest of the Agile engineering toolkit.

## Collaboration, not imposition

A recurring point in the Chapter 6 treatment:

> The intent is not for a group of architects to ascend to an ivory tower and develop esoteric fitness functions that developers cannot understand. Architects must ensure that developers understand the purpose of the fitness function before imposing it on them. (source: chapter-06-measuring-and-governing-architecture-characteristics.md)

A fitness function that developers can't interpret is a fitness function that will be bypassed or disabled. This is one reason the "distance from the main sequence" check, powerful as it is, needs explicit documentation; it's also why ArchUnit's layered-architecture API reads like prose.

## Why they matter

Without fitness functions, architectural characteristics drift silently. Developers making local changes cannot tell which choices affect which characteristics; the characteristic degrades; the system still seems to work until the degradation crosses a threshold that manifests as an incident or a customer complaint. This is **[[architecture-vitality|structural decay]]**. Fitness functions are how [[evolutionary-architecture]] prevents decay — they make the invariants executable.

## Decomposition-pattern fitness functions (Hard Parts Ch 5)

*The Hard Parts* Chapter 5 attaches **at least one fitness function to every [[component-based-decomposition|decomposition pattern]]**, making the whole six-pattern sequence amenable to automated governance (source: raw/software-architecture-the-hard-parts/chapter-05-component-based-decomposition-patterns.md). These are atomic, triggered, static fitness functions that run on deployment via CI/CD and alert the architect on drift:

| Pattern | Fitness function |
|---|---|
| [[identify-and-size-components-pattern]] | Maintain component inventory; no component exceeds *X*% of codebase; no component exceeds *N* standard deviations from the mean size |
| [[gather-common-domain-components-pattern]] | Find common leaf-node namespace names; find common source-file names across components (with exclusion lists) |
| [[flatten-components-pattern]] | No source code shall reside in a root namespace |
| [[determine-component-dependencies-pattern]] | No component shall have more than *N* total dependencies; component X shall not depend on component Y (ArchUnit rule per restriction) |
| [[create-component-domains-pattern]] | All namespaces under the root shall be restricted to the approved list of domains (ArchUnit) |
| [[create-domain-services-pattern]] | All components in a given domain service shall share the same namespace prefix (ArchUnit) |

The editorial point reinforced by this list: fitness functions are how a long-running migration avoids quietly regressing. Each pattern is fragile on its own — orphaned classes creep in, coupling grows back, new domains sprout — and each pattern's fitness function catches the regression on the next deployment instead of the next architect review.

## Re-iterated in *The Hard Parts* (Chapter 1)

Ford, Richards, Sadalage, and Dehghani's *Software Architecture: The Hard Parts* (2021) frames fitness functions alongside ADRs as the book's two load-bearing governance primitives. Chapter 1 restates the Building-Evolutionary-Architectures definition verbatim — *"any mechanism that performs an objective integrity assessment of some architecture characteristic or combination of architecture characteristics"* — and recaps the atomic/holistic distinction and the JDepend cycle-test / ArchUnit / NetArchTest examples (source: raw/software-architecture-the-hard-parts/chapter-01-what-happens-when-there-are-no-best-practices.md).

Two framings Chapter 1 sharpens:

1. **Governance follows documentation.** *"Documenting a decision is important for an architect, but governing the proper use of the decision is a separate topic."* Every [[architecture-decision-record|ADR]] in the book has an implied fitness function asking *"how will we know this decision is being followed?"* — automated when possible, manual when genuinely necessary.
2. **The Equifax cautionary tale.** Chapter 1 uses the 2017 Equifax breach — where a published Struts CVE and a DHS notification weren't enough to produce universal remediation, and the unpatched instances were still in production months later — as the canonical example of the **zero-day governance problem** fitness functions solve: if every project has a "slot" in its deployment pipeline where the security team can drop in a test for the vulnerable framework version, a CVE plus one push catches every project, and failing builds notify teams automatically. This reframes fitness functions from "architect's local discipline" to **enterprise-wide governance mechanism** (source: raw/software-architecture-the-hard-parts/chapter-01-what-happens-when-there-are-no-best-practices.md).

The Checklist Manifesto framing carries over from *Fundamentals* Chapter 6 — fitness functions are the "important but not urgent" checklist developers can't skip, and the ivory-tower warning still applies ("architects should not form a cabal and retreat to an ivory tower to build an impossibly complex, interlocking set of fitness functions that merely frustrate developers and teams").

## Relation to other wiki concepts

- [[architecture-governance]] — the umbrella; fitness functions are the primary mechanism.
- [[measuring-architecture-characteristics]] — the prerequisite; a characteristic must be defined objectively before a fitness function can test it.
- [[architecture-vitality]] — fitness functions are the mechanism for maintaining the property.
- [[evolutionary-architecture]] — the umbrella concept; fitness functions are its load-bearing technique.
- [[cyclomatic-complexity]] — a common structural measurement used as a fitness function.
- [[coupling-metrics]] — afferent/efferent and distance-from-the-main-sequence as fitness-function inputs.
- [[architecture-decisions-vs-design-principles]] — decisions tend to produce hard pass/fail fitness functions; principles produce monitors and trend alerts.
- [[architect-expectations]] — expectation #4 (ensure compliance) is largely automated via fitness functions.
- [[desired-state-management]] — same spirit; declare the property, let automation maintain it.
- [[monitoring-and-observability]] — runtime substrate for metric-based fitness functions.
- [[synthetic-transactions]] — a particular dynamic fitness-function family.
- [[fault-tolerance]] — chaos engineering as holistic fitness function.

## Related pages

- [[architecture-governance]]
- [[measuring-architecture-characteristics]]
- [[cyclomatic-complexity]]
- [[coupling-metrics]]
- [[evolutionary-architecture]]
- [[architecture-vitality]]
- [[architecture-characteristics]]
- [[architecture-decisions-vs-design-principles]]
- [[architect-expectations]]
- [[synthetic-transactions]]
- [[monitoring-and-observability]]
- [[desired-state-management]]
- [[fault-tolerance]]
- [[laws-of-software-architecture]]
- [[component-based-decomposition]]
- [[fundamentals-of-software-architecture]]
- [[software-architecture-the-hard-parts]]
