# PRR Continuous Improvement

**Summary**: The steady-state phase after [[prr-onboarding-phase|Onboarding]] completes. The SRE team sustains reliability as the service evolves in response to new features, dependencies, and upgrades, and contributes lessons back to the [[production-guide|Production Guide]] so the broader organisation benefits.

**Sources**: `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## Why this is a named phase

A service doesn't stand still after SRE takes over. Active services continuously change in response to new demands and conditions — user requests for new features, evolving system dependencies, technology upgrades, and more (source: chapter-32-the-evolving-sre-engagement-model.md). The SRE team has to maintain reliability standards in the face of all of that, which is an ongoing discipline, not a one-time event.

Chapter 32 names this the "Continuous Improvement" phase to signal that the PRR process does not end at onboarding. The team has production responsibility now, but its review-style engagement with changes continues.

## How the SRE team drives improvement

Two directions of learning feed the discipline (source: chapter-32-the-evolving-sre-engagement-model.md):

- **Inward.** The team learns more about the service by operating it, reviewing new changes, responding to incidents, and conducting [[blameless-postmortem|postmortems]] and [[learning-from-outages|root-cause analyses]]
- **Outward.** That expertise is shared back with the development team as suggestions and proposals for changes to the service whenever new features, components, or dependencies are added

The outward flow is the mechanism by which SRE influence outlasts the PRR itself — every feature addition is implicitly a mini-PRR, reviewed against what the team has learned since onboarding.

## Feeding the Production Guide

Lessons from managing the service are also contributed to best practices and documented in the Production Guide (source: chapter-32-the-evolving-sre-engagement-model.md). This is how a single service's hard-won knowledge becomes available to every other team running a PRR: the checklist a future Analysis phase uses gets better because past Continuous Improvement phases fed it.

## Relationship to other SRE disciplines

Continuous Improvement is the umbrella phase where the other ongoing SRE disciplines land:

- [[production-meetings|Weekly production meetings]] — the recurring forum for surfacing changes, outages, and follow-ups
- [[sre-dev-collaboration|SRE-dev collaboration]] — the long-term partnership seeded during Onboarding
- [[blameless-postmortem|Postmortems]] and [[postmortem-review-process|review]] — the structured learning pipeline
- [[outage-tracking|Outage tracking]] — the longitudinal record that makes trend analysis possible

In that sense, Continuous Improvement is less a "phase" than the normal operating mode of an SRE team with a service it owns.

## Related pages

- [[simple-prr-model]]
- [[production-readiness-review]]
- [[prr-onboarding-phase]]
- [[production-guide]]
- [[production-meetings]]
- [[sre-dev-collaboration]]
- [[blameless-postmortem]]
- [[learning-from-outages]]
- [[outage-tracking]]
- [[site-reliability-engineering]]
