# The Benchmark Wars

**Summary**: Reis and Housley's skeptical take on database and cloud vendor benchmarks. Vendor benchmarks are almost always engineered to mislead — via undersized datasets, nonsensical cost comparisons, or asymmetric optimisation. Chapter 4's signature comparison: choosing between a Boeing 787 Business Jet and a Tesla Model S on "performance" specs is absurd, yet vendors routinely do exactly this with databases.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## The opening analogy

Chapter 4 opens the section with a thought experiment (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

Imagine you're a billionaire shopping for new transportation. Compare:

- **787 Business Jet** — range 9,945 nm, Mach 0.90 max, 25 passengers, Mach 0.85 cruise.
- **Tesla Model S Plaid** — range 560 km, 322 km/h, 0-100 in 2.1s, 1020 HP.

Which has better performance? The question is idiotic — they're designed for completely different use cases. Yet Chapter 4 observes:

> We see such apples-to-oranges comparisons made all the time in the database space.

## Three common tricks

Chapter 4 names three tricks (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

### 1. Big data... for the 1990s

Products that claim to support "big data" at petabyte scale benchmark on datasets small enough to fit on a smartphone. For systems that rely on caching, the whole test dataset sits in SSD or memory, so repeated queries on the same data show ultra-high performance. A small dataset also minimises RAM and SSD costs when quoting pricing.

**Countermeasure:** simulate anticipated real-world data and query size. Evaluate based on your own needs, not the vendor's synthetic benchmark.

### 2. Nonsensical cost comparisons

A standard trick when analysing price/performance or TCO. Many MPP systems can't be readily created and deleted — they run continuously for years once configured. Other databases support dynamic compute charged per query or per second. Comparing ephemeral and non-ephemeral systems on a cost-per-second basis is meaningless, "but we see this all the time in benchmarks."

### 3. Asymmetric optimisation

Chapter 4's example: a vendor compares a **row-based MPP** system against a **columnar** database using a complex-join benchmark on **highly normalised** data. The normalised model is ideal for the row-based system; the columnar system would need schema changes to reach its potential. To make it worse, the vendor pre-indexes joins in their system but does not apply comparable tuning (e.g., materialised views) to the competitor.

Result: the comparison looks fair but is rigged from the start.

## The DeWitt clauses

Chapter 4 observes a historical point (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> We're glad to see many database vendors finally dropping DeWitt clauses from their customer contracts.

DeWitt clauses — historically standard database contract terms — prohibited customers from publishing benchmarks of the database without vendor approval. Dropping them allows more honest public comparisons, but the quality of published benchmarks has not necessarily improved.

## Caveat emptor

Chapter 4's summary (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> As with all things in data technology, let the buyer beware. Do your homework before blindly relying on vendor benchmarks to evaluate and choose technology.

The practical discipline:

- **Test on your own data.** Size, shape, query patterns, concurrency.
- **Model real cost structures.** Not per-second-of-use against always-on systems.
- **Tune both sides fairly** when comparing technologies, or be explicit about untuned-vs-tuned.
- **Read benchmarks critically** — who ran it, under what conditions, with what incentives.

## Cross-book framing

- [[statistical-comparative-thinking]] (SRE) is the statistical discipline that lets you judge whether a performance difference is signal or noise.
- [[queries-per-second-pitfalls]] (SRE) names the analogous trap for capacity planning — QPS is rarely a meaningful unit across services.
- [[performance-tests]] / [[stress-tests]] — the honest engineering counterpart to vendor benchmarks.

## Related pages

- [[technology-selection]]
- [[build-vs-buy]]
- [[proprietary-walled-garden]]
- [[queries-per-second-pitfalls]]
- [[statistical-comparative-thinking]]
- [[performance-tests]]
- [[stress-tests]]
- [[principles-of-good-data-architecture]]
