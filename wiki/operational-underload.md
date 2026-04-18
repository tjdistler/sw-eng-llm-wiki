# Operational Underload

**Summary**: The "treacherous enemy" of an SRE team — being on-call for a system so quiet that engineers lose touch with production. Chapter 11's position is that underload is as dangerous as overload, because knowledge gaps and miscalibrated confidence only surface during an incident. The remedies are team sizing, Wheel of Misfortune exercises, and Google's annual DiRT disaster-recovery drills.

**Sources**: `raw/site-reliability-engineering/chapter-11-being-on-call.md`, `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## Why quiet is dangerous

A system that never pages is blissful until it does. Chapter 11's framing (source: chapter-11-being-on-call.md):

> An operational underload is undesirable for an SRE team. Being out of touch with production for long periods of time can lead to confidence issues, both in terms of overconfidence and underconfidence, while knowledge gaps are discovered only when an incident occurs.

Two failure modes fall out of underload:

- **Overconfidence** — the system has been fine for months, so the engineer assumes they understand it. The incident reveals they don't.
- **Underconfidence** — the engineer hasn't touched production recently, hesitates to act, and MTTR suffers.

Either way, the first page after a long quiet period is where the cost comes due.

## The remedies

### Team sizing

SRE teams should be sized to allow **every engineer to be on-call at least once or twice a quarter** (source: chapter-11-being-on-call.md). That's the lower bound on rotation size that keeps exposure frequent enough to stay current.

This is why Chapter 11 argues against growing a single-site team past ~8 when a service gets bigger — the [[multi-site-on-call|multi-site alternative]] keeps rotations small enough that each engineer still gets hands-on production exposure.

### Wheel of Misfortune

Scenario-based on-call exercises (see [[on-call-playbook]] and [[disaster-role-playing]]) are team activities for *honing and improving troubleshooting skills and knowledge of the service* (source: chapter-11-being-on-call.md). Chapter 28 covers these in depth.

A Wheel of Misfortune session simulates an incident: one engineer plays on-call, others play the game master injecting symptoms. The engineer has to diagnose the problem using the same tools and playbooks they'd use in production. The exercise builds:

- Reflexes for the tools.
- Familiarity with the playbook.
- Visibility into where the playbook is wrong or incomplete.
- Realistic calibration of how long things actually take.

Chapter 28's operational framing adds another detail the underload remedy benefits from: the scenarios are often taken **from the team's own historical incidents** (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md), which means the exercise doubles as institutional-memory refresh. Quiet teams especially benefit: the veterans may remember the old incidents but haven't rehearsed responding to them in years, and the newer members may never have seen them at all. See [[teachable-postmortems]] for how postmortems feed the scenario library.

### DiRT — Disaster Recovery Training

Google runs a **company-wide annual DiRT event** (source: chapter-11-being-on-call.md, citing [Kri12]) that combines theoretical and practical drills to perform multi-day testing of infrastructure systems and individual services. It is the organisational-scale version of Wheel of Misfortune — whole systems and whole on-call rotations exercised at once, as realistic as it's possible to make them without causing an actual outage.

## The balance

Operational [[operational-overload|overload]] and operational underload are the two failure modes at opposite ends of the on-call quantity axis. The [[balanced-on-call|balanced zone]] — 25% on-call with 2 or fewer incidents per shift — is the sustainable centre. Both ends compromise the engineer's ability to respond to the service.

The balance is harder than it looks: a team that successfully drives an overloaded service toward lower incidents has to watch for the flip into underload, and put the drills in place before the quiet sets in.

## Related pages

- [[operational-overload]]
- [[balanced-on-call]]
- [[multi-site-on-call]]
- [[sre-on-call-engagement]]
- [[on-call-playbook]]
- [[emergency-response]]
- [[toil-and-engineering-balance]]
- [[sre-tenets]]
- [[disaster-role-playing]]
- [[breaking-real-systems]]
- [[sre-continuing-education]]
- [[sre-onboarding]]
- [[teachable-postmortems]]
