# SRE Monitoring Outputs

**Summary**: Chapter 1 of the SRE book insists there are **only three valid outputs** of a monitoring system: alerts, tickets, and logs. The common industry practice of firing email alerts that a human must read and interpret is identified as an anti-pattern.

**Sources**: `raw/site-reliability-engineering/chapter-01-introduction.md`, `raw/site-reliability-engineering/chapter-06-monitoring-distributed-systems.md`, `raw/site-reliability-engineering/chapter-10-practical-alerting-from-time-series-data.md`, `raw/site-reliability-engineering/chapter-16-tracking-outages.md`

**Last updated**: 2026-04-17

---

## The principle

> Monitoring should never require a human to interpret any part of the alerting domain. Instead, software should do the interpreting, and humans should be notified only when they need to take action. (source: chapter-01-introduction.md)

The classic email-alert pattern — the system sends an email when a threshold is crossed, a human reads it, a human decides whether to act — is **fundamentally flawed**. Humans are bad at this loop: they tune out repeated signals, they miss alerts in their inbox, they apply inconsistent judgment across shifts. If a condition requires human judgment to decide whether action is needed, that judgment belongs in the monitoring system, not in the email reader.

## The three valid outputs

Once that principle is adopted, there are only three things monitoring can usefully produce (source: chapter-01-introduction.md):

### Alerts

> Signify that a human needs to take action immediately in response to something that is either happening or about to happen, in order to improve the situation.

Alerts page someone. They are reserved for situations where *not* responding quickly causes harm.

### Tickets

> Signify that a human needs to take action, but not immediately. The system cannot automatically handle the situation, but if a human takes action in a few days, no damage will result.

Tickets are the asynchronous cousin of alerts. They capture work that needs to be done but that doesn't require waking anyone up.

### Logging

> No one needs to look at this information, but it is recorded for diagnostic or forensic purposes. The expectation is that no one reads logs unless something else prompts them to do so.

Logs are write-only under normal operation. They exist for the postmortem, the security investigation, the debugging session — not for routine awareness.

## Why email alerts are the anti-pattern

An email alert that requires interpretation fails every test of the taxonomy:

- It's not an **alert**: immediate action isn't clearly required.
- It's not a **ticket**: it's not tracked, not assigned, not prioritised.
- It's not a **log**: it's being actively directed at someone's attention.

It's a fourth category the taxonomy deliberately excludes: *stuff that pesters a human into doing the monitoring system's job*.

## Chapter 6 reinforcement: dashboards replace email alerts

Chapter 6's conclusion sharpens the email-alert case (source: chapter-06-monitoring-distributed-systems.md):

> Email alerts are of very limited value and tend to easily become overrun with noise; instead, you should favor a dashboard that monitors all ongoing subcritical problems for the sort of information that typically ends up in email alerts. A dashboard might also be paired with a log, in order to analyze historical correlations.

This is a concrete replacement for the email-alert anti-pattern: the *dashboard plus log* pair. The dashboard is always-on situational awareness for a human who chooses to look; the log is the queryable record for post-hoc correlation. Neither demands a human's attention in the way an email does.

Chapter 6 also gives fuller framing for what *does* belong in the alert bucket (versus the ticket or log buckets). That philosophy is [[alert-philosophy]]: urgent, actionable, user-visible, novel, and requiring intelligence. Pages that fail any of those tests are the same noise this page warns against — now characterised from the input side.

## The mechanism: Alertmanager

Chapter 10 shows the concrete routing mechanism that implements the three-output split (source: chapter-10-practical-alerting-from-time-series-data.md). When a rule in the time-series monitoring system fires, it sends an `Alert` RPC to a central [[alertmanager]] service. Alertmanager is configured to route by label:

> Teams send their page-worthy alerts to their on-call rotation and their important but subcritical alerts to their ticket queues. All other alerts should be retained as informational data for status dashboards.

So the three-output taxonomy is not just a conceptual split — it is the actual routing schema baked into the production monitoring infrastructure. The alert's `severity` label determines which bucket it lands in, and Alertmanager additionally deduplicates, groups, and inhibits alerts to keep each bucket clean.

## The archival side

Chapter 16 adds the long-term counterpart to Alertmanager's real-time routing (source: chapter-16-tracking-outages.md). An ack-tracking service follows each alert and escalates on timeout; an outage-level archive ingests the full notification stream and lets SRE teams **annotate, group, tag, and analyse** it over weeks and quarters.

The stack for a given page-worthy event:

1. A rule in the time-series monitoring system fires → Alert RPC.
2. [[alertmanager]] routes the alert by label to pager + ticket queue / dashboard / archive destinations.
3. The ack tracker waits for ack and escalates if none arrives.
4. The archive stores the notification, allowing [[incident-aggregation|post-hoc grouping]] into incidents, [[incident-tagging|tagging]], and [[outage-analysis|longitudinal analysis]].

The three-output taxonomy and Alertmanager's routing handle the *notification moment*. The archive handles the *institutional memory* — what the team looks at weeks later to answer "how noisy has our alert load been?" or "what's causing the most incidents this quarter?" The two are complementary: real-time clarity and archival clarity need different machinery.

## Connection to other tenets

- [[blameless-postmortem]] — every significant incident produces a postmortem, whether it paged or not. **Non-paging incidents are even more valuable**, because they indicate monitoring gaps. The postmortem is the feedback loop that turns those gaps into better alerts, better tickets, or better automation.
- [[emergency-response]] — alerts that fire are the input to emergency response. If the alerts don't fire quickly and specifically, MTTR suffers.
- [[change-management-sre]] — the "quickly and accurately detecting problems" piece of the change-management trio depends on the monitoring system. Email alerts cannot detect anything quickly or accurately enough for automated rollback.

## Cross-book connection

This taxonomy is compatible with and sharper than the framings elsewhere in the wiki:

- Newman's [[monitoring-and-observability]] covers monitoring-vs-observability (known-vs-unknown failure modes). SRE's three-output taxonomy fits inside the *monitoring* half of Newman's distinction.
- Burns's [[adapter-pattern]] ([[unified-monitoring-interface]], [[log-normalization]], [[health-check-adapter]]) is the container-level mechanism that delivers the data feeding those alerts, tickets, and logs.

## Related pages

- [[sre-tenets]]
- [[alert-philosophy]]
- [[four-golden-signals]]
- [[symptoms-vs-causes]]
- [[black-box-vs-white-box-monitoring]]
- [[monitoring-simplicity]]
- [[monitoring-and-observability]]
- [[blameless-postmortem]]
- [[emergency-response]]
- [[change-management-sre]]
- [[alertmanager]]
- [[outage-tracking]]
