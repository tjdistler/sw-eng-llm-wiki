# Migration Pattern Selection

**Summary**: A guide to choosing among the migration patterns Newman covers in Chapter 3. The two dominant decision factors are *can you change the monolith?* and *where is the call you need to intercept?*. There is no single right pattern; Newman's experience is that most migrations use a mix.

**Sources**: `raw/monolith-to-microservices/chapter-03-splitting-the-monolith.md`

**Last updated**: 2026-04-16

---

## The first question: can you change the monolith?

Whether you can modify the existing system is the first filter, because it determines which patterns are even available (source: chapter-03-splitting-the-monolith.md).

You **cannot** change the monolith if it is:

- Vendor software with no source access.
- Written in a technology your team can no longer support.
- Owned by a separate team you can't get cycles from.
- In a state where the cost of change is judged too high.
- (Newman's anecdote) the source code has been lost and nobody wants to admit it.

There may also be *softer* reasons not to change it — for example, many teams are actively working on it and you don't want to interfere. Branch by abstraction can mitigate the contention concern but you may still judge the disruption too great (source: chapter-03-splitting-the-monolith.md).

## Cut, copy, or reimplement?

Even when you can change the monolith, you have a choice for the functionality being migrated (source: chapter-03-splitting-the-monolith.md):

- **Copy the code** to the new service while leaving it in place in the monolith. Gives you a rollback point and lets you run both in [[parallel-run-pattern|parallel]]. Only remove from the monolith once you trust the new implementation.
- **Reimplement** in the new service from scratch. More common in practice — most teams Newman has seen do clean-room reimplementation of small slices.

The risk with reimplementation is recreating big-bang rewrite problems on a smaller scale. Newman's rule of thumb: *if a single service's reimplementation timeline reaches several months, reconsider*. Days or weeks per service is the sustainable range (source: chapter-03-splitting-the-monolith.md).

## The second question: where is the call?

Different patterns target different points in the request flow.

| Where the call to migrate enters | Best-fit pattern |
|---|---|
| At the perimeter, cleanly attributable | [[strangler-fig-pattern]] |
| Deep inside the monolith, called from many places | [[branch-by-abstraction]] |
| You can't change the monolith but the inbound request/response carries enough info | [[decorating-collaborator-pattern]] |
| You can't change the monolith and you need to react to data changes | [[change-data-capture]] |
| User-facing change with vertical slice ownership | [[ui-composition]] |

(source: chapter-03-splitting-the-monolith.md)

## Verification needs

If correctness or non-functional behaviour of the migrated functionality is high-stakes — financial pricing, medical records — overlay [[parallel-run-pattern]] on whichever code-movement pattern you chose. For high-risk releases more generally, lean on [[progressive-delivery]] techniques (source: chapter-03-splitting-the-monolith.md).

## Refactor first, or extract directly?

Newman's stated preference is to refactor the monolith into clean modules along business-domain lines *before* extracting (see [[seams-and-legacy-code]] and [[modular-monolith]]). In practice he observes that few teams do this — and some find that the refactoring alone solves enough of their problems that they no longer need microservices (source: chapter-03-splitting-the-monolith.md).

## Don't change behaviour during migration

A subtle trap: changing functionality *while* migrating it complicates rollback. If the new Payroll service has bug fixes the old one doesn't, rolling back reintroduces the bugs; if it has new features, rolling back removes them from users (source: chapter-03-splitting-the-monolith.md).

The advice: **freeze behaviour of the slice being migrated for the duration of its migration**. The shorter each migration, the easier this freeze is to enforce — yet another argument for small steps and [[incremental-migration]].

## Mix and match

> "Most folks end up using a mix of approaches; it's rare that one single technique will handle every situation." (source: chapter-03-splitting-the-monolith.md)

The patterns are tools; the work is choosing the right one for each piece of functionality.

## Related pages

- [[strangler-fig-pattern]]
- [[branch-by-abstraction]]
- [[decorating-collaborator-pattern]]
- [[change-data-capture]]
- [[parallel-run-pattern]]
- [[ui-composition]]
- [[progressive-delivery]]
- [[modular-monolith]]
- [[seams-and-legacy-code]]
- [[incremental-migration]]
