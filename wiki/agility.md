# Agility

**Summary**: A **compound architecture characteristic** — the ability of a system to respond quickly to change. Ford and Richards define agility as the combination of **[[maintainability]]**, **[[testability]]**, and **[[deployability]]**; it is the primary mechanism by which [[architectural-modularity]] produces [[speed-to-market]].

**Sources**: `raw/software-architecture-the-hard-parts/chapter-03-architectural-modularity.md`, `raw/fundamentals-of-software-architecture/chapter-05-identifying-architectural-characteristics.md`, `raw/fundamentals-of-software-architecture/chapter-06-measuring-and-governing-architecture-characteristics.md`

**Last updated**: 2026-04-19

---

## Agility is a composite, not a primitive

Chapter 3 of *Software Architecture: The Hard Parts* is blunt (source: raw/software-architecture-the-hard-parts/chapter-03-architectural-modularity.md):

> Agility is a compound architectural characteristic made up of many other architecture characteristics, including maintainability, testability, and deployability.

This echoes Fundamentals Chapter 5, which warns that "agility" and "time to market" are domain concerns that have to be decomposed into measurable sub-characteristics before they can drive structural decisions (source: raw/fundamentals-of-software-architecture/chapter-05-identifying-architectural-characteristics.md). The trap of treating agility as a primitive characteristic is that different stakeholders read it differently: a product owner hears "we ship features faster"; an architect hears "we can restructure without breakage"; an SRE hears "we can roll back without incident." Decomposing agility into three concrete sub-characteristics forces alignment.

## The three components

### Maintainability

Ease of adding, changing, and removing features; ease of internal maintenance (upgrades, patches). Drives how much time each change takes. Measured via [[coupling-metrics|coupling]], [[cohesion]], [[cyclomatic-complexity]], component size. See [[maintainability]].

### Testability

Ease and completeness of automated testing. Drives how confidently each change can be shipped. Measured via test-suite runtime, test coverage, flake rate, scope of tests needed per change. See [[testability]].

### Deployability

Ease, frequency, and low risk of deployment. Drives how quickly a finished change reaches production. Measured via deployment frequency, deployment duration, deployment failure rate, mean time to recovery. See [[deployability]].

None of the three alone is sufficient. A codebase that is trivially maintainable but takes two months to deploy is not agile. A system with fifteen-second deployments and five-minute test suites but a monolithic codebase where every change touches ten components is not agile.

## The path from modularity to speed to market

Chapter 3's Figure 3-3 (source: raw/software-architecture-the-hard-parts/chapter-03-architectural-modularity.md) connects the dots:

```
              architectural modularity
                       |
     +----------+------+------+----------+
     |          |             |          |
maintainability testability deployability  ... scalability, availability
     |          |             |
     +----------+-------------+
                |
            AGILITY
                |
        speed to market
                |
        competitive advantage
```

[[architectural-modularity]] is the structural move; agility is the composite characteristic that results; [[speed-to-market]] is the business outcome; competitive advantage is the strategic outcome.

This also frames the inverse: a monolith with poor maintainability, slow test suites, and quarterly releases is structurally incapable of agility no matter how committed the team is to "being agile."

## Why modularity enables each of the three

The chapter's argument, distilled:

- **Maintainability** improves because scope of change shrinks from application-level (monolith) to domain-level (service-based) to function-level (microservices).
- **Testability** improves because test scope shrinks to one deployment unit.
- **Deployability** improves because deployment risk and ceremony shrink to one deployment unit.

Each benefit erodes if services chatter excessively (the [[architectural-modularity#the-chatter-problem-modularitys-failure-mode|chatter caveat]] on architectural-modularity). A [[distributed-monolith]] gets the distribution cost without the agility benefit — the three components all collapse back to their monolithic baselines.

## Governance: agility must be measured

Because agility is compound, you cannot govern it directly — you govern its three components. Chapter 6 of *Fundamentals of Software Architecture* makes this explicit: agility and deployability fall into the **process** axis of measurement (distinct from operational and structural axes), measured via deployment cadence, deploy duration, rollback frequency, and similar metrics (source: raw/fundamentals-of-software-architecture/chapter-06-measuring-and-governing-architecture-characteristics.md). [[architecture-fitness-function|Fitness functions]] for each of maintainability, testability, and deployability — running continuously — are the operational mechanism.

The alternative — declaring agility as a project value without decomposing and measuring it — is what Richards and Ford mean by a characteristic that "varies across teams and defeats ubiquitous language."

## Relation to other wiki concepts

- [[system-stability-vs-agility]] — SRE Chapter 9's framing of the agility/reliability balance. Luebbe's thesis ("reliable processes increase agility") is a process-axis claim; Ford and Richards's thesis ("modularity increases agility") is a structural-axis claim. Both are true, independently, and compose: a modular architecture with a reliable build pipeline is maximally agile.
- [[evolutionary-architecture]] — agility is a prerequisite. An architecture designed to evolve gracefully depends on being changeable (maintainability), verifiable (testability), and deployable (deployability).
- [[microservices]] — Ford and Richards give microservices five stars on agility in their Chapter 17 scorecard; that rating is the composite of five-star maintainability + testability + deployability. The monolithic styles cap at moderate agility because they cap at moderate deployability.

## Related pages

- [[architectural-modularity]]
- [[speed-to-market]]
- [[maintainability]]
- [[testability]]
- [[deployability]]
- [[architecture-characteristics]]
- [[architecture-fitness-function]]
- [[evolutionary-architecture]]
- [[system-stability-vs-agility]]
- [[independent-deployability]]
- [[microservices]]
- [[software-architecture-the-hard-parts]]
