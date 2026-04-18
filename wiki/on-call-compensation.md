# On-Call Compensation

**Summary**: Google pays for out-of-hours support with either **time-off-in-lieu** or **straight cash**, capped at a proportion of overall salary. The cap is deliberate — it limits how much on-call any one person can absorb, reinforcing the [[balanced-on-call|25%-per-engineer rule]] and protecting against burnout.

**Sources**: `raw/site-reliability-engineering/chapter-11-being-on-call.md`

**Last updated**: 2026-04-17

---

## The policy

Chapter 11 is explicit that out-of-hours support requires compensation (source: chapter-11-being-on-call.md):

> Adequate compensation needs to be considered for out-of-hours support.

Google offers two options:

- **Time off in lieu** of hours worked on-call.
- **Straight cash compensation**.

Either way the compensation is **capped at some proportion of overall salary**.

## Why the cap

The cap is the non-obvious part. Compensation without a cap incentivises the opposite of what the team needs: a few individuals absorbing most of the load, under-trained newcomers, burnt-out heroes.

The cap **limits the amount of on-call work any single individual will take on** (source: chapter-11-being-on-call.md). It does two things simultaneously:

1. **Incentivises participation** — on-call work is rewarded, so engineers are willing to do their share rather than treating it as unpaid extra.
2. **Prevents overload** — once an engineer hits the cap, additional on-call hours produce no additional reward, so they push back rather than volunteering.

Together the two effects produce a balanced distribution: everyone participates, nobody overparticipates.

## What the cap protects against

The explicit harms Chapter 11 names (source: chapter-11-being-on-call.md):

- **Burnout** — the accumulation of stress, sleep disruption, and interruptions.
- **Inadequate time for project work** — on-call always displaces engineering, and the 50% cap is supposed to protect engineering.

Both are the same failure mode the [[toil-and-engineering-balance|50% engineering cap]] protects against, viewed from a different angle. Compensation design is a structural lever that reinforces the cap from the incentives side.

## Cross-book connection

Most ops-industry compensation structures do not cap on-call pay; they scale it up as an incentive to volunteer for extra load. Chapter 11's cap is the opposite design — it treats *participation* as valuable and *over-participation* as a symptom of a broken team. The shift mirrors the broader SRE stance from [[sre-discipline]]: structural limits produce healthier behaviour than incentives aimed at individuals.

## Related pages

- [[balanced-on-call]]
- [[sre-on-call-engagement]]
- [[toil-and-engineering-balance]]
- [[sre-discipline]]
- [[operational-overload]]
