# Balanced On-Call

**Summary**: SRE's on-call load is managed on two axes — **quantity** (what percentage of an SRE's time is spent on-call) and **quality** (how many incidents occur per shift). Chapter 11 fixes concrete bounds on both: no more than 25% of SRE time on-call, no more than 2 incidents per 12-hour shift, with an 8-person single-site minimum team size falling out of the arithmetic.

**Sources**: `raw/site-reliability-engineering/chapter-11-being-on-call.md`, `raw/site-reliability-engineering/chapter-29-dealing-with-interrupts.md`

**Last updated**: 2026-04-17

---

## The two axes

On-call workload is not a single number. Chapter 11 decomposes it (source: chapter-11-being-on-call.md):

- **Quantity** = percent of SRE time spent on on-call duties.
- **Quality** = number of incidents per on-call shift.

SRE managers are responsible for keeping both axes balanced and sustainable. A team can be overloaded on quantity (too many shifts per person), on quality (too many pages per shift), or both — the remedies are different in each case.

## Balance in quantity: the 25% rule

The "E" in SRE is defining: **at least 50% of SRE time goes to engineering**, and of the remaining half, **no more than 25% goes to on-call** (source: chapter-11-being-on-call.md). That leaves up to 25% for other operational non-project work.

### The staffing arithmetic

The 25% cap produces a concrete minimum team size (source: chapter-11-being-on-call.md):

- Assume always two people on-call (primary + secondary).
- Week-long shifts.
- Each engineer should be on-call at most one week in four (25%).

For a **single-site team**: minimum 8 engineers (each on primary *or* secondary for one week per month).

For a **dual-site team**: minimum 6 engineers per site, both to honour the 25% rule and to ensure a critical mass of engineers. Multi-site also eliminates night shifts — see [[multi-site-on-call]].

The arithmetic floor from Chapter 5 (two weeks per month of on-call = 33% for a 6-person rotation, 25% for an 8-person rotation — see [[toil-and-engineering-balance]]) reappears here as the reason 8 is the target floor for single-site teams.

## Balance in quality: 2 incidents per 12-hour shift

Chapter 11 defines an **incident** as a sequence of events and alerts related to the same root cause that would be discussed in the same postmortem (source: chapter-11-being-on-call.md).

The empirical finding: **dealing with a single incident end-to-end — root-cause analysis, remediation, postmortem, bug fixes — averages 6 hours of work**. It follows that the upper bound on incidents per shift is:

> **Maximum 2 incidents per 12-hour on-call shift.**

The implication for the distribution: the median incidents/day should likely be **0**. A component that pages every day (median > 1) is unsustainable by definition — something else will also break at some point, pushing the total above 2.

If the bound is exceeded for a quarter, concrete corrective measures are required to return the load to sustainability — see [[operational-overload]] and Chapter 30.

## Relationship to Chapter 1's "two events per shift"

Chapter 1's "at most two events per 8-12-hour shift" from [[toil-and-engineering-balance]] is the same number from the other direction: Chapter 11 derives it from the 6-hour-per-incident average, rather than stating it as a rule. The shift length has widened (8-12 → 12) because Chapter 11 is talking about the worst case; the Chapter 1 range covers shorter shifts common in some teams.

## Relationship to the engineering cap

Balanced on-call is the operational realisation of the Chapter 5 engineering cap. The quantity axis (25% cap) is what keeps on-call from crowding out engineering; the quality axis (2 incidents per shift) is what keeps on-call from becoming firefighting that stops producing postmortems. Both axes together define the sustainable zone.

## On-call as a fully-polarised work mode (Chapter 29)

Chapter 29 sharpens the quantity axis with a specific rule: **an on-call week should be written off for project work**. An engineer who is on-call should focus solely on on-call work, and whatever tickets or cleanup fill the pager-is-quiet gaps. If a project is too important to let slip for the week, the engineer shouldn't be on-call — escalate and assign someone else (source: chapter-29-dealing-with-interrupts.md).

This is a stronger rule than the Chapter 11 25% cap: Chapter 11 says *at most one week in four*, Chapter 29 says *that week is entirely an interrupt mode, not a mix.* The two combine: the 25% figure is meaningful only when the 25% is fully polarised rather than interleaved — see [[polarizing-time]].

The structural reason: **on-call is a high-context-switch-cost interrupt mode**. Trying to simultaneously make project progress on-call produces the [[cognitive-flow-state|constant-interruptability]] state Chapter 29 is designed to defeat. The 2-incidents-per-shift quality bound and the fully-polarised on-call week are the two halves of making on-call reachable flow rather than stress.

## Related pages

- [[sre-on-call-engagement]]
- [[multi-site-on-call]]
- [[on-call-compensation]]
- [[operational-overload]]
- [[operational-underload]]
- [[toil-and-engineering-balance]]
- [[engineering-work-categories]]
- [[emergency-response]]
- [[blameless-postmortem]]
- [[sre-tenets]]
- [[dealing-with-interrupts]]
- [[polarizing-time]]
- [[cognitive-flow-state]]
