# Rapid Release System

**Summary**: Google's automated release system. Rapid orchestrates the full release lifecycle — creating release branches, running builds and tests on dedicated infrastructure, packaging artifacts into [[midas-package-manager|MPM]], executing system tests and canary deployments, and handing off to [[sisyphus]] for complicated rollouts. It is configured via **blueprints** and runs as a [[borg]] job so it can handle thousands of release requests simultaneously.

**Sources**: `raw/site-reliability-engineering/chapter-08-release-engineering.md`

**Last updated**: 2026-04-17

---

## What Rapid is

> Google has developed an automated release system called Rapid. Rapid is a system that leverages a number of Google technologies to provide a framework that delivers scalable, hermetic, and reliable releases. (source: chapter-08-release-engineering.md)

Three adjectives carry weight: **scalable** (runs on Borg so it can fan out), **hermetic** (wraps [[blaze-bazel|Blaze]] and pins build-tool versions, see [[hermetic-builds]]), **reliable** (workflows are explicit, gated, and logged).

## Blueprints

Rapid is configured with files called **blueprints**, written in an internal configuration language (source: chapter-08-release-engineering.md). A blueprint defines:

- Build and test targets.
- Rules for deployment.
- Administrative information (project owners).
- Role-based access control lists that enforce [[release-policy-enforcement|gated operations]].

Workflows inside a blueprint are the actual release steps. Workflow actions can run serially or in parallel, and one workflow can launch another.

## The typical release flow

The chapter walks through a typical run (source: chapter-08-release-engineering.md):

1. **Branch creation.** Rapid uses the requested integration revision (often obtained automatically from the continuous test system) to create a release branch. See [[release-branching-and-cherry-picking]].
2. **Build and test.** Rapid uses [[blaze-bazel|Blaze]] to compile binaries and execute unit tests, often in parallel. Compilation and testing run in **dedicated environments**, not in the Borg job where the Rapid workflow itself is executing — this separation is what makes parallelism cheap.
3. **System tests and canary.** Build artifacts are available for system testing and canary deployments. A typical canary starts a few jobs in production after system tests complete.
4. **Reporting and audit.** The results of each step are logged. A report of all changes since the last release is generated (the [[release-policy-enforcement|audit artefact]]).

Rapid also manages release branches and cherry picks: individual cherry-pick requests can be approved or rejected for inclusion in a release.

## How Rapid uses Borg

Rapid dispatches work requests to tasks running as a [[borg]] job on Google's production servers. Because Rapid rides the production infrastructure, it can handle **thousands of release requests simultaneously**. This is the same "use the cluster we already have" principle that lets [[google-monorepo|monorepo builds]] finish quickly: compute is cheap when you already own a datacenter.

## Rapid's handoff to Sisyphus

For simple deployments, Rapid drives the rollout directly: it updates Borg jobs to use newly built MPM packages based on the blueprint's deployment definitions and specialised task executors.

For **complicated deployments**, Rapid creates a rollout in a long-running [[sisyphus]] job and hands off. Rapid knows the build label associated with the MPM package it created, and passes that label to Sisyphus so the right version is deployed.

## The components

- **Blueprints** — declarative config for a Rapid project.
- **Workflows** — sequences of actions tied to a blueprint.
- **Task executors** — the code Rapid runs for each action (build, test, package, deploy).
- **Role-based ACLs** — who can launch what.
- **Borg jobs** — the runtime.

## Cross-book connections

- [[desired-state-management]] (Newman) — blueprints are declarative specs of the release process; Rapid reconciles actual release state against them
- [[operator-pattern]] (Burns) — Rapid's workflow-per-project model is structurally similar to a controller-per-workload: declarative desired state plus reconciliation
- [[continuous-integration-delivery-deployment]] (Bellemare) — Rapid is the Google-scale implementation of the CI/CD-through-CD pipeline; blueprints are the per-service pipeline configuration
- [[event-driven-batch-pattern]] (Burns) — Rapid's parallel-fan-out build/test workflow is structurally the event-driven batch pattern applied to release engineering

## Related pages

- [[release-engineering]]
- [[blaze-bazel]]
- [[midas-package-manager]]
- [[sisyphus]]
- [[release-branching-and-cherry-picking]]
- [[release-policy-enforcement]]
- [[hermetic-builds]]
- [[borg]]
- [[google-monorepo]]
