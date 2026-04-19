# Slowly Changing Dimensions

**Summary**: A family of patterns for how a [[dimension-table]] represents attribute changes over time. The question: when a customer moves zip codes, do historical facts continue to report the old zip or adopt the new one? SCD Types 0–6 give different answers. Types 1, 2, 3 are the ones Reis & Housley cover in detail; Type 2 is most common.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`, `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`

**Last updated**: 2026-04-18

---

## The question

A customer's zip code changes. Historical orders were placed at the old zip. Do we want queries to:

- See the **current** zip (so all of this customer's orders look like they came from the new zip)?
- See the **as-of** zip at the time of the order (so each order reports its historical context)?
- Preserve **both**?

SCD types formalize these answers.

## Types 0–7

Reis & Housley mention seven levels exist; the three they cover explicitly are 1, 2, 3 (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

### Type 0 — retain original

Never update. The value at creation time persists forever.

### Type 1 — overwrite

Overwrite the old value with the new one. **History lost.** Simple; the default behaviour of most data warehouses. Queries see only the current state.

### Type 2 — new row per change

When an attribute changes, a **new row** is inserted with the new value and the existing row is marked inactive. Standard columns:

- `EFF_StartDate` — when this version became active.
- `EFF_EndDate` — when it was superseded. `9999-01-01` conventionally marks "still active."
- `IsCurrent` flag (optional).

Queries for current state filter `WHERE EFF_EndDate = '9999-01-01'`. Historical queries filter `WHERE order_date BETWEEN EFF_StartDate AND EFF_EndDate`.

Chapter 8's worked example: Matt Housley's customer record shows two rows with the same natural key — one with start `2020-05-04` / end `2021-09-19` (old zip), one with start `2021-09-19` / end `9999-01-01` (new zip) (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

**Most common in practice.** Full history is retained; fact-to-dimension joins need to carry the version surrogate key, not just the natural key.

### Type 3 — new column per change

When an attribute changes, add a **new column** (`current_zip`, `previous_zip`, `zip_changed_date`). Limited history depth — only one prior value. Rare in practice; useful for known-bounded attributes.

### Types 4–7

Less common; combinations of the above. Type 4 maintains a separate history table; Type 6 is a hybrid of 1, 2, and 3.

## Relationship to stream-table joins

DDIA points out that SCD Type 2 is the standard way to make [[stream-joins|stream-table joins]] deterministic when the lookup table changes over time (source: raw/designing-data-intensive-applications/chapter-11-stream-processing.md). If you give each version its own surrogate key, a streaming join can reference the specific version active at event time — reproducible under [[reprocessing-event-streams|reprocessing]].

The trade-off: every version must be retained, so [[log-compaction]] on the dimension's changelog is incompatible with Type-2 semantics.

## Not for streaming at the warehouse layer

Reis & Housley explicitly note that translating SCD Type 2 to a streaming paradigm — continuously updating the dimension as events stream in — would "bring your data warehouse to its knees." SCD patterns assume **batch**-rate dimension updates; streaming data modeling remains an unsettled art (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md). See [[streaming-data-modeling]].

## Cross-book connections

- [[stream-joins]] — DDIA's treatment of time-dependent joins, which lands on SCD Type 2 as the determinism technique.

## Related pages

- [[dimension-table]]
- [[star-schema]]
- [[kimball-model]]
- [[stream-joins]]
- [[reprocessing-event-streams]]
- [[streaming-data-modeling]]
