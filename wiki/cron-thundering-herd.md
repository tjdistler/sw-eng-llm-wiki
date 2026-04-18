# Cron Thundering Herd

**Summary**: Chapter 24's operational footnote on running cron at scale: humans configure "daily" jobs for **midnight**, "hourly" jobs for the top of the hour, and "every five minutes" jobs for times divisible by five — producing synchronised launch spikes that can overwhelm the datacenter even when each individual job is reasonable. Google's mitigation is an extension to the crontab syntax: the **`?` wildcard**, which lets the cron system hash the job's identity into a stable-but-distributed time within the allowed range, spreading synchronised launches out across the window.

**Sources**: `raw/site-reliability-engineering/chapter-24-distributed-periodic-scheduling-with-cron.md`

**Last updated**: 2026-04-17

---

## The thundering herd pattern in cron

A classic single-machine cron has on the order of tens of jobs; synchronised launches are a minor scheduling footnote. A datacenter-wide cron serving thousands of machines can easily host thousands of jobs. When people configure "daily at midnight" with crontab spec `0 0 * * *`, all those jobs launch at the same instant (source: chapter-24-distributed-periodic-scheduling-with-cron.md).

The aggregate effect:

- Each "daily" job that spawns a 1,000-worker [[mapreduce]] requests 1,000 [[borg|Borg]] tasks.
- Thirty teams with daily jobs → 30,000 tasks requested at the same moment.
- The datacenter scheduler, resource-allocation layer, network, and storage systems all see a coordinated demand spike.

This is the [[cascading-failure|thundering herd]] pattern applied to a scheduling workload: a synchronising event (the minute rollover at midnight) causes many independent clients to make requests at the same time.

## The `?` wildcard extension

Google's fix is a **new crontab wildcard character**: `?` (source: chapter-24-distributed-periodic-scheduling-with-cron.md).

In a standard crontab field, the user can specify a literal value (`0`), a range (`0-5`), a step (`*/5`), or `*` meaning "any value." The `?` extension adds a fifth option: **"any value is acceptable, and the cron system is free to choose."**

The system chooses deterministically by **hashing the cron job configuration** over the given range. Two consequences:

- The same job always gets the same chosen value (stable — the job doesn't drift around every time the user reloads their crontab).
- Different jobs hash to different values (distributing — the launches spread out evenly across the range).

A user who genuinely wants "some time today" writes:

```
0 ? * * *       # any hour of the day, evenly hash-distributed across jobs
```

Instead of:

```
0 0 * * *       # literally midnight; synchronises with every other midnight job
```

## Why hash-over-time works

Hashing the job identity (name, configuration, whatever identifies it) gives three useful properties:

1. **Stability** — the hash output is a pure function of the job definition, so the chosen launch time is the same every day. Job owners can predict when their job will run.
2. **Distribution** — hashes of unrelated jobs are effectively uniform, so the aggregate launch schedule across all `?`-using jobs is smooth.
3. **Self-adjusting** — when jobs are added or removed, the hash doesn't remap existing jobs (it's stateless), so the distribution remains even without operator intervention.

This is a generalisation of the same technique used anywhere you want stable, distribution-preserving assignment — [[consistent-hashing]] applies the same idea to partition assignment, [[deterministic-subsetting]] applies it to load-balancer pools.

## What `?` cannot fix

Chapter 24 is honest that the `?` extension mitigates the problem but does not eliminate it. The chapter's closing observation: "Despite this change, the load caused by the cron jobs is still very spiky" (source: chapter-24-distributed-periodic-scheduling-with-cron.md). Figure 24-3's global-cron-launch graph shows persistent spikes driven by jobs that legitimately need specific times — e.g., jobs tied to external events (a report due at 9am for a market opening, a billing run at end-of-month) where the time is part of the business requirement and cannot be distributed.

So `?` removes the preventable spikes caused by user habit (midnight as a default); it does not remove spikes driven by actual time-dependent business logic.

## Lessons for other distributed schedulers

The pattern generalises: any scheduler where users can specify "approximate" times should **offer the approximation as a first-class syntax** rather than forcing users to pick an exact time they don't actually care about. Without it, users pick round numbers, and round numbers synchronise.

Equivalents exist outside cron:

- **Kubernetes CronJob** with the `random-offset` annotation in some operators.
- **Airflow** with jittered schedule interval or `randomize_next_dag_run` hooks.
- **Queue-based scheduling** where the scheduler itself adds a random delay.

The cron `?` syntax has the nice property of being an explicit user choice — the user declares that they don't care exactly when, and the scheduler distributes. That is more honest than implicit jitter the user doesn't know about and can't reason about.

## Relationship to cascading failure

Chapter 24 doesn't use the term "cascading failure" in this section, but the thundering herd is one of the triggers Chapter 22 catalogues (see [[cascading-failure]] and [[cascading-failure-triggers]]). A synchronised launch spike can overflow the datacenter scheduler's queue, deny resources to other services, and indirectly cause timeouts in unrelated paths. The `?` extension is a narrow preventive measure for one specific common trigger of this class of failure.

## Relationship to general retry-amplification defences

The thundering herd from synchronised cron launches is structurally similar to the [[retry-amplification]] thundering herd — many clients making requests simultaneously because they are synchronised to an external event (cache expiry, service restart, minute rollover). The defences differ:

- **Retry amplification** is fixed by randomised exponential backoff on the retry loop.
- **Cron thundering herd** is fixed by distributing the initial launch time via hashing.

Both are instances of the same general principle: **break synchronisation that the underlying time-distribution of events didn't intend to create**.

## Related pages

- [[distributed-cron]]
- [[cascading-failure]]
- [[retry-amplification]]
- [[consistent-hashing]]
- [[deterministic-subsetting]]
- [[borg]]
