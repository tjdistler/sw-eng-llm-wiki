# Minimal APIs

**Summary**: Chapter 9 of *Site Reliability Engineering*'s application of Saint-Exupery's design principle to software interfaces: perfection is attained "when there is no longer anything to take away." Small APIs are easier to understand, easier to make good, and a hallmark of a well-understood problem. Adding methods and parameters is often the path of least resistance; the discipline is to deliberately narrow the interface.

**Sources**: `raw/site-reliability-engineering/chapter-09-simplicity.md`

**Last updated**: 2026-04-17

---

## The Saint-Exupery quote

Chapter 9 borrows from Antoine de Saint-Exupery's 1939 *Wind, Sand and Stars* (source: chapter-09-simplicity.md):

> Perfection is finally attained not when there is no longer more to add, but when there is no longer anything to take away.

Luebbe applies this directly to API design:

> Writing clear, minimal APIs is an essential aspect of managing simplicity in a software system. The fewer methods and arguments we provide to consumers of the API, the easier that API will be to understand, and the more effort we can devote to making those methods as good as they can possibly be.

## Why less really is more

Chapter 9's argument decomposes into three related claims (source: chapter-09-simplicity.md):

1. **Fewer methods = easier to understand.** A consumer reading the API documentation has less to learn before they can use it correctly.
2. **Fewer methods = more engineering effort per method.** The team maintaining the API has a budget, and spreading that budget over a smaller surface produces better individual methods.
3. **A small API is a signal.** "A small, simple API is usually also a hallmark of a well-understood problem." The act of minimising the interface forces clarity about what the service is *for*.

The third point is the subtle one: minimal APIs are not just easier to use, they are an artefact of the team doing the design work properly. A sprawling API often indicates that the team has not decided what the service's job is and has hedged by exposing every possibility.

## The conscious "no" to certain problems

Chapter 9 frames minimal APIs as an instance of a broader recurring theme (source: chapter-09-simplicity.md):

> The conscious decision to not take on certain problems allows us to focus on our core problem and make the solutions we explicitly set out to create substantially better.

Every added method expands the set of problems the API is now committed to solving well. Refusing that expansion is not a failure of imagination — it is a deliberate choice to invest the available engineering effort in depth rather than breadth.

## Connection to Newman's "expose as little as possible"

Chapter 9's framing is the SRE restatement of an older piece of software-design advice Newman captures in [[information-hiding]]:

> I adopt the approach of exposing as little as possible from a module (or microservice) boundary. Once something becomes part of a module interface, it's hard to walk that back. But if you hide it now, you can always decide to share it later.

The two framings have the same structure:

| Framing | Source | Motivation |
|---|---|---|
| "There is no longer anything to take away" | Chapter 9, Saint-Exupery | Simplicity as a virtue in itself |
| "Expose as little as possible" | Newman, Parnas | Preserving freedom to change internals |

The Newman/Parnas motivation — protecting future change — is the operational reason the Chapter 9 aesthetic advice is correct. A minimal API is not just elegant; it is the API that leaves the implementation the most room to evolve.

## Chapter 9's API-modularity point

The section is short, but Chapter 9 also notes (in the next section, Modularity) that APIs themselves must be modular if they are going to change safely (source: chapter-09-simplicity.md):

> Just a single change to an API can force developers to rebuild their entire system and run the risk of introducing new bugs. Versioning APIs allows developers to continue to use the version that their system depends upon while they upgrade to a newer version in a safe and considered way.

Minimal APIs keep the versioning cost manageable: fewer methods means fewer version-skew cases to reason about. See [[backward-forward-compatibility]] for the compatibility machinery and [[protocol-buffers]] for the specific Google tooling.

## Cross-book connections

- [[information-hiding]] (Newman / Parnas) — the operational motivation for minimal APIs: the less is exposed, the more can change
- [[coupling]] (Newman) — small APIs reduce domain coupling; the Pick Instruction example in Newman's coupling treatment is minimal-API design applied to inter-service messages
- [[backward-forward-compatibility]] (Kleppmann / Bellemare) — version skew management; minimising the API surface minimises the skew cases
- [[protocol-buffers]] (Ch 2) — Google's specific mechanism; backward and forward compatibility are first-class design goals
- [[unix-philosophy]] (Kleppmann) — "do one thing and do it well" is the tool-level version of minimal-API discipline
- [[service-granularity]] — small, focused APIs are closely related to the right-sized-service question; Richardson's "as small an interface as possible" framing lines up exactly
- [[accidental-complexity]] — API bloat is a prolific source of accidental complexity; minimal APIs are the design-time countermeasure

## Related pages

- [[simplicity-sre]]
- [[information-hiding]]
- [[coupling]]
- [[modularity]]
- [[backward-forward-compatibility]]
- [[protocol-buffers]]
- [[service-granularity]]
- [[accidental-complexity]]
- [[site-reliability-engineering]]
