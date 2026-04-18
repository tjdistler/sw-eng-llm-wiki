# Break-Glass Push

**Summary**: An emergency mechanism that lets an operator push a configuration or binary change *before* release testing completes — the "break the glass" metaphor for an override used only in urgent situations. Chapter 17's guidance: don't disable the tests, just let the push proceed in parallel and back-annotate any test failures so a flawed push can be followed quickly by a corrected one, with the push event filed as a bug for a more robust resolution next time.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The principle

> You can implement a break-glass mechanism to disable release testing. Doing so means that whoever makes a hurried manual edit isn't told about any mistakes until the real user impact is reported by monitoring. It's better to leave the tests running, associate the early push event with the pending testing event, and (as soon as possible) back-annotate the push with any broken tests. This way, a flawed manual push can be quickly followed by another (hopefully less flawed) manual push. (source: chapter-17-testing-for-reliability.md)

Two ways to implement "break the glass":

1. **Disable release testing** — push proceeds with no testing gate. Mistakes reach users. Monitoring finds them.
2. **Keep testing running, push in parallel** — the push has already gone to production when the tests finish. Tests that fail back-annotate the push, giving the operator a fast signal to push a corrective fix.

The chapter argues firmly for the second model. Silencing tests silences the feedback channel that tells you whether you just made it worse.

## Boost test priority on break-glass

> Ideally, that break-glass mechanism automatically boosts the priority of those release tests so that they can preempt the routine incremental validation and coverage workload that the test infrastructure is already processing. (source: chapter-17-testing-for-reliability.md)

The tests for a break-glass push are time-critical in a way routine tests are not — a delay in surfacing a break means a delay in corrective action. Preempting the regular queue is worth it.

## Where break-glass interacts with reliability

Chapter 17 frames break-glass in a reliability-budget sense (source: chapter-17-testing-for-reliability.md):

> Since breaking the glass impairs reliability, it's generally a good idea to make the break noisy by (for example) filing a bug requesting a more robust resolution for next time.

Two consequences:

- Break-glass should be used **rarely** — noisy each time it happens.
- Each use should produce a bug for engineering work to make the manual intervention unnecessary the next time. Repeated break-glass events on the same code path are a signal that the system's normal release path isn't good enough.

This is an MTTR-MTBF trade: break-glass cuts MTTR in a specific incident by bypassing the normal gate, and the bug-filing discipline reinvests the savings into raising MTBF.

## Cross-book connections

- [[configuration-management-sre]] (Ch 8) — configuration files exist partly to keep MTTR low by being faster to change than a binary rebuild; break-glass is the extreme form
- [[mttr-and-mttf]] — break-glass is explicitly an MTTR-favouring mechanism; Ch 17 frames it as an acceptable trade when the bug-filing discipline is followed
- [[change-management-sre]] — break-glass is a controlled deviation from the automation trio; the discipline is what keeps it from becoming the default
- [[operational-overload]] (Ch 11) — teams that break glass frequently are showing one of the overload symptoms; the bug backlog from break-glass events is a leading indicator

## Related pages

- [[testing-for-reliability]]
- [[configuration-management-sre]]
- [[change-management-sre]]
- [[mttr-and-mttf]]
