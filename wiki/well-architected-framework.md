# AWS Well-Architected Framework

**Summary**: AWS's six-pillar framework for evaluating and improving cloud architectures. Reis and Housley cite it as one of the two primary inspirations for their [[principles-of-good-data-architecture|nine principles of good data architecture]]; the other is Google Cloud's [[cloud-native-principles|five cloud-native principles]].

**Sources**: `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`

**Last updated**: 2026-04-18

---

## The six pillars

Chapter 3 names the pillars (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

1. **Operational excellence** — running and monitoring systems, continuously improving processes
2. **Security** — protecting information and systems
3. **Reliability** — recovering from failures, meeting demand, adapting to load change
4. **Performance efficiency** — using resources efficiently as demand changes
5. **Cost optimization** — avoiding unneeded costs (overlaps heavily with [[finops]])
6. **Sustainability** — minimising environmental impact of workloads

## Why it matters for data architecture

Reis and Housley recommend data architects study the Well-Architected Framework in full, extract valuable ideas, and identify points of disagreement (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md). Their [[principles-of-good-data-architecture|nine principles]] are their opinionated synthesis — not a straight restatement.

The mapping is loose, not 1-to-1:

- Reliability pillar ↔ Principle 2 (Plan for failure)
- Performance efficiency ↔ Principle 3 (Architect for scalability)
- Cost optimization ↔ Principle 9 (Embrace [[finops]])
- Security pillar ↔ Principle 8 (Prioritize security)
- Operational excellence ↔ threads through Principles 4 (leadership) and 5 (always be architecting)
- Sustainability does not get a dedicated counterpart in the data principles

## Related pages

- [[principles-of-good-data-architecture]]
- [[cloud-native-principles]]
- [[data-architecture]]
- [[finops]]
- [[reliability]]
- [[data-security]]
