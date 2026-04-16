# Cost of Change

**Summary**: Different decisions in a microservice migration have wildly different rollback costs. Push experimentation toward the cheap end (whiteboards, code refactors); reserve deliberation for the expensive end (database splits, public API contracts).

**Sources**: `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`

**Last updated**: 2026-04-16

---

## The cost gradient

A microservice migration involves decisions that vary by orders of magnitude in their cost-to-undo (source: chapter-02-planning-a-migration.md):

- **Cheap**: moving code around within a codebase. Tools support it; mistakes are quick to fix.
- **Cheap**: trying a service shape on a whiteboard or in a design document.
- **Moderate**: extracting a service from the monolith using safe patterns (e.g., strangler fig).
- **Expensive**: splitting a database. Rolling back a database change is just as complex as making it.
- **Expensive**: untangling an overly coupled integration between services after the fact.
- **Expensive**: rewriting an API used by multiple consumers.

Newman's heuristic: **make mistakes where the impact will be lowest**.

## The whiteboard as the cheapest place

Newman explicitly recommends doing much of the design thinking on the whiteboard — the place where the cost of change and the cost of mistakes are both as close to zero as they get (source: chapter-02-planning-a-migration.md).

Concrete technique: sketch your proposed service boundaries, then run real use cases across them. For a music shop, walk through:

- A customer searching for a record.
- A customer registering with the website.
- A customer purchasing an album.

What service calls fire? Are there odd circular references? Are two services so chatty they should probably be one? These questions are far cheaper to answer in pen than in production.

## Implications for migration order

Cost-of-change shapes the order of work:

- **Code-level refactoring first.** Rearrange boundaries within the monolith before extracting a service.
- **Service extraction next**, using safe patterns that allow rollback.
- **Database decomposition last**, because the cost is highest. (Newman dedicates a whole chapter — Chapter 4 — to it.)

This ordering also informs the [[extraction-prioritization|effort vs benefit]] model — what looks "easy to extract" usually means *not currently entangled with shared data*.

## Connection to other ideas

- [[reversible-vs-irreversible-decisions]] — cost of change is what places a decision on the spectrum.
- [[incremental-migration]] — small steps keep most individual decisions in the cheap range.
- [[information-hiding]] — well-hidden internals lower the cost of changing implementation.
- [[coupling]] — looser coupling lowers the cost of changing one service without ripple effects.

## Related pages

- [[reversible-vs-irreversible-decisions]]
- [[incremental-migration]]
- [[extraction-prioritization]]
- [[information-hiding]]
- [[coupling]]
