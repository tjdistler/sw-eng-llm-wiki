# Pattern: Database Wrapping Service

**Summary**: Place a thin service in front of a problematic shared schema so that database dependencies become service dependencies. The mess is hidden, the schema stops growing, and consumers can be migrated to a proper interface even though the underlying schema hasn't been split.

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## The pattern

When a schema is too tangled to extract from, you wrap it in a thin service. The service's API becomes the only legitimate way to access the data. New consumers (and, eventually, old ones) talk to the service instead of the schema. (source: chapter-04-decomposing-the-database.md)

This converts what used to be hidden, schema-level [[coupling]] into explicit service-level coupling — a much better starting point.

## The Australian bank entitlements story

Newman recounts a large Australian bank whose business-banking entitlements system had grown over 30 years inside the database, with logic encoded in stored procedures. The DBA's plea: "Stop them from putting things into the database!" Pulling the entitlements logic apart was too risky; a wrong step could lock customers out of their own accounts. (source: chapter-04-decomposing-the-database.md)

The pragmatic answer: introduce a new `Entitlements` service that wrapped the existing schema. The service had very little behaviour at first — most logic was still in the stored procedures — but it gave them three things (source: chapter-04-decomposing-the-database.md):

1. **A point of governance.** Other teams now had a defined API to call instead of writing into the schema directly.
2. **A signal to teams** to keep their own data local and treat the entitlements schema as someone else's.
3. **Headroom to extract.** Once the new schema's growth was under control, easier parts of the entitlements data could be extracted to relieve database load.

## Where to use it

This pattern works well when the underlying schema is *too hard to consider pulling apart*. By placing an explicit wrapper around it and making clear that data can only be accessed through that wrapper, you put a brake on further growth. It clearly delineates "yours" vs "someone else's." (source: chapter-04-decomposing-the-database.md)

Newman's caveats (source: chapter-04-decomposing-the-database.md):

- **Align ownership.** The team that owns the underlying schema should also own the wrapping service; otherwise the API becomes another battleground.
- **Treat the service API as a managed interface** — the same care you'd give a public API.
- **Easier to test against.** Upstream consumers can stub the API instead of the database.

## Compared to a database view

A wrapping service has real advantages over [[database-view-pattern]] (source: chapter-04-decomposing-the-database.md):

- It can present richer projections than the underlying tables make easy.
- It can take **writes** via API calls (views typically can't).
- It is not constrained to the same database engine.

The cost: upstream consumers must change from direct DB access to API calls.

## Bandage or stepping stone?

Newman acknowledges this can look like "putting a bandage on the problem." But in the spirit of [[incremental-migration]], it is genuinely useful: it stops the bleeding, gives the team time to break apart the schema underneath the API, and is a safer cutover than trying to do everything at once. Ideally it is a stepping stone to deeper decomposition, not the destination. (source: chapter-04-decomposing-the-database.md)

## Related pages

- [[database-decomposition]]
- [[shared-database-antipattern]]
- [[database-view-pattern]]
- [[database-as-a-service-interface]]
- [[information-hiding]]
- [[aggregate-exposing-monolith]]
- [[incremental-migration]]
