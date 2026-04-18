# Monitoring Topology Sharding

**Summary**: How Google scales [[borgmon]] to global deployment: a hierarchy of Borgmon instances, where upper tiers pull aggregated time-series from lower tiers over a streaming protocol. Datacenter-level Borgmon scrape local servers; global-level Borgmon aggregate across datacenters; very large services shard the DC tier into scrapers + aggregators.

**Sources**: `raw/site-reliability-engineering/chapter-10-practical-alerting-from-time-series-data.md`

**Last updated**: 2026-04-17

---

## The scaling problem

Trying to collect from all tasks in a service globally from a single Borgmon quickly becomes a **scaling bottleneck** and a **single point of failure** (source: chapter-10-practical-alerting-from-time-series-data.md). RAM, CPU, and network all limit how many `/varz` endpoints one Borgmon can scrape.

Sharding the topology solves both: spread the work, and build the result from many loosely-coupled pieces.

## The hierarchy

The typical Google shape (source: chapter-10-practical-alerting-from-time-series-data.md):

- **One Borgmon per cluster** — scrapes local servers' `/varz`, stores in its [[time-series-arena]], evaluates its `[[borgmon-rules]]`.
- **A pair at the global level** — aggregates across datacenters. Pair (not single) because Google divides the production network into zones for maintenance; two global replicas provide diversity against the otherwise-SPOF.

For very large services, the datacenter tier splits further:

- **Scraper shards** — pure scraping, minimal rule evaluation, small arena. Exist because a single Borgmon's RAM or CPU is insufficient to hold the service's complete label-cross-product.
- **DC aggregation layer** — pulls pre-aggregated time-series from the scrapers; runs most of the rule evaluation.
- **Global tier may also split** — rule evaluation on one set of Borgmon, dashboarding on another.

## Borgmon-to-Borgmon streaming

Upper-tier Borgmon can **import time-series from lower-tier Borgmon** directly, using a streaming protocol (source: chapter-10-practical-alerting-from-time-series-data.md). This is distinct from scraping `/varz`:

- Streaming saves CPU and network compared to the text-based varz format.
- Upper tiers **filter** what they pull. A global Borgmon does not want every per-task time-series from every cluster — that defeats the purpose of aggregation. Instead it pulls already-aggregated series (e.g. `dc:http_requests:rate10m,zone=us-west`).

The aggregation hierarchy therefore builds **local caches of relevant time-series** at each level; drill-down from global to DC to task is possible but not constantly loaded.

## Pruning between tiers

The filter-on-import behaviour is load-bearing for cost: without it, a global Borgmon's arena would need to be as large as the sum of all DC arenas. With it, each tier holds only the aggregation level relevant to its alerting and dashboarding responsibilities. Lower tiers retain the granular series for incident drill-down; upper tiers keep only the summaries for global alerts.

## Why two global replicas, not more

Google's zone-based production change model means any single global Borgmon could be taken down for a planned maintenance window. Two replicas cover that. More than two doesn't add much — the replicas see the same lower-tier data, and [[alertmanager]] deduplicates overlapping alerts from them.

## Cross-book connections

- [[capacity-planning]] — the DC-tier-plus-global-tier pattern is an instance of the same hierarchical aggregation a capacity forecast uses: local detail at the leaves, summarised signals at the root.
- [[sharded-service-pattern]] (Burns) — the scraper tier is a sharded service: root-plus-shards where each shard owns a disjoint subset of the work. Burns's generic pattern is the architectural family monitoring topology belongs to.
- [[scatter-gather-pattern]] (Burns) — the upper-tier pull-from-lower-tiers is a scatter-gather read where results are aggregated rather than concatenated.
- [[prometheus-connection]] — Prometheus federation implements exactly this pattern: a higher-level Prometheus scrapes aggregated series from lower-level Prometheus instances.
- [[partitioning]] (Kleppmann) — the scraper-shard / DC-aggregator / global-aggregator split is time-series data partitioned first by locality then by aggregation level.

## Related pages

- [[borgmon]]
- [[time-series-arena]]
- [[borgmon-rules]]
- [[alertmanager]]
- [[prober]]
- [[prometheus-connection]]
- [[site-reliability-engineering]]
