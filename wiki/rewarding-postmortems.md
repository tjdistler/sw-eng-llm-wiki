# Rewarding Postmortems

**Summary**: Chapter 15's named best practice — *visibly reward people for doing the right thing*. A blameless culture removes the fear of punishment, but removing fear isn't enough on its own; sustained postmortem discipline requires the **positive** incentive as well. Google's mechanisms include peer bonuses, public recognition at company-wide TGIF meetings, and internal social praise.

**Sources**: `raw/site-reliability-engineering/chapter-15-postmortem-culture-learning-from-failure.md`

**Last updated**: 2026-04-17

---

## The principle

The blameless framing in [[blameless-postmortem]] removes the *negative* incentive against postmortems — fear of blame. But fear removal alone is insufficient. Chapter 15's reward-focused best practice (source: chapter-15-postmortem-culture-learning-from-failure.md):

> Make sure that writing effective postmortems is a rewarded and celebrated practice, both publicly through the social methods mentioned earlier, and through individual and team performance management.

Two parallel channels:

- **Public social recognition** — postmortem of the month, TGIF spotlights, peer bonuses.
- **Performance management** — postmortem quality and follow-through count toward individual and team reviews.

The second is easy to overlook but load-bearing. If postmortem work doesn't show up in performance reviews, the implicit organisational signal is that it doesn't matter. The first is what makes the reward visible and salient to the rest of the organisation.

## The TGIF story

Chapter 15 tells one incident in detail as the worked example of visible reward (source: chapter-15-postmortem-culture-learning-from-failure.md):

> A 2014 TGIF focused on "The Art of the Postmortem," which featured SRE discussion of high-impact incidents. One SRE discussed a release he had recently pushed; despite thorough testing, an unexpected interaction inadvertently took down a critical service for four minutes. The incident only lasted four minutes because the SRE had the presence of mind to roll back the change immediately, averting a much longer and larger-scale outage.

This is the Chapter 13 [[change-induced-emergency|change-induced emergency]] retold from the recognition angle. What the SRE received:

- **Two peer bonuses** immediately afterward — Google's peer-to-peer cash recognition mechanism for exceptional work (Chapter 15 footnote 3).
- **A huge round of applause** from the TGIF audience of Googlers numbering in the thousands, with company founders present.

The details matter. The engineer who caused the outage was publicly **celebrated**, not punished — specifically because his rapid response (roll-back-on-first-sign-of-trouble) was the behaviour the organisation wanted reinforced. The four-minute outage became the benchmark-case for what good incident response looks like.

## What's being rewarded

Chapter 15's TGIF example rewards a specific bundle of behaviours:

- **Level-headed handling** — the SRE didn't panic or try to debug-first.
- **Quick rollback** — see [[change-management-sre]] and the Chapter 13 lessons on rollback-as-primary-response.
- **Presence of mind under stress** — see [[incident-response-mindset]] for the cognitive-load argument.

The reward isn't for "avoiding an outage" — the outage happened. It's for **limiting the outage's impact by responding correctly once it was detected**. This sharpens the organisational signal: what matters is the full loop (detect, respond, recover, learn), not the impossible ideal of never breaking anything.

## Peer bonuses and internal social networks

Beyond TGIF, Chapter 15 names two ongoing channels (source: chapter-15-postmortem-culture-learning-from-failure.md):

- **The Peer Bonus program** (footnote 3) — a way for fellow Googlers to recognise colleagues for exceptional efforts, with a token cash reward.
- **Internal social networks** that drive peer praise toward well-written postmortems and exceptional incident handling. Recognition comes from peers, CEOs, and everyone in between.

The distribution of recognition sources is deliberate. Top-down recognition alone (CEO-only) is unsustainable; peer-only recognition can miss the organisational-significance signal. Having recognition flow from all directions makes it robust.

## Why fear-removal isn't enough

An organisation could plausibly have:

- Blameless postmortem culture (no punishment for incidents).
- No positive reward for postmortem work.

The predicted outcome: postmortems get written, but perfunctorily — nobody is *punished* for a shallow postmortem, and nobody is *rewarded* for a deep one, so the rational act is to do the minimum. Chapter 15's argument is that the full cultural loop requires both polarities: fear off, reward on.

## The alignment with Chapter 13

Chapter 13's [[learning-from-outages]] page ends with the claim that organisations doing this consistently will, over years, run better systems than organisations that don't. Chapter 15's reward mechanisms are the incentive infrastructure that makes the consistency possible. Without rewards, the discipline depends on individual motivation and decays with turnover.

## Stigma avoidance

Chapter 15 also reiterates the inverse — **don't stigmatise frequent postmortem production** (source: chapter-15-postmortem-culture-learning-from-failure.md). Teams that write many postmortems are, on average, teams that are good at surfacing failures. Penalising them (or their individual engineers) produces the cover-up failure mode the whole system is designed to prevent. See [[postmortem-triggers]] for the related cost-of-writing framing.

## Related pages

- [[postmortem-philosophy]]
- [[blameless-postmortem]]
- [[postmortem-culture-activities]]
- [[postmortem-review-process]]
- [[change-induced-emergency]]
- [[incident-response-mindset]]
- [[change-management-sre]]
- [[learning-from-outages]]
