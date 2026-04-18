# Change Management (SRE)

**Summary**: Roughly **70% of outages are due to changes in a live system**. SRE's change-management tenet is the automation trio that makes change safe: progressive rollouts, quick and accurate problem detection, and safe rollback.

**Sources**: `raw/site-reliability-engineering/chapter-01-introduction.md`, `raw/site-reliability-engineering/chapter-07-the-evolution-of-automation-at-google.md`, `raw/site-reliability-engineering/chapter-08-release-engineering.md`, `raw/site-reliability-engineering/chapter-12-effective-troubleshooting.md`, `raw/site-reliability-engineering/chapter-13-emergency-response.md`, `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`, `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`, `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`

**Last updated**: 2026-04-17

---

## The 70% finding

> SRE has found that roughly 70% of outages are due to changes in a live system. (source: chapter-01-introduction.md)

This number is the empirical backbone of SRE's change-management practice. If most outages come from change, the single biggest lever on reliability is making change safer — not gating it out of existence (the [[sysadmin-approach]] move), but wrapping it in mechanisms that limit blast radius when things go wrong.

## The automation trio

Best practices in this domain use automation to accomplish three things (source: chapter-01-introduction.md):

1. **Implementing progressive rollouts** — expose the change to a small fraction of traffic first, expand if healthy.
2. **Quickly and accurately detecting problems** — monitoring that fires fast and specifically when the rollout goes wrong.
3. **Rolling back changes safely when problems arise** — automated, low-risk reversal.

This trio minimises both the number of users and operations exposed to bad changes *and* the time they are exposed to them. It is the reliability-friendly answer to dev wanting velocity and ops wanting stability.

## Removing humans from the loop

The payoff of automation here is not speed but **consistency** (source: chapter-01-introduction.md):

> By removing humans from the loop, these practices avoid the normal problems of fatigue, familiarity/contempt, and inattention to highly repetitive tasks. As a result, both release velocity and safety increase.

Humans manually watching a rollout, clicking "proceed" every so often, are the thing that makes releases slow *and* risky. Remove them and both dimensions improve at once.

## Cross-book connections

This tenet has direct counterparts elsewhere in the wiki, framed from different angles:

- [[progressive-delivery]] — Newman and Burns cover the same recipe: canary, dark launch, parallel run, feature flags. SRE's framing is more compressed but identical in spirit.
- [[deployment-vs-release]] — the separation that makes progressive delivery possible.
- [[edm-deployment-patterns]] — Bellemare's deployment patterns for event-driven services lean on the same three ideas.
- [[blue-green-deployment]] — one concrete realisation of the rollback half of the trio.

## Applying the trio to automation itself (Chapter 7)

Chapter 7's [[automation-gone-wrong|Diskerase incident]] showed that the same discipline applies **one level up**: automation that drives changes is itself a changing system, and needs progressive rollout, detection, and rollback (source: chapter-07-the-evolution-of-automation-at-google.md). The Diskerase workflow failed because an empty-set sentinel meant "nothing to do" at the producer and "everything" at the consumer; the workflow then wiped every CDN machine in minutes.

The mitigations the chapter adopted after the incident map directly onto the trio:

- **Rate limiting** — the progressive-rollout analogue. Even a correct automation shouldn't be able to perform a destructive action across the whole fleet in one burst.
- **Auditing and RPC logging** — the detection analogue. Local Admin Daemons log the requestor, parameters, and results of every RPC for debugging and security.
- **Workflow-level idempotence** — the rollback / safe-restart analogue. Restarting a partially completed destructive workflow from scratch should be safe, not catastrophic.

Chapter 7 also reinforces a subtler rule: **automation must not rely on implicit safety signals**. The [[automation-gone-wrong|Bigtable disk-zero]] story illustrates the failure mode — a convention established by the humans who set up the cluster (disk 0 intentionally disabled for latency) was later reinterpreted by downstream automation as "no storage here, safe to wipe." The change-management discipline applied here is: express intent explicitly in configuration rather than through conventions, and require positive confirmation for destructive actions rather than inferring safety from an absence.

## The release-engineering discipline that implements the trio (Chapter 8)

Chapter 8 shows the full tool stack that actually realises progressive rollout + detection + safe rollback at Google scale. The [[release-engineering]] discipline is the home for this machinery (source: chapter-08-release-engineering.md):

- **Progressive rollouts** — [[sisyphus]] is the SRE-developed general-purpose rollout framework; it can fan out to all clusters at once, expand exponentially over hours, or interleave across geographic regions over several days. Deployment is **fit to the risk profile of the service**, not to a fixed template.
- **Fast detection** — canary deployments run system tests on the first few jobs before the rollout expands. The [[rapid-release-system|Rapid]] workflow logs every step and produces a change report for SRE triage.
- **Safe rollback** — [[midas-package-manager|MPM]]'s movable labels (dev / canary / production) make rollback a label move to the previous package rather than a rebuild. Reverting `production` to the last-known-good package is cheap and fast.

The upstream discipline that makes all of this possible:

- [[hermetic-builds]] — rollback is only safe if the "previous version" is still byte-identical to what was tested.
- [[release-branching-and-cherry-picking]] — the branch model keeps each release's content precisely known so that "roll back to the previous release" means something definite.
- [[release-policy-enforcement]] — gated operations on cherry picks, releases, and deploys keep the trio auditable.

Chapter 8's framing of this as an **engineering discipline** with its own job function is the thing Chapter 1 leaves implicit. The trio doesn't emerge from good intentions — it emerges from a team that owns the tools.

## "What touched it last" (Chapter 12)

Chapter 12's [[divide-and-conquer-debugging|diagnosis]] section gives the 70%-from-change finding an operational read: **recent changes to a system are the productive first place to look** when something breaks (source: chapter-12-effective-troubleshooting.md).

> Systems have inertia: we've found that a working computer system tends to remain in motion until acted upon by an external force, such as a configuration change or a shift in the type of load served. Recent changes to a system can be a productive place to start identifying what's going wrong.

For this heuristic to be fast rather than archaeological, the change-management infrastructure must produce a **queryable change timeline** at every layer of the stack — server binary versions, configuration pushes, OS package updates. Chapter 12's recommendation (source: chapter-12-effective-troubleshooting.md):

> Well-designed systems should have extensive production logging to track new version deployments and configuration changes at all layers of the stack, from the server binaries handling user traffic down to the packages installed on individual nodes in the cluster.

The chapter also recommends **annotating monitoring dashboards with deployment start/end markers** so that performance changes can be visually correlated with deploys. The [[rapid-release-system|Rapid]] workflow's change reports and [[midas-package-manager|MPM]]'s package-label history are the pieces of infrastructure that make this cheap at Google.

## When the canary is insufficient (Chapter 13)

Chapter 13's [[change-induced-emergency|second case study]] adds a specific failure mode of the progressive-rollout leg (source: chapter-13-emergency-response.md). A configuration change to Google's abuse-protection infrastructure had gone through an earlier thorough canary on a nominally similar feature — but the earlier canary did not exercise the **rare, specific configuration keyword** that, combined with the new feature, triggered a crash-loop bug. The change was not considered risky, so it followed a less stringent canary process. When it pushed globally, it used the untested keyword/feature combination and crash-looped essentially all external-facing Google services.

The sharpened rule: **canary coverage must match the combinatorial surface, not the apparent risk level**. A canary that exercises a feature on 1% of traffic but doesn't exercise the 0.01% of customer configurations that trip the failure mode is not a real canary for that failure mode. The same is true for infrastructure changes with rare-keyword interactions.

Chapter 13 also surfaces a defensive-in-depth pattern that paid off in the same incident: the affected system **rate-limited how quickly it provided full updates to new clients**. This internal rate limit throttled the crash-loop's propagation and kept jobs up long enough to service requests between crashes. The general principle — **rate limits on change distribution are a reliability asset, not only a capacity one** — applies to the change-distribution infrastructure itself, not just to client-facing APIs.

## Rollback must be rehearsed (Chapter 13)

Chapter 13's [[test-induced-emergency|first case study]] adds a second sharpening: the **safe-rollback** leg of the trio is only real if rollback has been tested. In the MySQL permissions-test incident, the rollback procedure had never been exercised in a test environment; when the test went wrong, rollback failed and the team had to construct an alternative recovery path from scratch (source: chapter-13-emergency-response.md).

The explicit follow-up rule from the chapter: **thoroughly test rollback procedures before large-scale tests**. By extension, this applies to any production release whose risk profile requires rollback to be a real option rather than a theoretical one.

## Canary as structured user acceptance (Chapter 17)

Chapter 17 develops the [[canary-test|canary test]] as the production-side complement to the automation trio. The chapter's sharpening: a canary **is not a test** — it is structured user acceptance against live production traffic, with an exponential rollout schedule (0.1% → 1% → 10% → 100% across four days in the rule-of-thumb) that is mathematically designed to surface the order of a fault with minimum user impact (source: chapter-17-testing-for-reliability.md).

Fault order matters because it determines whether [[regression-tests|regression tests]] can capture the bug:

- Order 1 (linear in traffic): convert logs of unusual responses into regression tests.
- Order 2+ (cross-request interactions): regression tests can't reproduce; canary is the only mechanism that catches them reliably.

Chapter 17's framing reinforces Chapter 13's canary-coverage-must-match-combinatorial-surface lesson by giving it a quantitative foundation.

## Changes as cascade triggers (Chapter 22)

Chapter 22's [[cascading-failure-triggers|triggering conditions]] section explicitly names change as one of the major cascade-trigger categories, alongside process death, organic growth, and planned drains (source: chapter-22-addressing-cascading-failures.md):

> A new binary, configuration changes, or a change to the underlying infrastructure stack can result in changes to request profiles, resource usage and limits, backends, or a number of other system components that can trigger a cascading failure. During a cascading failure, it's usually wise to check for recent changes and consider reverting them, particularly if those changes affected capacity or altered the request profile.

This is the 70%-of-outages finding applied at the incident-response level: when a cascade starts, the highest-prior guess for the trigger is a recent change. Chapter 22 recommends that every service implement some form of change logging for exactly this diagnostic reason. [[outalator]] and [[sisyphus]] already provide this record at Google; open-source equivalents are audit logs and deployment-tracking dashboards.

Chapter 22 also adds a subtler warning about *what counts as a change*: changes that improve steady-state reliability can *worsen* cascade risk. Adding retries reduces transient error rates and increases retry-amplification risk. Adding caches improves latency and creates a [[slow-startup-and-cold-caching|cold-cache]] hard dependency. Automatic failover reduces MTTR and can death-loop under load. The trio (progressive rollout + fast detection + safe rollback) is the right mechanism for **any** change, but evaluating the change must also include its cascading-failure behaviour, which is specifically what [[testing-for-cascading-failures|testing to failure and beyond]] measures.

## Connection to the error budget

Progressive rollouts and 1% experiments are explicitly framed in Chapter 1 as ways to **free up [[error-budget]]**: if you can roll out without consuming much budget, you can launch more often without violating the [[service-level-objective|SLO]]. This is the positive feedback loop between change management and velocity that makes the whole SRE model hang together.

## Launches as a specialised form of change (Chapter 27)

Chapter 27 specialises the change-management discipline for **product launches**: any new code introducing an externally visible change (source: chapter-27-reliable-product-launches-at-scale.md). Google does up to 70 launches per week, which makes a codified launch process worth building — and a dedicated [[launch-coordination-engineering|Launch Coordination Engineering]] team worth staffing.

The chapter's techniques map onto the automation trio:

- **Progressive rollouts** — [[gradual-rollout]] is Chapter 27's name for the same discipline: canary first, datacenter expansion, global rollout, each with verification. Client-side rollouts (Android app fractions) and invite systems are further realisations.
- **Fast detection** — the [[launch-checklist]] captures known detection gaps as pre-launch requirements; [[overload-behavior-launches]] makes load tests mandatory because overload nonlinearity can't be predicted from first principles.
- **Safe rollback** — [[feature-flag-framework|feature flag frameworks]] give independent revert per feature without binary rollback; server-controlled client configuration and the [[abusive-client-behavior|dormant-functionality pattern]] are the client-fleet versions.

Chapter 27 also adds specific discipline to the change-management trio for launch conditions that don't normally arise in steady-state releases: launch spikes up to 15x estimates, publicity-driven ramps, hard external deadlines, and novel product verticals that may require re-synthesising the checklist from first principles.

## Related pages

- [[sre-tenets]]
- [[error-budget]]
- [[progressive-delivery]]
- [[deployment-vs-release]]
- [[blue-green-deployment]]
- [[edm-deployment-patterns]]
- [[provisioning]]
- [[automation-at-google]]
- [[automation-gone-wrong]]
- [[idempotence]]
- [[release-engineering]]
- [[rapid-release-system]]
- [[sisyphus]]
- [[midas-package-manager]]
- [[push-on-green]]
- [[divide-and-conquer-debugging]]
- [[troubleshooting-model]]
- [[change-induced-emergency]]
- [[test-induced-emergency]]
- [[process-induced-emergency]]
- [[rate-limiting]]
- [[canary-test]]
- [[testing-for-reliability]]
- [[cascading-failure]]
- [[cascading-failure-triggers]]
- [[testing-for-cascading-failures]]
- [[reliable-product-launches]]
- [[launch-coordination-engineering]]
- [[launch-checklist]]
- [[gradual-rollout]]
- [[feature-flag-framework]]
