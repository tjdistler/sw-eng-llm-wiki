# "Enterprisey" Data Engineering

**Summary**: Reis and Housley's term for the trickle-down of data management, governance, operations, and quality practices — historically reserved for giant organisations — to companies of every size. Chapter 11 frames this as one of the two "safer" predictions in the chapter: it's already happening day by day as tooling simplifies and the hard technology problems get abstracted away.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md`

**Last updated**: 2026-04-18

---

## The word "enterprisey"

The chapter opens with a disclaimer. "Enterprise," to many readers, "conjures Kafkaesque nightmares of faceless committees dressed in overly starched blue shirts and khakis, endless red tape, and waterfall-managed development projects with constantly slipping schedules and ballooning budgets." Reis and Housley are **not** predicting the return of that enterprise (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

What they mean by "enterprisey" is the **good things big companies do with data** — management, operations, governance, the "boring stuff." Big companies had to invent these practices because their scale forced them to. Now, as tooling makes it trivial for any company to operate large-scale data infrastructure, the bottleneck moves from technology to management, and everyone faces the boring-stuff problem.

## What's trickling down

Concepts and tools once reserved for Fortune-500-style organisations are now standard offerings for SMBs (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

- **[[data-management]]** — DAMA DMBOK-style practices around stewardship, lifecycle, and lineage.
- **[[data-governance]]** — discoverability, security, accountability, policy.
- **[[data-quality]]** — accuracy, completeness, timeliness as programmed checks.
- **[[dataops|DataOps]]** — automation, [[data-observability|observability]], incident response as first-class disciplines.
- **[[data-catalog|Data cataloging]]** and **[[data-lineage|lineage]]** — becoming table stakes, not big-company luxuries.
- **[[data-lifecycle-management]]** and **[[data-retention]]** — driven by GDPR, CCPA, and the general compliance floor.

## Why it's happening now

Two drivers (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

- **Simplification of tooling.** Once hard parts of big data and streaming have been "largely abstracted away, with the focus shifting to ease of use, interoperability, and other refinements." The stuff that's left is management, not plumbing.
- **Documented best practices.** The field has matured to the point that common patterns are written down and shared.

The net effect: data engineers working on new tooling find opportunities "in the abstractions of data management, DataOps, and all the other undercurrents of data engineering."

## Alignment with the maturity model

The prediction is an extension of the [[data-maturity|data-maturity model]] from Chapter 1. Stage 3 ("leading with data") is where enterprisey concerns already dominate a data engineer's day-to-day (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md). Chapter 11's prediction is that **Stage-3 concerns arrive sooner at every company** — smaller companies hit them earlier in their life cycle, because the tools make the technology easy and the governance is what's left.

See [[data-engineering-history]] for the pattern: what's old is new again. Enterprise data governance was "for banks"; it's now in every well-run Stage 3 company and increasingly in Stage 2 companies too.

## How safe is this prediction?

Chapter 11 explicitly flags this as one of the safer predictions in the chapter (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

> Some aspects of our prognostication sit on a relatively secure footing. The simplification of managed tooling and the rise of "enterprisey" data engineering have proceeded day by day as we've written this book.

Contrast with the more speculative [[live-data-stack]] prediction.

## Consequence for the data engineer

Data engineers should expect to spend more of their time on (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

- Governance design, not just pipeline design.
- Quality programs, not just quality code.
- Observability and SLA management, not just monitoring.
- Communication with compliance, legal, and business stakeholders, not just with SWE/DS peers.

See [[data-engineer]] for the role's broader evolution and [[titles-will-morph]] for how role boundaries blur with SWE, DS, and MLE.

## Related pages

- [[future-of-data-engineering]]
- [[data-management]]
- [[data-governance]]
- [[data-quality]]
- [[data-observability]]
- [[dataops]]
- [[data-catalog]]
- [[data-lineage]]
- [[data-lifecycle-management]]
- [[data-maturity]]
- [[data-engineering-history]]
- [[data-engineer]]
