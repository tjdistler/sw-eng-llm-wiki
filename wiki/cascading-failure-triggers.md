# Cascading Failure Triggers

**Summary**: SRE Chapter 22's catalogue of conditions that, applied to a vulnerable system, initiate the domino effect. None of these are inherently catastrophic — a resilient system absorbs all of them — but on a system with the vulnerabilities from [[cascading-failure]]'s catalogue (unbounded queues, unbounded retries, hardcoded deadlines, capacity caches, intra-layer communication), they reliably start cascades. The five classes: process deaths, process updates, new rollouts, organic growth, and planned changes including drains and turndowns. The operational lesson: during a cascading failure, check recent changes first — many cascades correlate with a change in the last hour.

**Sources**: `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`

**Last updated**: 2026-04-17

---

## The framing

From Chapter 22 (source: chapter-22-addressing-cascading-failures.md):

> When a service is susceptible to cascading failures, there are several possible disturbances that can initiate the domino effect. This section identifies some of the factors that trigger cascading failures.

A cascade requires two ingredients: vulnerability (the design-level issues Chapter 22 catalogues) and a trigger (this page). Eliminating the vulnerabilities is the long-term defence; recognising the triggers is the incident-response hint.

## Process death

> Some server tasks may die, reducing the amount of available capacity. Tasks might die because of a Query of Death (an RPC whose contents trigger a failure in the process), cluster issues, assertion failures, or a number of other reasons. A very small event (e.g., a couple of crashes or tasks rescheduled to other machines) may cause a service on the brink of falling to break.

The size of the event is misleading. A healthy service comfortably handles many task deaths; a service on the edge of capacity cannot tolerate the temporary reduction. The Query of Death variant (a malformed input that triggers an assertion) is particularly dangerous because the *same* input will continue arriving until the client changes — so restarts don't fix the failure, they just reset the crash clock.

## Process updates

> Pushing a new version of the binary or updating its configuration may initiate a cascading failure if a large number of tasks are affected simultaneously. To prevent this scenario, either account for necessary capacity overhead when setting up the service's update infrastructure, or push off-peak. Dynamically adjusting the number of inflight task updates based on the volume of requests and available capacity may be a workable approach.

The mechanism: during an update, some fraction of tasks are between-versions and not serving traffic. The remaining tasks carry the load. If the update rate is too aggressive, the fleet goes below safe capacity momentarily. If a traffic spike coincides with the update, a cascade begins.

The mitigations:

- **Push off-peak.** Low traffic means more headroom during the update.
- **Dynamic throttling.** The update system watches traffic and available capacity and only pushes when there's margin.
- **Smaller batches.** The smaller the batch size, the smaller the instantaneous capacity reduction.

This connects to [[n-plus-2-redundancy]] — one of the "+2" slots is specifically to cover the task being updated.

## New rollouts

> A new binary, configuration changes, or a change to the underlying infrastructure stack can result in changes to request profiles, resource usage and limits, backends, or a number of other system components that can trigger a cascading failure. During a cascading failure, it's usually wise to check for recent changes and consider reverting them, particularly if those changes affected capacity or altered the request profile.

The diagnostic hint is the practical value of this trigger category: **during a cascading failure, check what changed in the last hour**. The chapter's [[change-management-sre|70%-of-outages-come-from-change]] finding combined with Chapter 22's "changes that improve steady state can worsen cascade risk" argument means: the most likely cause of the cascade is a recent change, and reverting it is often the fastest path to mitigation.

The chapter adds:

> Your service should implement some type of change logging, which can help quickly identify recent changes.

An [[outage-tracking|outage-tracking archive]] and rollout automation typically record enough to answer the "what changed" question fast.

## Organic growth

> In many cases, a cascading failure isn't triggered by a specific service change, but because a growth in usage wasn't accompanied by an adjustment to capacity.

The slow version of the overload scenario. No incident lights up, no alert predicts the crossover — user traffic crept past safe capacity over weeks or months, and a minor perturbation (a task restart, a small traffic spike) tips the system into cascade.

The defence is [[capacity-planning]] — and specifically, the discipline of testing to failure described in [[testing-for-cascading-failures]]. A service whose breaking point was measured three months ago and whose peak traffic has grown 40% since may be already past its safe limit and not know it.

## Planned changes, drains, or turndowns

> If your service is multihomed, some of your capacity may be unavailable because of maintenance or outages in a cluster. Similarly, one of the service's critical dependencies may be drained, resulting in a reduction in capacity for the upstream service due to drain dependencies, or an increase in latency due to having to send the requests to a more distant cluster.

The drain-amplification mechanism: draining cluster A shifts traffic to cluster B. If B is now too hot, some of its traffic goes to cluster C. Each cluster picks up more work than planned. If any cluster is near its limit, the drain tips it. The problem is worse when drains cascade — you drain A, B gets full, B gets drained preventively, C gets full, and so on.

### Request profile changes

The chapter includes a sub-case under "Planned Changes":

> A backend service may receive requests from different clusters because a frontend service shifted its traffic due to load balancing configuration changes, changes in the traffic mix, or cluster fullness.

The request mix itself can change without any explicit capacity reduction. Shifted traffic from a different frontend might have different request sizes, different cost profiles, or different keyspaces (hitting a cold cache). The effective capacity shifts even though the nominal capacity did not.

> Also, the average cost to handle an individual payload may have changed due to frontend code or configuration changes. Similarly, the data handled by the service may have changed organically due to increased or differing usage by existing users: for instance, both the number and size of images, per user, for a photo storage service tend to increase over time.

Organic data growth — users accumulate more data over time — changes per-request cost even when the request rate doesn't. A service sized for the traffic mix of six months ago may be undersized for today's mix without anything "changing."

### Resource limits

The chapter's warning on over-commitment:

> Some cluster operating systems allow resource overcommitment. CPU is a fungible resource; often, some machines have some amount of slack CPU available, which provides a bit of a safety net against CPU spikes. The availability of this slack CPU differs between cells, and also between machines within the cell. Depending upon this slack CPU as your safety net is dangerous. Its availability is entirely dependent on the behavior of the other jobs in the cluster, so it might suddenly drop out at any time.

The example: a team kicks off a MapReduce that consumes CPU broadly; aggregate slack drops; a service relying on slack for its safety margin tips into CPU starvation. The mitigation is tight — when load-testing, stay within committed resource limits, not within the generous-seeming slack envelope.

## Relationship to other wiki concepts

### Triggers and [[change-management-sre]]

The [[change-management-sre|70%-of-outages-come-from-change]] finding from Chapter 1 is the statistical backing for Chapter 22's "check recent changes first" directive. The three triggers classes that are explicitly change-driven — process updates, new rollouts, planned changes — are the ones most obviously in the 70%. Even the other two (process death and organic growth) often reduce to "change": a query of death is a recent frontend change; organic growth hit the crossover during a quiet drift with no code change.

### Triggers and [[capacity-planning]]

[[capacity-planning]] is the discipline that keeps the system out of the condition where any trigger can cascade. A service running at 40% of capacity absorbs every trigger on this list without noticing; a service running at 95% of capacity is triggered by all of them. The art is knowing which one you are.

### Triggers and [[testing-for-cascading-failures]]

Chapter 22's testing prescription covers several of these triggers explicitly. Production tests the chapter suggests include "reducing task counts quickly or slowly over time, beyond expected traffic patterns" and "rapidly losing a cluster's worth of capacity" — these are exactly the drain and process-death triggers simulated deliberately.

### Triggers and [[canary-test]]

[[canary-test]] is one of the mitigations for the *new rollouts* trigger: a gradual rollout with failure detection catches a bad binary before it reaches full production. A canary that's too small or too fast won't see cascade-inducing behaviour in time to prevent the full rollout from triggering one.

### Triggers and [[addressing-ongoing-cascading-failure]]

Chapter 22's [[addressing-ongoing-cascading-failure|immediate-steps]] list starts with "check what changed" because the trigger class often tells you the mitigation. A cascade triggered by a rollout: roll it back. A cascade triggered by a drain: stop the drain. A cascade triggered by organic growth: add capacity.

## Related pages

- [[cascading-failure]]
- [[change-management-sre]]
- [[capacity-planning]]
- [[testing-for-cascading-failures]]
- [[addressing-ongoing-cascading-failure]]
- [[canary-test]]
- [[n-plus-2-redundancy]]
- [[site-reliability-engineering]]
