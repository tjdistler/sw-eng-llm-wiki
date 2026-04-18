# Production Meetings

**Summary**: Chapter 31's canonical SRE communication instrument — a weekly 30-60 minute service-oriented meeting where the team articulates the state of its services to itself and invited stakeholders, connects operational performance back to design and implementation decisions, and closes the feedback loop from production experience to engineering choices. Unlike most meetings in the literature, the chapter argues, this one pays for itself.

**Sources**: `raw/site-reliability-engineering/chapter-31-communication-and-collaboration-in-sre.md`

**Last updated**: 2026-04-17

---

## Purpose

The production meeting has two goals (source: chapter-31-communication-and-collaboration-in-sre.md):

1. **Shared understanding**: everyone leaves with the same idea of what is going on with the service.
2. **Feedback loop from production to engineering**: discuss operational performance in detail, and relate it to design, configuration, or implementation — then make recommendations for fixes.

The second goal is the load-bearing one. The chapter calls it "an immensely powerful feedback loop" — connecting the performance of the service to design decisions in a regular meeting is what turns production experience into engineering work. It is the organisational realisation of SRE's [[sre-discipline|software-engineers-running-operations]] premise.

The meeting is **service-oriented, not status-oriented**. It is not about what individuals did; it is about what the service did.

## Frequency and duration

Weekly is the default. The chapter's reasoning (source: chapter-31-communication-and-collaboration-in-sre.md):

- Any less frequent and relevant material doesn't accumulate predictably; any more frequent and people find excuses to skip.
- 30-60 minutes is the right duration. **Less than 30 minutes** suggests you're rushing important material or your service portfolio is too small. **More than 60 minutes** suggests you're mired in detail or the team/service set needs sharding.

## Chairing

The meeting needs a chair. Many SRE teams **rotate the chair** through team members. Trade-off:

- **Benefits**: everyone feels a stake in the service and notional ownership of issues; chairing skills are cultivated and are directly useful during incident-coordination work ([[incident-commander|incident command]], [[incident-handoff|handoffs]]).
- **Cost**: not everyone chairs equally well; some weeks are temporarily suboptimal.

The chapter explicitly argues the trade-off favours rotation — the value of group ownership outweighs weekly chair-skill variance.

### The video-conference asymmetric-teams trick

When two SRE teams meet by video and one is much larger than the other, **put the chair on the smaller side**. The larger side tends to dominate unintentionally (worsened by video latency) and side-conversations proliferate; a chair on the smaller side pulls the centre of attention toward equal participation (source: chapter-31-communication-and-collaboration-in-sre.md). The chapter acknowledges there's no known scientific basis for the technique — just empirical success.

## Default agenda

Not prescriptive, but the chapter's default (Appendix F example) looks like this (source: chapter-31-communication-and-collaboration-in-sre.md):

### Upcoming production changes

Track the useful properties of each change: start time, duration, expected effect. The chapter notes that change-tracking meetings often get misused industry-wide as venues for *stopping* change; Google's production environment defaults to **enabling** change, so the meeting tracks what's coming rather than gatekeeping it. This is near-term horizon visibility.

### Metrics

Service-oriented discussion anchored on the core metrics of the systems in question (see [[four-golden-signals]] and [[monitoring-and-observability]]). Even when no dramatic failure occurred that week, load typically grows gradually (or sharply) throughout the year, and tracking latency, CPU utilisation, and resource usage over time develops a feeling for the service's performance envelope. Some teams track resource usage and efficiency as a slower, more insidious system-change signal.

### Outages

Postmortem-sized problems — the indispensable learning opportunity. A good [[blameless-postmortem|postmortem analysis]] should "always set the juices flowing" (source: chapter-31-communication-and-collaboration-in-sre.md).

### Paging events

The tactical complement to Outages. Where Outages looks at the big picture, this item reviews the week's pages: who was paged, what happened, what the response was. Two implicit questions every paging event needs to answer:

1. **Should that alert have paged in the way it did?**
2. **Should it have paged at all?**

If the answer to (2) is no, **remove the unactionable page**. This is the weekly enforcement of the [[alert-philosophy|alert philosophy]] — the venue where pager noise is actually reduced.

### Nonpaging events

Three buckets (source: chapter-31-communication-and-collaboration-in-sre.md):

- **Should have paged but didn't** — fix the monitoring so the event would trigger a page. Usually surfaced while chasing something else, or associated with a tracked metric that lacks an alert.
- **Not pageable but requires attention** — low-impact data corruption, non-user-facing slowness, reactive operational work. Track these here.
- **Not pageable and does not require attention** — remove the alert entirely. It's noise.

### Prior action items

The preceding discussions generate actions: fix this, monitor that, develop a subsystem. Track them like any other meeting's action items — assigned to people, with progress tracked. **Consistent delivery on these action items is a wonderful credibility and trust builder**, and how that delivery is tracked matters less than the fact that it is tracked (source: chapter-31-communication-and-collaboration-in-sre.md).

## Attendance

Attendance is **compulsory for all members of the SRE team in question**, especially for teams spread across countries or time zones — the meeting is their major opportunity to interact as a group (source: chapter-31-communication-and-collaboration-in-sre.md).

**Major stakeholders should attend**, as should **partner product development teams**. Some teams split the meeting: SRE-only matters in the first half, joint in the second. That's acceptable as long as everyone leaves with the same idea of what's going on.

From time to time other SRE teams' representatives turn up, particularly for cross-team issues. In general, though, attendance is the SRE team in question plus major partner teams.

### If the product development team can't be invited

The chapter's blunt framing: **if your relationship is such that you cannot invite your product development partners, you need to fix that relationship** (source: chapter-31-communication-and-collaboration-in-sre.md). Steps:

1. Invite one representative.
2. Find a trusted intermediary to proxy communication.
3. Model healthy interactions externally and hope they propagate.

The rationale: the end goal is the **feedback loop from operations to engineering**. Without it, "a large part of the value of having an SRE team is lost."

### Handling too many attendees

Techniques when attendee count or busyness gets unmanageable:

- **Less active services**: one product-development representative per meeting, or commitment to read and comment on the agenda minutes.
- **Large product-development teams**: nominate a subset of representatives.
- **Busy-but-crucial attendees**: provide feedback and steering in advance using the **prefilled agenda technique** below.

## The Google Docs agenda

One of the chapter's distinctive spins on running the meeting: use **real-time collaborative document editing** (specifically Google Docs) for the agenda (source: chapter-31-communication-and-collaboration-in-sre.md). Many SRE teams maintain such a doc at a well-known address accessible to anyone in engineering. Two practices this enables:

- **Pre-populating the agenda with bottom-up ideas, comments, and information**. Anyone can add items before the meeting; the meeting time is then spent on discussion, not on collecting topics.
- **Preparing the agenda in parallel and in advance**. During the meeting itself, the chair types while someone else supplies source-material links in brackets, a third person cleans up spelling. The chapter's argument: this kind of simultaneous multi-hand collaboration makes more people feel they own a slice of the team's work — beyond just accelerating the meeting itself.

## Why this meeting works when most don't

The common antipattern is the meeting that runs because it's on the calendar. The production meeting avoids that trap because it has a **specific service-oriented purpose with a concrete output** (action items that address operational issues by changing the service), a **clear feedback loop** (next week's metrics reflect this week's actions), and a **weekly cadence tuned to content generation rate**.

It also inherits credibility from SRE's broader discipline: a team that has publicly committed to the [[toil-and-engineering-balance|50% engineering cap]] and is measured on [[service-level-objective|SLOs]] has structural reasons to convert meeting discussions into engineering work rather than just airing complaints.

## Related pages

- [[communication-and-collaboration-in-sre]]
- [[sre-team-composition]]
- [[four-golden-signals]]
- [[alert-philosophy]]
- [[blameless-postmortem]]
- [[sre-monitoring-outputs]]
- [[change-management-sre]]
- [[architectural-checklists]]
- [[architect-leadership-skills]]
