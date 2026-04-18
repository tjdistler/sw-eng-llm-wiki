# Software Engineering in SRE

**Summary**: Chapter 18's argument that SRE teams should run full-fledged software engineering projects — not just one-off automation scripts — and the practices that make such projects succeed. The central case study is [[auxon|Auxon]], Google's [[intent-based-capacity-planning|intent-based capacity planner]]; the chapter generalises from it into lessons on project selection, staffing, adoption, and organisational discipline.

**Sources**: `raw/site-reliability-engineering/chapter-18-software-engineering-in-sre.md`

**Last updated**: 2026-04-17

---

## The argument

SREs are uniquely positioned to write internal tools that solve internal production problems, because they have **firsthand experience** of the problem space and a **direct relationship with the intended user** (themselves and fellow SREs) (source: chapter-18-software-engineering-in-sre.md). Third-party tools rarely operate at Google's scale; the people running production are the ones who most clearly see what needs to exist.

The bigger organisational argument: SRE-supported services grow exponentially but SRE headcount must grow only linearly (or slower). The gap is closed by **perpetual automation work** and **tool development** — the only sustainable way to handle that growth is to have the people running the systems also build the software that makes running them easier. See [[sre-discipline]] for the sublinear-scaling thesis this builds on.

## Why develop software inside SRE

Four advantages Chapter 18 lists (source: chapter-18-software-engineering-in-sre.md):

- **Appropriate design considerations** — SREs bring production-specific concerns (scalability, graceful degradation, infrastructure integration) as first-class design inputs.
- **Subject-matter embedding** — the developers *are* the customers, so requirements are understood directly, not translated.
- **High-signal feedback** — releasing to internal SRE users means frank, technically-grounded feedback and tolerance of rough edges.
- **Organisational scaling** — linear SRE team growth against exponential service growth is impossible without automation, and the best automation is written by the people doing the automation.

## Why develop software *as an SRE*

The argument flows the other way too. Software-engineering projects benefit SREs and the SRE org (source: chapter-18-software-engineering-in-sre.md):

- **Career development** — a path for SREs who want to keep their coding skills sharp.
- **Balance against interrupts and on-call** — long-term project work is the antidote to the spikiness of operational load. See [[engineering-work-categories]] for where this fits in the four-way taxonomy.
- **Team diversity** — development projects attract engineers with varied backgrounds, which helps SRE's blind-spot problem.
- **Staffing and retention** — Google deliberately staffs SRE teams with a mix of traditional software-engineering and systems-engineering backgrounds.

## The case study: Auxon

Chapter 18's worked example is [[auxon|Auxon]], an SRE-built tool for [[intent-based-capacity-planning|intent-based capacity planning]] that replaced spreadsheet-driven bin-packing across several Google divisions. Auxon demonstrates every point in the chapter:

- Firsthand-experience origin (SRE + TPM who had both done manual capacity planning)
- Launch-and-iterate development under uncertainty (the "Stupid Solver")
- Agnostic design that let customers bring their own tools
- Deliberate adoption strategy (target teams with no incumbent; white-glove onboarding; customer case studies as advertising)
- Ongoing SRE embedding: the Auxon team stayed on call for services, so they remained their own customer

See [[auxon]] for the full architecture and [[sre-product-adoption]] for the adoption lessons.

## Lessons learned: building the software

Chapter 18 distils Auxon's development into a set of named disciplines. See [[sre-software-development-lessons]] for the catalogue. The short version:

- **Approximation** — don't focus on perfection when bounds aren't known; build a simplified component (the Stupid Solver), hide it behind an interface, and replace it later.
- **Agnostic design** — integrate with whatever the customer already uses, so adoption doesn't require abandoning existing tools.
- **Modularity** for fuzzy requirements — when data or integrations will change, hide them behind interfaces so future swaps don't force a rewrite.
- **Launch and iterate** — ship something useful early; let real use drive the roadmap.

## Lessons learned: driving adoption

The technical work is necessary but insufficient. Chapter 18 devotes a full section to the **socialisation** and **adoption** work that turns a working tool into a widely-used one. See [[sre-product-adoption]].

- Consistent messaging and user advocacy
- Sponsorship from senior engineers and management
- Setting expectations (aspirational long-term vs MVP short-term)
- Identifying the right first customers (teams with no incumbent beat teams with a working home-grown alternative)
- White-glove customer service for early adopters
- Designing at the right level of generality

## Picking projects: what makes a good candidate

Chapter 18 closes with selection criteria (source: chapter-18-software-engineering-in-sre.md). See [[fostering-software-engineering-in-sre]] for the full discussion. Strong positive signals:

- Engineers with firsthand domain experience who want to work on it
- A highly-technical target user base (for high-signal bug reports)
- Noticeable benefits — reduced toil, improved infrastructure, streamlined complex processes
- Alignment with the organisation's overall objectives, so leadership can advocate for it

Red flags:

- Touches many moving parts at once
- Requires an all-or-nothing approach (no iterative path)
- Service-specific benefits that don't generalise (SRE's service-aligned team structure makes this common)
- At the opposite extreme: too generic, too universal, too abstract — flexibility without concrete use cases

## Staffing and development time

Two prerequisites for SRE software development to actually happen (source: chapter-18-software-engineering-in-sre.md):

- **A mix of generalists and specialists** on the seed team — generalists for breadth, specialists for depth. Auxon's team eventually added statisticians and optimisation experts, but not until after the basic product was working.
- **Partnership with PMs / TPMs / SWE-experienced engineers** who know how to run a user-facing software project. The anecdote: "I have a design doc; why do we need requirements?" is the conventional-SRE stance the partnership corrects.
- **Dedicated, non-interrupt project time** — aggressively defended. You cannot write code while thrashing between tickets.

The essential constraint: **SREs doing software development must continue working as SREs**. Don't let them become full-time embedded developers; the production-world immersion is what makes the software good.

## Introducing the model: "getting there"

Chapter 18's closing section is a change-management guide for SRE leaders who want to establish software-development practice in an existing SRE org. See [[introducing-sre-software-development]] for the detail. The four moves:

1. **Create and communicate a clear message** — start with skepticism ("SREs are a skeptical lot… we specifically hire for it"); sell benefits explicitly (consistent solutions speed new-SRE ramp-up; reducing the number of ways to do a task makes skills portable across teams).
2. **Evaluate organisational capabilities** — identify missing roles (PM, agile coach, product owner) and fill them by borrowing from product-development teams or, eventually, hiring.
3. **Launch and iterate** — deliver something of value early; establish credibility with a straightforward, uncontroversial first target; six-month release rhythm.
4. **Don't lower standards** — apply the same code review, testing, and production-readiness bar to SRE-developed software as to any other software. Treat it as a product an SRE team would onboard.

## Related pages

- [[auxon]]
- [[intent-based-capacity-planning]]
- [[traditional-capacity-planning]]
- [[sre-software-development-lessons]]
- [[sre-product-adoption]]
- [[fostering-software-engineering-in-sre]]
- [[introducing-sre-software-development]]
- [[sre-discipline]]
- [[engineering-work-categories]]
- [[toil-and-engineering-balance]]
- [[capacity-planning]]
- [[site-reliability-engineering]]
