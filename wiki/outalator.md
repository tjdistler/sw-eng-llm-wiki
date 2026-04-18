# Outalator

**Summary**: Google's internal **outage tracker** — a system that passively receives all alerts sent by monitoring, and lets SRE teams annotate, group, tag, and analyse the resulting record. Chapter 16 positions Outalator as the complement to the [[postmortem-philosophy|postmortem]]: postmortems capture individual high-impact incidents in depth, but only an outage tracker captures the **aggregate** — the small-but-frequent, the cross-team patterns, the alert load per shift, the signal/noise ratio. The two together are how SRE does "systematic learning from past problems."

**Sources**: `raw/site-reliability-engineering/chapter-16-tracking-outages.md`

**Last updated**: 2026-04-17

---

## Why Outalator exists

Improving reliability over time requires a **known baseline and tracked progress** (source: chapter-16-tracking-outages.md). Chapter 16's opening argument:

> Systematically learning from past problems is essential to effective service management. Postmortems (Chapter 15) provide detailed information for individual outages, but they are only part of the answer.

The gap postmortems leave:

- Postmortems are **only written for high-impact incidents**. Small-but-frequent issues (widespread low-impact alerts, chronic noisy monitors) fall outside their scope.
- Postmortems are per-service. They miss opportunities with **poor per-incident cost/benefit** but **large horizontal impact** — a mitigation that's barely worth doing once, but clearly worth doing if the same pattern appears across many events.
- Postmortems don't easily answer operational questions like: "How many alerts per on-call shift does this team get?", "What's the ratio of actionable/nonactionable alerts over the last quarter?", "Which of the services this team manages creates the most toil?"

Outalator answers all three. It's the aggregate-view tool that sits beside the incident-specific postmortem corpus.

## How it works

Outalator builds on [[escalator|Escalator]] (the centralised paging/ack tracker) by moving to **the next layer of abstraction: outages** (source: chapter-16-tracking-outages.md).

The core affordances:

- **Time-interleaved multi-queue view.** Users see notifications for multiple queues at once rather than switching between queues. A single SRE team is often the primary on-call for services whose developer teams are distinct secondary escalation targets; seeing them together matters.
- **Original notifications stored.** Outalator saves a copy of every inbound notification, and silently captures email replies as well so follow-up threads aren't fragmented.
- **Annotations.** Incidents can be annotated inline. Annotations can be marked **"important"**, in which case other parts of the message collapse to reduce clutter. This gives more context than a half-remembered email thread when you come back to the incident later.
- **Grouping** (see [[incident-aggregation]]) — multiple alerts combined into a single **incident** entity. This unclutters the overview and enables separate accounting of "incidents per day" versus "alerts per day."
- **Tagging** (see [[incident-tagging]]) — free-form words with colon-namespaced prefixes (`cause:network:switch`, `bug:76543`) add metadata that analysis and reports can key on.
- **Reporting and handoff** (see [[outage-analysis]]) — select outalations, include their subjects, tags, and important annotations in an email to the next on-call; "report mode" expands important annotations inline for periodic (weekly) service reviews.

## Outalator and the three monitoring outputs

Outalator is where [[sre-monitoring-outputs|alerts, tickets, and logs]] accumulate into an **institutional record**. [[alertmanager]] routes each alert to its destination in real time; Outalator is the write-side of that routing — the durable, annotatable history Alertmanager's deduped pages eventually pile into.

Chapter 16 makes this concrete: some teams set up **dummy Escalator configs** where no human receives notifications. The notifications still flow into Outalator, where they can be tagged, annotated, and reviewed. Examples:

- Logging and auditing privileged or role-account usage (a technical audit trail, not a legal one).
- Recording non-idempotent periodic jobs — e.g., automatic schema-change application from version control to databases — so each run has a record that can be annotated if it misbehaves.

This use of Outalator as a **system of record** extends its reach well beyond outages proper.

## The unexpected benefits

Chapter 16's closing section lists payoffs that weren't the original motivation:

- **Cross-team visibility.** If your service has a disruption that looks like a Bigtable incident, you can see whether the Bigtable SRE team has been paged. If they haven't, you page them manually. Chapter 16's one-line summary: *improved cross-team visibility can and does make a big difference in incident resolution, or at least in incident mitigation.*
- **Correlation across alerts.** Identifying that an alert flood coincides with a known other outage speeds diagnosis and reduces load on other teams (they now know it's the same underlying thing).
- **Dummy-escalator system-of-record use cases** as described above.

## Build-your-own note

Chapter 16 observes that many organisations use Slack, HipChat, or IRC for incident communication and status dashboards. These are **natural hook points** for an Outalator-like system — integrate the alert stream with the chat archive, and most of the raw material is already flowing through one channel.

## Relationship to postmortems

Outalator and [[postmortem-philosophy|postmortems]] are complementary:

- **Postmortems** = depth on the incidents that cleared the significance bar.
- **Outalator** = breadth across everything, including the sub-postmortem-threshold noise.

The two feed each other. Outalator reveals patterns (e.g., "this team gets 30 alerts a shift, 5 of which are actionable") that become postmortem action items or trigger an alert-hygiene project. Postmortems inform how Outalator tags are used (`cause:network` hierarchies stabilise once a few postmortems have classified their root causes).

See [[outage-tracking]] for the hub framing and [[outage-analysis]] for the detailed analytic layer.

## Related pages

- [[outage-tracking]]
- [[escalator]]
- [[incident-aggregation]]
- [[incident-tagging]]
- [[outage-analysis]]
- [[alertmanager]]
- [[sre-monitoring-outputs]]
- [[postmortem-philosophy]]
- [[learning-from-outages]]
- [[alert-philosophy]]
- [[site-reliability-engineering]]
