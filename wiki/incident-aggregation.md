# Incident Aggregation

**Summary**: Chapter 16's framing of the **group-multiple-alerts-into-one-incident** affordance in an outage-tracking archive. A single underlying event routinely produces many alerts — different error symptoms, different affected teams, different backend reports — and grouping them into one logical incident is what makes the resulting record usable for counting, comparison, and trend analysis. Without grouping, "incidents per day" and "alerts per day" blur into one number that measures neither.

**Sources**: `raw/site-reliability-engineering/chapter-16-tracking-outages.md`

**Last updated**: 2026-04-17

---

## The duplication problem

Chapter 16 names the reality every on-call engineer knows (source: chapter-16-tracking-outages.md):

> A single event may, and often will, trigger multiple alerts. For example, network failures cause timeouts and unreachable backend services for everyone, so all affected teams receive their own alerts, including the owners of backend services; meanwhile, the network operations center will have its own klaxons ringing. However, even smaller issues affecting a single service may trigger multiple alerts due to multiple error conditions being diagnosed.

Two sources of alert multiplication:

- **Horizontal fan-out.** One event → many teams with their own symptoms. A backbone network outage wakes up the network team, every service using the affected path, every team whose SLO it breaks.
- **Vertical fan-out.** One event → multiple symptom-specific alerts within a single service. Different error conditions are diagnosed separately, each firing its own alert.

While you should minimise alerts per event where feasible, "triggering multiple alerts is unavoidable in most trade-off calculations between false positives and false negatives." The economics of alert hygiene puts some duplication at the floor.

## Why grouping matters in the record

Alertmanager handles real-time **suppression** via inhibition and deduplication (see [[alertmanager]]). Aggregation in Outalator is the **archival** equivalent: after the fact, a human groups the related notifications into a single entity.

Chapter 16's argument for why this matters (source: chapter-16-tracking-outages.md):

> Sending an email saying "this is the same thing as that other thing; they are symptoms of the same incident" works for a given alert: it can prevent duplication of debugging or panic. But sending an email for each alert is not a practical or scalable solution for handling duplicate alerts within a team, let alone between teams or over longer periods of time.

The scaling argument is the one to notice. A one-off "same thing" email works within an incident. It doesn't work *across* incidents, *across* teams, or *across* weeks. Grouping inside Outalator persists the association.

## What grouping enables

With alerts grouped into incidents, the record supports two distinct counts:

- **Incidents per day** — how many distinct problems occurred.
- **Alerts per day** — how much notification traffic the team absorbed.

These are very different numbers. A week with 7 incidents and 400 alerts is a week where **each event fanned out 50x** — probably an alerting-hygiene problem. A week with 30 incidents and 35 alerts is a week with high event frequency but clean per-event signals. You can't distinguish these cases from a raw alert count alone.

See [[outage-analysis]] for how the two counts feed higher-layer analysis.

## Not every alert is an incident

Grouping also lets the record **omit**. Chapter 16 observes that notifications flowing through Outalator include:

- Real alerts tied to real incidents.
- Unrelated auditable events (privileged database access logged through a dummy Escalator config).
- Spurious monitoring failures.
- Test alerts, mistargeted emails from humans.

The grouping affordance combined with [[incident-tagging]] (especially the widely-used `bogus` tag for false positives) is what separates signal from noise in the archive. Without these, the record would conflate all four categories.

## Relationship to Alertmanager

[[alertmanager]]'s inhibition, deduplication, and grouping-by-labelset are the **real-time** counterparts. They prevent noisy paging at the moment alerts fire. Outalator's aggregation is the **post-hoc** counterpart — when multiple alerts did fire, a human ties them together in the record so the historical view is clean.

The two work together: Alertmanager keeps the page-to-human ratio manageable during an incident; incident aggregation keeps the historical record interpretable weeks later.

## Related pages

- [[outage-tracking]]
- [[incident-tagging]]
- [[outage-analysis]]
- [[alertmanager]]
- [[alert-philosophy]]
- [[operational-overload]]
- [[site-reliability-engineering]]
