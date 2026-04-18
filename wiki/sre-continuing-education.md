# SRE Continuing Education

**Summary**: Chapter 28's closing framing — going on-call is not the end of learning but a shift in its shape. After a newbie joins the rotation, learning becomes self-directed and continuous: regular team learning series, presentations by SREs shepherding new features, co-presenting with developers, and outward talks to developer counterparts.

**Sources**: `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## The rite-of-passage framing

Chapter 28's transition (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> Regardless of how you gate this milestone, going on-call is a rite of passage and it should be celebrated as a team.

The celebration is not just morale — it is a cultural signal that the bar has been met. The team publicly acknowledges that the new SRE is trusted with the pager; that acknowledgement creates the accountability that sustains the trust going forward.

## Why learning does not stop

Chapter 28's rhetorical question and answer:

> Does learning stop when a student joins the ranks of on-call? Of course not! To remain vigilant as SREs, your team will always need to be active and aware of changes to come.

Production systems keep changing. The SRE who stops learning discovers that their mental model of the system has quietly diverged from reality — typically during the incident where that divergence becomes visible. Continuing education is the countermeasure, and it applies to everyone on the team, not only newbies.

## The regular learning series

Chapter 28's primary mechanism (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> Set up a regular learning series for your whole team, where overviews of new and upcoming changes to your stack are given as presentations by the SREs who are shepherding the changes, who can co-present with developers as needed.

Three design elements:

- **Regular rhythm** — not on-demand; scheduled so there is always a next session on the calendar
- **SRE-led with developer participation** — the SRE shepherding the change presents, optionally with the developer author; this framing keeps SRE in the driver's seat of production understanding
- **Forward-looking** — overviews of upcoming changes, not just retrospectives of what already shipped

## Record the sessions

Chapter 28's note: *if you can, record the presentations so that you can build a training library for future students.* The same recording serves two purposes:

- **Continuing education** for the team that attended live
- **Onboarding material** for future newbies going through the [[cumulative-learning-paths|learning paths]] when that subsystem comes up

This compounds: each recorded session is one less thing a future newbie has to learn by interrogating senior SREs individually.

## Talks to the developer side

A secondary mechanism (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> Consider having SREs give talks to your developer counterparts. The better your development peers understand your work and the challenges your team faces, the easier it will be to reach fully informed decisions on later projects.

The framing is mutual: SRE presentations to devs improve the quality of the eventual system because devs make design decisions with more awareness of production constraints. It is also a career-development channel — SREs get visible exposure to a broader audience, which matters for growth and retention.

## What continuing education is *not*

Chapter 28 does not describe continuing education as a separate curriculum. It is the ongoing version of the same practices newbies went through:

- [[teachable-postmortems|Postmortem reading]] — now as a regular review habit rather than a first introduction
- [[disaster-role-playing|Wheel of Misfortune]] — weekly, keeping veterans current on new features just as much as onboarding newbies
- Learning series presentations on new stack changes (this page's core content)

The distinction is in *stance*: newbie learning is mostly receptive and sequential; continuing learning is mostly self-directed and prioritised against project work.

## Connection to operational underload

Chapter 11's [[operational-underload]] identifies the failure mode continuing education is meant to prevent: a quiet service where engineers drift out of touch with production. The remedies Chapter 11 names (Wheel of Misfortune, DiRT, sufficient rotation frequency) are structurally the same as Chapter 28's continuing-education catalogue — they just target veterans rather than newbies. The two chapters solve the same problem at different career stages.

## The governing maxim, again

Chapter 28's closing line (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> As SRE, you have to scale your humans faster than you scale your machines. Good luck to you and your teams in creating a culture of learning and teaching!

Continuing education is how that scaling is sustained. Onboarding gets humans to full productivity the first time; continuing education keeps them there as production changes underneath them.

## Related pages

- [[sre-onboarding]]
- [[operational-underload]]
- [[on-call-playbook]]
- [[disaster-role-playing]]
- [[teachable-postmortems]]
- [[cumulative-learning-paths]]
- [[shadow-on-call]]
- [[balanced-on-call]]
