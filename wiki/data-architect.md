# Data Architect

**Summary**: The role responsible for technology decisions, architecture descriptions, and disseminating those choices through leadership and training. Reis and Housley argue the role is evolving away from the ivory-tower archetype toward one that is technically current, agile, and inseparable from data engineering.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`, `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## What a data architect does

From Chapter 3 (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

> Data architects are responsible for technology decisions and architecture descriptions and disseminating these choices through effective leadership and training.

The data architect is:

- **Technically competent** — deep enough to make good decisions and credibly mentor
- **Delegatory** — most individual-contributor work goes to others
- **A leader** — in the mentoring-and-enabling sense, not the command-and-control sense

Strong leadership combined with high technical competence is **rare and extremely valuable**; the best architects take this duality seriously.

## Against command-and-control

Chapter 3 explicitly rejects the older archetype (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

> It was not uncommon in the past for architects to choose one proprietary database technology and force every team to house their data there. We oppose this approach because it can significantly hinder current data projects.

Modern architects balance common-component choices with flexibility that lets project teams innovate. The cloud makes this balance much easier to strike — storage-compute separation, plug-and-play services, and self-serve platforms let an architect enable rather than dictate.

## The *Architectus Oryzus* archetype

Chapter 3 adopts Martin Fowler's archetype directly (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

> In many ways, the most important activity of Architectus Oryzus is to mentor the development team, to raise their level so they can take on more complex issues. Improving the development team's ability gives an architect much greater leverage than being the sole decision-maker and thus running the risk of being an architectural bottleneck.

The data architect embodies this: has the technical skills of a data engineer but no longer does data engineering day to day; mentors current engineers; makes careful technology choices in consultation with the organisation; disseminates expertise through training.

This parallels the leadership framing in Richards and Ford's [[architect-expectations|eight architect expectations]] — especially *mentoring and leading* and *possessing both technical depth and business acumen*.

## Architect vs data engineer

Chapter 2 first drew the line: the [[data-engineer]] is usually a separate role from the data architect. The engineer works alongside the architect, **delivers on their designs, and provides architectural feedback** (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

Chapter 3 then argues the line is softening (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

> Gone are the days of ivory tower data architecture. In the past, architecture was largely orthogonal to engineering. We expect this distinction will disappear as data engineering, and engineering in general, quickly evolves, becoming more agile, with less separation between engineering and architecture.

In practice:

- Big companies still employ dedicated data architects — but those architects must stay current on technology and data
- Small or low-maturity companies often have a data engineer doing double duty as architect
- The engineer-architect collaboration is the normal mode; trade-offs get evaluated together

## The trade-offs the architect works on

Chapter 3's examples of the questions a data architect faces (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- What are the trade-offs of adopting a cloud [[data-warehousing|data warehouse]] versus a [[data-lake]]?
- What are the trade-offs of various cloud platforms?
- When is a unified batch/streaming framework (Beam, Flink) the right choice?

The architect's job is to study these choices **in the abstract** before facing the concrete decision — so that when the moment arrives, a good decision can be made quickly and with documented justification.

## Cross-book framing

- Richards and Ford's [[architect-expectations]] — the eight behavioural expectations placed on any architect regardless of title
- [[architect-career-path]] — how engineers become architects
- [[architect-control-spectrum]] — the control-spectrum framing that situates Reis and Housley's rejection of command-and-control

## Related pages

- [[data-architecture]]
- [[data-engineer]]
- [[principles-of-good-data-architecture]]
- [[architect-expectations]]
- [[architect-control-spectrum]]
- [[architectural-thinking]]
- [[trade-off-analysis]]
- [[data-engineering-lifecycle]]
