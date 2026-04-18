# Negative Results Are Magic

**Summary**: Randall Bosetti's sidebar in Chapter 12 arguing that experiments whose outcome disconfirms the hypothesis — designs that didn't work, heuristics that didn't improve things, benchmarks that revealed limits — are not failures but conclusive evidence that moves the state of knowledge forward. Negative results should be documented and published, not quietly discarded.

**Sources**: `raw/site-reliability-engineering/chapter-12-effective-troubleshooting.md`

**Last updated**: 2026-04-17

---

## What counts as a negative result

Bosetti's definition (source: chapter-12-effective-troubleshooting.md):

> A "negative" result is an experimental outcome in which the expected effect is absent — that is, any experiment that doesn't work out as planned. This includes new designs, heuristics, or human processes that fail to improve upon the systems they replace.

The category is broad. An architectural prototype that performs worse than the existing system, a tuning change that didn't move the metric, a load test that found the breaking point — all are negative results.

## The core claim

> Realizing you're wrong has much value: a clear negative result can resolve some of the hardest design questions.

The asymmetry Bosetti is pointing at: design teams often spend weeks debating between two options because neither has been ruled out. A rigorously-run experiment that disconfirms one option conclusively resolves the debate — a far bigger win than a positive result that merely confirms something you already believed.

## Why negative results are conclusive

Bosetti's framing (source: chapter-12-effective-troubleshooting.md):

> Experiments with negative results are conclusive. They tell us something certain about production, or the design space, or the performance limits of an existing system. They can help others determine whether their own experiments or designs are worthwhile.

The worked example: a development team evaluated a web server that handled only ~800 concurrent connections before failing under lock contention, when they needed 8,000. They rejected it. A subsequent team evaluating web servers can reuse this result directly — either (a) they need fewer than 800 connections, in which case the server is a candidate, or (b) they need more, in which case the previous team's work tells them to check whether the lock-contention problem has been fixed before retesting.

Without the published negative result, the second team starts from scratch.

## Value beyond the specific result

Bosetti identifies three additional payoffs (source: chapter-12-effective-troubleshooting.md):

### Tools and methods outlive the experiment

> Benchmarking tools and load generators can result just as easily from a disconfirming experiment as a supporting one.

Apache Bench is a load testing tool that grew out of difficult detail-oriented work producing what were likely disappointing first results. Many webmasters have benefited from the tool since, regardless of what its first experiment concluded.

### Supplementary data helps later experiments

Even when the negative result doesn't apply directly, the observations collected in running the experiment often do: benchmarks, documented antipatterns, project postmortems.

### Publishing builds a data-driven culture

> Accounting for negative results and statistical insignificance reduces the bias in our metrics and provides an example to others of how to maturely accept uncertainty.

Bosetti cross-references SRE's high-quality postmortem culture as an existing example of publishing-including-failure improving outcomes across the organisation.

## Why negative results go unreported

> It's tempting and common to avoid reporting negative results because it's easy to perceive that the experiment "failed."

The psychological trap: authors conflate "my experiment disconfirmed the hypothesis" with "my experiment failed." Bosetti pushes back — the hypothesis failed; the experiment did its job.

A second reason for under-reporting is filtered review: some experiments are doomed, and those get caught and not run. The *majority* of unreported negative results aren't doomed-and-filtered; they're rigorously-run-but-quietly-shelved.

## The advice

Four directives, distilled from the sidebar:

1. **Consider scope when designing experiments.** A broad or especially robust negative result helps more peers.
2. **Build repeatable tooling.** The script that tried SSDs this time can try indices next time. Automation persists.
3. **Publish.** If you were interested, others probably were too; save them the trouble of rerunning.
4. **Be skeptical of writeups that don't mention failure.** A design document or performance review with no negative results is either too filtered or not rigorous enough.

## Connection to Chapter 12's main argument

Negative Results Are Magic is a Chapter 12 sidebar because the **test/treat** step of troubleshooting is an experimental method, and experiments that disconfirm hypotheses are the bulk of troubleshooting's productive work. Rule-out is as much information as rule-in. See [[test-and-treat]] for the main-line version of this argument applied to incident response.

The sidebar generalises the point from incident-response to all of engineering: the same epistemic discipline that makes debugging fast also makes design decisions sound.

## Cross-book connection

- [[architecture-decision-record]] (Richards & Ford) — ADRs' Consequences section is a natural home for negative results: "we tried X, here's why it didn't work" is the kind of supporting data that future readers benefit from.
- [[blameless-postmortem]] — Bosetti explicitly names postmortems as an existing SRE cultural practice of publishing-including-failure. The negative-results argument is postmortem culture extended to design experiments.
- [[unknown-unknowns]] (Richards & Ford) — negative results are the mechanism by which unknown-unknowns are converted to known-unknowns, and then to ruled-out; publishing them shares that conversion with everyone else.

## Related pages

- [[test-and-treat]]
- [[troubleshooting-model]]
- [[hypothetico-deductive-debugging]]
- [[blameless-postmortem]]
- [[architecture-decision-record]]
- [[site-reliability-engineering]]
