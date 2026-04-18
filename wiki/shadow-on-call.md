# Shadow On-Call

**Summary**: Chapter 28's penultimate onboarding practice — the newbie is copied on incoming pages during business hours, giving them a front-row seat to real incidents while the primary on-caller retains ownership. Builds the mentor's visibility into the student's progress, builds the team's confidence in the newbie's eventual rotation entry, and gives the student their first exposure to real pages without the time pressure of being responsible for them.

**Sources**: `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## Why shadow at all

Chapter 28's concession (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> Ultimately, no amount of hypothetical disaster exercises or other training mechanisms will fully prepare an SRE for going on-call. At the end of the day, tackling real outages will always be more beneficial from a learning standpoint than engaging with hypotheticals.

But:

> Yet it's unfair to make newbies wait until their first real page to have a chance to learn and retain knowledge.

Shadow on-call is the **bridge**: the newbie gets real-incident exposure before the full responsibility of being primary. The two "front row seat to the outage while it unfolds" property is load-bearing — reading postmortems afterwards is far less instructive than watching the process unfold in real time.

## Prerequisites

Shadow on-call is not day one. Chapter 28's placement (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> After the student has made their way through all system fundamentals (by completing, for example, an [[on-call-learning-checklist|on-call learning checklist]]), consider configuring your alerting system to copy incoming pages to your newbie, at first only during business hours.

Two preconditions:

- System fundamentals are **substantially complete** — the shadow can follow what's happening
- The alerting system supports **page copying** — the newbie receives the same information the primary does

The "at first only during business hours" qualifier is deliberate. Shadowing after-hours pages is higher-stakes and higher-stress; the business-hours constraint keeps the experience scoped until the newbie is ready.

## The two visibility payoffs

Chapter 28 names the benefits on both sides (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

- **For the mentor**: visibility into the student's progress — how do they reason about pages? what do they pick up quickly? where do they stall?
- **For the student**: visibility into the responsibilities of being on-call — not just the incident handling, but the tempo, the interruptions, the communication load

Shadowing multiple members of the team matters. Chapter 28's guidance: *by arranging for the newbie to shadow multiple members of their team, the team will become increasingly comfortable with the thought of this person entering the on-call rotation.* The team-comfort mechanism is explicit; shadowing builds trust one senior engineer at a time.

## The trust-building mechanism

Chapter 28's strongest claim about why this matters for the team as a whole (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> Instilling confidence in this manner is an effective method of building trust, allowing more senior members to detach when they aren't on-call, thus helping to avoid team burnout.

The pathology shadow on-call prevents: senior SREs who don't trust the newcomers can never fully go off-duty, which is how [[operational-overload|operational overload]] propagates from the team level into individuals' lives. Shadow rotations produce the observable evidence (*I watched them handle the last three pages*) that lets the senior team genuinely detach.

## During the shadowed incident

Chapter 28's operational guidance (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

- The new SRE is **not the appointed on-caller** — this removes time pressure; they can think without the clock on them
- Shadow and primary may **share a terminal session**, or sit near each other to compare notes
- After the incident, at a time of mutual convenience, the on-caller reviews the reasoning and process followed — this **increases the shadow's retention** of what actually occurred

The post-incident review step is where most of the learning consolidates. Chapter 28 emphasises "mutual convenience" — avoid the temptation to debrief immediately when both parties are drained.

## The postmortem co-authorship rule

Chapter 28's explicit warning (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> Should an outage occur for which writing a postmortem is beneficial, the on-caller should include the newbie as a coauthor. Do not dump the writeup solely on the student, because it could be mislearned that postmortems are somehow grunt work to be passed off on those most junior. It would be a mistake to create such an impression.

The co-authorship rule is culturally important. [[blameless-postmortem|Postmortems]] are a senior engineering artifact at Google — offloading them to the most junior person reverses the hierarchy of value. Chapter 28 insists on getting this framing right from the newbie's first exposure.

## The progression

Chapter 28's Figure 28-1 blueprint puts shadow on-call in the "immediately before going on-call" window. The common progression:

1. Complete system fundamentals and the [[on-call-learning-checklist]]
2. Begin **shadow on-call** across multiple mentors (business hours)
3. Possibly move to [[reverse-shadow-on-call|reverse shadow on-call]] — newbie is primary, mentor lurks independently
4. Go **full on-call** — a rite of passage to be celebrated ([[sre-continuing-education]] picks up here)

The stepping-stone structure lets readiness be demonstrated progressively rather than gated on a single exam.

## Related pages

- [[sre-onboarding]]
- [[reverse-shadow-on-call]]
- [[on-call-learning-checklist]]
- [[cumulative-learning-paths]]
- [[sre-continuing-education]]
- [[sre-on-call-engagement]]
- [[balanced-on-call]]
- [[operational-overload]]
- [[blameless-postmortem]]
- [[on-call-playbook]]
