# Release Engineering

**Summary**: A relatively new and fast-growing engineering discipline concerned with **building and delivering software**. Release engineers understand source code management, compilers, build configuration languages, automated build tools, package managers, and installers; they define how software moves from source to production. At Google it is a named job function that works alongside SWEs in product development and SREs to make releases repeatable rather than "unique snowflakes."

**Sources**: `raw/site-reliability-engineering/chapter-08-release-engineering.md`

**Last updated**: 2026-04-17

---

## The discipline

> Release engineering is a relatively new and fast-growing discipline of software engineering that can be concisely described as building and delivering software. (source: chapter-08-release-engineering.md)

Running reliable services requires reliable release processes. SREs need to know that the binaries and configurations they run are built reproducibly and automatically, so that releases are repeatable and aren't unique snowflakes. Changes to the release process should be intentional, not accidental.

Release engineering covers the whole path from source to deployment:

- How source is stored in the repository
- Build rules for compilation
- Testing
- Packaging
- Deployment

## The role of a release engineer

At Google, release engineering is a specific job function. Release engineers (source: chapter-08-release-engineering.md):

- Work with SWEs and SREs to define every step required to release software
- Build and maintain the tooling that implements the release process
- Define best practices for using that tooling (compiler flags, build-identification tags, required build steps) so project teams don't reinvent the wheel poorly
- Collect metrics on how releases actually behave — release velocity, feature usage in build configuration files — and iterate on the tools

The chapter frames release engineering as **data-driven**: most of Google's release tools were envisioned and developed by release engineers, and the discipline continuously feeds its own telemetry back into tool evolution.

Release engineers and SREs together develop strategies for [[progressive-delivery|canarying changes]], pushing out new releases without interrupting services, and rolling back features that demonstrate problems.

## The four guiding principles

Release engineering at Google is guided by four principles, each with its own page:

- [[release-engineering-principles]] — hub for all four
- [[self-service-release-model]] — teams run their own releases; release engineering provides tools and best practices
- [[high-release-velocity]] — frequent releases yield fewer changes per version, making testing and troubleshooting easier
- [[hermetic-builds]] — builds are reproducible and insensitive to the machine they run on; cherry-picking onto older revisions works because build tools are versioned too
- [[release-policy-enforcement]] — gated operations for who can approve CLs, create releases, approve cherry picks, and deploy

## The tooling stack

Google's continuous build and deployment system is assembled from a set of purpose-built components, of which one has a page here:

- [[rapid-release-system]] — the automated release system; runs workflows on [[borg]]; blueprints define build/test/deploy actions

Beyond it sit a hermetic dependency-graph-driven build tool (open-sourced as Bazel), a content-addressed package manager with movable labels (dev / canary / production), and a general-purpose rollout automation framework — all running from a single shared monorepo.

## Branching, testing, and cherry picks

- [[release-branching-and-cherry-picking]] — all code lands on mainline; projects branch from a specific revision and never merge back; bug fixes go to mainline and are cherry-picked into the branch
- Continuous testing on the mainline plus re-running tests on the release branch (so that cherry-picked content is validated in the context of what's actually being released)

## Configuration management

Configuration changes are a leading source of instability. The chapter lays out four patterns for distributing configuration files and lets project owners pick on a case-by-case basis — see [[configuration-management-sre]].

All four patterns share two rules: configuration lives in the primary source repository, and changes go through the same strict code review as code.

## The "start at the beginning" lesson

Release engineering is often an afterthought. The chapter argues this has to change (source: chapter-08-release-engineering.md):

- Budget for release engineering resources at the **beginning** of the product development cycle.
- It is cheaper to put good practices in place early than to retrofit later.
- Developers should not build and throw results over the fence to release engineers.
- Individual teams decide when release engineering becomes involved; managers often don't plan for it, so teams must do it themselves.

## "It's not just for Googlers"

The chapter ends by insisting that these ideas generalise (source: chapter-08-release-engineering.md). Every company, regardless of size, faces the same questions:

- How do you version packages?
- Continuous build and deploy, or periodic?
- How often should you release?
- What configuration management policies should you use?
- What release metrics matter?

Google built custom tools because open-source and vendor tools don't work at Google's scale, and because custom tools let them enforce policy. But the **policies must be defined first** regardless of whether the tools exist to enforce them. Defining your release process is the step no company can skip.

## Cross-book connections

- [[continuous-integration-delivery-deployment]] (Bellemare) — Rapid plus the hermetic build tool and package manager implement continuous delivery at the repository scale; Bellemare's per-service EDM pipeline is the microservice analogue
- [[progressive-delivery]] (Newman / Burns) — the canary, dark launch, and staged rollout techniques the release and rollout tools orchestrate at scale
- [[deployment-vs-release]] (Newman) — the package manager separates "built and packaged" from "deployed" via movable labels (dev / canary / production); moving a label promotes a package without rebuilding
- [[change-management-sre]] — release engineering is the discipline that implements the "progressive rollout + quick detection + safe rollback" trio
- [[automation-at-google]] — the release and rollout tools are level-4 internally-maintained system-specific automation; the discipline builds the tools that let SREs remain engineers not operators

## Related pages

- [[release-engineering-principles]]
- [[self-service-release-model]]
- [[high-release-velocity]]
- [[hermetic-builds]]
- [[release-policy-enforcement]]
- [[rapid-release-system]]
- [[release-branching-and-cherry-picking]]
- [[configuration-management-sre]]
- [[push-on-green]]
- [[change-management-sre]]
- [[progressive-delivery]]
- [[continuous-integration-delivery-deployment]]
- [[site-reliability-engineering]]
