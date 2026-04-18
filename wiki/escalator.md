# Escalator

**Summary**: Google's central replicated paging system — it receives alert notifications for all SRE on-call aliases, tracks whether a human has **acknowledged** the page, and escalates to the next configured destination (primary → secondary → …) if no ack arrives inside a configured interval. Escalator's original design choice (transparently copying emails sent to on-call aliases) let it integrate with pre-existing workflows without forcing any change in user or monitoring-system behaviour, which is why it spread.

**Sources**: `raw/site-reliability-engineering/chapter-16-tracking-outages.md`

**Last updated**: 2026-04-17

---

## What it does

Chapter 16's one-paragraph description (source: chapter-16-tracking-outages.md):

> At Google, all alert notifications for SRE share a central replicated system that tracks whether a human has acknowledged receipt of the notification. If no acknowledgment is received after a configured interval, the system escalates to the next configured destination(s) — e.g., from primary on-call to secondary.

Escalator is the **ack-tracking and auto-escalation** layer. Its job is to make sure a page that nobody grabs doesn't stay unacknowledged indefinitely.

## Why the "transparent email copy" design mattered

Escalator was initially designed as "a largely transparent tool that received copies of emails sent to on-call aliases." That wire-level choice was load-bearing (source: chapter-16-tracking-outages.md):

- **No change required to monitoring systems.** Any system that already emailed an on-call alias (which was most of them) immediately got escalation for free.
- **No change required to user behaviour.** On-call engineers kept reading the same alias; Escalator observed in the background.

This is a recurring SRE pattern: **the tool that wins is the one that plugs into existing workflow without forcing a migration**. See also the [[outalator|Outalator]] generalisation of the same move — Outalator explicitly cites Escalator as the example it followed.

## Relationship to Alertmanager

Escalator and [[alertmanager]] address adjacent concerns:

- **Alertmanager** — real-time routing, deduplication, inhibition, fan-in/fan-out. Decides *where* an alert should go based on its labels.
- **Escalator** — acknowledgment tracking across time. Decides *what happens next* if the human destination doesn't grab the alert in time.

A full production paging path is: [[borgmon]] fires → Alertmanager routes to the primary on-call's pager and to Escalator → if primary acks, Escalator stops; if not, Escalator re-routes to secondary, then to a manager, then further.

## Relationship to Outalator

[[outalator|Outalator]] is the next layer up. Escalator tracks **individual notifications** (did someone ack this page?); Outalator tracks **outages** — groups of notifications, with annotations, tags, and longitudinal analysis. Outalator consumes Escalator's stream and is what makes the record usable weeks or years after the fact.

Some teams set up **dummy Escalator configurations** where no human receives the notifications — the traffic just flows through Escalator into Outalator for archival, tagging, and audit. This is the "system of record" use case Chapter 16 describes for logging privileged role-account access and non-idempotent periodic jobs.

## Related pages

- [[outalator]]
- [[outage-tracking]]
- [[alertmanager]]
- [[sre-on-call-engagement]]
- [[sre-monitoring-outputs]]
- [[borgmon]]
- [[site-reliability-engineering]]
