# Google Monorepo

**Summary**: Google software engineers (outside a few open-source projects like Android and Chrome) work from a **single shared repository**. This shapes the development workflow in specific ways: cross-project fixes as a first-class pattern, mandatory code review, a central build service that compiles in parallel on datacenter-scale hardware, continuous testing on every change, and **push-on-green** as the end state for some projects.

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`, `raw/site-reliability-engineering/chapter-08-release-engineering.md`

**Last updated**: 2026-04-17

---

## The implications

Chapter 2 calls out a small number of practical consequences of the single-repo model (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

- **Cross-project fixes are normal.** If engineers encounter a problem in a component outside their project, they can fix it, send the proposed changes ("**changelist**" or CL) to the owner for review, and submit to the mainline.
- **All changes are reviewed.** Own-project changes still require a code review. No code lands without one.
- **Central build service.** When software is built, the build request is sent to build servers in a datacenter. Large builds still finish quickly because many build servers can compile in parallel.
- **Continuous testing.** Each CL runs tests on everything that may depend on it — directly or indirectly. If the framework believes the change broke other parts of the system, it notifies the CL author.
- **Push-on-green.** Some projects automatically push a new version to production after tests pass. Chapter 2 references the "Making Push On Green a Reality" paper; Chapter 1 already framed this as the velocity-plus-safety payoff of SRE's [[change-management-sre|change-management]] tenet.

## Why it works

The combination only makes sense with the prior building blocks in place:

- [[borg]] for cheap parallel build execution at datacenter scale.
- Strong [[stubby]]/[[protocol-buffers]] interface contracts, so that a CL touching one service is a bounded change.
- [[sre-monitoring-outputs]] / [[borgmon]] for detecting regressions fast enough for push-on-green to be safe.
- [[error-budget]] as the policy mechanism that tolerates occasional push-on-green regressions.

## The release view (Chapter 8)

Chapter 8 adds the [[release-engineering]] perspective on the monorepo (source: chapter-08-release-engineering.md):

- **All code lands on mainline.** Even projects that release frequently check changes into the main branch first. There is no upstream develop-branch-plus-release-branch split.
- **Release branches are read-only snapshots.** Most major projects branch from the mainline at a specific revision and never merge back. Bug fixes land on mainline and are [[release-branching-and-cherry-picking|cherry-picked]] into the release branch. This keeps each release's contents precisely known.
- **[[hermetic-builds]].** Because build tools themselves are versioned in the monorepo, a rebuild months later of an old release uses the compiler from then, not the compiler from now. This is what makes cherry-picking onto old branches safe.
- **Gated operations enforce policy.** [[release-policy-enforcement|Approving CLs, creating releases, approving cherry picks, deploying]], and modifying build configuration are each independently permissioned and auditable inside the repository.
- **[[push-on-green]].** The end state of the pipeline for projects that opt in: the [[continuous-integration-delivery-deployment|CI]] path in the monorepo runs all dependent tests on each CL, and green CLs flow to production automatically.

## Cross-book connections

- [[change-management-sre]] — push-on-green is the concrete realisation of SRE's automation trio (progressive rollouts, fast detection, safe rollback).
- [[continuous-integration-delivery-deployment]] (Bellemare) — Bellemare's EDM CI/CD pipeline shape is the per-service analogue; Google's is the full-repo version.
- [[code-ownership-models]] (Newman) — the CL-to-owner review workflow is *strong ownership at the file level* inside a *collectively visible repo*.
- [[independent-deployability]] — a monorepo is consistent with independent deployment when combined with strict interface discipline.

## Related pages

- [[release-engineering]]
- [[release-branching-and-cherry-picking]]
- [[release-policy-enforcement]]
- [[hermetic-builds]]
- [[push-on-green]]
- [[change-management-sre]]
- [[continuous-integration-delivery-deployment]]
- [[independent-deployability]]
- [[code-ownership-models]]
- [[stubby]]
- [[site-reliability-engineering]]
