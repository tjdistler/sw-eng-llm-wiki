# Technology Selection

**Summary**: Reis and Housley's Chapter 4 framework for choosing data technologies once a [[data-architecture|data architecture]] has been set. Architecture is strategic (the what, why, when); tools are tactical (the how). Choose architecture first, then pick the technologies that realise it.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## Architecture first, technology second

Chapter 4 opens by separating architecture from tools (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Architecture is the top-level design, roadmap, and blueprint of data systems that satisfy the strategic aims for the business. Architecture is the what, why, and when. Tools are used to make the architecture a reality; tools are the how.

Teams that pick technology before mapping out an architecture get "Dr. Seuss fantasy machines" driven by [[brownfield-vs-greenfield|shiny-object syndrome]], resume-driven development, and a lack of architectural expertise. The criterion for a good technology is simple: **does it add value to a data product and the broader business?**

## The ten selection considerations

Chapter 4 enumerates ten considerations for choosing data technologies across the [[data-engineering-lifecycle]] (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

1. **Team size and capabilities** — match complexity to the team's bandwidth; avoid [[cargo-cult-engineering|cargo-cult]] emulation of giant-tech stacks.
2. **[[speed-to-market|Speed to market]]** — "perfect is the enemy of good"; slow decisions kill data teams.
3. **[[interoperability]]** — tools rarely exist in isolation; design for modularity.
4. **Cost optimisation and business value** — [[total-cost-of-ownership|TCO]], [[total-opportunity-cost-of-ownership|TOCO]], and [[finops|FinOps]].
5. **Today versus the future** — [[immutable-vs-transitory-technologies|immutable vs transitory technologies]].
6. **Location** — [[on-premises]], [[cloud]], [[hybrid-cloud]], [[multicloud]].
7. **[[build-vs-buy|Build versus buy]]** — OSS, commercial OSS, proprietary walled gardens.
8. **[[monolith-vs-modular-data|Monolith vs modular]]** — decoupled best-of-breed tools vs self-contained stacks.
9. **[[serverless-vs-servers|Serverless vs servers]]** — FaaS, containers, traditional servers.
10. **Optimisation, performance, and [[benchmark-wars|the benchmark wars]]** — vendor benchmarks are almost always misleading.

The lifecycle undercurrents (data management, DataOps, data architecture, orchestration, software engineering) provide a second axis — any selected technology must also support them.

## Common threads

Several themes run across every selection criterion (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- **Lean toward [[reversible-vs-irreversible-decisions|reversible decisions]].** The data landscape changes rapidly — avoid "bear traps" that are easy to get into and painful to escape. Reis and Housley suggest re-evaluating tools **every two years**.
- **Lean toward managed services.** Engineers on small teams or with weaker technical chops should use as many managed/SaaS tools as possible and dedicate bandwidth to the complex problems that directly add business value. Avoid [[type-a-vs-type-b-data-engineers|undifferentiated heavy lifting]].
- **Lean toward simplicity.** "Architecture is a balance of use case, cost, build versus buy, and modularization. Always approach technology the same way as architecture: assess trade-offs and aim for reversible decisions."

## Relationship to the nine principles

Chapter 4 is the tactical complement to Chapter 3's [[principles-of-good-data-architecture|nine principles of good data architecture]]. Several principles show up directly in selection:

- Principle 1 (choose common components wisely) — Chapter 4's interoperability and modularity guidance.
- Principle 6 (loose coupling) — the [[monolith-vs-modular-data|modular]] position and the escape-plan framing.
- Principle 7 (reversible decisions) — the two-year re-evaluation, the bear-trap warning, [[immutable-vs-transitory-technologies|immutable vs transitory]].
- Principle 9 (FinOps) — [[total-cost-of-ownership|TCO]], [[total-opportunity-cost-of-ownership|TOCO]], [[opex-vs-capex|opex vs capex]].

## Related pages

- [[principles-of-good-data-architecture]]
- [[data-architecture]]
- [[speed-to-market]]
- [[interoperability]]
- [[total-cost-of-ownership]]
- [[total-opportunity-cost-of-ownership]]
- [[immutable-vs-transitory-technologies]]
- [[build-vs-buy]]
- [[monolith-vs-modular-data]]
- [[serverless-vs-servers]]
- [[benchmark-wars]]
- [[cargo-cult-engineering]]
- [[on-premises]]
- [[cloud]]
- [[hybrid-cloud]]
- [[multicloud]]
- [[fundamentals-of-data-engineering]]
