# Addressing an Ongoing Cascading Failure

**Summary**: SRE Chapter 22's operational playbook for the incident in progress. A cascading failure warrants the incident-management protocol, and the chapter lists eight strategies for recovery: **increase resources**, **stop health-check failures / deaths**, **restart servers**, **drop traffic**, **enter degraded modes**, **eliminate batch load**, **eliminate bad traffic**, and standard incident-response escalation. The recurring theme: **address the triggering condition before dropping load**, because otherwise the cascade will restart the moment traffic returns. The dramatic move — dropping traffic to 1% of normal — is often necessary because a crash-looping service can't recover without a fraction of its fleet becoming simultaneously healthy.

**Sources**: `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`

**Last updated**: 2026-04-17

---

## The opening framing

From Chapter 22 (source: chapter-22-addressing-cascading-failures.md):

> Once you have identified that your service is experiencing a cascading failure, you can use a few different strategies to remedy the situation — and of course, a cascading failure is a good opportunity to use your incident management protocol (Chapter 14).

The chapter orders the strategies from "try first, if applicable" to "big hammer." No single strategy works for every cascade; the choice depends on the trigger.

## 1. Increase resources

> If your system is running at degraded capacity and you have idle resources, adding tasks can be the most expedient way to recover from the outage. However, if the service has entered a death spiral of some sort, adding more resources may not be sufficient to recover.

The simplest case: the cascade was triggered by insufficient capacity for the current load. Adding tasks increases the fleet's capacity and breaks the failure feedback loop. This only works if:

- You have idle resources available to add (not always the case during a cluster-wide or region-wide event).
- The fresh tasks can become healthy quickly (see [[slow-startup-and-cold-caching]] — this often fails exactly because restart-under-load is the canonical cold-start problem).
- The service isn't in a death spiral that would just swallow the new capacity.

## 2. Stop health check failures and deaths

> Some cluster scheduling systems, such as Borg, check the health of tasks in a job and restart tasks that are unhealthy. This practice may create a failure mode in which health-checking itself makes the service unhealthy. For example, if half the tasks aren't able to accomplish any work because they're starting up and the other half will soon be killed because they're overloaded and failing health checks, temporarily disabling health checks may permit the system to stabilize until all the tasks are running.

The chapter's useful distinction:

> Process health checking ("is this binary responding at all?") and service health checking ("is this binary able to respond to this class of requests right now?") are two conceptually distinct operations. Process health checking is relevant to the cluster scheduler, whereas service health checking is relevant to the load balancer. Clearly distinguishing between the two types of health checks can help avoid this scenario.

A cascading failure can be sustained by the orchestrator's health check alone — tasks get killed for being overloaded, restart, come up cold, get overloaded, get killed. Breaking this loop by temporarily disabling or loosening the health check lets tasks finish starting before being killed off.

## 3. Restart servers

> If servers are somehow wedged and not making progress, restarting them may help. Try restarting servers when:
>
> - Java servers are in a [[gc-death-spiral|GC death spiral]]
> - Some in-flight requests have no deadlines but are consuming resources, leading them to block threads, for example
> - The servers are deadlocked

The crucial caveat:

> Make sure that you identify the source of the cascading failure before you restart your servers. Make sure that taking this action won't simply shift around load. Canary this change, and make it slowly. Your actions may amplify an existing cascading failure if the outage is actually due to an issue like a cold cache.

Restart is the right response when the cause is in-task state (wedged threads, heap fragmentation, deadlock). Restart is the wrong response when the cause is load (fresh tasks face the same load with lower capacity). Distinguishing which is which before pressing the button matters.

## 4. Drop traffic

The big hammer (source: chapter-22-addressing-cascading-failures.md):

> Dropping load is a big hammer, usually reserved for situations in which you have a true cascading failure on your hands and you cannot fix it by other means. For example, if heavy load causes most servers to crash as soon as they become healthy, you can get the service up and running again by:
>
> 1. Addressing the initial triggering condition (by adding capacity, for example).
> 2. Reducing load enough so that the crashing stops. Consider being aggressive here — if the entire service is crash-looping, only allow, say, 1% of the traffic through.
> 3. Allowing the majority of the servers to become healthy.
> 4. Gradually ramping up the load. This strategy allows caches to warm up, connections to be established, etc., before load returns to normal levels.

The four-step recipe is worth committing to memory: **fix → drop → stabilise → ramp**. Skipping step 1 means the cascade restarts as soon as step 4 completes. Skipping step 4 often triggers the same cascade all over again because warm-up didn't happen.

The chapter reinforces the step-1 warning:

> It is important to keep in mind that this strategy enables you to recover from a cascading outage once the underlying problem is fixed. If the issue that started the cascading failure is not fixed (e.g., insufficient global capacity), then the cascading failure may trigger shortly after all traffic returns. Therefore, before using this strategy, consider fixing (or at least papering over) the root cause or triggering condition.

Drop traffic to recover; don't drop traffic to "just see if it helps."

## 5. Enter degraded modes

> Serve degraded results by doing less work or dropping unimportant traffic. This strategy must be engineered into your service, and can be implemented only if you know which traffic can be degraded and you have the ability to differentiate between the various payloads.

This is [[graceful-degradation]] turned on manually. The chapter's warning is that this only works if it was designed in ahead of time — turning on degradation during an incident requires that the code paths already exist and are tested. See Chapter 22's warnings about rarely-used code paths: "the code path you never use is the code path that (often) doesn't work."

## 6. Eliminate batch load

> Some services have load that is important, but not critical. Consider turning off those sources of load. For example, if index updates, data copies, or statistics gathering consume resources of the serving path, consider turning off those sources of load during an outage.

A common realisation during incidents: a substantial fraction of the load comes from non-user-facing work. Batch index rebuilds, analytics pipelines, backup jobs, periodic maintenance. Pausing these frees capacity for user traffic immediately, without reducing what users see.

## 7. Eliminate bad traffic

> If some queries are creating heavy load or crashes (e.g., queries of death), consider blocking them or eliminating them via other means.

The canonical case: a malformed request pattern that consumes disproportionate resources, or a buggy client that hammers a hot endpoint. Blocking the offender at an upstream layer (reverse proxy, rate limiter, WAF) drops the attack traffic without affecting legitimate users.

## 8. Incident management

The chapter opens and closes this section with explicit reference to the Chapter 14 [[incident-management-framework]]. Cascading failures are characteristically high-cognitive-load events where the right move is often counterintuitive (drop traffic to 1%, disable health checks, restart a fleet). The framework's [[recursive-separation-of-responsibilities|role separation]] and [[live-incident-state-document|state document]] are how the team stays coordinated while individual responders work sub-problems.

## The Shakespeare narrative

Chapter 22 closes the section with a specific worked scenario (source: chapter-22-addressing-cascading-failures.md):

> A documentary about Shakespeare's works airs in Japan, and explicitly points to our Shakespeare service as an excellent place to conduct further research. Following the broadcast, traffic to our Asian datacenter surges beyond the service's capacity.

The response:

- Pre-existing safeguards help: [[graceful-degradation]] strips pictures and maps, non-critical RPCs are not retried, other RPCs use exponential backoff.
- But tasks still fail and Borg restart-loops them, driving healthy-task count down further.
- SREs respond with strategy #1: add tasks manually.
- The Asian cluster stabilises.
- Post-incident: configure [[gslb|GSLB]] to redirect traffic to neighbouring datacenters under such surges; enable autoscaling so the number of tasks automatically tracks demand.

The narrative shows the eight strategies in sequence: pre-existing defences buy time, operators apply strategy #1 manually, the postmortem turns the manual response into automation for next time.

## The meta-rule

The chapter's closing operational principle (source: chapter-22-addressing-cascading-failures.md):

> It is important to keep in mind that this strategy enables you to recover from a cascading outage once the underlying problem is fixed. If the issue that started the cascading failure is not fixed (e.g., insufficient global capacity), then the cascading failure may trigger shortly after all traffic returns.

**Fix the trigger before dropping the load.** This is the one sentence to take away. A cascade resumes the moment the trigger reasserts itself unless the trigger is neutralised first.

## Relationship to existing wiki concepts

### Addressing cascade and [[incident-management-framework]]

Chapter 22 explicitly calls the Chapter 14 incident management protocol into the cascade response. The strategies on this page are *what to do*; the framework is *how the team coordinates while doing it*. Cascading failures are exactly the incident class the framework is built for — complex, time-pressured, and requiring multi-person coordination with counterintuitive decisions.

### Addressing cascade and [[emergency-response]]

Chapter 1's [[emergency-response]] tenet sets the reliability-as-MTTR framing: faster recovery from incidents beats preventing them entirely. Chapter 22's eight strategies are the MTTR-reducing moves specifically for cascading failures.

### Addressing cascade and [[learning-from-outages]]

Chapter 13's directive to "keep a history of outages" is how the lessons from each cascade become organisation-wide knowledge. The Shakespeare post-incident (configure GSLB for surge redirect, enable autoscaling) is the kind of follow-up action that turns the incident into a system improvement.

### Addressing cascade and [[slow-startup-and-cold-caching]]

The specific caveat about restart-amplifying-cold-cache connects this page to [[slow-startup-and-cold-caching]]. Restart as a remedy only works when the cause is in-task state; when the cause is load, restart is an amplifier.

### Addressing cascade and [[graceful-degradation]]

Strategy #5 is [[graceful-degradation]] invoked operationally. The chapter's reminder that rarely-used code paths often don't work is a nudge to routinely exercise the degraded path — via canary, via load test, via production traffic splitting — so it is known to work when the incident starts.

### Addressing cascade and [[change-induced-emergency]]

The Chapter 13 [[change-induced-emergency]] case study demonstrates strategy #1 in practice (rollback the bad push is really a variant of "reduce load"). The general rule that recent changes are the most likely cause applies here — recent changes that triggered the cascade are recent changes that can be rolled back.

### Addressing cascade and [[statistical-testing-techniques]]

Chaos engineering's drill-for-the-response value is precisely about not doing these strategies for the first time during an incident. A team that has dropped traffic in a chaos exercise knows what the dashboards look like, knows the commands to run, and trusts the defences to work as traffic ramps back up.

## Related pages

- [[cascading-failure]]
- [[cascading-failure-triggers]]
- [[server-overload]]
- [[gc-death-spiral]]
- [[slow-startup-and-cold-caching]]
- [[graceful-degradation]]
- [[load-shedding]]
- [[incident-management-framework]]
- [[emergency-response]]
- [[learning-from-outages]]
- [[change-induced-emergency]]
- [[statistical-testing-techniques]]
- [[gslb]]
- [[site-reliability-engineering]]
