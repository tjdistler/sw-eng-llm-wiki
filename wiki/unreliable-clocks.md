# Unreliable Clocks

**Summary**: Each machine in a distributed system has its own clock, which may drift, jump, or disagree with other machines' clocks -- making it dangerous to rely on clocks for ordering events or coordinating actions across nodes.

**Sources**: `raw/designing-data-intensive-applications/chapter-08-the-trouble-with-distributed-systems.md`

**Last updated**: 2026-04-15

---

## Why clocks matter in distributed systems

Applications depend on clocks for two distinct purposes (source: designing-data-intensive-applications, chapter 8):

- **Measuring durations**: request timeouts, response times, queries per second, time spent on a page
- **Describing points in time**: publication timestamps, scheduled events, cache expiry, log timestamps

In a distributed system, communication is not instantaneous. Due to variable network delays, determining the order of events across machines is difficult. Each machine's clock is a physical hardware device (quartz crystal oscillator) that is not perfectly accurate, so machines have different notions of time. (source: designing-data-intensive-applications, chapter 8)

## Two kinds of clocks

### Time-of-day clocks

Return the current date and time according to a calendar (wall-clock time), typically as seconds or milliseconds since the Unix epoch. Examples: `clock_gettime(CLOCK_REALTIME)` on Linux, `System.currentTimeMillis()` in Java. (source: designing-data-intensive-applications, chapter 8)

- Usually synchronized with NTP, so timestamps from different machines (ideally) mean the same thing
- Can be **forcibly reset** by NTP, causing time to jump backward or forward
- Often ignore leap seconds
- Historically coarse-grained (e.g., 10ms steps on older Windows)
- **Unsuitable for measuring elapsed time** because of possible backward jumps

### Monotonic clocks

Suitable for measuring durations (time intervals). Examples: `clock_gettime(CLOCK_MONOTONIC)` on Linux, `System.nanoTime()` in Java. (source: designing-data-intensive-applications, chapter 8)

- Guaranteed to always move forward (never jump backward)
- Absolute value is meaningless (e.g., nanoseconds since boot) -- only differences are useful
- **Cannot be compared across machines** -- each machine's monotonic clock is independent
- NTP may adjust the rate (slewing) by up to 0.05% but will not cause jumps
- Usually microsecond or better resolution
- Good for measuring [[timeouts]] and elapsed time in distributed systems

## Clock synchronization problems

Time-of-day clocks are synchronized via NTP, but this is fragile (source: designing-data-intensive-applications, chapter 8):

- **Quartz drift**: Google assumes 200 ppm drift -- 6ms drift per 30-second sync interval, or 17 seconds drift per day
- **NTP refusal/reset**: if the local clock is too far off, NTP may refuse to sync or forcibly reset the clock, causing a visible jump
- **Firewall misconfiguration**: a node accidentally cut off from NTP servers may drift unnoticed for a long time
- **Network delay limits accuracy**: minimum ~35ms error over the internet; occasional spikes of ~1 second
- **Wrong NTP servers**: some servers are misconfigured, reporting wildly incorrect time
- **Leap seconds**: can crash systems that assume minutes are always 60 seconds. Mitigation: "smearing" the leap second over a day
- **VM clock virtualization**: VMs are paused while other VMs use the CPU, causing apparent clock jumps
- **Untrusted devices**: mobile or embedded devices may have deliberately wrong clocks

Very high accuracy (e.g., 100 microseconds for financial trading per MiFID II) is achievable with GPS receivers and the Precision Time Protocol (PTP), but requires significant investment. (source: designing-data-intensive-applications, chapter 8)

## The danger of silent incorrectness

Unlike a CPU defect or misconfigured network (which cause visible failures), an incorrect clock often goes unnoticed. Most things seem to work fine while the clock gradually drifts further from reality. The result is **silent, subtle data loss** rather than a dramatic crash. (source: designing-data-intensive-applications, chapter 8)

If software requires synchronized clocks, it is essential to monitor clock offsets between all machines and declare any node whose clock drifts too far as dead and remove it from the cluster. (source: designing-data-intensive-applications, chapter 8)

## Timestamps for ordering events: a dangerous temptation

Using time-of-day clocks to determine event order across nodes is tempting but broken. In [[multi-leader-replication]] with **last write wins (LWW)** conflict resolution, clock skew of even a few milliseconds can cause writes to be ordered incorrectly, silently dropping data. (source: designing-data-intensive-applications, chapter 8)

Problems with LWW and clocks:

- A node with a lagging clock cannot overwrite values from a node with a fast clock until the skew elapses -- causing silent data loss
- LWW cannot distinguish sequential writes from truly concurrent ones without additional causality tracking (e.g., [[version-vectors]])
- Two nodes can generate writes with the same timestamp, requiring arbitrary tiebreakers that may also violate causality

**Logical clocks** (incrementing counters) are a safer alternative for ordering events. They measure relative ordering rather than wall-clock time. (source: designing-data-intensive-applications, chapter 8)

## Clock confidence intervals

A clock reading is not a point in time but a **range** within a confidence interval. If the uncertainty is +/- 100ms, microsecond digits in the timestamp are meaningless. Most systems do not expose this uncertainty. (source: designing-data-intensive-applications, chapter 8)

**Google's TrueTime API** (used in Spanner) is an exception: it returns `[earliest, latest]` bounds. Spanner uses this for snapshot isolation across datacenters by deliberately waiting for the confidence interval to elapse before committing, ensuring transaction timestamps reflect causality. Google deploys GPS receivers or atomic clocks in each datacenter to keep uncertainty to ~7ms. (source: designing-data-intensive-applications, chapter 8)

## Related pages

- [[clock-synchronization]]
- [[partial-failures]]
- [[unreliable-networks]]
- [[timeouts]]
- [[process-pauses]]
- [[fencing-tokens]]
- [[multi-leader-replication]]
