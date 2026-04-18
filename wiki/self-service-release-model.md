# Self-Service Release Model

**Summary**: The first of the four [[release-engineering-principles]]. To work at scale, teams must run their own releases. Release engineering provides tools, defaults, and best practices; individual product development teams decide **when and how often** to release. At Google this is how thousands of engineers across many products achieve high release velocity without a central release bottleneck.

**Sources**: `raw/site-reliability-engineering/chapter-08-release-engineering.md`

**Last updated**: 2026-04-17

---

## The principle

> In order to work at scale, teams must be self-sufficient. Release engineering has developed best practices and tools that allow our product development teams to control and run their own release processes. (source: chapter-08-release-engineering.md)

Two consequences follow:

1. **Teams decide cadence.** Individual teams choose how often and when to release new versions of their products. No central schedule.
2. **Automation is the default.** Release processes can be automated to the point that they require minimal engineer involvement; many projects are automatically built and released by the combined build system and deployment tools. Engineers only get involved if and when problems arise.

## Release engineering's role in a self-service model

If the teams run the releases, what is release engineering for? (source: chapter-08-release-engineering.md)

- **Tool defaults.** The tools ([[rapid-release-system|Rapid]], [[blaze-bazel|Blaze]], [[midas-package-manager|MPM]], [[sisyphus|Sisyphus]]) have to behave correctly by default. A team shouldn't have to become a build expert to get a reproducible release.
- **Documentation.** Adequate documentation so teams can stay focused on features and users, not on reinventing release processes poorly.
- **Best-practice guidance.** Compiler flags, build-identification tag formats, required build steps — all defined once, applied everywhere.
- **Telemetry and metrics.** Release engineers measure release velocity and build-configuration usage and use those numbers to improve the tools.

## Why it scales

The chapter's implicit argument: the alternative — a central release team that runs every release — doesn't scale to Google's engineer count. The self-service model routes only the **exceptional cases** (a problem, a novel process need) through release engineering, while routine releases happen without them. This is structurally the same pattern SRE itself follows with the [[toil-and-engineering-balance|50/50 split]]: push routine work into automation, keep humans for the non-routine.

## Cross-book connections

- [[microservice-creation-workflow]] (Bellemare) — the EDM-platform "paved road" that scaffolds a new service, creates its repo, CI/CD pipeline, topic ACLs, and dashboards in one step is the same self-service pattern applied at the microservice boundary
- [[team-autonomy]] (Newman / Richards & Ford) — self-service releases are the operational substrate that lets product teams actually own their services
- [[automation-at-google]] — self-service is only possible when the automation has reached [[hierarchy-of-automation-classes|level 4]]: internally maintained, robust enough that non-experts can rely on it

## Related pages

- [[release-engineering]]
- [[release-engineering-principles]]
- [[high-release-velocity]]
- [[rapid-release-system]]
- [[microservice-creation-workflow]]
- [[team-autonomy]]
