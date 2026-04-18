# System Stability vs Agility

**Summary**: The governing tension Chapter 9 of *Site Reliability Engineering* identifies between change-induced risk and the need for change. A system in a vacuum — no code changes, no hardware or library changes, no user growth — would be perfectly stable. Real systems must evolve, so SRE's job is to **keep stability and agility in balance**, and to notice that reliable processes tend to *increase* developer agility rather than restrict it.

**Sources**: `raw/site-reliability-engineering/chapter-09-simplicity.md`, `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The vacuum thought experiment

Chapter 9 opens with a thought experiment (source: chapter-09-simplicity.md):

> Software systems are inherently dynamic and unstable. A software system can only be perfectly stable if it exists in a vacuum. If we stop changing the codebase, we stop introducing bugs. If the underlying hardware or libraries never change, neither of these components will introduce bugs. If we freeze the current user base, we'll never have to scale the system.

This framing matters because it reframes change itself as the source of instability, not the occasional bad change. Every change carries risk; change in aggregate is the load-bearing driver of almost all outages ([[change-management-sre|70% of outages come from changes]]).

## The SRE summary

Luebbe quotes his former manager Johan Anderson (source: chapter-09-simplicity.md):

> At the end of the day, our job is to keep agility and stability in balance in the system.

This is the operational-philosophy complement to the [[error-budget]] mechanism from Chapter 3. The budget is *how* the balance is struck quantitatively; "agility vs stability" is the thing being balanced qualitatively.

## Exploratory coding as a deliberate imbalance

Chapter 9 allows that sometimes stability should be sacrificed for agility on purpose (source: chapter-09-simplicity.md):

> I've often approached an unfamiliar problem domain by conducting what I call exploratory coding — setting an explicit shelf life for whatever code I write with the understanding that I'll need to try and fail once in order to really understand the task I need to accomplish. Code that comes with an expiration date can be much more liberal with test coverage and release management because it will never be shipped to production or be seen by users.

The release-discipline and test-coverage expectations are properties of the **production path**, not of code in general. Scoping exploratory code out of that path is what makes relaxed standards safe.

## Reliable processes increase agility

The counterintuitive claim in the section is that investing in reliability *helps* velocity rather than constraining it (source: chapter-09-simplicity.md):

> SREs work to create procedures, practices, and tools that render software more reliable. At the same time, SREs ensure that this work has as little impact on developer agility as possible. In fact, SRE's experience has found that reliable processes tend to actually increase developer agility: rapid, reliable production rollouts make changes in production easier to see. As a result, once a bug surfaces, it takes less time to find and fix that bug.

The logic:

1. Reliable rollouts → each change goes out in a small, observable batch.
2. Small batches → bugs surface against a small diff.
3. Small diff → fast triage, fast fix.
4. Fast fix → the team trusts the process and ships more often.

This is the same positive feedback loop [[high-release-velocity]] identifies from the release-engineering side and [[change-management-sre]] identifies from the automation side. Chapter 9's contribution is to name the loop explicitly in terms of developer experience: reliability is not a tax on velocity, it is the thing that lets velocity scale.

## Chapter 17's restatement through the build system

Chapter 17 frames the same tension through the lens of the build pipeline (source: chapter-17-testing-for-reliability.md):

> The concepts of stability and agility are traditionally in tension in the world of SRE. The last bullet point provides an interesting case where stability actually drives agility. When the build is predictably solid and reliable, developers can iterate faster!

The "last bullet point" is the observation that a broken mainline makes emergency releases (e.g. for security vulnerabilities) dramatically harder. A team whose default build state is green can ship an emergency fix in minutes; a team whose build is habitually broken has to stabilise before they can fix.

The reliability-drives-velocity framing in Chapter 9 is the macro version of the same claim. See [[build-system-discipline]] for Ch 17's full operational argument.

## The two forms of imbalance

Although Chapter 9 does not enumerate them, the text implies two failure modes:

- **Too much stability, not enough agility** — change freezes, overlong review processes, change-advisory-boards as the [[sysadmin-approach|sysadmin approach]] tends to produce. Reliability appears high in the short term but the organisation cannot respond to new requirements.
- **Too much agility, not enough stability** — unreviewed pushes, no progressive rollout, no rollback path. Features ship fast but reliability collapses and the team enters permanent firefighting.

Both failure modes are the subject of other chapters: [[sysadmin-approach]] for the stability-heavy side, [[automation-gone-wrong]] and the 70% change-induced outage rate for the agility-heavy side.

## Cross-book connections

- [[error-budget]] — the quantitative mechanism the balance is expressed through; velocity spent against the budget
- [[change-management-sre]] — the automation trio that makes agility safe without sacrificing stability
- [[high-release-velocity]] — the release-engineering side of the same argument: frequent small changes are both more agile and more reliable
- [[toil-and-engineering-balance]] — the related tension between operational work and engineering work that the 50% cap arbitrates
- [[sre-discipline]] — the staffing model that lets one team own both sides of the tension

## Related pages

- [[simplicity-sre]]
- [[error-budget]]
- [[change-management-sre]]
- [[high-release-velocity]]
- [[toil-and-engineering-balance]]
- [[sre-discipline]]
- [[sysadmin-approach]]
- [[site-reliability-engineering]]
- [[testing-for-reliability]]
- [[build-system-discipline]]
