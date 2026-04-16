# Stream Joins

**Summary**: Joins in [[stream-processing]] are more challenging than in [[batch-processing]] because new events can appear at any time. Three types exist: stream-stream (window joins), stream-table (enrichment), and table-table (materialized view maintenance).

**Sources**: `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`

**Last updated**: 2026-04-15

---

## Why stream joins are harder than batch joins

In [[batch-processing]], joins operate on bounded datasets with known contents (see [[sort-merge-joins]] and [[map-side-joins]]). In stream processing, new events can appear at any time, the dataset is unbounded, and sort-merge joins cannot be used because sorting requires reading the entire input. Stream processors must maintain state to perform joins (source: chapter-11-stream-processing.md).

## Stream-stream join (window join)

Both inputs are activity event streams. The join looks for related events that occur within some time [[windowing|window]] (source: chapter-11-stream-processing.md).

**Example**: Correlating search queries with clicks on search results to calculate click-through rates. Both events share a session ID, but the time between search and click varies from seconds to weeks. The click may even arrive before the search due to network delays (source: chapter-11-stream-processing.md).

**Implementation**: The stream processor maintains state -- all events in the join window, indexed by the join key (e.g., session ID). When a new event arrives, it checks the other index for a matching event. Unmatched events that expire from the window generate a "no match" output (useful for measuring search quality -- searches with no clicks) (source: chapter-11-stream-processing.md).

Note: embedding search details in the click event would only capture cases where the user *did* click, not cases where they abandoned the search. The join captures both (source: chapter-11-stream-processing.md).

## Stream-table join (stream enrichment)

One input is an activity event stream; the other is a database. The join enriches activity events with data from the database (source: chapter-11-stream-processing.md).

**Example**: Augmenting user activity events with profile information by looking up the user ID in a database.

**Implementation options** (source: chapter-11-stream-processing.md):

1. **Remote database query** -- simple but slow and risks overloading the database
2. **Local copy of the database** -- load a copy into the stream processor (in-memory hash table or local disk index), similar to [[map-side-joins|broadcast hash joins]] in batch processing

The key difference from batch processing: a batch job uses a point-in-time snapshot, but a stream processor runs indefinitely and the database changes over time. The local copy must be kept up to date. This can be solved by subscribing to a [[change-data-capture]] changelog of the database alongside the activity stream, making the stream-table join actually a join of two streams (source: chapter-11-stream-processing.md).

A stream-table join is very similar to a stream-stream join, except the table changelog uses a conceptually infinite window (reaching back to the "beginning of time"), with newer records overwriting older ones (source: chapter-11-stream-processing.md).

## Table-table join (materialized view maintenance)

Both inputs are database changelogs. Each change on one side is joined with the latest state from the other side. The result is a stream of changes to a materialized view (source: chapter-11-stream-processing.md).

**Example**: Twitter's home timeline cache. Maintaining this cache requires processing four event types:

- User sends a new tweet -- add it to every follower's timeline
- User deletes a tweet -- remove from all timelines
- User follows someone -- add recent tweets to their timeline
- User unfollows someone -- remove those tweets from their timeline

This is equivalent to materializing the following SQL join:

```sql
SELECT follows.follower_id AS timeline_id,
       array_agg(tweets.* ORDER BY tweets.timestamp DESC)
FROM tweets
JOIN follows ON follows.followee_id = tweets.sender_id
GROUP BY follows.follower_id
```

The stream of changes to the materialized view follows the product rule: any change to tweets is joined with current followers, and any change to followers is joined with current tweets (source: chapter-11-stream-processing.md).

## Time-dependence of joins

All three join types require the stream processor to maintain state from one input and query it when processing the other input. The order of state-maintaining events matters (following then unfollowing is different from the reverse) (source: chapter-11-stream-processing.md).

A fundamental question arises: if state changes over time, which version of the state do you join against? For example, if a user updates their profile, which activity events use the old profile vs the new profile? Tax rates change over time -- invoices should use the rate at the time of sale, not the current rate (source: chapter-11-stream-processing.md).

If event ordering across streams is nondeterministic, the join becomes nondeterministic: rerunning the same job on the same input may interleave events differently and produce different results. In data warehouses, this is called a **slowly changing dimension (SCD)**, addressed by giving each version of a record a unique identifier (e.g., each tax rate version gets its own ID, and invoices reference the specific version). This makes the join deterministic but prevents [[log-based-message-brokers|log compaction]] since all record versions must be retained (source: chapter-11-stream-processing.md).

## Related pages

- [[stream-processing]]
- [[windowing]]
- [[change-data-capture]]
- [[event-streams]]
- [[sort-merge-joins]]
- [[map-side-joins]]
- [[batch-processing]]
- [[log-based-message-brokers]]
- [[data-warehousing]]
