# Postmortem Triggers

**Summary**: The criteria Google uses to decide when a postmortem is required. Because writing a postmortem has a real time cost, teams are deliberate about when to invest in one — but the criteria must be **defined ahead of the incident** so the decision isn't made under post-hoc pressure.

**Sources**: `raw/site-reliability-engineering/chapter-15-postmortem-culture-learning-from-failure.md`

**Last updated**: 2026-04-17

---

## The rule: define triggers before the incident

Chapter 15's load-bearing sentence (source: chapter-15-postmortem-culture-learning-from-failure.md):

> It is important to define postmortem criteria before an incident occurs so that everyone knows when a postmortem is necessary.

Post-hoc decisions about whether an incident "deserves" a postmortem are the path to incidents getting quietly forgotten. Pre-declared triggers turn the question into a checklist: if any trigger fired, a postmortem is written, full stop.

## Google's common triggers

Chapter 15 lists the common triggers Google teams use (source: chapter-15-postmortem-culture-learning-from-failure.md):

- **User-visible downtime or degradation beyond a certain threshold.** The specific threshold is service-dependent; see [[service-level-objective|SLOs]] as the natural place to peg it.
- **Data loss of any kind.** Zero tolerance — any data loss triggers a postmortem regardless of scale.
- **On-call engineer intervention** — release rollback, rerouting of traffic, etc. A system that needed a human to keep running is a system with a failure mode worth investigating.
- **Resolution time above some threshold.** Even incidents that resolved without customer impact may be worth a postmortem if they took unexpectedly long to fix.
- **A monitoring failure** — which usually implies **manual incident discovery**. This is the critical one; see below.

## Monitoring failure as a trigger

The "monitoring failure" trigger is the one that makes the list reflexive. An incident that was **not caught by monitoring** is an incident that reveals a gap in the monitoring system itself. Chapter 1's [[blameless-postmortem|blameless postmortem]] page already surfaces this point: postmortems for non-paging incidents are arguably more valuable because they expose monitoring gaps the team didn't know it had.

This connects to the [[alert-philosophy]] / [[four-golden-signals]] material — every non-paged incident is a candidate signal the monitoring system should have been watching.

## Stakeholder-requested postmortems

Beyond the objective triggers, Chapter 15 explicitly allows (source: chapter-15-postmortem-culture-learning-from-failure.md):

> In addition to these objective triggers, any stakeholder may request a postmortem for an event.

This matters because stakeholders often see patterns the on-call engineer doesn't — a customer support lead might notice a class of user complaints correlating with a flap, even if no SLI tipped over a threshold. The stakeholder-request channel keeps the trigger list from becoming the only way in.

## Team flexibility vs consistency

Chapter 15 notes that teams have **internal flexibility** to set their own thresholds — the list above is common, not mandatory. Each SRE team calibrates to its service: a team running a storage service might set a tighter data-loss trigger than a team running a best-effort cache. What's not flexible:

- Triggers must be **written down** and agreed on in advance.
- Any stakeholder can always request one regardless of the team's list.
- Blamelessness and the review discipline apply uniformly.

## The cost-of-writing tradeoff

Chapter 15 acknowledges explicitly that postmortems have a cost in time and effort, which is why triggers exist as a gate. But the cost framing can mislead: a **poorly-scoped postmortem investment** is cheap short-term and expensive long-term (the incident recurs; new hires lack context; trend analysis can't see it). The chapter's closing section on continuous investment in postmortem culture is the counter-argument — **over Google's history, the investment has paid for itself in fewer outages**.

## The stigma warning

Chapter 15 also warns against a perverse incentive (source: chapter-15-postmortem-culture-learning-from-failure.md):

> It is also important not to stigmatize frequent production of postmortems by a person or team.

A team that has been writing lots of postmortems is not a team that is "bad at reliability" — it is, on average, a team that is **good at surfacing failures**. Stigmatising postmortem frequency produces the cover-up failure mode Chapter 15 is entirely designed to prevent.

## Related pages

- [[postmortem-philosophy]]
- [[blameless-postmortem]]
- [[postmortem-template]]
- [[postmortem-review-process]]
- [[alert-philosophy]]
- [[declaring-an-incident]]
- [[service-level-objective]]
