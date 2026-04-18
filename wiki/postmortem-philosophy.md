# Postmortem Philosophy

**Summary**: Chapter 15's framing of *why* Google writes postmortems: incidents are inevitable at scale and velocity, so without a formalised learning mechanism they recur ad infinitum. The postmortem is the written record whose primary goal is not documentation for its own sake but **effective preventive action** — ensuring the incident, its impact, the mitigations, the contributing causes, and the follow-ups are all captured so the organisation becomes harder to hurt the same way twice.

**Sources**: `raw/site-reliability-engineering/chapter-15-postmortem-culture-learning-from-failure.md`, `raw/site-reliability-engineering/chapter-16-tracking-outages.md`

**Last updated**: 2026-04-17

---

## The opening argument

Chapter 15 opens with an empirical claim and a structural consequence (source: chapter-15-postmortem-culture-learning-from-failure.md):

> As SREs, we work with large-scale, complex, distributed systems. We constantly enhance our services with new features and add new systems. Incidents and outages are inevitable given our scale and velocity of change. ... Unless we have some formalized process of learning from these incidents in place, they may recur ad infinitum. Left unchecked, incidents can multiply in complexity or even cascade, overwhelming a system and its operators and ultimately impacting our users.

The argument:

1. Scale + velocity → incidents are inevitable.
2. Without structured learning, the same incident recurs.
3. Worse: without structured learning, incidents **compound** — new systems built on the same un-learned-from substrate create failure modes that cascade.
4. Therefore the **only sustainable response** to incidents is a formalised learning mechanism. That mechanism is the postmortem.

This is the same logic as [[error-budget]] inverted: the error budget tolerates failure as the price of velocity; the postmortem is the mechanism that ensures the toleration doesn't turn into complacency.

## The three primary goals

The primary goals of a postmortem are (source: chapter-15-postmortem-culture-learning-from-failure.md):

1. **Document the incident.**
2. **Understand all contributing root causes.**
3. **Put effective preventive actions in place** to reduce the likelihood and/or impact of recurrence.

The emphasis is on the third. Chapter 15 explicitly calls out "effective preventive actions" as the special case worth stressing — a postmortem that captures the first two but doesn't produce durable preventive work is a postmortem that has failed its purpose.

Chapter 15 doesn't prescribe a specific root-cause-analysis technique. Teams pick what suits their service; see the chapter's reference to the Rooney survey [Roo04] for a detailed menu.

## Not a formality

Chapter 15 is explicit about what a postmortem is *not* (source: chapter-15-postmortem-culture-learning-from-failure.md):

> The postmortem is not written as a formality to be forgotten. Instead the postmortem is seen by engineers as an opportunity not only to fix a weakness, but to make Google more resilient as a whole.

This framing matters for two reasons:

- Postmortems written as compliance artefacts — "we had to write one because policy says so" — produce shallow analysis and follow-up items nobody tracks.
- Postmortems written as **genuine engineering opportunities** produce the action items that compound into systemic improvement.

The cultural preconditions for the second mode are what most of the rest of Chapter 15 is about: [[blameless-postmortem|blamelessness]], review discipline, visible rewards, survey-driven process improvement. See [[postmortem-culture-activities]] and [[rewarding-postmortems]].

## The blameless foundation

Blameless postmortems are a **tenet of SRE culture** (source: chapter-15-postmortem-culture-learning-from-failure.md). Chapter 15 is where the Chapter 1 one-line tenet gets its full development; the core material is catalogued in [[blameless-postmortem]]. The key sharpenings Chapter 15 adds:

- The origin story: blameless culture originated in **healthcare and avionics**, industries where mistakes can be fatal. Both nurture environments where every mistake is an opportunity to strengthen the system.
- The operative shift: from allocating blame to **investigating the systematic reasons why an individual or team had incomplete or incorrect information**.
- The mechanism: "you can't fix people, but you can fix systems and processes to better support people making the right choices."
- The failure mode of the alternative: "if a culture of finger pointing and shaming individuals or teams for doing the 'wrong' thing prevails, people will not bring issues to light for fear of punishment."

The two-example contrast (pointing fingers vs blameless) in Chapter 15 is a concrete demonstration: both texts identify the same technical issue (backend system breakage, long maintenance manual) but only the blameless version produces a constructive action item.

## When to write one

See [[postmortem-triggers]] for the full criteria. The headline rule: triggers must be **defined before an incident occurs** so everyone knows when a postmortem is necessary. Common triggers include user-visible degradation, data loss, on-call intervention, resolution-time thresholds, and monitoring failures (which are monitoring gaps made visible). Any stakeholder may also request one.

## The compounding loop

Chapter 15's closing argument (source: chapter-15-postmortem-culture-learning-from-failure.md):

> We can say with confidence that thanks to our continuous investment in cultivating a postmortem culture, Google weathers fewer outages and fosters a better user experience.

The compounding happens through several mechanisms:

- **Cross-team learning.** See [[postmortem-review-process]]: postmortems are shared to the widest possible audience, not kept within the team that had the incident.
- **Trend analysis.** See [[postmortems-at-google-working-group]]: aggregated postmortems reveal common themes that no single postmortem exposes.
- **Institutional memory.** Reading-club and Wheel-of-Misfortune replays keep years-old incidents alive as learning material; see [[postmortem-culture-activities]].
- **Reinforcement.** Visibly rewarding good incident handling and well-written postmortems makes the behaviour sustainable; see [[rewarding-postmortems]].

## What postmortems don't cover: Chapter 16's complement

Chapter 16 opens by naming a gap in postmortem coverage (source: chapter-16-tracking-outages.md):

> Postmortems (see Chapter 15) provide detailed information for individual outages, but they are only part of the answer. They are only written for incidents with a large impact, so issues that have individually small impact but are frequent and widespread don't fall within their scope. Similarly, postmortems tend to provide useful insights for improving a single service or set of services, but may miss opportunities that would have a small effect in individual cases, or opportunities that have a poor cost/benefit ratio, but that would have large horizontal impact.

Two structural limitations this names:

- **The significance bar.** Postmortems are triggered (see [[postmortem-triggers]]) only for incidents that cross a threshold. Chronic low-impact alerts and frequent-but-minor failures are invisible to the postmortem corpus.
- **The per-service lens.** A postmortem improves *this service*. Patterns that only show up when you aggregate across services — and mitigations whose per-incident payoff is small but whose horizontal payoff is large — aren't going to surface through the postmortem review process alone.

Chapter 16's [[outage-tracking|outage-tracking]] discipline is the **complement**, not the replacement. It provides the aggregate breadth that postmortems' depth leaves uncovered:

| Covered by postmortems (Ch 15) | Covered by outage tracking (Ch 16) |
|---|---|
| Depth per significant incident | Breadth across every alert |
| Root-cause analysis of one event | Cross-event and cross-team patterns |
| Triggered above a significance bar | Passive — captures everything |
| Per-service action items | Horizontal and infrastructure-level action items |
| Learning via [[postmortem-review-process|review pipeline]] | Learning via [[outage-analysis|three-layer analysis]] |

Both pipelines feed [[learning-from-outages|the same organisational-memory loop]]. Neither alone is sufficient.

## Cross-book connection

The SRE postmortem philosophy aligns with the [[unknown-unknowns]] framing in Richards & Ford: you cannot anticipate every failure mode, so the architecture must be learning-driven. The postmortem is the mechanism that converts each discovered unknown into captured, reviewable, acted-upon knowledge.

## Related pages

- [[blameless-postmortem]]
- [[postmortem-triggers]]
- [[postmortem-template]]
- [[postmortem-review-process]]
- [[postmortem-culture-activities]]
- [[rewarding-postmortems]]
- [[postmortem-feedback-surveys]]
- [[postmortems-at-google-working-group]]
- [[learning-from-outages]]
- [[outage-tracking]]
- [[outalator]]
- [[site-reliability-engineering]]
