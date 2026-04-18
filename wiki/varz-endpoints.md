# Varz Endpoints

**Summary**: Google's standardised HTTP endpoint (`/varz`, pronounced "var-zee") that every server binary exposes for metrics scraping. Plain-text key/value pairs, one per line; `[[borgmon]]` fetches them on an interval. The interface Prometheus later adopted essentially unchanged.

**Sources**: `raw/site-reliability-engineering/chapter-10-practical-alerting-from-time-series-data.md`

**Last updated**: 2026-04-17

---

## The interface

Chapter 10 formalises varz as a mass-collection replacement for the older custom-scripts-and-SNMP approach (source: chapter-10-practical-alerting-from-time-series-data.md):

```
% curl http://webserver:80/varz
http_requests 37
errors_total 12
```

Space-separated keys and values, one per line. A later extension adds **mapped variables** for label-qualified metrics and histograms:

```
http_responses map:code 200:25 404:0 500:12
```

This exposes 25 HTTP 200 responses and 12 HTTP 500s in a single variable with a `code` label.

## Why a text format

The schemaless textual interface makes the barrier to adding new instrumentation very low: one declaration in the source where the metric is needed, and it appears on `/varz` automatically. That is a positive for both the software engineering and SRE teams — adding metrics is cheap.

The trade-off is change management: the varz interface declares no schema, so the decoupling of the variable definition from its use in `[[borgmon-rules]]` requires care. Google addresses this with tools that validate and generate rules, and with emergent per-library rule templates ("the rule library ends up declaring a schema even though the varz interface does not"). See [[borgmon-rules]] for the maintenance-configuration story.

## Automatic registration

Each of Google's major languages has an implementation of the exported-variable API that **automatically registers** with the HTTP server built into every Google binary by default. The API allows obvious operations — add an amount to a counter, set a key to a specific value, export a map. Go's `expvar` library and its JSON output is a public variant of the same API pattern.

Many non-Google systems already expose their internal state over their service protocol (OpenLDAP's `cn=Monitor`, MySQL's `SHOW VARIABLES`, Apache's `mod_status`). Varz standardises the shape across Google so a single Borgmon can scrape any server without per-protocol adapters.

## Counter vs gauge

The underlying variables are untyped strings, but the convention matters (source: chapter-10-practical-alerting-from-time-series-data.md):

- **Counter** — any nonmonotonically decreasing variable; only increases in value. Total kilometres driven, total requests served.
- **Gauge** — may take any value. Current fuel remaining, current speed.

Chapter 10 argues **counters are preferred** for scraped monitoring because they don't lose meaning when events occur between sampling intervals. A gauge read at 1-minute intervals misses everything that happened in between; a counter's delta across two samples captures all of it.

Most varz are counters in practice. Borgmon's `rate()` function handles the corner cases of counter resets (e.g. task restart).

## Contrast with SNMP

SNMP is designed to have minimal transport requirements and to continue working when most other network applications fail. Scraping over HTTP seems to be at odds with this design principle. Chapter 10's answer: in practice it's rarely an issue, because the system being monitored is *already* designed to be robust against network and machine failures, and Borgmon turns collection failure itself into an alertable signal (via synthetic variables — see [[borgmon]]).

## Cross-book connections

- [[unified-monitoring-interface]] (Burns) — the container-level adapter pattern for exposing a consistent metrics interface across heterogeneous apps. The Prometheus exporter sidecar around Redis is the modern, containerised version of what `/varz` hard-codes into every Google binary by construction.
- [[monitoring-and-observability]] (Newman) — varz is the "metrics" half of Newman's toolbox, standardised.
- [[adapter-pattern]] (Burns) — when an app can't be modified to expose the fleet standard, an adapter container translates; varz avoids the need by making the standard universal from the start.

## Related pages

- [[borgmon]]
- [[borgmon-rules]]
- [[time-series-arena]]
- [[black-box-vs-white-box-monitoring]]
- [[prometheus-connection]]
- [[unified-monitoring-interface]]
- [[site-reliability-engineering]]
