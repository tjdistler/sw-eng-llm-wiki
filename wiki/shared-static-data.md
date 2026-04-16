# Shared Static Data

**Summary**: Static reference data like country codes, currency codes, and dress sizes presents a recurring decomposition question — should every service have its own copy? Read from a shared schema? Use a library? Call a service? Newman walks through four patterns and says, "It depends — here's how to choose."

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## Why this is its own topic

Country codes, postal codes, currency codes, ISO sizes — small, slow-changing, structurally simple data. It often ends up in the database "because that's where data goes," but that's not the only option. Newman is mildly bemused by how often country codes live in databases: there are only 249 entries in ISO 3166-1, and the last new country (South Sudan) was created in 2011. (source: chapter-04-decomposing-the-database.md)

The four patterns below all have legitimate uses. The choice depends on (a) volume of data, (b) frequency of change, and (c) whether services need to agree on the data exactly at all times.

## Pattern: Duplicate static reference data

Each service stores its own copy of the data. (source: chapter-04-decomposing-the-database.md)

Two objections people raise:

- **"I have to update it in many places."** True, but how often does this data change? For country codes, very rarely.
- **"What if copies disagree?"** Often that's fine. If `Warehouse` only uses country codes locally for "where was this CD made?" and `Finance` uses them for sales records, the two services don't need to agree on whether South Sudan exists for their respective purposes to work.

The key test from Newman: **does the data participate in cross-service communication?** If it's used purely *within* each [[bounded-context]], duplication is fine — that's exactly what bounded contexts are for. If services need to agree on it for inter-service communication, duplication is dangerous.

You can also keep the copies eventually-consistent with a background sync ([[eventual-consistency]]).

**Where to use:** Newman says "rarely." Larger volumes of data where exact consistency isn't essential — postal-code files, for instance.

## Pattern: Dedicated reference data schema

Move the static data into its own schema — perhaps a single shared schema for all reference data. (source: chapter-04-decomposing-the-database.md)

This re-introduces the [[shared-database-antipattern]], but the concerns are softened by the nature of the data: it changes infrequently, it's simply structured, and you can treat the schema as a versioned interface.

Allows services to use the data in joins on their own local data, but only if the schemas live on the same database engine — adding logical/physical coupling.

**Where to use:** Large volumes of data, or where you want cross-schema joins. Breaking changes to the schema will hurt across all consumers, so manage it carefully.

## Pattern: Static reference data library

Bundle the data into a shared library that any service can link. (source: chapter-04-decomposing-the-database.md)

Stitch Fix uses this — Randy Shoup (then VP of engineering) describes the sweet spot as small-volume, slow-changing data with plenty of advance warning when changes do happen. Classic clothes sizes (XS / S / M / L / XL), inseam measurements, and similar.

The downside is the **lock-step release** problem: if you need every service to immediately see the new value, you must redeploy them all at once — exactly what microservices are designed to avoid. Newman's relief: in practice, this data changes with months of lead time. New countries are not created on a whim.

You also need to accept that services will run *different versions* of the library at different times.

**Drawbacks:**
- Doesn't work cleanly across heterogeneous tech stacks (no single shared library).
- Different versions in production simultaneously must be acceptable.

**Where to use:** Small volumes, infrequent changes, language-homogeneous services.

## Pattern: Static reference data service

Create a dedicated microservice just for the reference data. (source: chapter-04-decomposing-the-database.md)

This divides Newman's audiences. People in environments with low cost of creating a new service ("press a button, get a service in production") love it. People in environments where new services take weeks of approvals are horrified.

Newman: "If, on the other hand, I could spin up a service template and push it to production in the space of a day or less, and have everything done for me, then I'd be much more likely to consider this as a viable option." Function-as-a-Service platforms (AWS Lambda, Azure Functions) make this very cheap and would suit a `CountryCodes` service well.

The latency concern (an extra network call) is usually overblown. The dataset fits trivially in memory; the service can serve it directly with no datastore. Aggressive client-side caching plus an event-driven invalidation when the data does change makes the cost negligible.

**Where to use:** When the *life cycle* of the data — adding new entries, exposing an update API, emitting events on change — needs a place to live. Then a service is the natural home. (source: chapter-04-decomposing-the-database.md)

## Newman's recommendation

Given the choice, Newman would:

- Use a **shared library** for small, simple, slow-changing data when services don't need exact consistency.
- Use the **local service database** for more complex or larger reference data.
- Create a **dedicated service** when services *do* need consistent views of the data (or you want a shared reference-data service spanning many such datasets).
- Reach for the **dedicated schema** only if creating a service is too expensive in your environment.

(source: chapter-04-decomposing-the-database.md)

## Related pages

- [[database-decomposition]]
- [[shared-database-antipattern]]
- [[bounded-context]]
- [[information-hiding]]
- [[eventual-consistency]]
- [[independent-deployability]]
- [[coupling]]
