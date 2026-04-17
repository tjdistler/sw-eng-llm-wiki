# Schema Change Notifications

**Summary**: A tool that subscribes to [[schema-registry]] updates and automatically notifies every team whose microservices consume a stream whose schema has evolved. Alerts route via the [[microservice-to-team-assignment]] system and are resolved through the [[event-stream-acls|ACLs]] that map streams to consuming services.

**Sources**: `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`

**Last updated**: 2026-04-17

---

## The problem

With many event streams and hundreds of services, a schema change that a producer makes — even a compatible one — has a large but unknown **blast radius**. Consumers might review every upstream change in a perfect world, but in practice they won't. Silent incompatible changes become production crises (source: chapter-14-supportive-tooling.md).

## How the notification pipeline works

The chain of information (source: chapter-14-supportive-tooling.md):

1. A producer registers an evolved schema with the [[schema-registry]]. Using Confluent's registry, this appears as a message on the dedicated schema event stream.
2. The notification tool consumes the schema stream.
3. For each evolved schema, it resolves the set of streams that reference it.
4. It cross-references the [[event-stream-acls|ACLs]] on those streams to identify all microservices holding `READ`.
5. It uses [[microservice-to-team-assignment]] to resolve each of those microservices to its owning team.
6. It notifies each owning team.

## What the tool gives you

- **A safety net for breaking-change detection** — even if the evolution is syntactically [[backward-forward-compatibility|backward compatible]], consumers often need to update code to take advantage of new fields or handle a changed default. Notification turns this from "hope they noticed" into "they were told."
- **Broad schema-change awareness** — a team may opt in to notifications on *all* public schemas across the business, giving analysts and platform teams a live feed of how the data model is evolving.
- **Audit trail** — combined with the [[event-stream-acls|ACL change stream]], schema evolutions become a durable, timestamped record of how interfaces moved.

## Relationship to existing wiki coverage

- **[[schema-evolution]]** — the rules for compatible change. Notifications sit on top of them.
- **[[breaking-changes]]** — Bellemare's "communicate early" rule is operationalized by this tool. The notification system is part of how the communication happens.
- **[[data-contract]]** — the notifier ensures that the implicit social contract around a data contract is made explicit.

## Related pages

- [[edm-supportive-tooling]]
- [[schema-registry]]
- [[schema-evolution]]
- [[breaking-changes]]
- [[data-contract]]
- [[event-stream-acls]]
- [[microservice-to-team-assignment]]
