# Reliability

**Summary**: Reliability means a system continues to perform its correct function, at the desired level of performance, even in the face of hardware faults, software bugs, and human error.

**Sources**: `raw/designing-data-intensive-applications/chapter-01-reliable-scalable-and-maintainable-applications.md`

**Last updated**: 2026-04-15

---

## What reliability means

A reliable system meets these expectations:

- The application performs the function users expect
- It tolerates user mistakes or unexpected usage
- Its performance is good enough for the required use case under expected load
- It prevents unauthorized access and abuse

## Fault vs failure — a critical distinction

A **fault** is one component of the system deviating from its spec. A **failure** is when the system as a whole stops providing the required service to the user. The goal of reliability engineering is to design **fault-tolerance mechanisms** — systems that prevent faults from cascading into failures.

It is impossible to reduce fault probability to zero; the practical goal is to stop faults from becoming failures.

## Types of faults

### Hardware faults

Hardware faults (disk crashes, RAM failures, power outages, network cable failures) are typically **random and uncorrelated** — one machine's disk failing does not imply another's will. The traditional response is redundancy: RAID, dual power supplies, hot-swappable components, backup generators.

Hard disks have a mean time to failure (MTTF) of 10–50 years. A 10,000-disk cluster should expect roughly one disk failure per day. (source: chapter-01)

As applications have moved to larger fleets and cloud platforms (where VM instances disappear without warning), **software fault-tolerance** has become necessary in addition to hardware redundancy. This also enables **rolling upgrades** — patching one node at a time without system-wide downtime.

### Software errors

Software faults are **systematic and correlated** — the same bug can affect every instance simultaneously, making them more dangerous than hardware faults. Examples:

- A bug triggered by a specific bad input that crashes all instances
- A runaway process consuming shared resources (CPU, memory, disk, network)
- A dependency that becomes unresponsive or returns corrupted data
- **Cascading failures**: a fault in one component triggers faults in others

Software bugs often lie dormant until an unusual combination of circumstances triggers them. Mitigations include: careful reasoning about assumptions, thorough testing, process isolation, crash-and-restart design, and continuous monitoring. Self-checking systems (e.g. verifying that incoming message count equals outgoing message count) can catch discrepancies early. (source: chapter-01)

### Human errors

Configuration errors by operators are the leading cause of outages in large internet services — more common than hardware faults, which account for only 10–25% of outages. (source: chapter-01)

Strategies for handling human error:

- Design APIs and admin interfaces that make the right action easy and the wrong action hard
- Provide non-production sandbox environments with real data, isolated from production
- Test thoroughly: unit, integration, and manual tests
- Enable fast rollback of configuration changes and gradual code rollout
- Set up detailed monitoring (telemetry) for early warning signals

## Fault injection and chaos engineering

Counterintuitively, deliberately inducing faults increases confidence in fault-tolerance. By randomly killing processes (as Netflix's **Chaos Monkey** does), teams ensure that fault-tolerance machinery is continually exercised. Many critical bugs are due to poor error handling that is never tested under normal conditions.

## Reliability vs prevention

For most fault types, tolerating faults is preferable to preventing them. Security is an exception: if an attacker has accessed sensitive data, that event cannot be undone — prevention is the only option.

## Related pages

- [[fault-tolerance]]
- [[scalability]]
- [[maintainability]]
