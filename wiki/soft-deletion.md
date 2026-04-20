# Soft Deletion

**Summary**: Chapter 26's first layer of [[defense-in-depth-data|defence in depth]]. **Soft deletion** marks data as deleted so it's invisible to normal application paths but still recoverable by administrative code. A grace period (commonly 15–60 days) passes before the data is actually destroyed. **Lazy deletion** is the storage-service counterpart: data deleted by an application becomes inaccessible to that application but is preserved by the cloud provider for up to a few weeks. Together they are the primary defence against accidental deletion by users, application developers, and hijackers.

**Sources**: `raw/site-reliability-engineering/chapter-26-data-integrity-what-you-read-is-what-you-wrote.md`

**Last updated**: 2026-04-17

---

## Why soft deletion is the first layer

When velocity is high and privacy matters, bugs in applications account for the vast majority of data-loss and corruption events (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md). The ability to **undelete data for a limited time** becomes the primary defence against the majority of otherwise permanent, inadvertent loss.

Soft deletion is also the cheapest of the three layers — no data is copied, only a flag is set, and a background job reaps expired items. It scales to arbitrary data volumes at roughly the cost of one boolean per record.

## The three user categories it protects against

Chapter 26 names three distinct accidental-deletion sources, each defended at a different tier of the soft-deletion stack:

1. **End users** — accidental deletion via the UI. The **trash folder** is the classic pattern: deleted items live there until emptied, and users can drag them back. Gmail's 30-day trash is the canonical example (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md).
2. **Application developers** — bugs in new or refactored code that delete too much. Soft deletion at the application level means deletion-bug impact is recoverable within the grace window.
3. **Hijackers** — attackers who compromise an account and delete the original user's data before spamming. Admin undelete restores the data when the user recovers the account.

## The trash folder pattern

The user-facing surface. Key properties:

- Deletion looks instantaneous from the user's perspective.
- Trash contents remain searchable and retrievable through a dedicated UI.
- Emptying the trash triggers the actual soft delete (application-level marking).
- After the retention window, hard deletion occurs.

## Administrative undelete

Behind the trash folder, soft-deleted data is visible to a narrow set of administrative code paths (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

- Legal discovery
- Hijacked-account recovery
- Enterprise administration
- User support
- Troubleshooting

Google implements this strategy for its most popular productivity applications. Without it, the user-support engineering burden would be untenable.

## Lazy deletion (the developer-facing counterpart)

For cloud platforms that serve developer customers, a second layer underneath application-level soft deletion. Definition (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> In a lazy deletion scenario, data that is deleted by a cloud application becomes immediately inaccessible to the application, but is preserved by the cloud service provider for up to a few weeks before destruction.

Where soft deletion is controlled by the **client application**, lazy deletion is controlled by the **storage system**. The contrast:

| Layer | Controlled by | Visibility to app after delete | Primary defence against |
|---|---|---|---|
| Trash folder | Application UI | Yes (in trash) | End-user error |
| Soft deletion | Application server | No (except admin paths) | Developer bug, account hijack |
| Lazy deletion | Cloud storage provider | No | Internal developer bug, customer developer bug |

Lazy deletion is the chapter's response to: *the application developer just wrote a pipeline that deletes 600,000 audio tracks by accident. How do we get them back?*

## The Blobstore example

Chapter 26's worked example of the idea (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> Rather than allow customers to delete Blob data and metadata directly, the Blob APIs implement many safety features, including default backup policies (offline replicas), end-to-end checksums, and default tombstone lifetimes (soft deletion). It turns out that on multiple occasions, soft deletion saved Blobstore's clients from data loss that could have been much, much worse.

The insight: a storage API that bakes in soft deletion protects developer customers whether or not they ask for it, and turns many otherwise-catastrophic bugs into recoverable ones.

## Retention window selection

Common choices: **15, 30, 45, or 60 days**. Factors (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

- Organisation's policies and applicable laws.
- Storage resource cost.
- Product pricing and market positioning, especially for short-lived data.
- Empirical recovery-request patterns.

Google's own data: *the majority of account hijacking and data integrity issues are reported or detected within 60 days*. So soft-deleting for longer than 60 days offers diminishing returns.

Lazy deletion has a harder ceiling. A long lazy-deletion window is **costly** in systems with a lot of short-lived data, and **impractical** in systems with privacy-driven deletion deadlines (data must be destroyed within a reasonable time). The retention choice is a trade-off against the [[data-integrity-sre|privacy]] requirement.

## Batch-pipeline developer as the danger class

The chapter names the most devastating class of acute data-deletion cases (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> The most devastating acute data deletion cases are caused by application developers unfamiliar with existing code but working on deletion-related code, especially batch processing pipelines (e.g., an offline MapReduce or Hadoop pipeline).

The architectural response: build soft deletion into the storage API so developers writing new code *can't bypass it by accident*. If the API makes the only deletion path a tombstone-with-TTL, a developer unfamiliar with the code can't write a pipeline that hard-deletes data even if they try.

A 2012 batch-pipeline incident at Google is this class of bug exactly — a refactored deletion pipeline introduced a race condition that removed data the soft-deletion layer never had a chance to protect.

## Summary of layer 1 defences

The chapter's own summary (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

- A **trash folder** that allows users to undelete data is the primary defence against user error.
- **Soft deletion** is the primary defence against developer error and the secondary defence against user error.
- In developer offerings, **lazy deletion** is the primary defence against internal developer error and the secondary defence against external developer error.

## Revision history as a partial substitute

Some products let users revert items to previous states. When user-facing, it's a form of trash. When developer-facing, it may or may not substitute for soft deletion — *some revision-history implementations treat deletion as a special case in which previous states must be removed*, destroying the history along with the item (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md). To provide adequate protection, apply the same lazy and soft-deletion principles to revision history.

## Related pages

- [[data-integrity-sre]]
- [[defense-in-depth-data]]
- [[tiered-backup-strategy]]
- [[data-validation-pipelines]]
- [[data-integrity-failure-modes]]
