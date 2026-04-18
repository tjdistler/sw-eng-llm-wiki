# Trial by Fire Anti-Pattern

**Summary**: Chapter 28's named anti-pattern for SRE onboarding — throwing a new hire at the ticket queue on day one and hoping they eventually "click." The approach is self-selected by ops-driven reactive teams, alienates capable engineers, and fails the core trust-building requirement for on-call.

**Sources**: `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## The pattern

Chapter 28 opens its *case for structure over chaos* section with a worked example (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> John is the newest member of the FooServer SRE team. Senior SREs on this team are tasked with a lot of grunt work, such as responding to tickets, dealing with alerts, and performing tedious binary rollouts. On John's first day on the job, he is assigned all new incoming tickets. [...] "Sure, there will be a lot of upfront learning that you'll have to do," says John's manager, "but eventually you'll get much faster at these tickets. One day, it will just click..."

A senior teammate completes the framing: *"We're throwing you in the deep end of the pool here."*

## Why teams do it

Widdowson's diagnosis: the anti-pattern is **born out of a team's current environment** (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md). Ops-driven, reactive SRE teams have nothing *but* reactive work to offer, so they onboard their newbies by making them react — over and over again.

It is a self-perpetuating failure mode: a team that hasn't been able to pay down its reactive work has no spare capacity to build a structured curriculum, so new hires are processed through the reactive queue, which guarantees the team stays reactive.

## Why it fails

Three problems:

- **Survivorship bias.** "If you're lucky, the engineers who are already good at navigating ambiguity will crawl out of the hole you've put them in. But chances are, this strategy has alienated several capable engineers" (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md). The people who come out the other side look fine; the ones who left or disengaged don't appear in the retrospective.
- **False premise about teaching by doing.** The anti-pattern assumes most aspects of the team can be taught strictly by doing, rather than by reasoning. Widdowson's sharp rebuttal: *if the set of work one encounters in a tickets queue will adequately provide training for said job, then this is not an SRE position*.
- **Confidence erosion.** SREs joining from university or traditional SWE/sysadmin roles already face identity disruption. Leaving basic progress questions unanswered — *what am I working on? how much progress have I made? when will I be ready for on-call?* — compounds that disruption into slower development and retention problems.

## What questions get left unanswered

Widdowson lists the three questions a newbie asks that trial-by-fire cannot answer (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

1. What am I working on?
2. How much progress have I made?
3. When will these activities accumulate enough experience for me to go on-call?

The ticket queue provides no answer to any of these. Each ticket is sui generis; cumulative progress toward a defined goal is not a property of the queue.

## The constructive alternative

Chapter 28's answer is to replace the queue with:

- [[cumulative-learning-paths]] — sequential, ordered curriculum with theory frontloaded and hands-on experience as soon as practical
- [[on-call-learning-checklist]] — the document artifact that enumerates what must be learned
- [[targeted-project-work]] — starter projects that build real ownership rather than reactive experience
- The broader blueprint in [[sre-onboarding]]

The constructive practices are **as concrete as any ticket or alert** — but they are *sequential*, so the newbie knows where they are and where they are going.

## Relationship to the broader SRE argument

Trial by fire is the onboarding-side equivalent of the [[sysadmin-approach|sysadmin anti-pattern]] at the discipline level: a reactive default that appears cheap in the short term but costs more over time. Chapter 1's [[toil-and-engineering-balance|50% cap on toil]] is how the team-level reactive spiral is broken; Chapter 28's cumulative learning paths are how the onboarding-level reactive spiral is broken.

The two are connected: a team trapped above the 50% cap is also the team that will onboard by trial by fire, because it has no engineering capacity to build anything else.

## Related pages

- [[sre-onboarding]]
- [[cumulative-learning-paths]]
- [[on-call-learning-checklist]]
- [[targeted-project-work]]
- [[sysadmin-approach]]
- [[toil-and-engineering-balance]]
- [[operational-overload]]
