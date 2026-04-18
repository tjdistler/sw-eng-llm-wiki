# Moiré Load Pattern

**Summary**: A subtle relative of the [[pipeline-thundering-herd|thundering herd]]: when **two or more periodic pipelines** run simultaneously and their execution sequences occasionally overlap in time, they consume a common shared resource in occasional aggregate spikes. Each pipeline in isolation looks reasonable; the aggregate pattern only appears in stacked plots of resource usage. Chapter 25 names it the **Moiré load pattern** by analogy with the visual interference pattern produced when two regular grids overlap at a slight angle.

**Sources**: `raw/site-reliability-engineering/chapter-25-data-processing-pipelines.md`

**Last updated**: 2026-04-17

---

## The pattern

The basic [[pipeline-thundering-herd|thundering herd]] is a single pipeline whose synchronised launches overwhelm shared infrastructure. The Moiré pattern is the multi-pipeline generalisation (source: chapter-25-data-processing-pipelines.md):

> A related problem we call "Moiré load pattern" occurs when two or more pipelines run simultaneously and their execution sequences occasionally overlap, causing them to simultaneously consume a common shared resource.

Each individual pipeline looks fine in isolation — its peak-load periods are within its allocated capacity. The problem appears only when:

1. The pipelines share resources (cluster CPU, network bandwidth, a shared filesystem).
2. Their schedules don't synchronise exactly but **occasionally drift into alignment** — the way two slightly-offset regular grids produce visible interference fringes.
3. During those alignment windows, their aggregate demand exceeds what the shared resource can supply.

Chapter 25's Figure 25-2 shows three periodic pipelines with their separate resource usage; Figure 25-3 stacks them and the peak impact (causing on-call pain) appears when the aggregate load crosses a threshold (~1.2M in the example). The peaks visible in the stacked plot do not appear in any individual pipeline's plot.

## Why it's subtle

Three properties make the Moiré pattern easy to miss:

- **Per-pipeline metrics look fine.** Each pipeline operator sees their pipeline running within budget and concludes there is no problem.
- **The pattern is intermittent.** When the pipelines drift back out of alignment, the aggregate spike disappears, and the problem doesn't recur until the next alignment window — possibly hours, days, or weeks later.
- **The on-call signal is on the shared resource, not on the pipelines.** The first symptom is usually a network-saturation alert, a filesystem-latency alert, or a cluster-scheduler queue-depth alert, none of which name a specific pipeline as the cause.

Chapter 25's recommendation is to plot pipeline usage of shared resources as a stacked time series — the pattern jumps out visually but is invisible in per-pipeline summaries.

## Why continuous pipelines reduce (but don't eliminate) this

Continuous pipelines have load that arrives more evenly over time. The chapter notes the Moiré pattern can still occur in continuous pipelines, but it's less common because the per-pipeline load is smoother — there's nothing to "occasionally overlap" the way two cron-scheduled spikes can. A pipeline whose demand is approximately constant has no peaks for a Moiré pattern to align.

The architectural argument: the periodic-pipeline pattern produces sharp peaks; sharp peaks at slightly-different periods produce Moiré interference. Removing the peaks (by going continuous) removes the substrate for the pattern.

## Mitigations short of going continuous

If the pipelines must remain periodic for other reasons, the chapter implicitly suggests two mitigations (consistent with broader SRE practice):

- **Distribute launch times deliberately.** The same hash-the-job-identity-into-the-time-window technique [[cron-thundering-herd|the `?` crontab extension]] uses for cron applies here: deliberately offset pipelines from each other so their schedules don't drift into alignment.
- **Provision the shared resource for aggregate peak.** If you cannot smooth the demand, capacity-plan for the worst-case alignment of all pipelines.

Both have costs. The first requires central coordination of pipeline schedules across teams. The second pays full peak-load cost continuously even though the peak only occurs occasionally.

## Cross-references

- [[pipeline-thundering-herd]] — the single-pipeline version; Moiré is the multi-pipeline generalisation
- [[cron-thundering-herd]] (SRE Ch 24) — the same kind of unintended synchronisation, addressed at the scheduler layer with the `?` extension
- [[cascading-failure]] / [[cascading-failure-triggers]] (SRE Ch 22) — the Moiré peak is a [[cascading-failure-triggers|trigger]] in Chapter 22's catalogue, with the special property that it is intermittent and weakly correlated with any single team's actions
- [[capacity-planning]] (SRE Ch 1 / Ch 18) — the Moiré pattern is one of the cases where naive per-service capacity planning underestimates the requirement; aggregate planning across all consumers of the shared resource is needed
- [[monitoring-topology-sharding]] (SRE Ch 10) — the kind of cross-service stacked-resource-usage plot the chapter recommends for spotting Moiré patterns is exactly what aggregator-level Borgmon dashboards are designed for

## Related pages

- [[pipeline-thundering-herd]]
- [[periodic-pipeline]]
- [[data-processing-pipelines]]
- [[continuous-data-processing]]
- [[google-workflow]]
- [[cron-thundering-herd]]
- [[cascading-failure]]
- [[capacity-planning]]
