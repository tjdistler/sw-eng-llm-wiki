# DevOps vs SRE

**Summary**: DevOps and SRE overlap heavily in principle but differ in specificity. Benjamin Treynor Sloss's framing from *Site Reliability Engineering* Chapter 1: DevOps is a generalisation of several core SRE principles to a wider range of organisations; SRE is a specific, more opinionated implementation of DevOps.

**Sources**: `raw/site-reliability-engineering/chapter-01-introduction.md`

**Last updated**: 2026-04-17

---

## Shared principles

The term DevOps emerged in industry in late 2008. Its core principles are consistent with many of SRE's (source: chapter-01-introduction.md):

- **Involvement of the IT function in each phase** of a system's design and development — the opposite of the [[sysadmin-approach|throw-it-over-the-wall]] model.
- **Heavy reliance on automation versus human effort.**
- **Application of engineering practices and tools to operations tasks.**

Both movements reject the same dysfunction: the cultural and communication gap between separate development and operations teams.

## The framing

Treynor Sloss offers two reciprocal views (source: chapter-01-introduction.md):

> One could view DevOps as a generalisation of several core SRE principles to a wider range of organisations, management structures, and personnel. One could equivalently view SRE as a specific implementation of DevOps with some idiosyncratic extensions.

## Where SRE is more opinionated

Reading the chapter, several SRE specifics go beyond the DevOps umbrella:

- **Hiring**: [[sre-discipline|SRE]] explicitly staffs operations with software engineers (50-60% from the standard SWE pipeline). DevOps does not prescribe a hiring model.
- **The 50% cap**: [[toil-and-engineering-balance]] is a concrete, measured limit with a defined feedback mechanism (push work back to dev). DevOps broadly endorses automation without this structural enforcement.
- **Error budgets**: [[error-budget]] is a specific contract that resolves the dev-vs-ops conflict by quantifying acceptable unreliability. Generic DevOps does not mandate error budgets.
- **Monitoring output taxonomy**: SRE insists there are only three valid monitoring outputs (alerts, tickets, logs — see [[sre-monitoring-outputs]]). DevOps is less prescriptive.
- **On-call discipline**: SRE has concrete rules (maximum two events per 8–12 hour shift, postmortems for significant incidents). See [[emergency-response]] and [[blameless-postmortem]].

These additions are what Treynor Sloss calls SRE's "idiosyncratic extensions" — the things that happen when a specific large organisation (Google) implements the general DevOps philosophy under its own constraints.

## When the distinction matters

For most organisations, the distinction is academic: both movements point in the same direction. It starts to matter when you try to scale a mature SRE practice into an organisation that has only adopted DevOps broadly. The error-budget conversation, in particular, requires a level of quantitative [[service-level-objective|SLO]] discipline and management support that many DevOps-named teams do not yet have.

## Related pages

- [[sre-discipline]]
- [[sysadmin-approach]]
- [[toil-and-engineering-balance]]
- [[error-budget]]
- [[sre-tenets]]
