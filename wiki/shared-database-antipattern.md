# Shared Database (Anti-Pattern)

**Summary**: Multiple services reading and writing the same logical schema directly. Newman calls this the most common form of [[coupling|implementation coupling]] in monolith-derived systems and the single biggest obstacle to [[independent-deployability]].

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## What's wrong with it

Sharing a single schema between services denies you the chance to decide what is shared and what is hidden — the opposite of [[information-hiding]] (source: chapter-04-decomposing-the-database.md). Concretely:

- **You don't know what parts of the schema can change safely.** Knowing an external party can access your database is one thing; not knowing *which tables and columns* they use is another.
- **Ownership is ambiguous.** If three services can all change the `Order` table, where does the order state machine live? See [[aggregate]].
- **Behaviour is scattered.** When the rule for "an order can transition to PAID" needs to change, you have to find and fix every service that writes to that table. This is the opposite of [[cohesion]].

Newman: "All too often a shared database implies the opposite of high cohesion of business functionality." (source: chapter-04-decomposing-the-database.md)

## Where it is acceptable

Newman names only two situations where direct sharing is appropriate in a microservice architecture (source: chapter-04-decomposing-the-database.md):

1. **Read-only static reference data** — country codes, postal codes, currency codes. Highly stable, change-controlled as an admin task. See [[shared-static-data]].
2. **A database that is *deliberately* designed as a public endpoint** — managed and versioned like any other API. See [[database-as-a-service-interface]].

Anything else is an anti-pattern, even if it is the *current* state of your system.

## The credit derivative system anecdote

Newman recounts re-platforming a credit derivative system at an investment bank. They needed to restructure the schema to improve write throughput, but found "over 20" external applications were reading the database, all using the same shared username and password. They couldn't even tell *who* was using it. They eventually disabled the shared account and waited for people to complain. (source: chapter-04-decomposing-the-database.md)

The lesson: **per-actor credentials matter**. Newman recommends dedicated secret stores like HashiCorp Vault that can mint short-lived, scoped, per-actor credentials. (source: chapter-04-decomposing-the-database.md)

The deeper lesson: once a database becomes a de facto public contract, **you can no longer change its schema** — at least not without a coordinated multi-team release.

## Coping patterns

If you cannot split the database right now, the following stop things getting worse and serve as stepping stones (source: chapter-04-decomposing-the-database.md):

- [[database-view-pattern]] — read-only projection that lets you change the underlying schema while preserving the consumer-facing shape.
- [[database-wrapping-service]] — turn DB dependencies into service dependencies; gate further additions to the schema.
- [[database-as-a-service-interface]] — when consumers genuinely need a database (e.g. Tableau, ad-hoc SQL), expose a separate one with a defined contract.

## Related pages

- [[database-decomposition]]
- [[information-hiding]]
- [[coupling]]
- [[cohesion]]
- [[aggregate]]
- [[database-view-pattern]]
- [[database-wrapping-service]]
- [[database-as-a-service-interface]]
- [[shared-static-data]]
