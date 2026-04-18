# Outage Tracking

**Summary**: Chapter 16's hub discipline — the practice of **capturing every alert and outage into a queryable, annotatable record**, then using that record to drive systemic reliability improvement. Outage tracking is the aggregate complement to [[postmortem-philosophy|postmortems]]: postmortems go deep on individual significant incidents, outage tracking goes wide across everything. Together they produce the baseline-plus-progress loop Chapter 16 opens with: *"improving reliability over time is only possible if you start from a known baseline and can track progress."*

**Sources**: `raw/site-reliability-engineering/chapter-16-tracking-outages.md`

**Last updated**: 2026-04-17

---

## The baseline-and-progress thesis

Chapter 16 opens with a one-line argument that the rest of the chapter supports (source: chapter-16-tracking-outages.md):

> Improving reliability over time is only possible if you start from a known baseline and can track progress.

Two implications:

1. **Every alert matters, not just every outage.** The chapter explicitly calls out the questions outage tracking answers that postmortems can't: alerts per on-call shift, actionable/nonactionable ratios, "which service produces the most toil for this team." None are answerable from the postmortem corpus alone.
2. **Reliability is longitudinal.** You cannot tell whether a change helped without before-and-after data. A tool that stores the before-and-after is the precondition for evidence-based reliability work.

## The two-layer architecture at Google

Chapter 16 names Google's two tools:

- [[escalator|Escalator]] — the paging-layer tool. Receives all SRE notifications, tracks ack/no-ack, escalates to the next destination after timeout.
- [[outalator|Outalator]] — the outage-layer tool built on top. Stores the notifications, groups them into incidents, lets teams annotate and tag, and produces reports.

Escalator was "a largely transparent tool that received copies of emails sent to on-call aliases." Outalator followed the same design principle: **plug into the existing workflow, don't force a migration**. That's how both spread inside Google.

## What outage tracking adds over postmortems

| Postmortems | Outage tracking |
|---|---|
| One document per significant incident | One record per notification; groupable into incidents |
| Depth on root cause and action items | Breadth across all alerts a team sees |
| Triggered only above a significance bar | Passive; captures everything |
| Per-service | Cross-service aggregation possible |
| Answer: "what happened in this incident?" | Answer: "how is the alert load trending this quarter?" |
| Paired with [[blameless-postmortem]] culture | Paired with [[incident-tagging]], [[outage-analysis]] |

Chapter 16's own framing of the gap: postmortems "may miss opportunities that would have a small effect in individual cases, or opportunities that have a poor cost/benefit ratio, but that would have large horizontal impact."

## The analysis layers

See [[outage-analysis]] for the full development. Chapter 16 arranges tracking-enabled analysis in three layers:

1. **Counting and basic aggregates** — incidents per week/month/quarter, alerts per incident.
2. **Comparison** — team vs team, time vs time. "That's the third time this week" is interpretable only with a baseline.
3. **Semantic analysis** — identifying the infrastructure component causing the most incidents across teams, surfacing cross-service root causes that no single team's postmortem would have found.

The third layer is what justifies horizontal investment in shared infrastructure — Chapter 16's footnote 1 gives the Bigtable example: a mitigation that's barely worthwhile for one service can be clearly worthwhile when it fixes a class of events across dozens of services.

## The unexpected benefits

Chapter 16's closing section lists payoffs the designers didn't originally target:

- **Cross-team awareness during incidents.** You can see whether the team whose system you suspect is already paged. If they're not, you page them.
- **System-of-record uses.** Dummy Escalator configs feed Outalator with auditable events (privileged role-account use, non-idempotent periodic job runs) that nobody needs to act on in real time but that teams want a searchable history of.

## Relationship to the rest of SRE

Outage tracking sits at the intersection of several SRE practices:

- [[alert-philosophy]] — outage-tracking data is the input to alert-hygiene projects. The "how many alerts per shift?" and "actionable ratio?" questions from Chapter 16 are what [[operational-overload]] symptoms look like when measured.
- [[learning-from-outages]] — Chapter 13's "keep a history of outages" directive gets its Escalator/Outalator machinery in Chapter 16, just as Chapter 15 gave that directive its postmortem machinery.
- [[postmortem-culture-activities]] — the monthly review and [[postmortem-review-process|review-and-broadcast pipeline]] are postmortem-layer activities; Outalator's weekly "report mode" is the same rhythm at the aggregate layer.
- [[alertmanager]] — the real-time routing side of the same data Outalator archives.
- [[sre-monitoring-outputs]] — Outalator is where alerts/tickets/logs accumulate into longitudinal history.

## Cross-book connections

- [[log-aggregation]] (Newman) — the organisational analogue: a single queryable durable record of everything that happened, used for diagnosis well after the fact. Outalator is log-aggregation applied to alerts and incidents rather than to application logs.
- [[architecture-fitness-function]] (Richards & Ford) — the second and third analysis layers (comparison across teams; semantic cross-cutting analysis) are fitness functions applied to reliability: objective, automatable, integrity assessments of operational characteristics.
- [[architecture-decision-record]] (Richards & Ford) — the longitudinal outage record is input material to Consequences sections; decisions whose consequences produced recurring alerts want to be linked back to the tracked history.
- [[unknown-unknowns]] (Richards & Ford) — Chapter 16's semantic-analysis layer is the mechanism that surfaces cross-cutting unknowns no single incident exposes.

## Related pages

- [[outalator]]
- [[escalator]]
- [[incident-aggregation]]
- [[incident-tagging]]
- [[outage-analysis]]
- [[alertmanager]]
- [[sre-monitoring-outputs]]
- [[postmortem-philosophy]]
- [[learning-from-outages]]
- [[alert-philosophy]]
- [[operational-overload]]
- [[site-reliability-engineering]]
