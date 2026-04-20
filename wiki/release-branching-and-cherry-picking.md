# Release Branching and Cherry Picking

**Summary**: Google's branch strategy for major projects. All code is checked into the **main branch** (mainline). For a release, a project **branches from a specific revision** of the mainline and **never merges the branch back**. Bug fixes are submitted to the mainline first and then **cherry-picked** into the release branch. This yields exact control over what each release contains — unrelated mainline changes cannot sneak in.

**Sources**: `raw/site-reliability-engineering/chapter-08-release-engineering.md`

**Last updated**: 2026-04-17

---

## The model

> All code is checked into the main branch of the source code tree (mainline). However, most major projects don't release directly from the mainline. Instead, we branch from the mainline at a specific revision and never merge changes from the branch back into the mainline. Bug fixes are submitted to the mainline and then cherry picked into the branch for inclusion in the release. (source: chapter-08-release-engineering.md)

Three rules:

1. **All code goes to mainline first.** There is no "release branch that developers work on." Release branches are downstream of mainline, not upstream.
2. **Never merge back.** A release branch is a read-only snapshot with selective additions, not a parallel universe of development.
3. **Cherry pick for fixes.** Bug fixes are landed on mainline, reviewed, and then selectively applied to the release branch.

## Why this is different from GitFlow

The more familiar GitFlow-style "develop branch, release branch, merge back" model would not give Google what this model gives them:

> This practice avoids inadvertently picking up unrelated changes submitted to the mainline since the original build occurred. Using this branch and cherry pick method, we know the exact contents of each release. (source: chapter-08-release-engineering.md)

The guarantee is **precise knowledge of the diff**. The release branch contains exactly the mainline state at branch time plus exactly the cherry picks that were approved. Nothing else.

## What cherry picking requires

For this to work, two other properties have to hold:

- [[hermetic-builds]] — rebuilding the branch produces a deterministic binary that differs from the original only by the cherry picks. The chapter explicitly calls out that build tools themselves are versioned so a rebuild months later uses last month's compiler, not this month's.
- **Test the branch, not just mainline** — during the release process, unit tests are re-run on the release branch, because if the branch contains cherry picks, it may contain a version of the code that doesn't exist anywhere on the mainline (source: chapter-08-release-engineering.md). This produces an audit trail that all tests passed on *the exact thing being released*.

## Gated approval for cherry picks

Each cherry-pick request is independently approved or rejected for inclusion in the release ([[release-policy-enforcement|gated operation]] #4). [[rapid-release-system|Rapid]] manages the approval workflow. This prevents the release branch from quietly accumulating unreviewed fixes.

## Cross-book connections

- [[strangler-fig-pattern]] (Newman) — the no-merge-back property is structurally the same discipline: once you've moved past something, you don't re-converge
- [[event-sourcing]] (Kleppmann) — the release-branch-plus-cherry-picks stream is analogous to an event-sourced state: a base snapshot plus a log of additive operations

## Related pages

- [[release-engineering]]
- [[release-engineering-principles]]
- [[hermetic-builds]]
- [[release-policy-enforcement]]
- [[rapid-release-system]]
