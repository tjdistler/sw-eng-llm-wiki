# SRE Onboarding

**Summary**: Chapter 28's blueprint for bootstrapping a new SRE to on-call and beyond. The thesis is that SRE onboarding must be a deliberately designed curriculum — not a trial by fire — because on-call depends on trust, and trust depends on demonstrable competence across reverse-engineering, statistical-comparative thinking, and improvisation.

**Sources**: `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## The framing

Chapter 28 (Andrew Widdowson) opens with the claim that up-front investment in training produces better engineers faster, and that SRE onboarding is harder than generic engineer onboarding because of the additional **trust** requirement: other on-callers need to trust that the new SRE knows the system, can diagnose atypical behaviour, asks for help when appropriate, and can react under pressure (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md).

That trust requirement reframes the training question. It is not enough to ask "what does a newbie need to learn to go on-call?" One must also ask:

- How can existing on-callers **assess the readiness** of the newbie for on-call?
- How can we **harness the enthusiasm** of new hires so senior SREs benefit from it?
- What activities benefit **everyone's** education, now and ongoing?

The goal is not to produce a functioning ticket-responder. It is to produce an SRE the rest of the team would be happy to hand the pager to.

## The blueprint (Figure 28-1)

Chapter 28's bootstrapping blueprint has two axes:

- **Time** — from day one to going on-call to continuing education
- **Abstract ↔ applied** — a spectrum from reading postmortems on one end to hands-on breakage on the other

Four reading rules:

1. New SREs start from **zero knowledge** of the target systems, so [[teachable-postmortems|postmortems]] and [[reverse-engineering-class|reverse-engineering exercises]] are good starting points.
2. After system fundamentals, SREs move to [[shadow-on-call|shadow on-call]] and documentation work.
3. Going on-call is a **milestone** — after it, learning becomes nebulous, self-directed, and continuous.
4. Project work starts small and grows; it does not stop at on-call (it continues throughout).

## The case for structure over chaos

Chapter 28's first major argument is against the [[trial-by-fire-anti-pattern|trial-by-fire anti-pattern]] — throwing newbies at the ticket queue and hoping they eventually "click." That approach presumes the discipline can be taught strictly by doing. Widdowson's counter: *if the set of work one encounters in a tickets queue adequately provides training for said job, then this is not an SRE position* (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md).

The constructive alternative:

- [[cumulative-learning-paths]] — sequential, ordered curriculum
- [[on-call-learning-checklist]] — the document artifact that structures the curriculum
- [[targeted-project-work]] — small, shippable starter projects instead of menial toil

## The three SRE aspirational attributes

Once you have a curriculum, what should it *develop*? Chapter 28 names three attributes that a production engineer at scale must exhibit:

- [[reverse-engineering-skills]] — the ability to figure out systems you've never seen before, because production is always changing
- [[statistical-comparative-thinking]] — the ability to prune a massive decision tree under pressure via hypothesis-construction and controlled-variable comparison
- [[improvisational-troubleshooting]] — the ability to compose defences when standard procedures don't fit the problem

[[reverse-engineering-class]] is Widdowson's worked example of a single course that touches all three.

## Five practices for aspiring on-callers

Chapter 28's core practice catalogue. Any or all can be adopted:

1. [[teachable-postmortems]] — curate, share, and discuss postmortems; reading clubs; "tales of fail"
2. [[disaster-role-playing]] — the [[on-call-playbook|Wheel of Misfortune]] tabletop exercise, weekly
3. [[breaking-real-systems]] — hands-on chaos on a loaned-from-production instance
4. [[documentation-as-apprenticeship]] — on-call learning checklist overhaul as a newbie assignment
5. [[shadow-on-call]] — copy the pager to the newbie during business hours; see also [[reverse-shadow-on-call]]

## Getting to on-call

The milestone. Chapter 28's framing:

- Completion of the [[on-call-learning-checklist]] — or a final exam-style gate — is the typical evidence of readiness
- Some teams use a [[reverse-shadow-on-call|reverse shadow]] rotation as the last step
- Going on-call is a **rite of passage** that should be celebrated as a team
- Learning **does not stop** — see [[sre-continuing-education]]

## The governing maxim

Widdowson's closing line captures the why (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> As SRE, you have to scale your humans faster than you scale your machines.

Onboarding is the mechanism by which that scaling happens. The [[sre-discipline|sublinear-scaling-of-SRE-with-system-size]] argument from Chapter 1 assumes that each new SRE quickly reaches full productivity; Chapter 28 is the operational manual for making that assumption hold.

## Related pages

- [[sre-discipline]]
- [[sre-on-call-engagement]]
- [[balanced-on-call]]
- [[operational-underload]]
- [[on-call-playbook]]
- [[blameless-postmortem]]
- [[postmortem-culture-activities]]
- [[trial-by-fire-anti-pattern]]
- [[cumulative-learning-paths]]
- [[on-call-learning-checklist]]
- [[targeted-project-work]]
- [[reverse-engineering-skills]]
- [[statistical-comparative-thinking]]
- [[improvisational-troubleshooting]]
- [[reverse-engineering-class]]
- [[teachable-postmortems]]
- [[disaster-role-playing]]
- [[breaking-real-systems]]
- [[documentation-as-apprenticeship]]
- [[shadow-on-call]]
- [[reverse-shadow-on-call]]
- [[sre-continuing-education]]
