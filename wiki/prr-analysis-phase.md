# PRR Analysis Phase

**Summary**: The first large work phase of the [[simple-prr-model|Simple PRR Model]]. SRE reviewers learn the service, gauge its maturity along SRE's axes of concern, and run it against a PRR checklist drawn from domain expertise, experience with related systems, and a shared production-best-practices repository. Output: a list of recommended improvements prioritised for reliability impact.

**Sources**: `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## What reviewers do

During Analysis, PRR reviewers (source: chapter-32-the-evolving-sre-engagement-model.md):

- Learn the service in detail
- Gauge the maturity of the service along [[sre-engagement-model|SRE's axes]]: architecture/dependencies, instrumentation/metrics/monitoring, emergency response, capacity planning, change management, performance
- Examine design and implementation against production best practices
- Consult other teams with experience on specific components or dependencies
- Review recent incidents and postmortems, plus their follow-up tasks, to assess emergency-response demands and operational-control maturity

## The PRR checklist

Each SRE team maintains a PRR checklist specific to its service portfolio, based on domain expertise, experience with related systems, and the Production Guide (source: chapter-32-the-evolving-sre-engagement-model.md). Representative checklist items from Chapter 32:

- **Update blast radius.** Do updates to the service impact an unreasonably large percentage of the system at once?
- **Dependency suitability.** Does the service connect to the appropriate serving instance of its dependencies? (End-user requests must not depend on systems designed for batch-processing.)
- **Network QoS.** Does the service request a sufficiently high network quality-of-service when talking to a critical remote service?
- **Error reporting.** Does the service report errors to central logging systems for analysis? Does it report all exceptional conditions that result in degraded responses or failures?
- **User-visible failures.** Are all user-visible request failures well instrumented and monitored, with suitable alerting configured?

## Team-specific gold standards

The checklist also captures operational standards a particular SRE team follows. A perfectly functional service configuration that doesn't match an SRE team's "gold standard" may still be refactored to work better with the team's scalable configuration tools (source: chapter-32-the-evolving-sre-engagement-model.md). The rationale is ongoing operational cost: mismatch with the team's automation has a toil price that compounds.

## Historical incident review

Reviewing recent incidents and postmortems gives the PRR team two things (source: chapter-32-the-evolving-sre-engagement-model.md):

- An empirical picture of the operational demands the pager rotation would inherit
- Evidence of whether operational controls and response procedures are well-established

This is where existing [[blameless-postmortem|postmortems]], [[outage-tracking|outage records]], and [[learning-from-outages|outage histories]] pay off: the PRR reviewer reads them as the service's operational fitness report.

## Output

The Analysis phase produces a ranked list of recommended improvements. That list feeds the [[prr-improvements-and-refactoring|Improvements and Refactoring phase]] where priorities are negotiated with the development team and executed jointly.

## Related pages

- [[simple-prr-model]]
- [[production-readiness-review]]
- [[prr-engagement-phase]]
- [[prr-improvements-and-refactoring]]
- [[sre-engagement-model]]
- [[blameless-postmortem]]
- [[site-reliability-engineering]]
