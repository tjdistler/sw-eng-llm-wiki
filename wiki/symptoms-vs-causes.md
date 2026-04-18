# Symptoms vs Causes

**Summary**: A monitoring system should answer two questions — *what's broken* (symptom) and *why* (cause). The symptom-vs-cause distinction is the single most important lever for maximising signal and minimising noise in alerting.

**Sources**: `raw/site-reliability-engineering/chapter-06-monitoring-distributed-systems.md`, `raw/site-reliability-engineering/chapter-12-effective-troubleshooting.md`

**Last updated**: 2026-04-17

---

## The distinction

Chapter 6 frames it bluntly (source: chapter-06-monitoring-distributed-systems.md):

> "What" versus "why" is one of the most important distinctions in writing good monitoring with maximum signal and minimum noise.

- **Symptom** — what a user or operator is observing *right now*. "The website is returning 500s." "The home page is slow."
- **Cause** (or intermediate cause) — the underlying reason. "The database is full." "The backup job is saturating the network."

A given incident has many possible causes; symptoms are the few things that tell you whether the service is actually broken.

## Page on symptoms, use causes for debugging

The Chapter 6 philosophy is sharp:

- **Pages** should fire on symptoms: a user-visible problem is either happening or imminent.
- **Causes** should appear on dashboards and in logs to help you debug *after* the symptom page fires.

The reason is noise control. Causes are many and context-dependent; any given cause may or may not produce a user-visible symptom depending on what else is happening. If you page on every cause, you page too often. If you page only on symptoms, every page means something real.

## Multi-layered systems: one person's symptom is another's cause

A subtlety that matters in distributed systems: **layers reframe the same event differently** (source: chapter-06-monitoring-distributed-systems.md).

Suppose a database is slow:

- To the database SRE, "slow database reads" are a *symptom*. Their monitoring should page on this.
- To the frontend SRE, "slow database reads" are a *cause*. Their monitoring should page on "slow user requests" — and the slow database is a debugging datum the frontend team correlates against.

This is why [[black-box-vs-white-box-monitoring|white-box monitoring]] is "sometimes symptom-oriented, sometimes cause-oriented" — it depends on the vantage point.

## What counts as a good symptom signal

The [[four-golden-signals]] are canonical symptom signals for a user-facing service: latency, traffic, errors, saturation (with saturation being the partial exception — it also serves as an imminent-cause signal via predictions like "disk fills in 4 hours").

Good symptom signals share:

- Direct observability of what users experience
- Independence from implementation details
- Stability across refactoring

Cause signals (CPU utilisation, cache hit rates, thread pool depths) are the opposite: implementation-specific, sensitive to refactoring, plentiful.

## The "worry only about definite imminent causes" rule

Chapter 6's [[alert-philosophy]] section sharpens the cause side: *when it comes to causes, only worry about very definite, very imminent causes*. Page on the saturation prediction "disk fills in 4 hours" — don't page on "CPU is elevated and it might mean something bad later".

## The split in the Examine phase (Chapter 12)

Chapter 12's [[troubleshooting-model|troubleshooting model]] makes the symptom/cause distinction operational during incident response (source: chapter-12-effective-troubleshooting.md). The Examine phase uses both kinds of signal but for different purposes:

- **Symptom time-series** (latency, error rate, availability) answer the first question: *is something actually wrong, and how bad is it?* These drive the Triage decision.
- **Cause signals** (CPU, RPC rates, histogram views, `/varz` exports) are where the actual debugging happens once Triage has stabilised the situation.

Chapter 12's Logging subsection catalogues the cause-side infrastructure that pages like this one assume exists: structured logs with variable verbosity, sampling, selection languages, and exposed current-state endpoints. A shop that pages on symptoms but has no cause-side instrumentation can triage incidents but cannot diagnose them; the symptom/cause split requires both halves.

## Cross-book connections

- [[monitoring-and-observability]] (Newman) — Newman's monitoring-vs-observability split is about known vs unknown failure modes; the symptom-vs-cause split is about what to *alert* on inside the monitoring half. The two are orthogonal and complementary.
- [[sre-monitoring-outputs]] — the three-output taxonomy (alerts / tickets / logs) combined with symptoms-vs-causes gives you a full matrix: symptom alerts, cause tickets (often), cause logs (always).
- [[blameless-postmortem]] — postmortems are where causes are identified and fed back into monitoring as either new symptom alerts, new dashboards, or automation.

## Related pages

- [[four-golden-signals]]
- [[black-box-vs-white-box-monitoring]]
- [[alert-philosophy]]
- [[monitoring-and-observability]]
- [[sre-monitoring-outputs]]
- [[troubleshooting-model]]
- [[site-reliability-engineering]]
