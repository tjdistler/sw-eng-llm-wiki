# Event Stream Metadata

**Summary**: Tags attached to event streams that record ownership, sensitivity, namespace, deprecation status, and other organization-specific attributes. Metadata is the input to access decisions, data discovery, stream-cleanup workflows, and regulatory handling — and it must be editable only by the stream's owning team.

**Sources**: `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`

**Last updated**: 2026-04-17

---

## The standard tag set

Bellemare's recommended baseline (source: chapter-14-supportive-tooling.md):

| Tag | Purpose |
|---|---|
| **Stream owner (service)** | Which microservice produces this stream. Anchors change-request routing and audit; redundant with [[single-writer-principle|single-writer]] ACLs but cheaper to read. |
| **PII** | Personally identifiable information. Triggers access restrictions — consumers must get explicit approval from the owning team. |
| **Financial information** | Anything pertaining to money, billing, or revenue events. Similar handling to PII but not identical. |
| **Namespace** | A descriptor aligned with nested [[bounded-context|bounded contexts]]. A stream in namespace *X* can be hidden from services outside *X*, reducing discovery noise for browsing users. |
| **Deprecation** | Marks a stream as outdated or superseded. Existing consumers keep reading; new subscriptions are blocked. Owner is notified when the consumer list empties so the stream can be deleted. |
| **Custom tags** | Any other attribute the business cares about. |

## Who can change metadata

Only teams that **own the production rights** to a stream can add, modify, or remove its tags (source: chapter-14-supportive-tooling.md). This is enforced via the [[microservice-to-team-assignment]] system — a team's identity is looked up, cross-referenced against the [[event-stream-acls|ACLs]], and the edit is allowed or rejected.

## Deprecation workflow

The deprecation tag carries a specific lifecycle. It is the usual answer when a **breaking schema change** needs to be made that cannot be absorbed via compatible [[schema-evolution|schema evolution]]:

1. Owner creates a new stream with the incompatible schema; new events flow there.
2. Owner tags the old stream **deprecated**. New consumers are blocked from subscribing; existing consumers are grandfathered in.
3. [[schema-change-notifications|Notifications]] alert the owning teams of all current consumers to migrate.
4. When the consumer list drops to zero, the owner is notified and may safely delete the old stream.

## PII and financial: access gating

Marking a stream PII or financial typically triggers centralized review when a team requests `READ` on it. The [[event-stream-acls|ACL system]] reads the metadata and routes the request through security review rather than directly to the owning team (source: chapter-14-supportive-tooling.md).

## Namespaces and data discovery

As event stream counts grow into the hundreds or thousands, discovery becomes a noise problem. Namespace tags let the discovery UI (often the [[dependency-tracking-and-topology-visualization|topology visualizer]]) filter streams by [[bounded-context]], so a developer sees only the ~10 streams in their subdomain and the public streams, not every internal stream in the company (source: chapter-14-supportive-tooling.md).

## Related pages

- [[edm-supportive-tooling]]
- [[event-stream-acls]]
- [[microservice-to-team-assignment]]
- [[bounded-context]]
- [[schema-evolution]]
- [[single-writer-principle]]
- [[dependency-tracking-and-topology-visualization]]
