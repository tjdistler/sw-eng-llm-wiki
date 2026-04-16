# Pattern: Database per Bounded Context

**Summary**: Even inside a [[modular-monolith]], give each [[bounded-context]] its own logically separate schema. The application is still a single deployable, but the data is decomposed — preserving the option to extract microservices later without having to do the schema split first.

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## The pattern

Once you've cleanly isolated data access (see [[repository-per-bounded-context]]), continue the separation into the schema. Each bounded context gets its own schema. The deployable remains a monolith. (source: chapter-04-decomposing-the-database.md)

This is "hedging your bets." A bit more work than a single schema, but if and when you decide to extract a microservice, the data is already partitioned the right way.

## The ThoughtWorks Revenue example

Newman recounts a project at ThoughtWorks where Peter Gillard-Moss's team needed to build new revenue-forecasting functionality. Three broad areas of functionality felt distinct, but the team was small (three people) and couldn't justify the operational overhead of three microservices. (source: chapter-04-decomposing-the-database.md)

They settled on a single deployable, a single `Revenue` service, containing three isolated bounded contexts (each a separate JAR). Each bounded context had its own separate schema. The intent was to extract them into microservices later if needed. (source: chapter-04-decomposing-the-database.md)

It was never needed. Years later, the system remains a [[modular-monolith]] with multiple databases — a real-world example of this pattern's value.

## Where to use it

Newman's strongest recommendation here is for **brand-new systems** (as opposed to reimplementing existing ones). He is not a fan of jumping into microservices for new products or startups, where the domain isn't well enough understood to identify stable boundaries. With this pattern, you get a halfway house: clear separation today, easy extraction tomorrow. (source: chapter-04-decomposing-the-database.md)

For existing systems undergoing decomposition, this is a natural intermediate state — your monolith now has multiple internal schemas, ready for a service extraction whenever you're ready.

## Trade-offs

- More schemas to maintain (migrations, backups, monitoring).
- You lose the ability to write cross-context joins directly in SQL — but that's the point. If you would have written that join, you'd have created the kind of coupling this pattern is designed to prevent.
- A single database engine can still host many schemas, so you don't need new infrastructure.

## Related pages

- [[database-decomposition]]
- [[repository-per-bounded-context]]
- [[bounded-context]]
- [[modular-monolith]]
- [[split-the-database-first]]
- [[independent-deployability]]
- [[when-microservices-are-a-bad-idea]]
