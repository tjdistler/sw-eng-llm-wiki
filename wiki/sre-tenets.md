# SRE Tenets

**Summary**: The eight core responsibilities every SRE team shares, and the principles governing how those responsibilities are carried out. Chapter 1 of the SRE book enumerates them; each later chapter develops one or more in depth.

**Sources**: `raw/site-reliability-engineering/chapter-01-introduction.md`, `raw/site-reliability-engineering/chapter-18-software-engineering-in-sre.md`, `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`, `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`, `raw/site-reliability-engineering/chapter-34-conclusion.md`

**Last updated**: 2026-04-17

---

## The eight areas of responsibility

> In general, an SRE team is responsible for the availability, latency, performance, efficiency, change management, monitoring, emergency response, and capacity planning of their service(s). (source: chapter-01-introduction.md)

The book codifies rules of engagement and working principles for how SRE teams interact with their environment — the production environment, product development teams, the testing teams, users. The goal of those rules is to keep SREs focused on *engineering* work rather than operations work.

Chapter 1 then expands the list into the concrete tenets catalogued below.

## The core tenets

### Durable focus on engineering

- [[toil-and-engineering-balance]] — the 50% cap on operations work; the safety valve that pushes overflow back to the product development team; the two-events-per-shift on-call target; blameless-postmortem practice as the feedback loop.

### Pursuing change velocity without violating the SLO

- [[error-budget]] — the mechanism that reframes reliability-vs-velocity as a shared budget.
- [[service-level-objective]] — the product-decision denominator from which the error budget is derived.

### Monitoring

- [[sre-monitoring-outputs]] — alerts, tickets, logs: the only three valid outputs of a monitoring system; email alerts as an anti-pattern.
- Cross-link: [[monitoring-and-observability]] for Newman's and Burns's complementary framings.

### Emergency response

- [[emergency-response]] — availability as a function of [[mttr-and-mttf|MTTR and MTTF]]; the ~3× MTTR improvement from practised on-call with a playbook.
- [[on-call-playbook]] — documented troubleshooting steps; Wheel of Misfortune drills.
- [[sre-on-call-engagement]] — Chapter 11's engagement model: paging response times, primary/secondary rotations.
- [[balanced-on-call]] — quantity (25% cap, 8-engineer single-site minimum) and quality (2 incidents per 12-hour shift).
- [[on-call-compensation]] — time-off or cash, capped at a salary fraction; the cap as a structural limit on overload.
- [[multi-site-on-call]] — follow-the-sun rotations; no night shifts; coordination overhead.
- [[incident-response-mindset]] — Kahneman intuitive vs rational; stress hormones; escalation, protocol, and blameless postmortems as supporting resources.
- [[operational-overload]] — measurable symptoms, monitoring-config fixes, alert fan-out control, giving back the pager.
- [[operational-underload]] — quiet systems as a treacherous enemy; team sizing, Wheel of Misfortune, DiRT.
- [[test-induced-emergency]] — Chapter 13 case study: proactive MySQL dependency test; untested rollback; incident-response process not yet disseminated.
- [[change-induced-emergency]] — Chapter 13 case study: Friday abuse-protection config push crash-loops external and internal services; rapid rollback by the push engineer.
- [[process-induced-emergency]] — Chapter 13 case study: Diskerase CDN wipe retold from the response side; traffic drain, automation freeze, three-day phased manual rebuild.
- [[learning-from-outages]] — Chapter 13 closing: keep a written history, ask big improbable questions, encourage proactive testing; follow-through on action items as the accountability rule.
- [[incident-management-framework]] — Chapter 14 hub: Google's adaptation of the Incident Command System; five elements that turn well-meaning engineers into a coordinated response.
- [[incident-command-system]] — Chapter 14: FEMA's ICS as the source; clarity and scalability as the borrowing rationale.
- [[recursive-separation-of-responsibilities]] — Chapter 14: the IC holds everything not delegated; vertical and horizontal recursion; clear boundaries increase autonomy.
- [[incident-commander]], [[incident-ops-lead]], [[incident-communications-lead]], [[incident-planning-lead]] — the four delegable roles.
- [[recognized-command-post]] — Chapter 14: known place (war room / IRC) for stakeholders; chat as durable log.
- [[live-incident-state-document]] — Chapter 14: the IC's most important responsibility; concurrently editable; independent of the system being fixed.
- [[incident-handoff]] — Chapter 14: explicit verbal handoff with firm acknowledgment; broadcast to the team.
- [[declaring-an-incident]] — Chapter 14: bias toward declaring early; the three-question test; use the framework on planned operations to stay fluent.
- [[unmanaged-incident-anti-patterns]] — Chapter 14: sharp focus, poor communication, freelancing — the three failure modes the framework defeats.

### Change management

- [[change-management-sre]] — 70% of outages come from change; progressive rollouts + fast detection + safe rollback as the automation trio.
- Cross-link: [[progressive-delivery]] for the same recipe from the Newman/Burns side.

### Demand forecasting and capacity planning

- [[capacity-planning]] — organic + inorganic demand forecasting; load-testing to correlate raw capacity to service capacity.
- [[intent-based-capacity-planning]] — Chapter 18's proposed approach: encode the service's intent and let a solver produce the allocation plan.

### Provisioning

- [[provisioning]] — the intersection of change management and capacity planning; performed quickly and only when necessary; riskier than load shifting.

### Efficiency and performance

- [[sre-efficiency]] — resource use as a function of demand, capacity, and software efficiency; why SRE's control of provisioning makes efficiency their lever.

### Software engineering within SRE

Not one of the Chapter 1 eight, but Chapter 18 adds it as a first-class organisational responsibility:

- [[software-engineering-in-sre]] — Chapter 18 hub: why SRE teams build full software-engineering projects; the Auxon case study; the lessons catalogue
- [[fostering-software-engineering-in-sre]] — project selection, staffing, defending project time
- [[sre-product-adoption]] — raising awareness, targeting early customers, setting expectations
- [[sre-software-development-lessons]] — approximation, launch-and-iterate, agnostic design, modularity
- [[introducing-sre-software-development]] — change-management guide for introducing the practice into an SRE org

### Engagement model — taking services on

Chapter 32 (Acacio Cruz and Ashish Bhambhani) adds another structural responsibility: *how* SRE takes on services and the production-concern set that every engagement is pointed at. The chapter's list of "aspects of a service collectively referred to as production" is the engagement-facing version of the tenets above (source: chapter-32-the-evolving-sre-engagement-model.md): system architecture and interservice dependencies; instrumentation, metrics, and monitoring; emergency response; capacity planning; change management; performance (availability, latency, efficiency).

- [[sre-engagement-model]] — the hub across the three engagement models
- [[simple-prr-model]] — the classical PRR-driven takeover of already-launched services
- [[production-readiness-review]] — the review artifact itself
- [[prr-engagement-phase]], [[prr-analysis-phase]], [[prr-improvements-and-refactoring]], [[prr-training-phase]], [[prr-onboarding-phase]], [[prr-continuous-improvement]] — the six phases
- [[early-engagement-model]] — SRE in the Design phase
- [[early-engagement-candidates]] — who qualifies
- [[disengaging-from-a-service]] — a positive outcome when appropriate
- [[frameworks-and-sre-platform]] — codified best practices in service frameworks
- [[service-framework]] — what a framework provides
- [[shared-responsibility-engagement]] — the staffing model frameworks unlock
- [[sre-alternative-support]] — documentation and consultation for services that don't get full engagement

### Training and onboarding

Chapter 28 (Andrew Widdowson) adds training as a structural responsibility, not a one-off process — "scale your humans faster than you scale your machines":

- [[sre-onboarding]] — the blueprint for bootstrapping a new SRE to on-call and beyond
- [[cumulative-learning-paths]] / [[on-call-learning-checklist]] — the curriculum backbone
- [[trial-by-fire-anti-pattern]] — the named anti-pattern to avoid
- [[reverse-engineering-skills]], [[statistical-comparative-thinking]], [[improvisational-troubleshooting]] — the three aspirational SRE attributes
- [[reverse-engineering-class]] — the worked training class that develops all three attributes
- [[teachable-postmortems]], [[disaster-role-playing]], [[breaking-real-systems]], [[documentation-as-apprenticeship]], [[shadow-on-call]] — the five practices for aspiring on-callers
- [[reverse-shadow-on-call]] — the optional final pre-on-call step
- [[sre-continuing-education]] — learning after going on-call

## Stability of the tenets, evolution of the activities (Chapter 34)

Benjamin Lutch's closing chapter names a pattern visible across SRE's first decade (source: chapter-34-conclusion.md):

> Our systems might be 1,000 times larger or faster, but ultimately, they still need to remain reliable, flexible, easy to manage in an emergency, well monitored, and capacity planned. At the same time, the typical activities undertaken by SRE evolve by necessity as Google's services and SRE's competencies mature. For example, what was once a goal to "build a dashboard for 20 machines" might now instead be "automate discovery, dashboard building, and alerting over a fleet of tens of thousands of machines."

Two claims about the list above:

1. **The tenets are the durable axioms.** The eight areas of responsibility Treynor Sloss enumerated in 2006 are still spot-on ten years later, despite the SRE organisation growing from a few hundred to over 1,000 engineers and the infrastructure scaling by orders of magnitude. The tenets pass the test for a good foundation: *general enough to be immediately useful, but that will remain relevant in the future.*
2. **The activities that realise them do not stay still.** The same tenet (monitoring) generates an entirely different engineering programme at 20 machines (dashboard) versus at tens of thousands (automate discovery, dashboard building, and alerting). This is why the tenets are framed as areas of responsibility rather than specific practices — the practices have to evolve with scale.

The practical consequence: when the tenets and the activities are confused, an SRE team either over-defends obsolete practices (defending the dashboard they built for 20 machines) or treats everything as negotiable (giving up capacity planning because the current method doesn't scale). The tenets are the invariant; the activities are the derivative.

## The shape of the list

Note that the tenets blend *what* the team is responsible for (monitoring, capacity, emergency response) with *how* they do it (engineering focus, error-budget discipline). That mixing is deliberate: the responsibilities are industry-standard operations concerns, but the handling of them — quantitative, automated, engineering-first — is what distinguishes the [[sre-discipline|SRE approach]] from the [[sysadmin-approach]].

## Related pages

- [[site-reliability-engineering]]
- [[sre-discipline]]
- [[error-budget]]
- [[toil-and-engineering-balance]]
- [[emergency-response]]
- [[change-management-sre]]
- [[capacity-planning]]
- [[provisioning]]
- [[sre-monitoring-outputs]]
- [[sre-efficiency]]
- [[sre-on-call-engagement]]
- [[balanced-on-call]]
- [[on-call-compensation]]
- [[multi-site-on-call]]
- [[incident-response-mindset]]
- [[operational-overload]]
- [[operational-underload]]
- [[test-induced-emergency]]
- [[change-induced-emergency]]
- [[process-induced-emergency]]
- [[learning-from-outages]]
- [[incident-management-framework]]
- [[incident-command-system]]
- [[recursive-separation-of-responsibilities]]
- [[incident-commander]]
- [[incident-ops-lead]]
- [[incident-communications-lead]]
- [[incident-planning-lead]]
- [[recognized-command-post]]
- [[live-incident-state-document]]
- [[incident-handoff]]
- [[declaring-an-incident]]
- [[unmanaged-incident-anti-patterns]]
- [[software-engineering-in-sre]]
- [[intent-based-capacity-planning]]
- [[traditional-capacity-planning]]
- [[fostering-software-engineering-in-sre]]
- [[sre-product-adoption]]
- [[sre-software-development-lessons]]
- [[introducing-sre-software-development]]
- [[sre-onboarding]]
- [[cumulative-learning-paths]]
- [[on-call-learning-checklist]]
- [[trial-by-fire-anti-pattern]]
- [[reverse-engineering-skills]]
- [[statistical-comparative-thinking]]
- [[improvisational-troubleshooting]]
- [[reverse-engineering-class]]
- [[teachable-postmortems]]
- [[disaster-role-playing]]
- [[breaking-real-systems]]
- [[documentation-as-apprenticeship]]
- [[shadow-on-call]]
- [[reverse-shadow-on-call]]
- [[sre-continuing-education]]
- [[sre-engagement-model]]
- [[simple-prr-model]]
- [[production-readiness-review]]
- [[early-engagement-model]]
- [[frameworks-and-sre-platform]]
- [[service-framework]]
- [[shared-responsibility-engagement]]
- [[sre-alternative-support]]
