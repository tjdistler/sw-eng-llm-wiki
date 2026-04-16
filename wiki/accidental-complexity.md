---
name: Accidental Complexity
description: Complexity arising from implementation choices rather than the inherent difficulty of the problem being solved
type: concept
---

# Accidental Complexity

**Summary**: Accidental complexity is complexity not inherent in the problem a system solves, but introduced by implementation choices — and unlike essential complexity, it can be removed.

**Sources**: `raw/designing-data-intensive-applications/chapter-01-reliable-scalable-and-maintainable-applications.md`

**Last updated**: 2026-04-15

---

## Definition

Moseley and Marks define complexity as **accidental** when it is not inherent in the problem that the software solves (as seen by the users) but arises only from the implementation. The complementary concept is **essential complexity** — the irreducible difficulty of the problem itself. (source: chapter-01)

Good system design minimizes accidental complexity while accepting essential complexity as unavoidable.

## Symptoms of complexity

As systems grow, accidental complexity accumulates in recognizable forms:

- Explosion of state space
- Tight coupling between modules
- Tangled dependencies
- Inconsistent naming and terminology
- Performance hacks embedded in business logic
- Special-casing to work around problems elsewhere

These symptoms slow everyone who works on the system, increase the risk of bugs when making changes (hidden assumptions and unintended interactions become harder to see), and drive up maintenance costs. (source: chapter-01)

## Abstraction as the primary tool

The best mechanism for removing accidental complexity is **abstraction** — hiding implementation detail behind a clean, simple-to-understand interface. A good abstraction:

- Makes the underlying complexity invisible to callers
- Can be reused across many different applications
- Allows quality improvements to propagate to all users of the abstraction

Examples of highly successful abstractions:
- High-level programming languages hiding machine code, CPU registers, and syscalls
- SQL hiding on-disk data structures, concurrent access, and crash recovery

Finding *good* abstractions is hard, especially in distributed systems where there are many good algorithms but less clarity on how to package them into reusable, complexity-hiding components. (source: chapter-01)

## Relationship to maintainability

Accidental complexity is the primary enemy of [[maintainability]]. A system mired in accidental complexity is sometimes called a "big ball of mud" — difficult to understand, risky to change, and expensive to operate. Removing it via abstraction is one of the highest-leverage activities in software design.

Reducing complexity does not mean reducing functionality. The goal is to make the *implementation* simpler, not the *capabilities* weaker.

## Relationship to evolvability

Simple, well-abstracted systems are easier to modify for unanticipated future requirements. Accidental complexity makes [[maintainability#Evolvability — making change easy|evolvability]] harder: when the system is difficult to understand, engineers cannot safely reason about the consequences of a change. (source: chapter-01)

## Related pages

- [[maintainability]]
- [[reliability]]
- [[scalability]]
