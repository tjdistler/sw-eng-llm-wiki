# Outage Analysis

**Summary**: Chapter 16's framing of the **analytic payoff** of an outage tracker — three stacked layers of analysis built on the data [[outalator]] captures, plus a reporting-and-communication layer that plugs the output of the analysis back into the weekly on-call rhythm. Chapter 16 is explicit: *enabling such analysis is one of the most important functions of an outage tracking tool*. Tracking outages without analysing them is box-checking; the value is in the second- and third-layer views that single incidents can't produce.

**Sources**: `raw/site-reliability-engineering/chapter-16-tracking-outages.md`

**Last updated**: 2026-04-17

---

## Why analysis is the point

Chapter 16 makes the argument explicit (source: chapter-16-tracking-outages.md):

> Of course, SRE does much more than just react to incidents. Historical data is useful when one is responding to an incident — the question "what did we do last time?" is always a good starting point. But historical information is far more useful when it concerns systemic, periodic, or other wider problems that may exist. Enabling such analysis is one of the most important functions of an outage tracking tool.

Two uses of the historical record, in ascending order of value:

1. **Tactical, during an incident.** "What did we do last time?" The log is a reference.
2. **Strategic, across incidents.** Systemic patterns, periodic problems, cross-team root causes. The log is a dataset.

The second is what justifies investing in the tool.

## Layer 1: counting and basic aggregates

The bottom layer is straightforward reporting:

- **Incidents per week / month / quarter.**
- **Alerts per incident.** (This is the ratio [[incident-aggregation|aggregation]] makes computable.)

Chapter 16 frames this as team-specific: "The details depend on the team, but include information such as incidents per week/month/quarter and alerts per incident." Different teams care about different cuts.

Even the simplest version of this analysis is unavailable without an outage tracker. Alerts-per-shift and actionable-ratio numbers live in nobody's head — they have to be counted.

## Layer 2: comparison

The next layer is **comparison over time and across teams** (source: chapter-16-tracking-outages.md):

> This layer allows teams to determine whether a given alert load is "normal" relative to their own track record and that of other services. "That's the third time this week" can be good or bad, but knowing whether "it" used to happen five times per day or five times per month allows interpretation.

The point Chapter 16 is making: **"third time this week" has no meaning without a baseline**. Comparison to your own history, and to peer teams, is what turns raw counts into a decision input.

This layer is where [[operational-overload]] becomes measurable. Chapter 11 defined the 25%-on-call cap and the two-incidents-per-shift guideline; Layer 2 analysis is the mechanism by which a team discovers they're over those caps.

## Layer 3: semantic cross-cutting analysis

The top layer requires more than counting (source: chapter-16-tracking-outages.md):

> The next step in data analysis is finding wider issues, which are not just raw counts but require some semantic analysis. For example, identifying the infrastructure component causing most incidents, and therefore the potential benefit from increasing the stability or performance of this component...

The worked example Chapter 16 gives: two teams have service-specific alerts — "stale data" on team A, "high latency" on team B. Both might trace to network congestion causing database replication delays. Neither team alone would see that pattern. Outage analysis across both tagged records can.

This is the layer where [[incident-tagging]] earns its keep. `cause:bigtable-replication-delay` applied consistently across teams is what enables this kind of cross-cutting query.

Chapter 16's footnote 2 adds an important caveat. "Most incidents caused" is a **starting point**, not a verdict:

- It might indicate over-sensitive monitoring (the infrastructure isn't the problem; the alerts are).
- It might be driven by a small set of misbehaving clients (the infrastructure is fine for everyone else).
- Incident count alone says nothing about **severity or difficulty to fix**.

The layer-3 output is hypotheses, not conclusions. Postmortems and targeted investigation remain the mechanism that turns a layer-3 pattern into a fix.

## The counterintuitive finding: over-performing infrastructure

Chapter 16 names a consequence of layer-3 analysis that most teams don't anticipate:

> Examining this information across multiple teams allows us to identify systemic problems and choose the correct solution, especially if the solution may be the introduction of more artificial failures to stop over-performing.

If an infrastructure component consistently over-performs its SLO, downstream teams come to depend on the higher level of service. When the infrastructure degrades to within its SLO, downstream teams page. The right fix may be to **deliberately introduce artificial failures** so downstream teams calibrate to the actual SLO rather than the over-performing reality. This is the [[slo-expectations|Chubby planned-outage technique]] generalised, and Chapter 16's outage analysis is the mechanism that tells you when to apply it.

## Reporting and communication

Layer 4 is plumbing the analysis back into day-to-day operations (source: chapter-16-tracking-outages.md):

- **Shift handoff.** Select zero or more outalations; include their subjects, tags, and "important" annotations in an email to the next on-call (and arbitrary cc list). The state of the production system transfers with the shift.
- **Weekly production review.** Most teams run one. Outalator supports **"report mode"**, in which important annotations expand inline with the main list — a quick-scan overview of the week's lowlights.

These aren't analysis in the layer-3 sense. They're the **operational surface** the analysis feeds. The weekly review is where layer-2 and layer-3 insights get raised with the team; shift handoff is where layer-0 (the raw record) gets passed forward.

## What outage analysis produces (in practice)

A rough taxonomy of decisions outage analysis supports:

- **Alert hygiene work** (layer 1–2). "We're getting 30 alerts per shift, 80% tagged `bogus`. Time for an alert-quality sprint." See [[alert-philosophy]].
- **Infrastructure investment priorities** (layer 3). "Four teams have `cause:replication-lag` in their top five tags. Replication is the right place to invest." See [[capacity-planning]] as a downstream consumer.
- **Over-performance recalibration.** See above — deliberate failures to match SLO expectations. See [[slo-expectations]].
- **Postmortem triggers.** Layer-1 counts can surface incidents that should have had postmortems but didn't. See [[postmortem-triggers]].
- **Organisational signals.** Layer-2 comparison across teams is an input to [[operational-overload]] assessment and the give-back-the-pager decision.

## Cross-book connections

- [[architecture-fitness-function]] (Richards & Ford) — layer 2 and 3 are fitness-function patterns at the reliability layer: objective, automatable integrity assessments of operational characteristics. "Incidents-per-quarter trend is flat or declining" is a fitness function; the outage-tracking tool is the measurement apparatus.
- [[unknown-unknowns]] (Richards & Ford) — layer 3 is the mechanism by which cross-cutting unknowns surface; no single incident would have exposed them.
- [[monitoring-and-observability]] (Newman) — outage analysis is what monitoring *data* turns into when aggregated with human annotation; the complement to Newman's observability-for-unknowns framing.

## Related pages

- [[outalator]]
- [[outage-tracking]]
- [[incident-tagging]]
- [[incident-aggregation]]
- [[alert-philosophy]]
- [[operational-overload]]
- [[slo-expectations]]
- [[postmortem-triggers]]
- [[learning-from-outages]]
- [[site-reliability-engineering]]
