# Hermetic Builds

**Summary**: A build is **hermetic** when it is insensitive to the machine it runs on. Given the same source revision and the same versioned build tools, two builds on two machines produce identical results. Google requires this property from its build tool (open-sourced as Bazel) so that releases are reproducible, audits are trustworthy, and old releases can be rebuilt months later for bug fixes without picking up unrelated drift.

**Sources**: `raw/site-reliability-engineering/chapter-08-release-engineering.md`, `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The property

> Our builds are hermetic, meaning that they are insensitive to the libraries and other software installed on the build machine. Instead, builds depend on known versions of build tools, such as compilers, and dependencies, such as libraries. The build process is self-contained and must not rely on services that are external to the build environment. (source: chapter-08-release-engineering.md)

Restated as a test: if two people build the same product at the same revision on different machines, the results must be identical.

## What hermetic rules out

- The compiler installed on the build machine being picked up implicitly.
- System libraries in `/usr/lib` being linked.
- Network calls during the build.
- Environment variables leaking in.
- The current time being baked into the binary.

Every input has to be explicit, versioned, and self-contained.

## Why it matters: rebuilding old releases

The distinguishing test case the chapter gives is **cherry-picking onto an old branch**. Suppose a bug in production needs a fix, and that bug lives in a release cut three months ago. You want to:

1. Rebuild at the exact revision of the original release.
2. Apply the fix (a [[release-branching-and-cherry-picking|cherry pick]]).
3. Produce a new binary that differs from the old one **only by the fix**.

For this to work, the build tools themselves have to be versioned:

> Our build tools are themselves versioned based on the revision in the source code repository for the project being built. Therefore, a project built last month won't use this month's version of the compiler if a cherry pick is required, because that version may contain incompatible or undesired features. (source: chapter-08-release-engineering.md)

Without versioned build tools, the rebuild picks up whatever compiler is installed today, and the output diverges from the old release in ways unrelated to the fix. Hermetic + versioned build tools is the combination that makes cherry-picking onto old branches safe.

## Why it matters: release audit trails

[[release-policy-enforcement|Policy enforcement]] relies on knowing exactly what is in a release. The automated release system produces a report of all changes contained in a release, which SREs use when troubleshooting. That report is only trustworthy if the build output is determined entirely by the report's inputs — i.e., if the build is hermetic.

## The dual to push-on-green

[[high-release-velocity|Hourly builds]] and [[push-on-green]] depend on every build being a known, reproducible artifact. If build output could vary across machines, the hourly pool would contain mystery binaries and "this build passed tests" would not generalise. Hermetic builds are what make the high-velocity cadence safe.

## Hermeticity and trustworthy tests (Chapter 17)

Chapter 17 surfaces a testing-side consequence of hermeticity. At Google's scale, a service's test suite may depend transitively on every object in the code repository (source: chapter-17-testing-for-reliability.md). [[testing-at-scale|Practical test selection]] relies on the build tool knowing exactly what each file depends on — which is only meaningful if the build is reproducible.

Chapter 17 also credits Bazel's dependency graphs for enabling selective rebuilds: "when a change is made to a file, Bazel only rebuilds the part of the software that depends on that file" (source: chapter-17-testing-for-reliability.md). Hermeticity is what makes the graph a contract rather than a hint.

## Cross-book connections

- [[idempotence]] — hermetic building is the build-time analogue of idempotent operations: same inputs, same outputs, regardless of how many times or where you run it
- [[architecture-fitness-function]] (Richards & Ford) — "this build produces bit-identical output on two different machines" is an objective, automatable integrity check on the release pipeline
- [[data-outlives-code]] (Kleppmann) — the inverse case: code outlives its build environment; hermetic builds are the discipline that keeps old code rebuildable

## Related pages

- [[release-engineering]]
- [[release-engineering-principles]]
- [[release-branching-and-cherry-picking]]
- [[rapid-release-system]]
- [[push-on-green]]
- [[testing-for-reliability]]
- [[testing-at-scale]]
- [[build-system-discipline]]
