# Emergency Response

**Summary**: One of the eight SRE tenets. The discipline of responding to production incidents — measured by MTTR — with a bias toward automation and, when humans are required, toward practised on-call engineers armed with playbooks.

**Sources**: `raw/site-reliability-engineering/chapter-01-introduction.md`, `raw/site-reliability-engineering/chapter-11-being-on-call.md`, `raw/site-reliability-engineering/chapter-12-effective-troubleshooting.md`, `raw/site-reliability-engineering/chapter-13-emergency-response.md`, `raw/site-reliability-engineering/chapter-14-managing-incidents.md`, `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`

**Last updated**: 2026-04-17

---

## The central metric: MTTR

The most relevant metric in evaluating the effectiveness of emergency response is **how quickly the response team can bring the system back to health** — that is, MTTR (source: chapter-01-introduction.md). See [[mttr-and-mttf]] for the MTTF/MTTR decomposition and why lowering MTTR is often a better investment than lowering failure frequency.

## Humans add latency

The Chapter 1 conclusion: *humans add latency*. A system that can avoid emergencies requiring human intervention will have higher availability than one of equal fault rate that requires hands-on intervention (source: chapter-01-introduction.md). Automated recovery — restart loops, failover, circuit breakers, health-check-driven removal from load balancers — is how MTTR gets pushed toward its floor.

## When humans are necessary: playbooks

When humans are required, two practices make the response dramatically more effective:

- **[[on-call-playbook|Playbooks]]**: documented troubleshooting steps, written ahead of time. Produces *roughly a 3× improvement in MTTR* versus winging it (source: chapter-01-introduction.md).
- **Wheel of Misfortune drills**: scenario-based on-call exercises. Chapter 1 references this; the book covers it in depth in "Disaster Role Playing".

Neither substitutes for a smart engineer thinking on the fly, but both sharpen that engineer's response during high-stakes or time-sensitive pages.

## The on-call shift target

Emergency response connects directly to the [[toil-and-engineering-balance|engineering-focus cap]]: when SREs are focused on ops work, the target is *at most two events per 8–12-hour on-call shift* (source: chapter-01-introduction.md). Two events gives enough time to:

1. Handle each event accurately and quickly.
2. Clean up and restore normal service.
3. **Conduct a [[blameless-postmortem|postmortem]].**

Push the rate above that and the postmortem is the first casualty — which is exactly the wrong thing to lose.

## Postmortems

Every significant incident produces a postmortem, whether it paged or not. See [[blameless-postmortem]] for the culture and [[sre-tenets]] for where emergency response sits among the other responsibilities.

## Staying rational under pressure (Chapter 11)

Chapter 11 adds the human-factors half of emergency response: incident handling is a cognitive task that *degrades under stress* (source: chapter-11-being-on-call.md). Cortisol and CRH impair decision-making and push engineers from deliberate analysis toward habitual heuristics — including confirmation bias against past pages. The three supporting resources SRE relies on to keep engineers in the rational mode:

- **Clear escalation paths** — developer teams on 24/7 rotation so serious outages with unknown dimensions can be escalated rather than absorbed.
- **A well-defined incident-management protocol** (Chapter 14) — plus tooling that automates role handoffs and status updates, freeing cognitive budget for the incident itself.
- **A [[blameless-postmortem|blameless postmortem]] culture** — so fear of post-incident judgment doesn't degrade in-the-moment decision making.

Full treatment on [[incident-response-mindset]].

## Balanced on-call (Chapter 11)

Emergency response only works if on-call load stays in the sustainable zone. Chapter 11 formalises Chapter 1's two-events-per-shift target on two axes (source: chapter-11-being-on-call.md):

- **Quantity** ≤ 25% of SRE time; 8-engineer minimum for a single-site rotation; dual-site preferred once the service justifies growth (avoids night shifts, keeps engineers in touch with production).
- **Quality** ≤ 2 incidents per 12-hour shift. Chapter 11 derives the 2 from the 6-hour-per-incident average (root-cause + remediation + postmortem + bug fixes).

See [[balanced-on-call]], [[sre-on-call-engagement]], [[multi-site-on-call]], and the failure modes: [[operational-overload]] and [[operational-underload]].

## Stop the bleeding first (Chapter 12)

Chapter 12 adds the emergency-response-side priority ordering that new SREs frequently get wrong (source: chapter-12-effective-troubleshooting.md): in a major outage, the first instinct to start root-causing is the wrong one.

> Your course of action should be to make the system work as well as it can under the circumstances. This may entail emergency options, such as diverting traffic from a broken cluster to others that are still working, dropping traffic wholesale to prevent a cascading failure, or disabling subsystems to lighten the load.

Chapter 12's pilot analogy is the one-line version: *novice pilots are taught that their first responsibility in an emergency is to fly the airplane*. Troubleshoot second. See [[triage-sre]] for the full argument, emergency options, and the evidence-preservation caveat.

Chapter 12's full troubleshooting workflow — which begins with triage and ends with a postmortem — is catalogued at [[troubleshooting-model]].

## What to do when systems break (Chapter 13)

Chapter 13 opens with a practitioner's checklist for the first minute of an incident (source: chapter-13-emergency-response.md):

> First of all, don't panic! You aren't alone, and the sky isn't falling. You're a professional and trained to handle this sort of situation.

The chapter's three concrete directives:

- **Don't panic.** Typically no one is in physical danger; at the very worst, half of the Internet is down. Take a breath, then carry on.
- **Pull in more people if you feel overwhelmed.** Sometimes paging the entire company is the right move. Heroism-by-silent-suffering is a failure mode.
- **Follow your incident-response process.** If one exists, use it; if you don't know it, that's the first gap to close.

Chapter 13's broader observation — *all problems have solutions* — is the directive to **cast your net farther** when stuck, including involving the person who triggered the event. They usually have the most context.

## The three Chapter 13 case studies

Chapter 13 teaches emergency response through three detailed postmortems, each catalogued as its own page:

- [[test-induced-emergency]] — a proactive MySQL dependency test whose blast radius was wildly larger than predicted; rollback procedures themselves were untested; a year-one example that exposed an unfamiliar incident-response process.
- [[change-induced-emergency]] — a Friday config push to abuse-protection infrastructure that crash-looped essentially all external Google services, including internal tooling; saved by real-time-chat-watching push engineer, out-of-band communication, and CLI fallback tools.
- [[process-induced-emergency]] — the Diskerase CDN wipe, viewed from the response side (see [[automation-gone-wrong]] for the structural read); the arc is traffic drain → automation freeze → three-day phased manual rebuild.

Chapter 13's closing comparison: the configuration-push response (year one) was competent but not yet mature; the Diskerase response (year two) was visibly sharper. **Disciplined incident-response, repeated, compounds.**

## Learn from the past

Chapter 13's final section formalises the learning half of the loop under [[learning-from-outages]] (source: chapter-13-emergency-response.md):

- **Keep a written history of outages.** Publish postmortems, organise them, *hold yourself and others accountable to the follow-up actions*.
- **Ask the big, improbable questions.** What if the datacenter goes dark? What if someone compromises the web server? Could the person next to you respond, or only you?
- **Encourage proactive testing.** Until the system has actually failed, you don't know how it behaves. A planned 2pm drill is cheaper than an unplanned 2am outage.

This is the [[blameless-postmortem|postmortem]] discipline generalised: not just write it up, but re-read, test against, and update the system based on it.

## The incident management framework (Chapter 14)

Chapter 14 supplies the structural complement to Chapter 11's human-factors framing: a defined process (roles, command post, living document, handoff protocol) that turns the same engineers from independent responders into a coordinated team (source: chapter-14-managing-incidents.md). Spinning the framework up early — see [[declaring-an-incident]] — is the explicit recommendation, since the cost of unnecessary structure is small and the cost of late structure is large.

Catalogued at [[incident-management-framework]]; the constituent pages:

- [[unmanaged-incident-anti-patterns]] — the three failure modes (sharp focus, poor communication, freelancing) the framework is designed to defeat
- [[incident-command-system]] — the FEMA-derived antecedent; clarity and scalability as the borrowing rationale
- [[recursive-separation-of-responsibilities]] — the organising principle; the IC holds everything not delegated
- [[incident-commander]], [[incident-ops-lead]], [[incident-communications-lead]], [[incident-planning-lead]] — the four delegable roles
- [[recognized-command-post]] — IRC / war room as the known place; logged communications double as postmortem material
- [[live-incident-state-document]] — the IC's most important responsibility; concurrently editable; independent of the system being fixed
- [[incident-handoff]] — explicit verbal "you're now the incident commander, okay?" plus broadcast to the team
- [[declaring-an-incident]] — the three-question test; bias toward declaring early; use the framework on planned operations to stay fluent

## Cascading failures (Chapter 22)

Chapter 22 names cascading failure as "a good opportunity to use your incident management protocol" (source: chapter-22-addressing-cascading-failures.md). The combination of rapid escalation, high cognitive load, and the need to make counterintuitive decisions — drop traffic to 1% of normal, disable health checks, restart the fleet — is exactly what the [[incident-management-framework]] is built for. Cascading-failure incidents are also characteristically events where *recent change* is the likely trigger, so the Chapter 13 "what changed" diagnostic discipline applies directly.

Chapter 22's eight immediate-step remedies — **increase resources**, **stop health-check failures**, **restart servers**, **drop traffic**, **enter degraded modes**, **eliminate batch load**, **eliminate bad traffic**, **escalate** — are catalogued on [[addressing-ongoing-cascading-failure]]. The meta-rule from Chapter 22 is that the triggering condition must be addressed before traffic is restored; a cascade that merely has its load reduced will resume the moment the load returns.

## Cross-book connection

- Newman's [[monitoring-and-observability]] discusses detection; SRE's emergency-response tenet picks up where detection ends, covering what happens once the alert has fired.
- Burns's [[health-probes|liveness and readiness probes]] and orchestration-level restart mechanisms are exactly the kind of automated recovery that keeps humans out of the loop in the first place.
- Chaos engineering (Chaos Monkey and similar industry practice) is the open-source form of Chapter 13's proactive-testing prescription.

## Related pages

- [[mttr-and-mttf]]
- [[on-call-playbook]]
- [[blameless-postmortem]]
- [[sre-tenets]]
- [[toil-and-engineering-balance]]
- [[monitoring-and-observability]]
- [[health-probes]]
- [[sre-on-call-engagement]]
- [[balanced-on-call]]
- [[incident-response-mindset]]
- [[operational-overload]]
- [[operational-underload]]
- [[multi-site-on-call]]
- [[on-call-compensation]]
- [[triage-sre]]
- [[troubleshooting-model]]
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
- [[cascading-failure]]
- [[addressing-ongoing-cascading-failure]]
- [[cascading-failure-triggers]]
