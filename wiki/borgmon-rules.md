# Borgmon Rules

**Summary**: Borgmon's **rule language** — simple algebraic expressions that compute new time-series from existing ones. Rules do aggregation, rate calculation, filtering, and thresholding; centralising them (vs per-target scripts) is what makes mass monitoring cheap and consistent.

**Sources**: `raw/site-reliability-engineering/chapter-10-practical-alerting-from-time-series-data.md`

**Last updated**: 2026-04-17

---

## What rules do

Chapter 10 frames Borgmon tersely (source: chapter-10-practical-alerting-from-time-series-data.md):

> Borgmon is really just a programmable calculator, with some syntactic sugar that enables it to generate alerts. The data collection and storage components already described are just necessary evils to make that programmable calculator ultimately fit for purpose here as a monitoring system.

Rules are algebraic expressions over time-series. Each rule reads one or more vectors from the arena (see [[time-series-arena]]) and writes a new named time-series back. The new series is indistinguishable from a scraped one and can feed further rules, dashboards, or alerts.

The rule engine can query along two axes:

- **Time axis** — the history of a single time-series (e.g. `[10m]` for the last 10 minutes)
- **Space axis** — a subset of labels across many time-series at once

Rules run in a parallel threadpool where possible but respect ordering when one rule depends on another's output.

## Centralisation vs per-target scripts

The pre-Borgmon world was custom scripts that checked responses and alerted, one script per target. Centralising rule evaluation in the monitoring system rather than per-forked-subprocess has three payoffs (source: chapter-10-practical-alerting-from-time-series-data.md):

- Computations run in parallel against many similar targets.
- Configuration shrinks because duplication is removed.
- Configuration gains expressiveness — rules can see the whole fleet, not just one target.

Centralisation is also what makes *the history* of collected data available for alert computation. A per-target script has no memory; a Borgmon rule can operate over a time window.

## Counters vs gauges

Borgmon rules almost always build on **counters** rather than gauges (source: chapter-10-practical-alerting-from-time-series-data.md; see also [[varz-endpoints]]):

- **Counter** — nonmonotonically decreasing; only grows. Total requests, total bytes written.
- **Gauge** — may take any value. Current memory used, current queue depth.

Counters are preferred because they don't lose meaning between sampling intervals. The `rate()` function converts a counter vector to a rate vector and handles corner cases like counter resets from task restart.

## Aggregation is the cornerstone

In a distributed environment, **aggregation** is the core operation (source: chapter-10-practical-alerting-from-time-series-data.md):

> Aggregation entails taking the sum of a set of time-series from the tasks in a job in order to treat the job as a whole.

Crucially, the chapter specifies *sum of rates* rather than *rate of sums*. Computing the sum of rates defends the result against counter resets or missing data (e.g. a task restart or a failed scrape). Rate-then-sum is robust; sum-then-rate is not.

## The naming convention

Rule-produced variables follow a colon-separated triplet:

`<aggregation_level>:<variable_name>:<operation>`

For example:

- `task:http_requests:rate10m` — task-level, variable `http_requests`, operation `rate10m`
- `dc:http_requests:rate10m` — datacenter-level, same variable, same operation
- `dc:http_errors:ratio_rate10m` — datacenter HTTP errors, 10-minute ratio of rates

The convention makes rules self-documenting: `dc:http_errors:ratio_rate10m` reads as "datacenter HTTP errors 10-minute ratio of rates."

## Worked example: error-ratio computation

The Chapter 10 worked example computes the fraction of requests that return non-200 codes and then alerts on it. The rules cascade:

```
# Per-task rate of requests over the last 10 minutes
{var=task:http_requests:rate10m,job=webserver} =
    rate({var=http_requests,job=webserver}[10m]);

# Cluster-wide rate (sum across instances; the `without instance`
# clause drops the instance label so rows can be summed)
{var=dc:http_requests:rate10m,job=webserver} =
    sum without instance({var=task:http_requests:rate10m,job=webserver})

# Per-task response rate broken down by `code` label
{var=task:http_responses:rate10m,job=webserver} =
    rate by code({var=http_responses,job=webserver}[10m]);

# Cluster-wide response rate, still broken down by code
{var=dc:http_responses:rate10m,job=webserver} =
    sum without instance({var=task:http_responses:rate10m,job=webserver});

# Cluster-wide error rate: drop the code label from all rows
# where code is not 200, then sum
{var=dc:http_errors:rate10m,job=webserver} = sum without code(
    {var=dc:http_responses:rate10m,job=webserver,code=!/200/});

# Error ratio: errors divided by requests
{var=dc:http_errors:ratio_rate10m,job=webserver} =
    {var=dc:http_errors:rate10m,job=webserver}
    /
    {var=dc:http_requests:rate10m,job=webserver};
```

Each rule's output is a new time-series appended to the arena. Intermediate series can be inspected on dashboards or queried ad hoc. If an ad hoc query proves useful, it can be promoted to a permanent rule.

## Alerting rules

An alerting rule produces a boolean time-series. When true for at least some minimum duration, it triggers an `Alert` RPC (typically to [[alertmanager]]). Example:

```
{var=dc:http_errors:ratio_rate10m,job=webserver} > 0.01
    and by job, error
{var=dc:http_errors:rate10m,job=webserver} > 1
    for 2m
    => ErrorRatioTooHigh
    details "webserver error ratio at [[trigger_value]]"
    labels {severity=page};
```

Two parts of this deserve attention:

- The **`for 2m`** clause is the **flap-prevention** window. Alerts can toggle state rapidly (flap); requiring the condition to hold for at least two rule-evaluation cycles avoids triggering on a single missed collection. Chapter 10's minimum: two evaluation cycles.
- The alert carries a **template-filled detail string** (`[[trigger_value]]`) so the page contains the triggering numbers, not just the rule name.

## Costs and debuggability

Rules run as fast as their input vectors are large. The chapter's operational advice:

- Rule runtime scales with vector size — adding CPU to a Borgmon task is the usual remedy for slow rules.
- Internal metrics on rule runtime are exported for performance debugging. The monitoring system monitors itself.

## Configuration maintenance

Two maintenance properties are load-bearing for Borgmon scaling (source: chapter-10-practical-alerting-from-time-series-data.md):

- **Rules and targets are separated.** The same rule set applies to many targets; writing a rule once is cheaper than repeating it per target.
- **Language templates** allow rule libraries. Libraries emerged naturally in two classes:
  1. Per-code-library schemas (HTTP server, RPC, memory allocator, storage client) — any user of the library inherits a ready-made rule template for its varz.
  2. Aggregation-from-task-to-global templates that codify the topology (task → job → shard → datacenter → service).

Rule evaluation depends on labels applied both at scrape time and in rules themselves. Labels fall into three types by purpose:

- Data-breakdown labels (e.g. HTTP response `code`)
- Source-of-data labels (instance, job)
- Locality/aggregation labels (zone, shard)

All three kinds are interchangeable from the rule language's perspective, but distinguishing them helps in designing templates.

## Testing

Borgmon rules are code, and Google treats them as such (source: chapter-10-practical-alerting-from-time-series-data.md):

- Extensive unit and regression tests can synthesise time-series data to exercise rules.
- A continuous integration service runs the test suite, packages the configuration, and ships it to all Borgmon in production.
- Each receiving Borgmon validates the configuration before accepting it.

This is a release-engineering pipeline for monitoring config, parallel to (but separate from) application releases.

## Cross-book connections

- [[prometheus-connection]] — PromQL's `rate()`, `sum by (...)`, `without (...)`, and the `for` clause are all direct descendants of Borgmon's rule language.
- [[release-engineering]] — the rule-testing/CI/ship/validate pipeline is the [[hermetic-builds]] pattern applied to monitoring configuration.
- [[architecture-fitness-function]] (Richards & Ford) — alerting rules are objective automatable integrity assessments of operational characteristics; the "sum of error rates over total request rate > 1%" rule is a fitness function made explicit.

## Related pages

- [[borgmon]]
- [[varz-endpoints]]
- [[time-series-arena]]
- [[alertmanager]]
- [[alert-philosophy]]
- [[prometheus-connection]]
- [[site-reliability-engineering]]
