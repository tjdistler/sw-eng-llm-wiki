# Release Policy Enforcement

**Summary**: The fourth of the four [[release-engineering-principles]]. Several layers of **security and access control** determine who can perform specific operations during a release: approving source code changes, specifying release actions, creating a new release, approving integration proposals and cherry picks, deploying, and modifying build configuration. Gated operations plus an auto-generated change report give SREs an auditable understanding of what is actually in each release.

**Sources**: `raw/site-reliability-engineering/chapter-08-release-engineering.md`

**Last updated**: 2026-04-17

---

## The gated operations

> Several layers of security and access control determine who can perform specific operations when releasing a project. (source: chapter-08-release-engineering.md)

The chapter enumerates six (source: chapter-08-release-engineering.md):

1. **Approving source code changes** — managed through configuration files scattered throughout the codebase.
2. **Specifying the actions to be performed during the release process**.
3. **Creating a new release**.
4. **Approving the initial integration proposal** (a request to perform a build at a specific revision) **and subsequent cherry picks**.
5. **Deploying a new release**.
6. **Making changes to a project's build configuration**.

Each is a separate permission, each is independently auditable, and each is evaluated by the release tooling rather than by humans remembering to check.

## Code review as the first layer

Almost all changes to the codebase require a code review, integrated into the normal developer workflow (source: chapter-08-release-engineering.md). This is the CL-to-owner pattern that ships with a shared monorepo: a file's owners, listed in in-repo configuration, must approve changes to it before submission.

## The release report

The automated release system produces a report of all changes contained in a release, archived alongside other build artifacts. The report's value (source: chapter-08-release-engineering.md):

> By allowing SREs to understand what changes are included in a new release of a project, this report can expedite troubleshooting when there are problems with a release.

This is the payoff of the whole policy-enforcement stack: the release is not just gated but **documented**, and the documentation is generated mechanically rather than composed by hand.

## Why tool-enforced matters

The chapter's argument for building custom tools rather than buying them (from the "It's Not Just for Googlers" section) leans on enforcement:

> Custom tools allow us to include functionality to support (and even enforce) release process policies. However, these policies must first be defined in order to add appropriate features to our tools.

Enforcement cannot be retrofitted onto a loose process. The sequence has to be: define the policy, then build the tools that enforce it. A release process that exists only as a wiki page or a habit will drift.

## Relation to [[hermetic-builds]]

Policy enforcement and hermetic builds compose: the release report is only trustworthy if the build from those CLs at those versions actually produces the archived binaries. Without hermetic builds, the audit trail describes what *should* be in the binary rather than what is.

## Cross-book connections

- [[architecture-governance]] (Richards & Ford) — release policy enforcement is architectural governance realised in the build/deploy layer; fitness functions are the equivalent for architecture characteristics
- [[code-ownership-models]] (Newman) — the CL-review file-owner model is strong ownership at the file level inside a collectively visible repository
- [[architecture-decision-record]] (Richards & Ford) — ADRs are the analogue for architecture decisions: who approves, what's decided, what's recorded
- [[event-stream-acls]] (Bellemare) — per-stream access control is the EDM-platform analogue of gated release operations

## Related pages

- [[release-engineering]]
- [[release-engineering-principles]]
- [[hermetic-builds]]
- [[release-branching-and-cherry-picking]]
- [[architecture-governance]]
