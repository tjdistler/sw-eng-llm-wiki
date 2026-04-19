# Tactical Forking

**Summary**: Fausto De La Torre's decomposition pattern for a monolith with little or no internal structure. Instead of extracting pieces from the tangle, **clone the entire codebase once per target service** and have each team *delete* what isn't theirs (source: raw/software-architecture-the-hard-parts/chapter-04-architectural-decomposition.md). Deletion sidesteps the extraction-dependency problem that defeats component-based approaches on a [[big-ball-of-mud|big ball of mud]]. The result is a small number of coarse-grained services, each still carrying latent mud, but separable and deployable.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-04-architectural-decomposition.md`

**Last updated**: 2026-04-19

---

## The pattern

The mechanics, from Chapter 4 of *The Hard Parts*:

1. Start with a single monolithic codebase containing several domain behaviours (the book's diagram uses abstract shapes — hexagons, squares, circles) with no clean internal organisation.
2. **Clone the full monolith once per target team / service.** Every team gets its own complete copy of the repo.
3. Each team decides which portions of the application's behaviour belong to *their* service, and **deletes everything else**. Deletion is verified the cheap way: the code still compiles, the relevant tests still pass.
4. Teams iterate the deletion until each fork is left with only its target portion (plus whatever latent mud happens to be entangled with it).
5. The forks are now separate services. The monolith is retired.

The illustrative end state in the chapter's example: one service owns the hexagon and square domain; another owns the circle domain.

## Why deletion beats extraction on a mud ball

The chapter's central observation is that **extraction and deletion are not symmetric on a highly-coupled codebase** (source: chapter-04-architectural-decomposition.md):

- **Extraction** — pulling the code you want into a new service — forces the architect to chase every dependency the extracted code touches. On a [[big-ball-of-mud|big ball of mud]], that's most of the codebase; the "extraction" snowballs into a rewrite.
- **Deletion** — removing the code you don't want — leaves the dependencies intact. If after deletion the remaining code compiles and its tests pass, the remaining dependencies were necessary. The chaotic internal structure no longer resists the operation; it simply survives the operation, in a smaller form.

This is why the pattern is called *tactical* — it's a pragmatic sidestep around the structural-decomposition problem, not a solution to it.

## The sculpture metaphor

The chapter's analogy: **component-based decomposition is like extracting a shape from granite; tactical forking is like Michelangelo's "I saw the angel in the marble and carved until I set him free."** Teams don't build new services by assembling clean parts; they uncover each service by chiselling away what doesn't belong (source: chapter-04-architectural-decomposition.md).

## Trade-offs

Richards and Ford are explicit about what the pattern buys and costs (source: chapter-04-architectural-decomposition.md):

**Benefits**

- **Teams can start immediately.** Virtually no up-front architectural analysis is required beyond the coarse-grained service partition. Compare with [[component-based-decomposition]], which requires months of refactoring before extractions can begin.
- **Deleting is easier than extracting on coupled code.** Every engineer has felt this: removing a feature you know doesn't belong is safer than trying to pull its *good* parts out of a tangle.
- **Incremental, compile-verifiable progress.** Each deletion either compiles and passes tests, or it doesn't. Rollback is trivial (`git revert`).

**Shortcomings**

- **Services carry latent mud.** The surviving fork contains all the code the team was afraid to delete plus whatever else was coupled to the target behaviour. The new service is smaller than the monolith but not cleaner.
- **Nothing improves the code quality.** Unless the team does additional refactoring after forking, the code inside the service is still mud — there's just less of it.
- **Shared-code drift.** Common utilities cloned across N forks can end up differently named, differently patched, and inconsistently evolved. Keeping shared concepts consistent across forks is manual, organisational work.
- **Coarse granularity only.** The pattern produces one service per team / team's-portion — typically 2–4 services, not dozens. It's a move away from monolith, not a move to [[microservices]] granularity.

## When to use it

The chapter's flow chart makes the selection rule explicit: tactical forking is the right approach when **the codebase is decomposable in principle (i.e., not so rotten that it has to be rewritten) but lacks observable component boundaries**. That's the [[big-ball-of-mud]] case where [[component-based-decomposition]] is infeasible because there are no components to refine.

Additional situational fits:

- **Team independence is the dominant goal.** If the main pain is "two teams blocking each other in one repo," tactical forking gives each team its own repo quickly, at the cost of duplicated code.
- **Speed-to-value matters more than cleanup.** Systems whose business value won't survive a 12-month cleanup may need this pragmatic move even if the result is ugly.
- **A subsequent clean-up phase is planned.** Tactical forking is most defensible when the team commits to a follow-on refactoring of each fork — otherwise the mud is permanent.

Conversely, when the codebase *does* have internal structure (identifiable components, namespaces, consistent layering), [[component-based-decomposition]] is the better path — the forking waste is avoidable.

## Relationship to other migration patterns

- **[[component-based-decomposition]]** — the preferred alternative. The Chapter 4 decision tree routes to one or the other based on codebase decomposability.
- **[[strangler-fig-pattern]]** — Newman's extraction-based default. Tactical forking is the *opposite philosophy* to strangler fig: instead of growing a new service beside the monolith and redirecting traffic, you fork the monolith and shrink the copies.
- **[[branch-by-abstraction]]** — also an extraction technique; fails for the same mud-ball reason strangler fig does (can't cleanly intercept what has no clean seams — see [[seams-and-legacy-code]]).
- **[[modular-monolith]]** — the opposite end of the spectrum. Tactical forking is what you reach for when a modular monolith is impossibly far away; working toward a modular monolith is what you'd prefer to do instead.
- **[[distributed-monolith]]** — the risk if tactical forking is done without discipline. Cloning a mud ball N times and leaving synchronous calls between the forks produces a distributed mud ball — all the drawbacks of both.

## The "technical debt by design" reading

Tactical forking is best understood as **choosing where to take the technical debt**. Component-based decomposition pays the debt up front (months of refactoring before extraction). Tactical forking defers the debt to after the split (latent mud inside each service, paid down — or not — later). Neither is free; the architect picks the payment schedule that fits the organisation's timeline and risk profile.

See [[trade-off-analysis]] for the *Hard Parts* method that frames these as two sides of a migration decision rather than competing "best practices."

## Related pages

- [[big-ball-of-mud]]
- [[component-based-decomposition]]
- [[migration-pattern-selection]]
- [[strangler-fig-pattern]]
- [[branch-by-abstraction]]
- [[modular-monolith]]
- [[distributed-monolith]]
- [[service-based-architecture]]
- [[coupling-metrics]]
- [[trade-off-analysis]]
- [[software-architecture-the-hard-parts]]
