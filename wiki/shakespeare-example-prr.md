# Shakespeare Example: PRR

**Summary**: The end-of-chapter worked example in Chapter 32, applying the [[simple-prr-model|Simple PRR Model]] to the Shakespeare service. The developers were originally responsible for pager, but growth in usage and revenue made SRE support desirable; a PRR surfaced a monitoring gap, the gap was fixed, and SRE took over the pager with two developers remaining in the rotation and joining the weekly on-call meeting.

**Sources**: `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## The setup

The Shakespeare service was launched and the development team was initially on the pager. Usage grew, revenue grew, and SRE support became desirable — the classic pre-PRR-takeover shape. The service being already launched means the Simple PRR Model applies (source: chapter-32-the-evolving-sre-engagement-model.md).

## What the PRR found

One concrete issue Chapter 32 names: dashboards were not completely covering some of the metrics defined in the SLO (source: chapter-32-the-evolving-sre-engagement-model.md). A monitoring gap that made the service's reliability commitments not fully observable — the kind of finding a [[prr-analysis-phase|PRR Analysis phase]] is designed to surface.

After the filed issues were fixed, SRE took over the pager.

## The handoff shape

Chapter 32 describes the steady-state arrangement after onboarding (source: chapter-32-the-evolving-sre-engagement-model.md):

- SRE holds the pager
- Two developers remain in the on-call rotation
- Developers attend the weekly on-call meeting, discussing last week's problems and upcoming large-scale maintenance or cluster turndowns
- Future plans for the service are now discussed with SRE to ensure new launches go flawlessly

This is the [[prr-onboarding-phase|Onboarding phase]]'s "mixed rotation" pattern: a partial-ownership handoff in which developers provide safety-net coverage and ongoing knowledge transfer while SRE settles in.

## Why this example is useful

Chapter 32 uses Shakespeare because the example recurs throughout the book as a running illustration of the Google production environment (see [[life-of-a-request]] and [[n-plus-2-redundancy]]). Applying the PRR to it closes the loop: the reader sees not just how the service works in production but how it *became* an SRE-supported service in the first place.

## Related pages

- [[simple-prr-model]]
- [[production-readiness-review]]
- [[prr-analysis-phase]]
- [[prr-onboarding-phase]]
- [[production-meetings]]
- [[life-of-a-request]]
- [[site-reliability-engineering]]
