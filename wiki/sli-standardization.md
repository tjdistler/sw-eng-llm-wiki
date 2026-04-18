# SLI Standardization

**Summary**: Chapter 4's recommendation to agree on common definition templates for SLIs so they don't have to be reasoned from first principles for every service. Standard templates specify aggregation interval, region, measurement frequency, request filters, data source, and latency definition — so an individual SLI spec only names what differs from the default.

**Sources**: `raw/site-reliability-engineering/chapter-04-service-level-objectives.md`

**Last updated**: 2026-04-17

---

## Why standardize

Without standard templates every SLI spec must fully describe itself. Small wording differences between teams' SLIs produce incomparable metrics, and reviewers have to re-derive meaning every time. The chapter's guidance: **build a set of reusable SLI templates for each common metric** (source: chapter-04-service-level-objectives.md). Anything that conforms to the template can be omitted from the spec.

## The six dimensions to standardize

Chapter 4 lists the attributes of an SLI definition that are candidates for a standard template (source: chapter-04-service-level-objectives.md):

| Dimension | Example default |
|---|---|
| **Aggregation intervals** | "Averaged over 1 minute" |
| **Aggregation regions** | "All the tasks in a cluster" |
| **Measurement frequency** | "Every 10 seconds" |
| **Request filter** | "HTTP GETs from black-box monitoring jobs" |
| **Data source** | "Through our monitoring, measured at the server" |
| **Data-access latency definition** | "Time to last byte" |

Once these are standardised, an SLI spec collapses from a paragraph to a sentence:

> 99% (averaged over 1 minute) of Get RPC calls will complete in less than 100 ms (measured across all the backend servers).

becomes:

> 99% of Get RPC calls will complete in less than 100 ms.

(source: chapter-04-service-level-objectives.md)

## Where this fits

- [[sli-aggregation]] — standardization is what keeps the aggregation choices from being re-argued per service.
- [[service-level-indicator]] — the individual indicator; the template is the shape into which indicators are written.
- [[service-level-objective]] — the SLO inherits the SLI's definitions; SLO expressions shorten similarly.

## Related pages

- [[service-level-indicator]]
- [[sli-aggregation]]
- [[service-level-objective]]
- [[sre-monitoring-outputs]]
