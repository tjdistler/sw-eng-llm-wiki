# Extraction Prioritization

**Summary**: Newman's two-axis model for choosing which microservice to extract first: plot candidates by ease of extraction (y-axis) against expected benefit (x-axis), and start in the easy-and-valuable upper right. Combine domain-model dependency analysis with the migration's stated goal.

**Sources**: `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`

**Last updated**: 2026-04-16

---

## The two questions

When deciding what to extract first, two factors trade off (source: chapter-02-planning-a-migration.md):

1. **How easy is it to extract?** Driven by how entangled the functionality is — both logically (in the [[bounded-context|domain model]]) and physically (in the code and database).
2. **How much benefit will extraction deliver?** Driven by the migration's actual [[why-microservices|goal]] — improved time to market, scaling, autonomy, etc.

Either alone is insufficient. Easy-but-pointless extractions waste effort. Valuable-but-impossible ones stall the project.

## The quadrant

Plot each candidate service on a 2x2 with effort on one axis and benefit on the other. The top-right quadrant — easy *and* valuable — is where you start. Pick one or two candidates from there for your first extractions.

## Using a domain model to assess effort

Newman uses a Music Corp example. From a high-level [[bounded-context]] map (the kind produced by [[domain-driven-design]] or [[event-storming]]):

- **Notification** has many *inbound* dependencies — many parts of the system call it. Extracting it means changing every caller from local invocation to a service call. Hard.
- **Invoicing** has no inbound dependencies. A pattern like the strangler fig can intercept its outbound traffic cleanly. Easier.

Inbound dependency count is a rough but useful proxy for extraction effort.

## Caveat: logical model ≠ code structure

A domain model represents the *logical* shape of the system; there's no guarantee the underlying code is structured the same way (source: chapter-02-planning-a-migration.md). The model is a starting point for the prioritization conversation, not a ground-truth measure of entanglement. You'll usually need to look at the code itself to confirm.

The model also doesn't show database boundaries. Invoicing might look easy to extract logically but turn out to own a great deal of shared data — pulling on that thread leads into Chapter 4 territory ([[information-hiding|database decomposition]]).

## Benefit must connect to the goal

A candidate service can be easy *and* fall in a part of the system that doesn't help the goal. If your migration is about improving time to market and Invoicing barely ever changes, extracting Invoicing is a wasted quick win — nice for momentum, useless for outcomes (source: chapter-02-planning-a-migration.md).

## Replan as you learn

Some "easy" extractions turn out hard; some "hard" ones turn out easy. The prioritisation exercise is not done once — revisit it as you learn from each extraction. As you make progress on the things you thought were easy-and-valuable, candidates you initially rated lower may rise.

## Related pages

- [[incremental-migration]]
- [[domain-driven-design]]
- [[bounded-context]]
- [[event-storming]]
- [[why-microservices]]
- [[cost-of-change]]
