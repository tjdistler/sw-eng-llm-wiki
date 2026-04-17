# Architecture Vitality

**Summary**: How viable an architecture defined three or more years ago remains today, given changes in business requirements and the technology ecosystem. An architect is expected to **continually analyze** an architecture because its opposite, structural decay, creeps in silently.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-01-introduction.md`

**Last updated**: 2026-04-16

---

## The concept

Richards and Ford introduce architecture vitality as the subject of the second of the eight [[architect-expectations]]: *continually analyze the architecture*. Vitality asks — given three or more years of drift in the business, the technology ecosystem, and the codebase itself — is the architecture still fit for purpose? (source: chapter-01-introduction.md)

The authors observe that most architects do not spend enough time on this, and that as a result most architectures experience **structural decay**.

## Structural decay

Structural decay happens when developers make coding or design changes that erode the required [[architecture-characteristics|architecture characteristics]] — performance, availability, scalability, and others (source: chapter-01-introduction.md). Each individual change is locally reasonable; the cumulative effect is that an architecture that once hit its characteristics no longer does.

Often-forgotten extensions of decay (source: chapter-01-introduction.md):

- **Testing environments** — if tests take weeks, no amount of source-code agility buys architectural agility.
- **Release environments** — if releases take months, the feedback loop is too slow for the architecture to evolve.

Richards and Ford are explicit that vitality is holistic: changes in technology, problem domain, tooling, and operational practice all matter.

## How to maintain vitality

The book develops mechanisms across multiple chapters; Chapter 1 flags them:

- **Fitness functions** — objective, automated checks on architecture characteristics that run on every change, so regression is visible immediately. Covered in Chapter 6. See [[architecture-fitness-function]].
- **[[evolutionary-architecture]]** — architecture designed from the start to change gracefully. Ford's separate book of the same name is the deep reference.
- **Architecture Decision Records** — per the [[laws-of-software-architecture|Second Law]], capturing *why* each decision was made lets future teams tell which decisions have been invalidated by context change and which still hold. Chapter 19.
- **[[architect-expectations|The architect's job]]** — expectation #2 makes vitality part of the role, not an optional extra. Expectation #4 (compliance) catches individual violations that cumulatively cause decay.

## Relation to earlier wiki material

- [[accidental-complexity]] — decay is largely the accumulation of accidental complexity; each shortcut adds a little.
- [[maintainability]] — vitality is to an architecture what maintainability is to a codebase: the long-run resistance to degradation.
- [[seams-and-legacy-code]] — Feathers's refactoring substrate inside a monolith is a code-level analogue of vitality work at the architectural level.
- [[breaking-changes]] — Newman's framing of accidental API breakage is a specific vector of structural decay at service boundaries.

## Why it matters

The [[laws-of-software-architecture|First Law]] says every architecture is a bundle of trade-offs. Over time, the environment that made those trade-offs correct shifts: cloud availability zones replace data centres; language runtimes get faster; team topology changes; the business moves into a new market. An architecture that was optimal three years ago may be clearly sub-optimal now — but it will continue running until someone looks. Vitality work is that looking.

## Related pages

- [[architect-expectations]]
- [[architecture-characteristics]]
- [[architecture-fitness-function]]
- [[evolutionary-architecture]]
- [[software-architecture-definition]]
- [[laws-of-software-architecture]]
- [[accidental-complexity]]
- [[maintainability]]
- [[breaking-changes]]
- [[fundamentals-of-software-architecture]]
