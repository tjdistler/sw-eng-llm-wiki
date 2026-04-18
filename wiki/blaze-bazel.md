# Blaze / Bazel

**Summary**: Google's internal build tool, open-sourced as **Bazel**. Blaze builds binaries from a range of languages (C++, Java, Python, Go, JavaScript) given declarative **build targets** with explicit **dependency lists**. It is the mechanism that makes [[hermetic-builds]] possible at Google and the substrate [[rapid-release-system|Rapid]] invokes for every release.

**Sources**: `raw/site-reliability-engineering/chapter-08-release-engineering.md`

**Last updated**: 2026-04-17

---

## What Blaze does

> Blaze is Google's build tool of choice. It supports building binaries from a range of languages, including our standard languages of C++, Java, Python, Go, and JavaScript. (source: chapter-08-release-engineering.md)

Engineers use Blaze to:

- Define **build targets** — the output of a build, such as a JAR file or a binary.
- Specify the **dependencies** for each target.
- Let Blaze automatically build the transitive dependency graph when a target is requested.

Project-specific flags (like a unique build identifier) are passed by Rapid to Blaze during a release. All binaries support a standard flag that displays the build date, revision number, and build identifier — so every deployed binary can be traced back to a specific build.

## Open-sourced as Bazel

The chapter notes:

> Blaze has been open sourced as Bazel. See "Bazel FAQ" on the Bazel website. (source: chapter-08-release-engineering.md)

Bazel is the externally usable form of the same tool and is the reference implementation of the dependency-graph-plus-hermetic-build model for public consumption.

## Why it matters for release engineering

Blaze is the concrete mechanism behind several of the [[release-engineering-principles|four principles]]:

- **Hermetic** — Blaze pins tool versions and dependency versions; same inputs always produce the same outputs. See [[hermetic-builds]].
- **High velocity** — the dependency graph is complete and cacheable, so builds are fast enough to run hourly.
- **Policy enforcement** — Blaze's declarative `BUILD` files are themselves source-controlled and subject to code review ([[release-policy-enforcement]] enumerates "making changes to a project's build configuration" as a gated operation).

Blaze also lets [[midas-package-manager|MPM]] work: MPM assembles packages based on Blaze rules that list the build artifacts to include along with their owners and permissions.

## Cross-book connections

- [[monorepo]]-friendly tooling is a category Bazel essentially defined; [[google-monorepo]] presupposes a build tool with Bazel's properties
- [[desired-state-management]] (Newman) — a `BUILD` file is a declarative spec of what a target *should* contain; Blaze reconciles actual build outputs against it
- [[unix-philosophy]] (Kleppmann) — Blaze is the opposite of Make's shell-plumbing approach: explicit graph, no implicit filesystem state, hermetic

## Related pages

- [[release-engineering]]
- [[hermetic-builds]]
- [[rapid-release-system]]
- [[midas-package-manager]]
- [[google-monorepo]]
