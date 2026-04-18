# Time-Series Arena

**Summary**: [[borgmon]]'s in-memory store for scraped metrics. Fixed-size block of RAM with a garbage collector that expires the oldest entries when full; the interval between newest and oldest entries is the **horizon**. Sized for roughly 12 hours of data in datacenter and global Borgmon. Older data lives in an external TSDB.

**Sources**: `raw/site-reliability-engineering/chapter-10-practical-alerting-from-time-series-data.md`

**Last updated**: 2026-04-17

---

## Shape of the data

A service is typically many binaries running as many tasks, on many machines, in many clusters. Borgmon stores all that data in an in-memory database, regularly checkpointed to disk (source: chapter-10-practical-alerting-from-time-series-data.md).

Each data point has the form `(timestamp, value)`. Data points are stored in chronological lists called **time-series**, each named by a unique set of `key=value` **labels**. Conceptually:

- One time-series is a 1D array progressing through time.
- Add a label dimension and the data becomes a multi-dimensional matrix.

## Vectors

A query for a label pattern returns a **vector** — a slice through the arena at a single point in time (or a small window). For example, the labelset

```
{var=http_requests,job=webserver,service=web,zone=us-west}
```

might resolve to a five-row vector when there are five webserver instances in the cluster. Adding a duration converts the vector into a window of history:

```
{var=http_requests,job=webserver,service=web,zone=us-west}[10m]
```

The vector abstraction is what makes `[[borgmon-rules]]` expressive: rules operate on vectors, not on single scalars.

## Required labels

For a time-series to be identifiable in the TSDB, it must have at minimum:

- **var** — the variable name (the key on the `/varz` page)
- **job** — the type of server being monitored
- **service** — a loosely-defined collection of jobs providing one service
- **zone** — Google convention for the location (usually the datacenter) of the collecting Borgmon

The full labelset for a single series looks like:

```
{var=http_requests,job=webserver,instance=host0:80,service=web,zone=us-west}
```

The `instance` label above is added from the target's name. In general, labels can come from four sources:

1. The target's name (job, instance)
2. The target itself (map-valued varz)
3. The Borgmon configuration (zone annotations, relabeling)
4. Borgmon rules being evaluated

## The arena

In practice the arena is a **fixed-size block of memory** with a garbage collector that expires the oldest entries once full. Two related numbers matter (source: chapter-10-practical-alerting-from-time-series-data.md):

- **Horizon** — the interval between the newest and oldest entries currently in the arena. How much queryable data is kept in RAM.
- **Memory per data point** — about 24 bytes.

Typical sizing: datacenter and global Borgmon hold ~12 hours of data (a magic number that trades off enough information for debugging an incident against not costing too much RAM). At 1-minute resolution, 1 million unique time-series for 12 hours fits in under 17 GB of RAM.

The lowest-level scraper Borgmon hold much less time — their job is to collect and forward, not to serve long queries.

## The Time-Series Database

Periodically the in-memory state is archived to an external system: the **Time-Series Database** (TSDB). Borgmon can query TSDB for older data; TSDB is slower than RAM but cheaper and larger. The arena + TSDB split is the classic hot/cold tiering familiar from storage: fast recent data in RAM for dashboards and alerting, cold historical data on disk for capacity planning and postmortems.

## Cross-book connections

- [[borgmon]] — the consumer; the arena is one part of Borgmon's internals.
- [[capacity-planning]] — the TSDB historical trend data is the input to capacity forecasting.
- [[column-oriented-storage]] (Kleppmann) — time-series databases are a specialised cousin: sparse per-label columns optimised for range scans by time.
- [[sstables-and-lsm-trees]] (Kleppmann) — Prometheus's on-disk format uses similar chunked/sorted layouts; Google's TSDB internals aren't documented in the chapter but face the same write-heavy workload.
- [[prometheus-connection]] — Prometheus's in-memory `tsdb` plus on-disk blocks is the same hot/cold pattern.

## Related pages

- [[borgmon]]
- [[borgmon-rules]]
- [[varz-endpoints]]
- [[capacity-planning]]
- [[prometheus-connection]]
- [[site-reliability-engineering]]
