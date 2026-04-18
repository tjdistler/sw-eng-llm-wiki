# SRE On-Call Engagement Model

**Summary**: The operational framing of on-call inside Google SRE — what an on-call engineer is responsible for, the paging response times the business agrees to, and how primary and secondary rotations divide the work. Chapter 11 spells out the role; the balance, compensation, and stress pieces build on top of it.

**Sources**: `raw/site-reliability-engineering/chapter-11-being-on-call.md`

**Last updated**: 2026-04-17

---

## What an on-call engineer does

On-call engineers are **guardians of production systems** (source: chapter-11-being-on-call.md). They:

- Manage outages affecting the team's services.
- Perform or vet production changes.
- Acknowledge pages and triage the problem, working toward resolution and escalating as needed.
- Handle or vet non-paging production events (lower-priority alerts, software releases) during business hours.

Paging events take priority over almost every other task, including project work. Non-paging activities are less urgent but still flow through on-call.

## Paging response times

The response SLA is an organisational commitment, not a personal preference. Chapter 11 gives two typical values (source: chapter-11-being-on-call.md):

- **5 minutes** for user-facing or otherwise time-critical services.
- **30 minutes** for less time-sensitive systems.

The arithmetic is tight: a user-facing system targeting 99.99% availability has only ~13 minutes of quarterly downtime (see [[availability-measurement]] and Appendix A), so the on-call response time has to be in that ballpark — strictly speaking, under 13 minutes.

Google provides the page-receiving device (typically a phone) and operates a flexible alert-delivery system capable of dispatching pages via email, SMS, robot call, or an app, across multiple devices (source: chapter-11-being-on-call.md).

## Primary and secondary rotations

Many teams run both a primary and a secondary on-call rotation. Chapter 11 catalogues three common divisions of labour (source: chapter-11-being-on-call.md):

1. **Secondary as fall-through** — the secondary catches pages the primary misses.
2. **Primary handles pages, secondary handles non-urgent production activities** — pure role split.
3. **Two related teams as each other's secondaries** — cross-team fall-through, eliminating the need for a dedicated in-team secondary rotation.

Option 3 is common where a single-team secondary can't be justified by workload alone but some redundancy is still needed. For detailed analysis of on-call organisation, Chapter 11 points at the "Oncall" chapter of [Lim14].

## Connection to the engineering balance

The on-call role is where the [[toil-and-engineering-balance|50% cap]] meets the pager. The at-most-two-events-per-shift target from Chapter 1 is the *quality* side; Chapter 11 adds the *quantity* side (the 25%-on-call rule) and the staffing arithmetic that falls out of it — see [[balanced-on-call]].

## Related pages

- [[balanced-on-call]]
- [[on-call-compensation]]
- [[multi-site-on-call]]
- [[emergency-response]]
- [[on-call-playbook]]
- [[toil-and-engineering-balance]]
- [[availability-measurement]]
- [[sre-tenets]]
