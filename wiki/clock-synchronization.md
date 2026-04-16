# Clock Synchronization

**Summary**: The mechanisms and limitations of keeping clocks aligned across machines in a distributed system, primarily via NTP, and the specialized approaches (GPS, atomic clocks, TrueTime) used when high accuracy is required.

**Sources**: `raw/designing-data-intensive-applications/chapter-08-the-trouble-with-distributed-systems.md`

**Last updated**: 2026-04-15

---

## NTP (Network Time Protocol)

The most commonly used mechanism for clock synchronization. NTP adjusts a computer's clock according to the time reported by a group of servers, which in turn get their time from more accurate sources such as GPS receivers. (source: designing-data-intensive-applications, chapter 8)

### Limitations of NTP

- **Network delay bounds accuracy**: synchronization can only be as good as the network round-trip time. Over the internet, minimum error is ~35ms; spikes can reach ~1 second. Large delays can cause the NTP client to give up.
- **Clock resets**: if the local clock is too far off, NTP may forcibly reset it, causing time to jump. Applications observing time before and after the reset may see time go backward or leap forward.
- **Quartz drift between syncs**: Google assumes 200 ppm drift -- equivalent to 6ms per 30-second sync interval or 17 seconds per day.
- **Wrong servers**: some NTP servers are misconfigured. NTP clients query multiple servers and ignore outliers, but incorrect time from an NTP server can still cause problems.
- **Firewalling**: a node accidentally cut off from NTP servers may drift unnoticed for an extended period. (source: designing-data-intensive-applications, chapter 8)

### Monotonic clock slewing

NTP does not cause the monotonic clock to jump. Instead, it may adjust the rate at which the monotonic clock advances (**slewing**) by up to 0.05%, speeding up or slowing down the clock gradually. (source: designing-data-intensive-applications, chapter 8)

## High-accuracy approaches

When very precise synchronization is required (e.g., MiFID II regulation mandates 100-microsecond accuracy for high-frequency trading), specialized hardware is used (source: designing-data-intensive-applications, chapter 8):

- **GPS receivers** attached to servers
- **Atomic (caesium) clocks** with manufacturer-reported error bounds
- **Precision Time Protocol (PTP)**

These require significant effort, expertise, and investment.

## Google's TrueTime API

Used in Google's Spanner database. TrueTime does not return a single timestamp but a **confidence interval**: `[earliest, latest]`. The actual current time is guaranteed to be somewhere within that interval. The width depends on how long since the last sync with a more accurate source. (source: designing-data-intensive-applications, chapter 8)

Google deploys GPS receivers or atomic clocks in each datacenter, keeping uncertainty to about 7ms. Spanner uses this for distributed [[snapshot-isolation]]: it waits for the confidence interval to elapse before committing read-write transactions, ensuring that transaction timestamps reflect causality. (source: designing-data-intensive-applications, chapter 8)

## Monitoring

If software relies on synchronized clocks, clock offsets between all machines should be monitored. Any node whose clock drifts too far must be declared dead and removed from the cluster, before it causes silent data corruption. (source: designing-data-intensive-applications, chapter 8)

## Related pages

- [[unreliable-clocks]]
- [[partial-failures]]
- [[timeouts]]
