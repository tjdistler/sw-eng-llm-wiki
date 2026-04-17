# Unknown Unknowns

**Summary**: Donald Rumsfeld's three-way classification (known knowns, known unknowns, unknown unknowns) applied to software. *Unknown unknowns* are the things no one knew were going to crop up on a project. They are the reason Big Design Up Front fails and the reason all architecture eventually becomes iterative.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-01-introduction.md`

**Last updated**: 2026-04-16

---

## The Rumsfeld quote

> …because as we know, there are known knowns; there are things we know we know. We also know there are known unknowns; that is to say we know there are some things we do not know. But there are also unknown unknowns — the ones we don't know we don't know. — Former US Secretary of Defense Donald Rumsfeld (quoted in source: chapter-01-introduction.md)

## Why architects care

Richards and Ford frame unknown unknowns as the nemesis of software systems (source: chapter-01-introduction.md). Every non-trivial project starts with a list of *known unknowns* — things the team knows it will need to learn. But projects are repeatedly ambushed by *unknown unknowns* — things no one on the team, in the business, or in the industry anticipated. A new regulation; an upstream system retiring an API mid-project; a performance cliff that only appears at unexpected scale; a dependency acquired and discontinued.

The implication is sharp:

> This is why all "Big Design Up Front" software efforts suffer: architects cannot design for unknown unknowns. (source: chapter-01-introduction.md)

If unknown unknowns are certain to appear and cannot be predicted, then a plan that assumes the initial design is final is guaranteed to fail.

## Mark Richards's corollary

The book quotes Mark (one of the authors):

> All architectures become iterative because of unknown unknowns, Agile just recognizes this and does it sooner. (source: chapter-01-introduction.md)

The argument: iterative architecture is not optional. The only question is whether a team embraces it early (Agile-style, with short feedback loops) or is forced into it late (typically after a painful midcourse correction when an unknown unknown surfaces). Richards and Ford treat Agile engineering practices as a baseline throughout the book for exactly this reason.

## How to survive them

You cannot predict unknown unknowns, but you can design for their *arrival*:

- **[[evolutionary-architecture]]** — architect the system so that it changes gracefully; validate via [[architecture-fitness-function|fitness functions]] that change hasn't silently broken anything.
- **Short feedback loops** — iterate frequently; discover wrong assumptions before they're embedded deeply.
- **Reversible decisions** — prefer two-way doors; see [[reversible-vs-irreversible-decisions]].
- **Deployment flexibility** — [[strangler-fig-pattern]], [[feature-toggle]], [[parallel-run-pattern]], [[branch-by-abstraction]] all exist because production reality uncovers things staging cannot.
- **Capture the why** — per the [[laws-of-software-architecture|Second Law]], when an unknown unknown does arrive, the team needs to know which existing decisions were grounded in now-invalidated assumptions.

## Relation to other wiki concepts

- [[accidental-complexity]] — one common outcome of hitting an unknown unknown is quick-fix accidental complexity; recognising the pattern is how you unwind it instead of layering on top.
- [[architecture-vitality]] — the architect's continuous analysis is partly a hunt for unknowns that have become known.
- [[cost-of-change]] — Newman's push-experiments-toward-the-whiteboard heuristic is the cost-aware form of "iterate early."
- [[incremental-migration]] — Newman's migration discipline is built around the assumption that production will reveal things no plan could anticipate.
- [[robustness-vs-resilience]] — Woods's resilience concept explicitly covers the system's ability to keep functioning when something unanticipated happens; it's the runtime counterpart of designing for unknown unknowns.

## Related pages

- [[evolutionary-architecture]]
- [[architecture-fitness-function]]
- [[architecture-vitality]]
- [[reversible-vs-irreversible-decisions]]
- [[incremental-migration]]
- [[cost-of-change]]
- [[robustness-vs-resilience]]
- [[laws-of-software-architecture]]
- [[strangler-fig-pattern]]
- [[feature-toggle]]
- [[fundamentals-of-software-architecture]]
