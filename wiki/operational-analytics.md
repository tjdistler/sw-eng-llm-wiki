# Operational Analytics

**Summary**: Analytics used to take **immediate action**. Where [[business-analytics]] uses data to uncover actionable insights over time, operational analytics uses data to act *right now*, while the problem is occurring. Chapter 9's slogan: "operational analytics versus business analytics = immediate action versus actionable insights."

**Sources**: `raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md`

**Last updated**: 2026-04-18

---

## The defining property

Time. "Data used in business analytics takes a longer view of the question under consideration. Up-to-the-second updates are nice to know but won't materially impact the quality or outcome. Operational analytics is quite the opposite, as real-time updates can be impactful in addressing a problem when it occurs" (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

## Chapter 9's canonical example

Real-time application monitoring. An engineering team dashboards requests-per-second, database I/O, and whatever other metrics matter. Threshold breaches trigger autoscaling (add capacity if servers are overloaded) or alerts (text, group chat, email) (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

The shape is the same across domains: live metric → threshold → action.

## The blurring with business analytics

Chapter 9 flags an interesting trend (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

> The line between business and operational analytics has begun to blur. As streaming and low-latency data become more pervasive, it is only natural to apply operational approaches to business analytics problems; in addition to monitoring website performance on Black Friday, an online retailer could also analyze and present sales, revenue and the impact of advertising campaigns in real time.

The authors' 10-year forecast: **streaming will supplant batch**. "Data products over the next 10 years will likely be streaming-first, with the ability to seamlessly blend historical data. After real-time collection, data can still be consumed and processed in batches as required."

## The "what will you do with it?" question

Chapter 9's governance question for any streaming / operational analytics proposal: **"If you have streaming data, what are you going to do with it? What action should you take?"**

"Correct action creates impact and value. Real-time data without action is an unrelenting distraction." Real-time systems without real-time consequences are just expensive batch systems with a latency budget (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

## Chapter 9's extended factory example

Building on the running-shorts [[business-analytics]] case: the retailer deploys real-time analytics at the fabric factory. Cameras stream video; an off-the-shelf cloud machine-vision tool identifies defects in real time. Defect events are tied to item serial numbers and streamed. Floor analysts correlate defect spikes with specific raw-material boxes, find quality varies box-to-box, and reject defective batches back to the supplier.

The operational-analytics payoff: defective material is caught *on the line*, not in returns weeks later (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

## What serves operational analytics

Chapter 9 notes that **operational analytics databases** play a growing role — these "combine aspects of OLAP databases with stream-processing systems," allowing queries to run across a large range of historical data while encompassing up-to-the-second current data.

See also [[streaming-queries]] from Chapter 8 — the query-engine side of the same shift.

## Cross-book connections

- **[[four-golden-signals]]** / **[[monitoring-and-observability]]** (SRE) — operational analytics over service metrics is the SRE craft. Chapter 9's framing makes explicit that what SREs do *is* operational analytics on their systems.
- **[[stream-processing]]** / **[[kappa-architecture]]** / **[[dataflow-model]]** — the processing engines that make operational analytics feasible at scale.

## Related pages

- [[analytics]]
- [[business-analytics]]
- [[embedded-analytics]]
- [[streaming-queries]]
- [[stream-processing]]
- [[data-serving]]
- [[kappa-architecture]]
- [[monitoring-and-observability]]
