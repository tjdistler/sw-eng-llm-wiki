# MOC: Reliability and Operations

**Summary**: Entry point for questions about *the operational promise a service makes and the discipline required to keep it* — SLOs and error budgets as the economic framing of reliability, monitoring and observability as the feedback loop, on-call and incident response as the human response, postmortems as the learning loop, cascading-failure and overload dynamics as the failure patterns you have to engineer against, release engineering and launch coordination as the forward-looking safety practice, and the platform topics (load balancing, capacity planning, service discovery) that keep the whole thing upright. Start here when the question is "what promise should this service make and how do we keep it?" rather than "what shape should the service itself have?" (that's [[moc-container-and-serving-patterns]]) or "how do services talk?" (that's [[moc-events-and-streaming]]).

**Sources**: (meta-page; aggregates concept pages and links to raw chapters)

**Last updated**: 2026-04-19

---

## When to read this

You have a production service (or one you're about to launch) and the question is about its *promise* and the *practice* that keeps it. Maybe you're launching and need a real SLO, not a gut feel. Maybe your alerts wake you up every night and you can't tell signal from noise. Maybe an incident is in progress and you want to understand the roles in the room. Maybe your last three outages were all cascading-failure flavour and "just add retries" keeps making it worse. Maybe the team is discussing whether to adopt SRE, or has adopted SRE and the relationship with the product team is unhealthy.

The canonical shape of a question that lands here: *"What's a sensible SLO adoption path for a service with no history?"*, *"Why are we exhausting our error budget — and what do we do about it?"*, *"How do I monitor this service without drowning in alerts?"*, *"Our canary deployment hit an SLO gate — what actually happens next?"*, *"Our retries made a blip into an outage — what do we do structurally?"*, *"How do I run an incident as incident commander?"*, *"What goes into a production-readiness review?"*, *"What should our on-call shift look like?"*

Jurisdictional rule for this MOC:

- **This MOC** owns the *operational promise and discipline* — SLOs/SLIs/error budgets, monitoring philosophy, on-call health, incident command, postmortem culture, cascading-failure and overload dynamics, launch coordination, production-readiness review, platform topics (load balancing at scale, capacity planning, service discovery), and the SRE engagement model. Google's *Site Reliability Engineering* is the spine; the data-engineering reliability undercurrent (data integrity, data observability, dataops) rounds out the data side.
- [[moc-container-and-serving-patterns]] owns the *shape and mechanics* of the service you're operating — how its containers compose, how it's replicated/sharded, what deployment pattern its rollout uses. Deployment patterns are shared: this MOC owns them as *safety practice* (progressive delivery as error-budget protection, canary as SLO-gated rollout); that MOC owns them as *mechanism*.
- [[moc-distributed-systems]] owns the *mechanisms* whose operational story this MOC tells. Consensus monitoring, fencing-token semantics, partial-failure modes, unreliable-network realities. This MOC says "the SRE runbook for a consensus-backed system"; that MOC says "here is why the consensus protocol does what it does."
- [[moc-data-processing]] owns the *pipeline-execution* half of SRE Ch 25 and [[dataops]]; this MOC owns the broader operational discipline the pipeline team plugs into.
- [[moc-security-and-privacy]] owns security as its own undercurrent; this MOC cites [[security-monitoring]] under the observability lens while the security MOC owns threat modelling, encryption, access control, and privacy compliance.

Shared pages (deployment patterns, capacity planning, consensus-monitoring, data-integrity) appear here under the *operational-discipline* lens. Follow sibling MOCs for the mechanism or security lenses.

## What SRE *is* — the frame before the techniques

Before any practice, know what problem SRE is solving and what distinguishes it from plain ops. Get this wrong and every chapter below is cargo-culted.

- [[site-reliability-engineering]] — the book-level summary page. The "class SRE implements DevOps" framing, Google's operational tenets, the read-order suggestion.
- [[sre-discipline]] — the definition: software engineers applied to operations problems, with a mandate to automate their way out of toil. The distinguishing feature from "ops team that also codes."
- [[sre-tenets]] — the durable principles: embrace risk, service-level objectives, eliminate toil, monitor, automate, release engineer, simplify. Every chapter in the book is a deepening of one of these.
- [[devops-vs-sre]] — why SRE is a specific implementation of DevOps philosophy rather than a competitor to it. The distinction that avoids sterile turf wars.
- [[velocity-vs-reliability-tradeoff]] — the core trade-off SRE explicitly negotiates. Error budget as the currency that settles it. The framing that makes SRE-vs-product tension productive rather than perpetual.
- [[sysadmin-approach]] — the traditional ops model SRE is distinguishing itself from: component assembly plus a separate "operations team" that holds the pager. The anti-frame; understanding it in detail is the fastest way to articulate what SRE actually changes.
- [[system-stability-vs-agility]] — the core tension every SRE conversation eventually lands on: change is the biggest source of outage, and not-changing is the biggest source of decay. Reliable processes (release engineering, canarying, feature flags) *increase* agility rather than tax it — the reframing the book returns to repeatedly.
- [[virtue-of-boring]] — the cultural stance: predictable software that follows the script is positive, surprise is the enemy. Read alongside [[simplicity-sre]]; they're the two sides of the same principle.

Deeper reading: [[site-reliability-engineering#chapter-1-introduction]] for the framing; [[site-reliability-engineering#chapter-2-the-production-environment-at-google-from-the-viewpoint-of-an-sre]] for the concrete Google-production-stack grounding.

## Embracing risk — error budgets and SLOs

Reliability is not a feature to be maximised; it is a budget to be *spent*. Nothing else in this MOC makes sense until this frame is internalised.

- [[risk-tolerance]] — service-specific, not organisation-wide. Payments tolerates different risk than analytics. The acceptable-unreliability number is a product decision, not an engineering one.
- [[error-budget]] — `1 - SLO` expressed as budget. If your SLO is 99.9%, you have 43 minutes per month to spend. Spend it on launches and experimentation; hoard it when something is systemically unstable. The economic object that converts velocity-vs-reliability from a debate into an accounting exercise.
- [[risk-management-sre]] — using the error budget as a decision input: launch pace, rollout cautiousness, feature-flag exposure. The day-to-day practice the budget enables.
- [[availability-measurement]] — the mechanics: time-based (uptime) vs request-based (success ratio). Why request-based is almost always the right one for services.
- [[reliability]] — the broader "-ility" framing; how reliability sits alongside availability, durability, latency. The vocabulary for any SLO discussion.

### SLIs, SLOs, SLAs

- [[service-level-indicator]] — SLI: the *measurement*. Request success rate, p95 latency, queue freshness. Choose SLIs that reflect user experience, not internal convenience.
- [[service-level-objective]] — SLO: the *target* an SLI must meet. "99.9% of requests return 200 within 300ms over a rolling 30-day window." The commitment the team makes to itself.
- [[service-level-agreement]] — SLA: the *contract* with external customers, with consequences (credits, refunds, support escalation) for missing it. Always strictly weaker than the internal SLO — you want the buffer.
- [[slo-expectations]] — how SLOs shape stakeholder conversations. The frame for "we missed this quarter's error budget and won't ship feature X until we're back in budget." The structured negotiation SLOs enable.
- [[sli-standardization]] — standard SLI catalogs (availability, latency, freshness, correctness, coverage, throughput) so every team isn't inventing the wheel. The prerequisite for cross-team error-budget policies.
- [[sli-aggregation]] — how SLIs roll up across shards, regions, endpoints. The mechanics that turn a minute-by-minute measurement into a 30-day error-budget number.

Deeper reading: [[site-reliability-engineering#chapter-3-embracing-risk]] and [[site-reliability-engineering#chapter-4-service-level-objectives]]. These two chapters are the load-bearing theory for this entire MOC.

## Eliminating toil — the automation mandate

Toil is the operational work that scales linearly with service growth. An SRE team whose work is dominated by toil has no bandwidth to improve anything.

- [[toil-and-engineering-balance]] — the explicit ≤50% toil cap. SRE time above that threshold is reinvested in automation; below that, the team stays close enough to operations to understand what to automate. The cap that preserves the engineering mandate.
- [[sre-efficiency]] — the measurement: the effective capacity of an SRE team scales with how much of its operational load it has automated away. A team drowning in toil is a team without a future.
- [[engineering-work-categories]] — the four-way taxonomy the 50% cap is expressed in: software engineering, systems engineering, toil, overhead. The accounting categories that make "are we hitting the cap?" a calculation rather than a gut-feel argument.
- [[operational-load]] — the total work of keeping a complex system running: pages, tickets, ongoing responsibilities. The thing toil-caps, interrupt rotations, and project-time protection are together managing.
- [[ops-mode]] — the anti-pattern the toil cap exists to prevent: when load grows, the team's reflex is to add human labour (hire another ops engineer) rather than automate. Structurally guarantees drift away from engineering.
- [[autonomous-systems]] — the top of the automation-maturity ladder: operational concerns handled as intrinsic design properties rather than external scripts. Not a team process — a software-design goal. The aspirational end state [[automation-at-google]] traces the path to.
- [[software-engineering-in-sre]] — the SRE Ch 18 argument that SRE teams should run full software projects (monitoring platforms, release tooling, capacity-planning systems) solving internal production problems. The counter to the "SRE just writes scripts" caricature.
- [[negative-lines-of-code]] — the aesthetic cousin: every line of code is a liability, so code *deletion* is the highest-value change. A simplicity heuristic that frequently wins over new-feature work for reliability-critical services.

### Automation as the response

- [[automation-at-google]] — the hierarchy of automation maturity: no automation → externally-maintained scripts → externally-maintained code → internally-maintained code → autonomous systems. Every operational workflow should be progressing up the hierarchy over time.
- [[hierarchy-of-automation-classes]] — the named levels in the above progression; the vocabulary for saying "we're at level 3 and need to get to level 4."
- [[automation-gone-wrong]] — the counter-examples: automation that amplifies errors, automation that hides operational knowledge, automation that becomes its own maintenance nightmare. The reminder that "automate everything" is not the goal.
- [[cluster-turnup-automation]] — the worked Google example: the multi-year progression from shell scripts to Prodtest-driven declarative turnup. A concrete arc up the hierarchy.

Deeper reading: [[site-reliability-engineering#chapter-5-eliminating-toil]] and [[site-reliability-engineering#chapter-7-the-evolution-of-automation-at-google]].

## Monitoring and observability

The feedback loop. Everything else in this MOC — SLOs, alerts, incident response, cascading-failure avoidance — depends on being able to see the system accurately and at the right resolution.

### Monitoring philosophy

- [[monitoring-and-observability]] — the top-level framing. Monitoring is the explicit observation of known properties (SLIs, health, saturation); observability is the broader property of being able to ask new questions about the system after the fact. SLIs are the core deliverable; dashboards and traces are how you answer the questions SLIs provoke.
- [[four-golden-signals]] — Latency, Traffic, Errors, Saturation. The four dimensions every user-facing service should expose. The default SLI menu if you can't think of better ones.
- [[black-box-vs-white-box-monitoring]] — blackbox tests user-visible symptoms (can the front door be opened?); whitebox tests internal state (is this queue growing?). Alert on blackbox, diagnose with whitebox. Most teams do the opposite and wonder why the pager is useless.
- [[symptoms-vs-causes]] — alert on symptoms (SLO violations), investigate causes during response. A cause-based alert ("disk is 90% full") pages you before anything is broken; a symptom-based alert ("user-visible error rate is elevated") pages you because something actually *is*.
- [[monitoring-simplicity]] — the explicit principle: monitoring code is not exempt from simplicity constraints. Complex monitoring is brittle, misleading, and unmaintainable. The prose cousin of [[simplicity-sre]].
- [[monitoring-resolution]] — the sampling-rate question. Per-second vs per-minute vs per-hour. Fine-grained enough to catch spikes; coarse enough to keep cost and retention tractable. Usually a mix.
- [[mttr-and-mttf]] — mean time to repair and mean time to failure; the arithmetic behind any availability SLO. The vocabulary that turns "how reliable is this service?" into a number derived from incident history, not intuition.
- [[response-time-percentiles]] — p50, p95, p99, p99.9. Means lie about user experience; percentiles reveal it. The measurement discipline that makes latency SLIs honest.
- [[long-tail-latency]] — the subset of requests that take much longer than the median; empirically, percentile distributions matter more than means in any user-visible latency conversation. The motivator for the percentile SLIs above.

### Monitoring infrastructure

- [[monitoring-topology-sharding]] — at Google-scale, monitoring can't be a single Prometheus. Sharding by query workload, regional aggregation, and federation patterns. The operational shape of monitoring itself.
- [[distributed-tracing]] — the one signal that actually tells you *which hop* in a request was slow or broken. Dapper/Jaeger/Zipkin-style span propagation. The tool you reach for when "which service is the bottleneck?" is the question. Cross-cited from [[monolith-to-microservices]] because extracting a service makes a single request a trace-able graph.
- [[log-aggregation]] — centralised logs so you can correlate across services. The substrate under incident debugging and postmortem evidence-gathering.
- [[alert-philosophy]] — every page should be actionable. If it's informational, make it a ticket. If you can't articulate what the on-call should do, the alert shouldn't fire. The single most-violated principle in production ops.
- [[alertmanager]] — the Prometheus-native router. Grouping, silencing, deduplication, routing to pager/Slack. The page-fatigue mitigations live here.
- [[sre-monitoring-outputs]] — the three outputs monitoring should produce: alerts (pages), tickets (asynchronous follow-up), and logs/dashboards (investigation and trend). Any monitoring signal that doesn't land in one of these three is noise.
- [[prober]] — the blackbox-monitoring tool: synthetic protocol checks against live endpoints to catch failures the service's own whitebox instrumentation can't see. The "can the front door be opened from outside?" signal.
- [[production-probes]] — the forward-looking variant: monitoring requests that replay a curated test set against production to catch version-to-version drift and cross-service contract breaks. The canary's observability cousin.
- [[prometheus-connection]] — the open-source genealogy: the ideas in this section (time-series storage, rules-based alerting, multi-dimensional labels) are available outside Google through Prometheus and its ecosystem. The framing that makes this MOC transferable to teams not running Google's internal stack.

### Specialised monitoring domains

- [[consumer-lag-monitoring]] — stream-consumer-specific signal: how far behind are we? The SLI for "is our stream-processing job healthy?" More useful than CPU/memory for stream workloads.
- [[consensus-monitoring]] — member health, leader existence, leader-change rate, proposal rates for ZooKeeper/etcd/Raft-backed systems. Cross-cited from [[moc-distributed-systems]].
- [[pipeline-monitoring-problems]] — the canonical failure modes of pipeline monitoring: alerts on job completion without alerts on correctness, thundering-herd downstream on restart, missing dependencies. The anti-pattern catalogue.
- [[security-monitoring]] — access, resource-use, billing-anomaly, and excess-permission signals. A distinct discipline from ordinary observability; see [[moc-security-and-privacy]] for the full picture.

Deeper reading: [[site-reliability-engineering#chapter-6-monitoring-distributed-systems]] and [[site-reliability-engineering#chapter-10-practical-alerting-from-time-series-data]].

## Simplicity — the meta-principle

Every other practice in this MOC fails when the underlying system is gratuitously complex. Simplicity is not aesthetic; it is operational.

- [[simplicity-sre]] — the SRE Ch 9 thesis: reliability requires simplicity. Complex systems have more failure modes, more interactions, more surface area for bugs. The continuous discipline of *removing* what isn't earning its complexity.
- [[release-simplicity]] — the release-engineering cousin: small, frequent releases fail smaller. Simplicity applied to the deployment pipeline.
- [[monitoring-simplicity]] — the monitoring cousin: a simple monitoring stack that you understand beats a comprehensive one you don't.

Deeper reading: [[site-reliability-engineering#chapter-9-simplicity]].

## Release engineering — safety on the way in

The reliability discipline applied to the act of introducing change. This section deliberately overlaps with [[moc-container-and-serving-patterns]]; that MOC owns the *mechanisms*, this one owns the *safety practice* around them.

### The release-engineering discipline

- [[release-engineering]] — SRE Ch 8: release engineering as an engineering discipline with its own principles, tooling, and organisational model. Not a side-effect of development; a first-class product.
- [[release-engineering-principles]] — self-service, high velocity, hermetic builds, enforcement of policies. The principles any mature release pipeline embodies.
- [[hermetic-builds]] — builds that produce byte-identical outputs from the same inputs. The foundation under "rebuild from the tag" and "this artifact is the one we tested."
- [[release-policy-enforcement]] — policy-as-code gating what a release must pass. The mechanism under "you can't bypass the canary."
- [[self-service-release-model]] — any engineer can release any service at any time because the pipeline is self-service infrastructure. The end state of release-engineering maturity.
- [[high-release-velocity]] — frequent releases improve safety, not diminish it. The counter-intuitive but empirically durable observation.
- [[rapid-release-system]] — Google's actual release frequency; the existence proof for the principle above.
- [[release-branching-and-cherry-picking]] — the Git workflow: main-branch development, release branches cut on cadence, cherry-picks for hotfixes.
- [[continuous-integration-delivery-deployment]] — the vocabulary map for CI, CD-delivery, CD-deployment. Different commitments, different operational costs.
- [[build-system-discipline]] — the foundational practices underneath everything above: versioned source control, continuous build, fast failure, reproducible outputs. Release engineering is built on top of these; skipping them produces intermittent release-pipeline mysteries for years.
- [[change-management-sre]] — the three-part automation response to change-induced risk: progressive rollouts, fast detection of problems, quick rollback. The operational trio most release-engineering practice composes.
- [[configuration-management-sre]] — treating configuration changes as first-class releases: versioned, reviewed, canaried, rolled back. The discipline that catches the "nobody shipped code but the service broke" class of incident.
- [[push-on-green]] — the end-state release model: every build that passes its test gates auto-deploys to production. Raises the reliability floor of the test gates in exchange for eliminating human-scheduler delay.
- [[break-glass-push]] — the deliberate-emergency-only override for the release gates. The presence of this mechanism is usually necessary; the normalisation of using it is the anti-pattern. Audit frequency-of-use as a signal.
- [[fake-backend-versions]] — hermetic test backends pinned to the exact production revision so integration tests aren't chasing upstream drift. The mechanism that keeps the release gate from being the place cross-service bugs first surface.

### Rollout mechanisms, under the safety lens

These mechanisms are owned as *shapes* by [[moc-container-and-serving-patterns]]. Under this MOC's lens, they are safety practices that protect the error budget.

- [[deployment-vs-release]] — decoupling deploy from release (via feature flags) is the single largest reliability win of the last decade. Dark-launched code runs in production unobserved until the team is ready; a bad release becomes a flag flip, not a redeploy.
- [[canary-test]] — expose the new version to 1% of traffic and watch SLIs. The cheap version of progressive delivery.
- [[progressive-delivery]] — automated canary analysis: as long as SLO gates hold, traffic percentage increases; on gate failure, automatic rollback. The safety mechanism that protects a tight error budget.
- [[gradual-rollout]] — the generalisation: any growing-cohort exposure mechanism. Canary, feature-flag-percentage, geographic rollout.
- [[feature-toggle]] — the primitive: a runtime switch that gates a code path without a redeploy. Under the reliability lens, the mechanism that turns a bad release from a redeploy into a flag flip — seconds instead of minutes of MTTR.
- [[feature-flag-framework]] — the infrastructure that makes deploy-vs-release workable at scale: registry, SDK, targeting rules, kill-switch semantics.
- [[blue-green-deployment]] — atomic cutover between environments; the safest rollback mechanism at the cost of 2x capacity during transition.
- [[rolling-update-pattern]] — the default for replicated services; safe when the new version is wire-compatible with the old.

Deeper reading: [[site-reliability-engineering#chapter-8-release-engineering]].

### Reliable product launches

Launching is a distinct discipline from steady-state operation. The failure modes are different; the tooling needs to be different.

- [[reliable-product-launches]] — the end-to-end SRE Ch 27 story: what it takes to launch a product without burning the next six months of error budget in the first week.
- [[launch-coordination-engineering]] — the practice: a team (or rotation) whose job is to make launches go well. Checklists, rehearsals, production-readiness reviews.
- [[launch-coordination-engineer-role]] — the human role inside that practice; what an LCE actually does day to day.
- [[launch-checklist]] — the artifact. Architecture review, capacity projection, dependencies audited, monitoring wired, runbook written, rollback tested. The thing you fill out before the rollout, not after the incident.
- [[launch-checklist-themes]] — the themes the checklist covers; the structure that keeps launches from turning into bespoke one-offs each time.
- [[overload-behavior-launches]] — launch-specific failure mode: traffic ramps faster than projections, the service overloads. Connects to the overload section below.

### Production-readiness review (PRR)

- [[production-readiness-review]] — the SRE-Ch-32 ritual: before an SRE team accepts responsibility for a service, it must pass PRR. Monitoring, capacity, release practices, documentation, on-call readiness. The gate that prevents "here, take this service, good luck."
- [[prr-continuous-improvement]] — PRR is not one-shot. Services that passed PRR can drift; periodic re-review catches drift before it becomes an outage.
- [[simple-prr-model]] — the classical five-phase SRE engagement: engagement → analysis → improvements → training → onboarding. The shape the individual PRR phases below compose into; start here before reading any one phase.
- [[prr-engagement-phase]] — phase 1: SRE leadership and reviewers identify the team, open discussion of the service, and decide whether PRR will proceed. The go/no-go step.
- [[prr-analysis-phase]] — phase 2: reviewers learn the service, gauge production maturity, and write the improvement recommendations. The step that produces the punch list.
- [[prr-improvements-and-refactoring]] — phase 3: the dev team turns PRR findings into changes, negotiated by priority. Not every finding has to be resolved before onboarding; the point is *explicit* acknowledgement and a plan.
- [[prr-training-phase]] — phase 4: PRR reviewers teach the receiving SRE team everything needed to take production ownership. The knowledge-transfer step; under-invested by every team until after their first post-onboarding incident.
- [[prr-onboarding-phase]] — phase 5: progressive transfer of production responsibility to SRE. Shadow-on-call first, primary on-call last. The completion of engagement.
- [[shared-responsibility-engagement]] — the variant where SRE owns platform infrastructure and development owns functional bugs; shared pages route by root cause. The model for services SRE helps operate but doesn't take outright.
- [[early-engagement-model]] — SRE joins during the design phase rather than at PRR time. Cheaper in total and produces a more reliable launch; requires SRE capacity that most organisations under-staff.
- [[early-engagement-candidates]] — three service patterns most eligible for early engagement: new services of strategic importance, services replacing an existing SRE-supported system, services with unusual reliability demands. The triage filter.
- [[disengaging-from-a-service]] — the valid-outcome case: a service reaches a state of sufficient reliability, low toil, and stable ownership that SRE can step back. Not a failure mode — a capacity-freeing success.

Deeper reading: [[site-reliability-engineering#chapter-27-reliable-product-launches-at-scale]] and [[site-reliability-engineering#chapter-32-the-evolving-sre-engagement-model]].

## On-call health and incident response — safety under fire

Things break. The question is what the response looks like — competent and bounded, or panicked and infinitely escalating.

### The on-call life

- [[on-call-playbook]] — the SRE Ch 11 framing. What an on-call shift looks like, what the expectations are, what makes the difference between a healthy on-call culture and a burn-out one.
- [[balanced-on-call]] — the structural constraint: no engineer pages more than twice per shift, no shift longer than 12 hours, no rotation shorter than two people deep. Violate any of these and the rotation collapses over time.
- [[multi-site-on-call]] — follow-the-sun for 24/7 coverage without nighttime paging. The scaling pattern once a team is big enough for it.
- [[on-call-compensation]] — the compensation mechanism (cash, time-in-lieu, reduced-hour-week). Free on-call is not free — it's paid in attrition.
- [[on-call-learning-checklist]] — what a new engineer needs to know before taking the pager. The prerequisite for putting anyone on-call at all.
- [[shadow-on-call]] — the first phase: new on-call shadows an experienced one, no independent action.
- [[reverse-shadow-on-call]] — the second phase: new on-call runs the pager, experienced one shadows. The handoff before going solo.
- [[dealing-with-interrupts]] — the day-to-day reality for embedded SRE: balancing long-term engineering work against the steady stream of operational interrupts. The structural responses (ticket triage, interrupt shifts, office hours).
- [[interrupt-role-structuring]] — the concrete structure: primary (pager) / secondary (ticket triage) / builder (protected engineering time). Rotate weekly.
- [[reducing-interrupts]] — the meta-goal: every recurring interrupt is a bug. The practice of investing in fixes so the interrupt rate trends down.
- [[polarizing-time]] — the team-design lever: structure a day as project-work OR interrupts, not both. Context-switching is too expensive to mix at the hour granularity; polarise by day or by week.
- [[cognitive-flow-state]] — the thing polarised time exists to protect: engineers do their best work in uninterrupted stretches measured in hours, and a single mid-flow page costs more than the page itself.
- [[context-switch-cost]] — the measurement behind the above: a context switch is not free and not small. Explicit in the SRE time-budget argument.
- [[production-meetings]] — the weekly service-oriented ritual that keeps dev and SRE aligned: service health, recent incidents, capacity, upcoming launches. The meeting that makes SRE-dev collaboration habitual rather than event-driven.

### Incident response — during the event

- [[incident-response-mindset]] — the mindset the on-call adopts when a real incident starts. Don't fix and discuss later; communicate as you go; prioritise stabilisation over root-cause discovery.
- [[declaring-an-incident]] — the explicit call-out. "This is an incident. I am incident commander." The mechanism that transitions from "a page fired" to a coordinated response.
- [[incident-management-framework]] — the SRE Ch 14 structure: Incident Commander, Operations Lead, Communications Lead, Planning Lead. Named roles so everyone knows who is doing what.
- [[incident-command-system]] — the broader framing (borrowed from firefighting / emergency services) under which the SRE role structure sits. Useful for arguing the shape's legitimacy.
- [[incident-commander]] — IC: owns the overall response, makes go/no-go calls, does not touch keyboards. The role whose job is to *not* fix the bug because they need to be free to coordinate.
- [[incident-ops-lead]] — Ops Lead: owns the fix; coordinates the engineers actually typing. Reports status to the IC.
- [[incident-communications-lead]] — Comms Lead: owns external communication (status page, customer email, executive updates). Frees the IC from the comms treadmill.
- [[incident-planning-lead]] — Planning Lead: documents timeline, tracks action items, manages shift changes during long incidents.
- [[live-incident-state-document]] — the single collaborative document that is the authoritative state of the incident. IC keeps it current; everyone reads it. Prevents the "what's happening?" question on loop.
- [[incident-handoff]] — shift-change during a long incident. Structured handoff doc + sync call. The thing that prevents "the new IC doesn't know what we've already tried."
- [[incident-aggregation]] — grouping related pages into a single incident. Prevents ten pages for one failure from becoming ten parallel investigations.
- [[incident-tagging]] — categorisation for later analysis: severity, root-cause bucket, affected product. The data that drives the quarterly trends.
- [[unmanaged-incident-anti-patterns]] — what unmanaged incidents look like: no IC, no single source of truth, everyone typing at once, no comms, no plan for shift change. The shape of the failure the framework above prevents.
- [[recognized-command-post]] — the designated location (physical room, virtual channel, document) where the incident commander is reachable. The rule that prevents six parallel side-conversations from starting before the IC even knows about them.
- [[recursive-separation-of-responsibilities]] — the scaling rule for long or large incidents: each role (IC, Ops, Comms, Planning) can subdivide recursively under load. The mechanism that keeps the role structure usable during incidents big enough to need twenty responders.

### Troubleshooting under pressure

- [[triage-sre]] — the first-5-minutes discipline: stop the bleeding (maybe rollback, maybe throttle, maybe traffic-shift) before starting root-cause investigation. The ordering error that turns a 10-minute incident into an hour.
- [[troubleshooting-model]] — the SRE Ch 12 structured approach: observe → hypothesise → test. Don't skip steps; don't pattern-match ahead of evidence.
- [[troubleshooting-anti-patterns]] — the common failures: confirmation bias, streetlight effect ("let's look where it's bright"), fixing causes instead of symptoms, solo heroics without communication.
- [[improvisational-troubleshooting]] — the acknowledgement that real incidents rarely match the runbook. How to stay rigorous while improvising. Closest SRE comes to teaching debugging taste.
- [[making-troubleshooting-easier]] — the forward-looking practice: design services so they can be debugged. Good logs, good dashboards, good runbooks. The work that pays off every time an incident lands.
- [[divide-and-conquer-debugging]] — the generic troubleshooting technique that works without deep system knowledge: bisect the request path, bisect the time window, bisect the code change set. The fallback when you don't already know where the bug is.
- [[hypothetico-deductive-debugging]] — the scientific frame: generate hypotheses, design experiments that rule them in or out, iterate. The antidote to confirmation bias and streetlight-effect fixes.
- [[test-and-treat]] — the phase inside hypothetico-deductive debugging where you *design* the experiments: what would disconfirm this theory, and how can you actually run that experiment against production or a replica?
- [[identifying-kindling]] — the forward-looking discipline: spot the structural weaknesses positioned to become the *next* emergency (a tightly-coupled deploy, a shared cache with no quota, a single-replica service) before they ignite. Preemptive postmortem work.
- [[breaking-real-systems]] — the SRE training practice: hands-on chaos exercises against real (staging or production-with-guardrails) systems, so on-call engineers have seen the failure mode before the pager fires. The simulator pilots get; on-calls rarely do.

### Emergency response

- [[emergency-response]] — the SRE Ch 13 framing: the highest-severity shape of incident response. Nation-state-scale outages, data loss, safety-critical failures. When the stakes raise, the process gets tighter, not looser.
- [[test-induced-emergency]] — an emergency caused by a load test, a canary, a fault-injection test. The "we did this to ourselves" category; usually easier to diagnose, sometimes more embarrassing.
- [[change-induced-emergency]] — by far the most common kind: someone shipped something. The question is always "what changed?" Good release engineering (section above) cuts the MTTR here dramatically.
- [[process-induced-emergency]] — an emergency caused by a workflow or ritual that went wrong: failed data-pipeline refresh, missed capacity-order, expired certificate. The case for operational process being an engineering artifact itself.

Deeper reading: [[site-reliability-engineering#chapter-11-being-on-call]], [[site-reliability-engineering#chapter-12-effective-troubleshooting]], [[site-reliability-engineering#chapter-13-emergency-response]], [[site-reliability-engineering#chapter-14-managing-incidents]].

## Postmortem culture — learning from failure

Incidents happen. A mature team extracts compounding learning from every one. An immature team relives them.

- [[blameless-postmortem]] — the foundational norm: the postmortem focuses on *what failed* and *how to prevent recurrence*, not on who is at fault. Without this, people hide failures, and the learning loop breaks.
- [[postmortem-philosophy]] — the deeper framing: incidents are expected; the purpose of a postmortem is institutional memory and structural improvement, not catharsis.
- [[postmortem-template]] — the artifact. Timeline, impact, root cause, contributing factors, action items with owners. A consistent template so postmortems aggregate usefully over time.
- [[postmortem-triggers]] — the criteria for writing one. Not every page becomes a postmortem, but "customer-visible impact over threshold X" should always be one.
- [[postmortem-review-process]] — the rhythm: draft → review → publish → track action items. The steps that prevent a postmortem from being a doc that no one reads.
- [[teachable-postmortems]] — postmortems written to be read by others who weren't there. The "shareable" bar — with enough context that a new engineer gets educated from reading it.
- [[postmortem-culture-activities]] — the cultural practices: postmortem reading groups, wheel-of-misfortune drills, postmortem-of-the-month awards. How a team keeps postmortems alive rather than filed and forgotten.
- [[rewarding-postmortems]] — the explicit organisational reinforcement: incentive structure visibly rewards learning from failure. Without this, the team reverts to blame or silence.
- [[postmortem-feedback-surveys]] — measuring postmortem quality itself. Are postmortems useful? Are they read? Are action items tracked?
- [[postmortems-at-google-working-group]] — the Google-internal community of practice around postmortems. The existence proof that postmortem culture needs community investment to sustain.
- [[bad-apple-theory]] — the postmortem-mindset antipattern the "blameless" norm was built to counter: the idea that mistakes come from individual bad actors rather than structural conditions. Naming the theory explicitly is the fastest way to recognise when a postmortem is drifting toward it.
- [[organizational-safety-culture]] — the organisational frame around postmortem practice: management visibly prioritises safety, so workers raise concerns without fear. The cultural precondition for blameless postmortems actually producing honest accounts.
- [[near-miss-reporting]] — preemptive-postmortem practice: events that *could* have caused serious harm but didn't get the full postmortem treatment. The aviation-industry discipline that Chapter 33 urges SRE to import.
- [[negative-results]] — the documentation practice for experiments and investigations that disconfirmed a hypothesis. The discipline that prevents the same unsuccessful fix from being tried three times across successive incidents.

### Tracking outages

- [[outage-tracking]] — aggregating outages across time to surface trends. The input to every "are we getting better?" question a leadership team asks.
- [[outage-analysis]] — cross-incident pattern recognition: which failure modes recur, which services are reliability hotspots, which action items never shipped.
- [[learning-from-outages]] — the broader framing: postmortems are one artifact, trend analysis is another, incident-review meetings are a third. Collectively, the institutional-memory system.

Deeper reading: [[site-reliability-engineering#chapter-15-postmortem-culture-learning-from-failure]] and [[site-reliability-engineering#chapter-16-tracking-outages]].

## Handling overload and cascading failure

Three failure patterns dominate production incidents at scale: overload (demand exceeds capacity), cascading failure (a local overload propagates into a global one), and coordinated-amplification (everyone retries at once). Engineer against all three structurally, not reactively.

- [[handling-overload]] — the SRE Ch 21 catalogue. Load shedding at the edge, graceful degradation mid-service, queue management under pressure. The structural answers to "we can't serve everyone — what do we do?"
- [[load-shedding]] — refuse a subset of requests at the edge so the accepted subset can succeed. The structural alternative to queueing until everything times out. Choose what to shed by priority, client tier, or random sampling.
- [[graceful-degradation]] — serve a reduced version of the service when the full version can't be sustained. Show cached results, skip personalisation, return stale data. The mechanism that keeps the service *useful* rather than *absent* under load.
- [[queue-management]] — bounded queues with explicit admission control. Unbounded queues are a delayed failure; bounded queues are an explicit one.
- [[server-overload]] — the shape: arrival rate > service rate, queue grows, latency grows, clients time out and retry, making it worse. The positive-feedback loop that defines overload.
- [[bimodal-latency]] — the specific overload failure mode where a minority of slow requests exhaust capacity by holding threads or connections past their deadlines, and the majority of fast requests never get served. Deadline enforcement is the structural fix.
- [[deadline-propagation]] — the cascading-failure defence where each RPC's deadline flows through the call graph, so downstream work is abandoned as soon as the caller has timed out. Protects against the "downstream keeps working on a request nobody's waiting for" energy-waste.
- [[latency-and-deadlines]] — the framing for deadline propagation: deadlines aren't a latency guarantee, they're a resource-protection mechanism. The more RPCs an incoming request fans out to, the more a budget-cap on total wall time matters.
- [[adaptive-throttling]] — client-side throttling that sheds load at the *source* rather than at the overloaded backend's edge. The structural complement to backend load shedding.
- [[request-criticality]] — the four-valued RPC priority (CRITICAL_PLUS, CRITICAL, SHEDDABLE_PLUS, SHEDDABLE) that tells the backend which requests to drop first when it has to drop some. The mechanism that lets load shedding preserve what the business cares about.
- [[per-customer-quotas]] — the first line of load defence: the backend rejects requests from customers over their budget, so one customer's spike doesn't consume another's capacity. Works only if the quota is measured in the right unit — see below.
- [[queries-per-second-pitfalls]] — QPS is a notoriously bad capacity metric because "a query" is not a fixed unit. Measure available resources (CPU, memory, connections) instead; QPS capacity is derived, not primary.
- [[abusive-client-behavior]] — the class of load that isn't a single customer spike but a pattern: retry storms, stuck clients, misconfigured automation. The SRE engagement pattern for managing non-user-initiated load.
- [[barrier-defenses]] — the structural protection for maintenance software (cron jobs, batch workflows, administrative scripts) that can trigger huge blast radius if misconfigured. Defense-in-depth for the tools your own team operates.

### Cascading failure — the structural cousin

- [[cascading-failure]] — SRE Ch 22. A local overload spreads: A can't serve, B retries A, B overloads, C retries B, etc. Most large outages are cascading-failure-shaped. Designing against them is structural, not reactive.
- [[addressing-ongoing-cascading-failure]] — the during-incident playbook: identify the cascade's leading edge, drop load there, selectively restart, restore capacity in the right order. The reason runbooks for this category of incident exist.
- [[testing-for-cascading-failures]] — load tests and fault-injection specifically designed to surface cascade dynamics. Part of [[testing-for-reliability]]'s catalogue.
- [[slow-startup-and-cold-caching]] — the specific cascade trigger: a restarted service needs warming before it can take full load, but is given full load immediately and fails. Mitigations: warm-start, progressive load ramping, pre-warmed caches.
- [[cascading-failure-triggers]] — the catalogue of conditions that initiate cascades in vulnerable systems: rollout of bad config, dependency latency spike, traffic surge during cold-start, GC pressure, shared-state lock contention. The vocabulary for "what set this off?"
- [[gc-death-spiral]] — the JVM-specific cascade trigger: GC → CPU starvation → slower requests → more allocations in flight → more memory pressure → more GC. Once started, self-reinforcing; the rollback target when the service is Java.
- [[resource-exhaustion]] — the mechanism underneath every overload cascade: the resource dimension that's actually pinned (threads, file descriptors, connections, memory, CPU) determines what shedding or scaling will and won't help. Diagnose before responding.
- [[intra-layer-communication]] — the hidden cascade risk when backend tiers talk among themselves (tier-A fans out to tier-B, tier-B fans out to tier-A). A stalled A-to-B call amplifies into a fleet-wide stall. Structural avoidance is cheaper than dynamic resolution.

### Retry amplification

- [[retry-amplification]] — retries turn blips into stampedes. A 1-second downstream hiccup becomes a 10-second cascade because every client retried during that second.
- [[retry-budget]] — cap retries at the callsite so the retry-rate stays bounded even under failure. The practical fix: "no more than N retries per second, regardless of incoming request rate."
- [[circuit-breaker]] — stop calling a downstream that's failing; fail fast for a cooldown period; probe cautiously before resuming. The per-caller back-pressure discipline that keeps retries from piling on.
- [[bulkhead]] — isolate thread/connection pools per dependency so one slow downstream doesn't exhaust the shared pool and bring down everything. Structural isolation of the retry-amplification blast radius.
- [[fault-tolerance]] — the umbrella "-ility" these patterns together constitute. A service is fault-tolerant if it keeps most of its promise even when pieces of it (or its dependencies) fail. The architectural characteristic, see [[moc-architecture-fundamentals]] for the broader -ilities catalogue.

Deeper reading: [[site-reliability-engineering#chapter-21-handling-overload]] and [[site-reliability-engineering#chapter-22-addressing-cascading-failures]].

## Platform topics — load balancing, capacity, service discovery

The infrastructure that every service sits on. Operational maturity here is the difference between "our service is fine when our load balancer is fine" and "our service handles what load balancers actually do in production."

### Service discovery

- [[service-discovery]] — how a service instance finds its dependencies. DNS-based, client-side lookup against a registry (ZooKeeper/etcd/Consul), sidecar-proxy-based. The primitive under every cross-service call in a fleet of more than two services.
- [[request-routing]] — the routing-tier half of service discovery: given a discovered set of instances, how is an individual request routed? Round-robin, least-connections, consistent-hashing, latency-weighted.
- [[backend-task-states]] — the three-state backend health model (healthy / lame-duck / unhealthy) that clients need to understand to drain connections cleanly during rollouts. The RPC-health primitive underneath graceful shutdown.
- [[lame-duck-state]] — the specific middle state: the backend is still serving in-flight requests but refusing new ones. The mechanism that makes zero-downtime deploys possible without connection-storm disruption.

### Load balancing

- [[frontend-load-balancing]] — SRE Ch 19: load balancing at the edge, where traffic enters. DNS-based geographic routing, anycast, virtual-IP. The layer closest to the user and the one where most failures first show up.
- [[datacenter-load-balancing]] — SRE Ch 20: load balancing inside a datacenter. Different constraints (known topology, trusted clients), different mechanisms.
- [[dns-load-balancing]] — DNS as the most basic load-balancing mechanism. Limitations: DNS caching, TTL tradeoffs, client-side DNS rotation not under your control.
- [[anycast-dns]] — the same IP advertised from multiple locations; BGP routes clients to the nearest one. The mechanism under geographic routing for most consumer internet services.
- [[network-load-balancer]] — L4 (transport) load balancing: TCP/UDP connection distribution. Fast, protocol-agnostic, stateless. The front-door for high-throughput services.
- [[smart-load-balancer]] — application-aware (L7) load balancing: looks at HTTP headers, routes by path, terminates TLS. Slower, more capable. Most modern service meshes are smart load balancers.
- [[least-loaded-round-robin]] — the classic algorithm. Robust, cheap, usually good enough. When more-complex schemes don't measurably win, stay here.
- [[packet-encapsulation-load-balancer]] — GRE/VXLAN/Maglev-style load balancing: connections steered by encapsulation rather than NAT. The Google-style high-scale shape.
- [[load-balancing-policies]] — the policy menu: weighted round-robin, least-connections, consistent-hashing, P2C (power-of-two-choices). Pick per workload.
- [[gslb]] — Google's Global Software Load Balancer. The worked example of frontend load balancing at Google scale.
- [[connection-level-load]] — the signal the load balancer needs: how loaded is each backend? Active connections, queue depth, utilisation. The right-signal question is non-trivial.
- [[load-parameters]] — what "load" means for a given service. QPS, connections, bytes/sec, active users, complexity-weighted requests. Load that isn't measured in the right units can't be balanced correctly.
- [[simple-round-robin]] — the baseline policy: rotate through healthy backends. Robust, cheap, usually good enough; the starting point against which all fancier schemes must measurably prove themselves.
- [[weighted-round-robin]] — rotation weighted by each backend's self-reported capacity score. The useful-in-practice variant when backends are heterogeneous or already partially loaded.
- [[subsetting]] — limiting how many backends each client talks to, so connection count doesn't grow quadratically with fleet size. The primitive under any large-scale mesh; the cost paid for not doing it is measured in file-descriptor exhaustion.
- [[deterministic-subsetting]] — the subsetting algorithm that produces near-perfect connection distribution by design (not by chance). The right choice when connection imbalance itself is a risk.
- [[random-subsetting]] — the baseline-and-rejected algorithm: simple, but produces uneven connection distributions at scale. Read to understand why deterministic is usually the right pick.
- [[virtual-ip-address]] — a single advertised IP routed by the load balancer across multiple backends. The primitive that lets client code not care about fleet topology.
- [[direct-server-return]] — the LB shape where incoming requests pass through the load balancer but responses return directly to the client. Doubles effective LB capacity when response bytes dominate request bytes.
- [[edns0-client-subnet]] — the DNS extension that tells authoritative servers the client's approximate location so geographic routing can target the right cluster. The mechanism that makes DNS-based geolocation accurate enough to be useful.

Deeper reading: [[site-reliability-engineering#chapter-19-load-balancing-at-the-frontend]] and [[site-reliability-engineering#chapter-20-load-balancing-in-the-datacenter]].

### Capacity planning

- [[capacity-planning]] — the SRE practice. Forecast demand, procure resources, provision with margin, re-forecast. Done well, invisible; done badly, the reason launches fail under load.
- [[intent-based-capacity-planning]] — the Google shape: teams declare *intent* (SLO, serving region, redundancy level) and capacity-planning systems compute the actual machine counts. The mechanism that scales beyond what per-team spreadsheets can sustain.
- [[traditional-capacity-planning]] — the pre-intent-based shape: forecasts, orders, installs. Still relevant at smaller scales and during the transition to intent-based.
- [[swing-capacity]] — reserve capacity that isn't earmarked to any one service; allocated dynamically as services hit unexpected load. The systemic buffer against forecast error.
- [[utilization-signals]] — what you actually measure to size capacity: CPU, memory, request rate, queue depth, latency percentiles. Which signals lead vs lag is the operational art.
- [[moire-load-pattern]] — the failure mode: synchronised load across instances because of shared cron timing, shared cache TTL, shared retry backoff. Capacity is spent on the peak of the moiré pattern, not the average. Desynchronising via jitter is the mitigation.
- [[n-plus-2-redundancy]] — the sizing rule: provision enough replicas that losing *two* (one to scheduled maintenance, one to unexpected failure) still leaves capacity to serve. The margin that makes rolling updates safe.
- [[provisioning]] — the activity of bringing new capacity online: instance creation, location placement, configuration push, health validation, gradual inclusion in load-balancing pools. The operational process underneath any "add capacity" decision.
- [[scalability]] — the system property the capacity-planning practice is managing: ability to cope with growth in load through well-understood mechanisms (horizontal scaling, sharding, caching) rather than ad-hoc heroics. The measurable architectural characteristic.

Deeper reading: [[site-reliability-engineering#chapter-18-software-engineering-in-sre]] for capacity planning as an engineering problem rather than a procurement one.

## Testing for reliability

Testing the service *under production conditions* — not correctness testing (unit/integration), but load, chaos, and disaster testing.

- [[testing-for-reliability]] — the SRE Ch 17 hub. Integration tests, load tests, fault-injection tests, disaster tests. The taxonomy.
- [[testing-for-cascading-failures]] — cascade-specific testing: sustained load past capacity, fault injection in dependencies, retry-storm simulation.
- [[testing-disaster-recovery]] — SRE Ch 26 cousin: testing that the disaster-recovery path actually works. Backup restore, cross-region failover, rebuild-from-scratch. If you don't test it, it doesn't work.
- [[disaster-role-playing]] — tabletop exercise form. Walk through a realistic scenario with the on-call team, find the gaps, fix them before the real thing.
- [[recovery-testing]] — the more targeted version: specific recovery procedures (restore from backup, rotate a key, promote a replica) tested on a cadence.
- [[preparedness-and-disaster-testing]] — the umbrella term for the disaster-testing discipline. DiRT (Disaster Recovery Testing) at Google is the worked example.
- [[zero-mttr-testing]] — tests where the system recovers without human intervention. If recovery is automated, validate the automation, not just the design.
- [[testing-automation-tools]] — the tooling side: platforms for chaos engineering, load generation, fault injection.

### The test hierarchy — unit through production

The testing-for-reliability practice rests on a conventional test hierarchy that many teams know informally. Making the hierarchy explicit is the prerequisite to deciding where a new test belongs — and to noticing which layers the team is under-investing in.

- [[unit-tests]] — the smallest test form: a separable unit (function, class) exercised for correctness in isolation. The fastest feedback loop; the cheapest test layer to maintain; usually the layer with the highest coverage ratio.
- [[integration-tests]] — assembled components with their dependencies (real or mocked) exercised for correct interaction. Catches the "each piece worked alone but together they don't" class of bug that unit tests structurally can't.
- [[smoke-tests]] — the simplest system tests: critical end-to-end behaviours as sanity checks. Runs in seconds, catches the "the build boots but nothing works" class. The floor of every CI pipeline.
- [[regression-tests]] — system tests written to preserve previously-fixed bugs as recurring assertions. The mechanism that keeps a fix from being reintroduced by a later refactor.
- [[system-tests]] — the largest undeployed test form: fully assembled components exercised end-to-end. Slow, expensive, and irreplaceable; the test layer where cross-service contracts get exercised.
- [[performance-tests]] — system tests establishing acceptable performance characteristics over the lifecycle of the system. The test layer that prevents "the feature works but is too slow to ship."
- [[stress-tests]] — finding the system's limits by deliberately pushing past safe operating points. Answers "where does this break?" rather than "does this work?"; the cascade-finding cousin of load testing.
- [[configuration-test]] — a production test comparing checked-in configuration against live system state. Catches the drift class of incident: the config changed in the repo but never pushed, or vice versa.
- [[configuration-integration-testing]] — testing configuration files as potentially hostile input to the interpreters that read them. Surfaces the "this config loads fine but produces a bad runtime state" bug before production does.
- [[statistical-testing-techniques]] — the non-deterministic test family: fuzzing, chaos engineering, property-based testing. The methods for finding bugs the deterministic test suites were never going to surface.
- [[testing-at-scale]] — the operational surface of running large test fleets: the dependency-closure problem, the branch-point strategy, the test-infrastructure choices that turn test runs from hours into minutes.
- [[test-flakiness-budget]] — at massive test-suite scale, even a tiny per-test flakiness floor produces a near-certain build failure. The arithmetic argument for zero-tolerance flakiness policies on large test fleets.
- [[testing-deadlines]] — the user-facing dimension: interactive tests keep the author's attention (seconds-minutes); batch tests address reviewers and CI (minutes-hours); slow tests address nobody and produce little feedback. Designed-for-deadline.
- [[testing-entry-strategy]] — the adoption path when a team has inadequate testing: start with smoke tests, convert every new bug into a test, invest in CI reliability last. The high-impact-low-effort ordering.
- [[testing-scalable-tools]] — testing the SRE-developed tooling side specifically: metric collection, automation scripts, data-refactoring jobs. Tools that break silently are the ones that produce the largest postmortems.

Deeper reading: [[site-reliability-engineering#chapter-17-testing-for-reliability]] and [[site-reliability-engineering#chapter-26-data-integrity-what-you-read-is-what-you-wrote]].

## Data integrity — the reliability specialisation for data systems

Services with data (most of them) have a second reliability dimension beyond "is it serving?" — is the data correct, and can you recover what you had?

- [[data-integrity-sre]] — the SRE Ch 26 hub: data integrity is the reliability dimension where "available" isn't enough. A service that returns wrong data is often worse than a service that returns nothing.
- [[data-integrity-principles]] — the principles: strict change control, defense-in-depth, explicit detection-and-recovery, validated backups. The ideas under the patterns below.
- [[data-integrity-failure-modes]] — the taxonomy: bugs that corrupt data silently, operator error that deletes data, ransomware that encrypts it, physical disaster that destroys it. Different failure modes need different mitigations.
- [[data-availability-vs-integrity]] — the distinction: a broken replica that returns nothing is an availability problem; a broken replica that returns wrong data is an integrity problem. Different alerting, different playbooks.
- [[defense-in-depth-data]] — soft delete, tiered backups, validators, replication across media types. The reason any one failure mode doesn't cause permanent data loss. Shared with [[moc-security-and-privacy]] under the ransomware-backup lens.
- [[backups-vs-archives]] — backups for restore within SLO; archives for compliance and discovery. Different retention, different validation frequency, different access controls. Shared with [[moc-security-and-privacy]].
- [[tiered-backup-strategy]] — hot / warm / cold tiers with different restore SLOs. The architecture that makes backup both affordable and usable.
- [[data-validation-pipelines]] — periodic validators that check invariants the service depends on. Often the only way silent corruption gets detected.
- [[gmail-gtape-restore]] — the worked Google example: the 2011 Gmail restore from tape. The existence proof that tape backups matter even in the cloud era.
- [[data-observability]] — the data-engineering cousin of monitoring: "is the data healthy?" answered the same way "is the service healthy?" is — via signals, dashboards, alerts. See [[moc-data-engineering]] for the broader data-reliability undercurrent.
- [[robustness-vs-resilience]] — the distinction at the heart of reliability thinking: robustness handles *expected* variations; resilience adapts to *unforeseen* ones. Different investments produce each; a highly robust system can still be fragile, and vice versa.
- [[safety-integrity-level]] — the regulatory-safety vocabulary (SIL levels) borrowed from industrial-controls standards: a discrete scale for how reliable the software must be given the safety consequences of failure. The right frame for services where the question "how reliable?" has a legal answer.

Deeper reading: [[site-reliability-engineering#chapter-26-data-integrity-what-you-read-is-what-you-wrote]].

## DataOps — the pipeline-operations sister discipline

Data pipelines have operational characteristics distinct enough from services to warrant their own discipline. The techniques converge with SRE; the artifacts differ.

- [[dataops]] — Agile + DevOps + Statistical Process Control applied to data pipelines. Observability, test-first, continuous validation. The data-engineering-cultural undercurrent parallel to SRE for services.

[[moc-data-processing]] owns pipeline-execution mechanics; [[moc-data-engineering]] owns the discipline's full scope. This MOC cites DataOps as the bridge because pipeline reliability is often shared ownership.

## SRE as an organisation — the engagement model

How SRE teams are structured, relate to product teams, and sustain over time.

- [[sre-engagement-model]] — the SRE Ch 32 framing: how SRE commits to a service (PRR, ongoing support, handoff). Not every service is SRE-supported; criteria govern when the commitment is made.
- [[sre-alternative-support]] — models below full SRE support: consulting, guided on-call, observability-only. The realistic menu for the 95% of services that don't get a dedicated SRE team.
- [[sre-product-adoption]] — the path for a product team to become SRE-supported. PRR is the gate; the path leading up to it is the engagement.
- [[sre-team-composition]] — the mix inside an SRE team: systems engineers, software engineers, generalists. Balance sustains the team; imbalance causes drift (all-systems → ops-only; all-software → detachment from production).
- [[sre-onboarding]] — the new-member path: shadow, reverse-shadow, training. The investment that protects the team's on-call culture.
- [[sre-continuing-education]] — ongoing learning after onboarding. Postmortem reading groups, wheel-of-misfortune drills, internal tech talks.
- [[trial-by-fire-anti-pattern]] — the anti-pattern: new SREs are handed the pager and expected to learn on real incidents. Produces burnt-out engineers, poor handling of the incidents they were supposed to learn from, and silent attrition.
- [[cumulative-learning-paths]] — the alternative: a sequential onboarding curriculum that builds production competence before the pager lands. Investment in cumulative curricula pays off every time a new engineer finishes onboarding and is immediately useful on-call.
- [[documentation-as-apprenticeship]] — the onboarding practice of assigning documentation overhaul to new engineers as a first project. Forces deep engagement with the system, produces durable artifacts for the next hire, sidesteps the "give the newbie busy-work" trap.
- [[reverse-engineering-class]] — the SRE training flagship: figure out an unfamiliar production service without the owner's help, using logs, metrics, binaries, and code. The exercise that builds the baseline SRE attribute below.
- [[reverse-engineering-skills]] — the baseline attribute: understanding unfamiliar systems well enough to debug them, from whatever artifacts are available. The skill that separates an SRE from an operator following a runbook.
- [[targeted-project-work]] — the onboarding practice of giving new engineers real problems to own and solve (not simulations, not toy issues). The thing that turns fresh hires into effective team members faster than any classroom format.
- [[leading-questions]] — the embedded-SRE technique of guiding dev teams toward first-principles reasoning instead of prescribing answers. "What would you expect to see in the metrics if that hypothesis were true?" builds durable reasoning skill; a direct answer doesn't.
- [[explaining-reasoning]] — the embedded-SRE discipline of making *why* visible, not just *what*. Teams that see the reasoning trace can predict the follow-up recommendation and eventually internalise the framework.
- [[statistical-comparative-thinking]] — the SRE attribute of pruning decision trees via careful hypothesis construction and comparative reasoning rather than exhaustive search. The skill that makes troubleshooting under time pressure possible.
- [[structured-and-rational-decision-making]] — the data-driven discipline under the above: agreed basis for decision, clear inputs, explicit assumptions. The format that lets decisions be audited and improved rather than vibe-checked.
- [[sre-discipline]] — (cross-cited from top). The framing of what SRE *is* that the engagement model depends on.
- [[sre-on-call-engagement]] — the specifically-on-call part of the engagement model: shared rotation with dev, embedded-SRE rotation, or pure-SRE rotation.
- [[sre-dev-collaboration]] — the day-to-day working relationship. Joint roadmap planning, shared design reviews, shared incident response. The thing that prevents SRE-vs-dev becoming SRE-against-dev.
- [[sre-software-development-lessons]] — patterns from building SRE-built software (monitoring platforms, release tooling, incident-management tooling). The distinct constraints of software that other SREs operate.
- [[introducing-sre-software-development]] — the case for SRE teams shipping production-quality software, not just scripts. The argument that blurs SRE and traditional SWE.
- [[fostering-software-engineering-in-sre]] — the practices that keep SRE teams doing real engineering: protected project time, promotion paths for software work, rotation into pure-SWE roles.
- [[embedding-sre]] — SRE Ch 30: embedding an individual SRE in a product team to rescue an operationally overloaded service. The intervention pattern for services drowning in toil.
- [[operational-overload]] — the state embedding exists to rescue: a team unable to keep up with operations, falling further behind each week. The anti-pattern SRE is built to prevent.
- [[operational-underload]] — the opposite failure: a team with so little production load they lose operational muscle. Remedied with shared rotations, game-day drills, or merging with a busier team.
- [[frameworks-and-sre-platform]] — the platform-team shape: SRE infrastructure (monitoring, CI/CD, capacity) offered as a self-service platform rather than person-by-person support.
- [[cross-sre-collaboration]] — horizontal coordination across SRE teams: shared tooling, shared on-call across related services, community of practice.
- [[communication-and-collaboration-in-sre]] — SRE Ch 31 hub: how SRE teams communicate internally and externally. Rituals, documents, meetings that actually work.

Deeper reading: [[site-reliability-engineering#chapter-28-accelerating-sres-to-on-call-and-beyond]], [[site-reliability-engineering#chapter-29-dealing-with-interrupts]], [[site-reliability-engineering#chapter-30-embedding-an-sre-to-recover-from-operational-overload]], [[site-reliability-engineering#chapter-31-communication-and-collaboration-in-sre]], [[site-reliability-engineering#chapter-32-the-evolving-sre-engagement-model]], [[site-reliability-engineering#chapter-33-lessons-learned-from-other-industries]].

## Lessons from other industries

SRE is not the first discipline to grapple with running high-stakes systems reliably. The parallels are worth drawing explicitly.

- [[lessons-from-other-industries]] — SRE Ch 33 hub: aviation, nuclear, medicine. What the safety-critical industries do differently, what SRE borrows (blameless postmortem, checklist, simulation), what it doesn't.
- [[norad-tracks-santa]] — the one concrete Google-SRE case study of handling a production system with safety-critical framing: reliability theatre that doubles as real reliability practice.

Deeper reading: [[site-reliability-engineering#chapter-33-lessons-learned-from-other-industries]].

## Adoption paths

If you're adopting SRE practices rather than running an established one, three entry points dominate:

1. **Start with one SLO.** Pick the most user-facing service, define one SLI (availability or latency), set a deliberately loose SLO, watch the error budget for a quarter. The shift in conversation from "how do we make it more reliable?" to "how are we spending the budget?" is the whole point.
2. **Start with postmortems.** [[blameless-postmortem]] culture is the cheapest SRE practice to adopt and has the largest compounding effect. Pick a recent incident, write one, share it, read it at a team meeting.
3. **Start with one automation.** Pick the toil item that is most painful and most obvious. Automate it. Use the saved time to automate the next one. The practice of "we invest in automation" is a culture change as much as a technical one.

Do all three in parallel; none of them work in isolation. See [[question-patterns]]'s *Adopt SLOs and reliability practices for an existing system* archetype for the full composition of MOCs, concept pages, and raw chapters that ground a from-scratch adoption plan.

## Sibling MOCs

- [[moc-container-and-serving-patterns]] — owns the shape and mechanics of the service being operated. Read together with this MOC for any rollout, launch, or shape change.
- [[moc-distributed-systems]] — owns the mechanisms (consensus, replication, partial failure) whose operational story this MOC tells. [[consensus-monitoring]] and [[partial-failures]] appear in both MOCs under different lenses.
- [[moc-data-processing]] — owns data-pipeline execution and SRE Ch 25. [[dataops]] is the bridge to this MOC's service-operational discipline.
- [[moc-data-engineering]] — owns the discipline view including [[data-observability]] and the data-quality undercurrent; this MOC cites them under the service-operations lens.
- [[moc-security-and-privacy]] — owns security as undercurrent. [[security-monitoring]], [[backups-vs-archives]], and [[defense-in-depth-data]] appear in both with different framings — integrity / availability here; confidentiality / compliance there.
- [[moc-decomposition]] — owns the extraction playbook. A newly extracted service inherits an operational step-up that lives in this MOC.
- [[moc-microservices]] — owns the organisational frame around a services fleet. Platform-as-a-product frameworks plug into this MOC's [[frameworks-and-sre-platform]].
- [[moc-architecture-fundamentals]] — owns the -ilities catalogue (availability, reliability, fault-tolerance). This MOC owns the practice that keeps the -ilities real in production.

## Related pages

- [[index]]
- [[site-reliability-engineering]]
- [[sre-tenets]]
- [[sre-discipline]]
- [[error-budget]]
- [[service-level-indicator]]
- [[service-level-objective]]
- [[service-level-agreement]]
- [[slo-expectations]]
- [[risk-tolerance]]
- [[velocity-vs-reliability-tradeoff]]
- [[toil-and-engineering-balance]]
- [[automation-at-google]]
- [[monitoring-and-observability]]
- [[four-golden-signals]]
- [[black-box-vs-white-box-monitoring]]
- [[symptoms-vs-causes]]
- [[alert-philosophy]]
- [[distributed-tracing]]
- [[simplicity-sre]]
- [[release-engineering]]
- [[release-engineering-principles]]
- [[progressive-delivery]]
- [[canary-test]]
- [[deployment-vs-release]]
- [[reliable-product-launches]]
- [[production-readiness-review]]
- [[on-call-playbook]]
- [[balanced-on-call]]
- [[incident-response-mindset]]
- [[incident-management-framework]]
- [[incident-commander]]
- [[blameless-postmortem]]
- [[postmortem-philosophy]]
- [[outage-tracking]]
- [[cascading-failure]]
- [[handling-overload]]
- [[load-shedding]]
- [[retry-budget]]
- [[circuit-breaker]]
- [[bulkhead]]
- [[testing-for-reliability]]
- [[frontend-load-balancing]]
- [[datacenter-load-balancing]]
- [[capacity-planning]]
- [[service-discovery]]
- [[data-integrity-sre]]
- [[defense-in-depth-data]]
- [[backups-vs-archives]]
- [[sre-engagement-model]]
