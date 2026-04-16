# Windowing

**Summary**: Windows define time-bounded subsets of an [[event-streams|event stream]] for aggregation and analysis. Choosing the right window type and correctly handling event time vs processing time are critical challenges in [[stream-processing]].

**Sources**: `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`

**Last updated**: 2026-04-15

---

## Event time vs processing time

A fundamental distinction in stream processing is between when an event **occurred** (event time, from the event's timestamp) and when it is **processed** (processing time, from the system clock of the processing machine) (source: chapter-11-stream-processing.md).

Many stream processing frameworks use processing time for windowing because it is simple. This works if the delay between creation and processing is negligible, but breaks down under significant lag (source: chapter-11-stream-processing.md).

### Why the distinction matters

Processing may be delayed for many reasons: queueing, network faults, contention in the broker or processor, consumer restarts, reprocessing past events after a bug fix. Message delays can also cause unpredictable ordering -- events may arrive at the processor in a different order than they occurred (source: chapter-11-stream-processing.md).

**The Star Wars analogy**: Episode IV was released in 1977 and Episode I in 1999. The episode number is the event timestamp; the release date is the processing time. Humans handle this discontinuity easily, but stream processing algorithms must be explicitly designed for it (source: chapter-11-stream-processing.md).

Confusing event time and processing time leads to bad data. If a stream processor is shut down and restarted, it processes a backlog of events quickly. Measuring rates by processing time would show a false spike during backlog processing, when the actual event rate was steady (source: chapter-11-stream-processing.md).

In [[batch-processing]], the same distinction exists but is less noticeable: batch processes always use event timestamps (there is no point looking at the system clock when processing a year of historical data in minutes) (source: chapter-11-stream-processing.md).

## When is a window complete?

When using event-time windows, you can never be certain you have received all events for a given window. Straggler events may arrive after the window has been declared complete due to buffering, network delays, or other causes (source: chapter-11-stream-processing.md).

Two approaches for handling stragglers:

1. **Ignore them** -- if they are a small percentage, drop them and track the drop rate as a metric. Alert if the drop rate becomes significant.
2. **Publish corrections** -- emit an updated window value that includes the stragglers, potentially retracting the previous output.

Some systems use special messages to indicate "no more messages with timestamp earlier than t," but this is complicated when multiple producers each have their own minimum timestamp thresholds (source: chapter-11-stream-processing.md).

## Whose clock?

Assigning timestamps is tricky when events are buffered at multiple points. Consider a mobile app that buffers events offline and sends them hours or days later. The device clock may be wrong (accidentally or deliberately), but the server clock, while more reliable, is less meaningful for describing the user interaction (source: chapter-11-stream-processing.md).

**Three-timestamp approach** to estimate true event time (source: chapter-11-stream-processing.md):

1. Time the event occurred (device clock)
2. Time the event was sent to the server (device clock)
3. Time the event was received by the server (server clock)

By subtracting (2) from (3), you estimate the device clock offset and apply it to (1). This assumes the offset didn't change between event occurrence and sending, and that network delay is small relative to required accuracy.

## Types of windows

| Window type | Fixed length? | Overlap? | Description |
|---|---|---|---|
| Tumbling | Yes | No | Fixed-size, non-overlapping. Every event belongs to exactly one window. Implemented by rounding timestamps down. |
| Hopping | Yes | Yes | Fixed-size, overlapping with a configurable hop size. E.g., 5-minute windows hopping every 1 minute. Implemented as tumbling windows aggregated over adjacent intervals. |
| Sliding | Yes (interval) | Yes | Contains all events within a time interval of each other. Unlike tumbling/hopping, does not use fixed boundaries. Implemented by keeping a time-sorted buffer and expiring old events. |
| Session | No | No | Groups events for the same user that occur closely together in time. Ends after a period of inactivity (e.g., 30 minutes with no events). Common for website analytics. |

(source: chapter-11-stream-processing.md)

### Examples

- **Tumbling**: 1-minute window groups events 10:03:00-10:03:59, then 10:04:00-10:04:59.
- **Hopping**: 5-minute window with 1-minute hop covers 10:03:00-10:07:59, then 10:04:00-10:08:59.
- **Sliding**: 5-minute sliding window puts events at 10:03:39 and 10:08:12 in the same window (less than 5 minutes apart), even though tumbling/hopping 5-minute windows would not.
- **Session**: All events from the same user within 30 minutes of each other. No fixed duration.

(source: chapter-11-stream-processing.md)

## Related pages

- [[stream-processing]]
- [[event-streams]]
- [[stream-joins]]
- [[stream-processing-fault-tolerance]]
- [[batch-processing]]
- [[response-time-percentiles]]
