# Least Privilege

**Summary**: A security principle central to the [[data-security]] undercurrent of the [[data-engineering-lifecycle]]: give every user or system access to only the essential data and resources needed to perform an intended function — and nothing more.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md`

**Last updated**: 2026-04-18

---

## Definition

"Giving a user or system access to only the essential data and resources to perform an intended function" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Antipatterns the principle prevents

Reis and Housley name two concrete bad habits the principle is meant to correct (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

1. **Giving admin access to everyone.** A "catastrophe waiting to happen." Users should get exactly the access they need to do their job today and no more.
2. **Engineers working as superuser by default.** Don't operate from a root shell when standard user access suffices; don't query with the superuser role in a database when a reader role would do.

The second point matters even for internal data engineering: running as superuser makes routine mistakes (accidental drops, mis-scoped updates) far more destructive than they need to be.

## Why it works

Least privilege is about **blast radius**. If every user and system has only narrow access, a compromised credential or a human mistake damages only a narrow slice. Contrast with admin-everywhere: a single compromised laptop or one fat-finger query destroys everything.

The principle also keeps engineers in a **security-first mindset** — imposing least privilege on yourself trains the habit of asking "what do I actually need access to?" which transfers to how you design access policies for others (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Time-boxing and revocation (Chapter 10)

Chapter 10 extends the principle beyond "minimum scope" to also include **minimum duration** (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

> Provide the user (or group they belong to) the IAM roles they need when they need them. When these roles are no longer needed, take them away. The same rule applies to service accounts. Treat humans and machines the same way: give them only the privileges and data they need to do their jobs, and only for the timespan when needed.

The operational implication: permissions drift *accumulates* — an analyst granted Redshift access for a six-week project may still have it six years later. [[security-monitoring|Security monitoring]] tools that auto-alert (or auto-revoke) on unused permissions turn the principle from a one-time grant decision into an ongoing control.

## Column/row/cell-level and masking

For sensitive data, least privilege extends *inside the table* (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

- **Column-level access controls** — some columns (SSN, email, salary) visible only to specific roles.
- **Row-level access controls** — analysts see only rows scoped to their region, department, or customer.
- **Cell-level access controls** — fine-grained redaction.
- **PII masking** — hash or tokenise sensitive values so downstream consumers can still join and aggregate but cannot read the raw identifier. See also [[data-ethics]].
- **Views over base tables** — create views containing only the columns the viewer needs; grant access to the view rather than the underlying table.

These are the mechanisms by which "need-to-know" becomes enforceable rather than aspirational.

## Broken-glass access

Some data must be retained for compliance or emergencies but should not be routinely accessible. Chapter 10 names the pattern (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

> Put this data behind a broken glass process: users can access it only after going through an emergency approval process to fix a problem, query critical historical information, etc. Access is revoked immediately once the work is done.

Properties of a well-designed broken-glass process:

- **Explicit approval step** — a human signs off, with the request recorded.
- **Time-bounded access** — access expires on its own, not when someone remembers to revoke it.
- **Auditable trail** — every broken-glass event is logged for post-hoc review.
- **Alerting** — broken-glass events trigger [[security-monitoring|security monitoring]] notifications so misuse is caught.

The parallel to [[break-glass-push]] in SRE is deliberate — same cultural pattern applied to a different domain.

## Related pages

- [[data-security]]
- [[data-engineering-lifecycle]]
- [[data-governance]]
- [[defense-in-depth-data]]
- [[event-stream-acls]]
- [[security-monitoring]]
- [[secrets-management]]
- [[break-glass-push]]
