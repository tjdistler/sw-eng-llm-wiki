# Speed to Market

**Summary**: Reis and Housley's second criterion for [[technology-selection|choosing data technologies]]. Deliver value early and often; "perfect is the enemy of good." Slow decisions and output are "the kiss of death" to data teams.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## The argument

Chapter 4 is blunt (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> In technology, speed to market wins. This means choosing the right technologies that help you deliver features and data faster while maintaining high-quality standards and security. It also means working in a tight feedback loop of launching, learning, iterating, and making improvements.

Reis and Housley have "seen more than a few data teams dissolve for moving too slow and failing to deliver the value they were hired to produce." Deliberating over tool choice for months or years without deciding is itself a failure mode.

## What it implies for tool choice

- **Use what works.** Team members have better leverage with tools they already know. A familiar but imperfect tool ships now; an unfamiliar best-in-class tool ships in six months if at all.
- **Avoid undifferentiated heavy lifting.** Don't engage the team in unnecessarily complex work that adds no differentiated value.
- **Choose tools that help you move quickly, reliably, safely, and securely.** All four, not one traded for the other.

## Relationship to other criteria

Speed to market trades against several Chapter 4 criteria:

- Against [[immutable-vs-transitory-technologies|today-vs-future]] — moving fast today can lock you into transitory tools; moving slow to find immutable ones risks never shipping. The [[reversible-vs-irreversible-decisions|reversible-decisions]] escape hatch is what reconciles them.
- With [[build-vs-buy]] — buying is almost always faster to ship than building; build only where it produces competitive advantage.
- With [[serverless-vs-servers]] — serverless tends to be the fastest path to first deployment, which is why Chapter 4 recommends "look at using serverless first."

## Cross-book framing

- [[reliable-product-launches]] and [[launch-checklist]] (SRE) are the reliability-engineering counterpart — shipping fast *and* safely requires a launch-coordination discipline.
- [[high-release-velocity]] (SRE release engineering) is the reliability lens on the same goal.
- [[cost-of-change]] (Richards and Ford) is the architectural counterpart — keep the cost of change low so shipping quickly remains viable long-term.

## Related pages

- [[technology-selection]]
- [[principles-of-good-data-architecture]]
- [[reversible-vs-irreversible-decisions]]
- [[immutable-vs-transitory-technologies]]
- [[build-vs-buy]]
- [[type-a-vs-type-b-data-engineers]]
- [[high-release-velocity]]
- [[cost-of-change]]
