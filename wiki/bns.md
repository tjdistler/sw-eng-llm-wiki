# Borg Naming Service (BNS)

**Summary**: Google's [[service-discovery]] layer for tasks managed by [[borg]]. BNS maps stable symbolic names like `/bns/<cluster>/<user>/<job>/<task>` to `<IP address>:<port>`, so clients never need to know where a task currently runs.

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`

**Last updated**: 2026-04-17

---

## Why BNS exists

Under [[borg]], tasks are fluidly allocated across machines — a failing task is restarted somewhere else, possibly on a different rack. The raw `IP:port` of a task is unstable by design. BNS adds one level of indirection so that clients can address a task by a logical name that outlives any particular placement (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md).

## Path format and resolution

BNS paths look like `/bns/<cluster>/<user>/<job name>/<task number>`, which resolves to `<IP address>:<port>` (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md). Each task is assigned a name and index number by Borg at job-start time; other processes connect via the BNS name.

## Storage in Chubby

The BNS name-to-address mapping is data that must be consistent across the cluster, and so is stored in [[chubby]], Google's [[consensus]]-backed lock/coordination service (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md). This is the same structural pattern as using [[zookeeper]] or etcd as the authoritative source of partition-to-node mappings elsewhere in the wiki (see [[request-routing]]).

## Relationship to GSLB

[[gslb|GSLB]] — the Global Software Load Balancer — uses BNS addresses as its inputs. Service owners register a symbolic name, a list of BNS addresses, and per-location capacity; GSLB then directs traffic across those BNS addresses (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md). So BNS is the within-cluster naming layer, and GSLB is the cross-cluster load-balancing layer stacked on top of it.

## Related pages

- [[borg]]
- [[chubby]]
- [[gslb]]
- [[service-discovery]]
- [[zookeeper]]
- [[request-routing]]
