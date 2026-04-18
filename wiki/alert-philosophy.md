# Alert Philosophy

**Summary**: Google SRE's philosophy on what should and should not trigger a page: alerts must be urgent, actionable, user-visible, and novel. A page that fails any of these criteria is noise — and noise erodes the team's ability to respond to real problems.

**Sources**: `raw/site-reliability-engineering/chapter-06-monitoring-distributed-systems.md`, `raw/site-reliability-engineering/chapter-10-practical-alerting-from-time-series-data.md`, `raw/site-reliability-engineering/chapter-11-being-on-call.md`

**Last updated**: 2026-04-17

---

## The fundamental philosophy

Chapter 6 states four principles about pages (source: chapter-06-monitoring-distributed-systems.md):

1. Every time the pager goes off, I should be able to react with a sense of urgency. **I can only react with a sense of urgency a few times a day before I become fatigued.**
2. **Every page should be actionable.**
3. **Every page response should require intelligence.** If a page merely merits a robotic response, it shouldn't be a page — it should be automation.
4. **Pages should be about a novel problem or an event that hasn't been seen before.**

Together these collapse a distinction the rest of the chapter cares about: once a page satisfies all four, *it doesn't matter whether white-box or black-box monitoring fired it* (see [[black-box-vs-white-box-monitoring]]).

## The five-question checklist for a new alert

Before adding a new alert rule, Chapter 6 recommends asking:

1. Does this rule detect an otherwise undetected condition that is **urgent**, **actionable**, and **actively or imminently user-visible**?
2. Will I ever be able to **ignore** this alert, knowing it's benign? When and why? How can I avoid that scenario?
3. Does this alert definitely indicate that users are being **negatively affected**? Are there cases (drained traffic, test deployments) where they aren't, that should be filtered out?
4. Can I take **action**? Is it urgent, or could it wait until morning? Could it be safely automated? Is it a real fix or a workaround?
5. Are **other people** getting paged for this same issue, making one of the pages unnecessary?

Zero-redundancy (N+0) counts as imminent. "Nearly full" counts as imminent.

## Why noise matters so much

The pager-fatigue argument is a core SRE tenet (source: chapter-06-monitoring-distributed-systems.md):

- A page at work interrupts workflow.
- A page at home interrupts personal time, perhaps sleep.
- Too many pages and employees second-guess, skim, or ignore incoming alerts.
- A real page then gets masked by the noise, prolonging outages.

The bar is high: *effective alerting systems have good signal and very low noise*.

## Page on symptoms, not causes

The flip side of the alert philosophy is where *not* to alert:

- **Do alert** on symptoms: the four golden signals (latency/traffic/errors/saturation), user-visible failures, imminent SLO exhaustion. See [[four-golden-signals]] and [[symptoms-vs-causes]].
- **Don't alert** on most causes. They belong on dashboards and in logs, surfaced by a human's post-hoc investigation of a symptom alert.
- **Only alert on causes** when they are *very definite* and *very imminent* — "the disk will be full in 4 hours" is a legitimate cause alert.

## Rote-response pages are a red flag

Chapter 6's Gmail case study drives this home: if an on-call engineer's response to a page is "run this exact command," the page isn't a page — it's a missed automation opportunity (source: chapter-06-monitoring-distributed-systems.md).

The section explicitly names the trap:

> Pages with rote, algorithmic responses should be a red flag. Unwillingness on the part of your team to automate such pages implies that the team lacks confidence that they can clean up their technical debt.

## The long-run trade-off

The Bigtable and Gmail case studies in Chapter 6 make the same structural point: a team drowning in pages can be forced to accept a short-term availability hit to buy time for real fixes. Both cases did exactly that:

- **Bigtable SRE** — dialled the SLO back from mean to 75th-percentile latency, disabled email alerts (too many to triage), and spent the reclaimed engineering time fixing root causes in Bigtable and the storage stack. Ultimately they returned to a better service than before.
- **Gmail SRE** — built a script to "poke" the rescheduler when Workqueue de-scheduled a task, debated automating the full loop, and eventually did. The team's anxiety about the "hack" getting left in place forever is a normal reaction; management has to actively support the long-term fix.

The general rule (source: chapter-06-monitoring-distributed-systems.md):

> It's important not to think of every page as an event in isolation, but to consider whether the overall level of paging leads toward a healthy, appropriately available system with a healthy, viable team and long-term outlook.

Google SRE reviews page-frequency statistics (incidents per shift, where an incident may span multiple pages) in quarterly reports with management.

## Flap prevention: the `for` clause

Chapter 10 adds a concrete mechanism that protects alert philosophy at the implementation level (source: chapter-10-practical-alerting-from-time-series-data.md). Experience shows that alerts can "flap" — toggle state rapidly when a metric oscillates around a threshold. Borgmon rules therefore require the alerting condition to hold for a **minimum duration** before the alert fires:

```
{var=dc:http_errors:ratio_rate10m,job=webserver} > 0.01
    for 2m
    => ErrorRatioTooHigh
```

The typical minimum is **at least two rule-evaluation cycles**, to ensure a single missed scrape doesn't fire a false alert. The `for` clause is the low-level realisation of the "every page should require intelligence" philosophy: we don't page on transient single-point conditions.

## Alertmanager: routing to the right bucket

Borgmon fires an `Alert` RPC to a central [[alertmanager]] service when a rule's condition holds for its minimum duration. Alertmanager is where page-worthy alerts diverge from ticket-worthy alerts diverge from dashboard-only informational data (source: chapter-10-practical-alerting-from-time-series-data.md):

> Teams send their page-worthy alerts to their on-call rotation and their important but subcritical alerts to their ticket queues. All other alerts should be retained as informational data for status dashboards.

This routing is driven by alert labels (e.g. `severity=page`). Alertmanager also **deduplicates** alerts fired by multiple Borgmon evaluating the same rule on the same data, **inhibits** lower-priority alerts when higher-priority causes are already firing, and **groups** related alerts by labelset — all three being noise-reduction mechanisms that serve the urgent/actionable/novel/intelligent philosophy at the infrastructure layer.

## Misconfigured monitoring as the top overload cause (Chapter 11)

Chapter 11 names **misconfigured monitoring** as the most common cause of SRE [[operational-overload]] (source: chapter-11-being-on-call.md). Three rules it pulls out:

- **Paging alerts must be aligned with symptoms that threaten the SLO** — the symptoms-not-causes rule, applied with SLO as the specific definition of "user-visible".
- **Every paging alert must be actionable** — a pageable alert the engineer can't act on is always an overload contributor.
- **Alert fan-out must be controlled** — a single abnormal condition should not generate many pages. Group related alerts at the monitoring/alerting layer; silence duplicate alerts during an active incident; tune noisy rules toward a 1:1 alert-to-incident ratio.

[[alertmanager]]'s grouping and inhibition features exist for exactly the fan-out problem.

## The email-alert sub-anti-pattern

Email alerts are specifically called out in the Chapter 6 conclusion as having very limited value: they become overrun with noise. The recommended substitute is a dashboard monitoring all ongoing subcritical problems, paired with a log for historical correlation. This is consistent with the Chapter 1 framing catalogued in [[sre-monitoring-outputs]]: there are only three valid monitoring outputs (alerts, tickets, logs), and the interpret-this-email pattern is none of them.

## Cross-book connections

- [[sre-monitoring-outputs]] — the three-valid-output taxonomy from Chapter 1; Chapter 6's alert philosophy is the sharper "what goes in the alert bucket" criterion.
- [[emergency-response]] — alerts are the input to emergency response; low-signal alerts destroy the practiced-engineer-with-playbook MTTR advantage.
- [[toil-and-engineering-balance]] — the "every page response should require intelligence" rule is the toil-cap discipline applied to on-call.
- [[change-management-sre]] — quickly and accurately detecting problems is one of the three change-management practices; alert philosophy defines "accurately".

## Related pages

- [[symptoms-vs-causes]]
- [[four-golden-signals]]
- [[black-box-vs-white-box-monitoring]]
- [[sre-monitoring-outputs]]
- [[emergency-response]]
- [[toil-and-engineering-balance]]
- [[blameless-postmortem]]
- [[monitoring-and-observability]]
- [[borgmon-rules]]
- [[alertmanager]]
- [[site-reliability-engineering]]
- [[operational-overload]]
- [[balanced-on-call]]
