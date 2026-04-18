# Build System Discipline

**Summary**: Chapter 17's playbook for a healthy build: versioned source control, continuous build that runs tests on every commit, immediate notification on breakage, and a team norm that **fixing a broken build preempts all other work**. The stability-drives-agility claim Chapter 17 highlights: when the build is predictably solid, developers iterate faster.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The foundational stack

Chapter 17's prerequisites for effective testing (source: chapter-17-testing-for-reliability.md):

> The foundation for a strong testing infrastructure is a versioned source control system that tracks every change to the codebase. Once source control is in place, you can add a continuous build system that builds the software and runs tests every time code is submitted. We've found it optimal if the build system notifies engineers the moment a change breaks a software project.

Three layers:

1. **Versioned source control.** The primitive every other layer rests on.
2. **Continuous build.** Every commit triggers a build-and-test run.
3. **Instant notification on breakage.** The moment a change breaks the build, the engineers know.

Miss any layer and testing investment is undermined by missing feedback.

## Fix-the-build-first

Chapter 17's culture norm (source: chapter-17-testing-for-reliability.md):

> When the build system notifies engineers about broken code, they should drop all of their other tasks and prioritize fixing the problem.

Four reasons given:

- It's usually harder to fix what's broken if there are changes to the codebase after the defect is introduced.
- Broken software slows down the team because they must work around the breakage.
- Release cadences (nightly, weekly) lose their value when mainline is broken.
- The team's ability to respond to an emergency release (security vulnerability, etc.) becomes much harder with a broken build.

The fourth reason is the one Chapter 17 highlights as structural.

## Stability drives agility

> The concepts of stability and agility are traditionally in tension in the world of SRE. The last bullet point provides an interesting case where stability actually drives agility. When the build is predictably solid and reliable, developers can iterate faster! (source: chapter-17-testing-for-reliability.md)

The claim is load-bearing: a rock-solid mainline makes emergency changes *cheaper* to ship, which means emergency response is faster, which means reliability is higher. "Go slow to go fast" framed as an organisational discipline.

## Bazel's role

The chapter credits [[blaze-bazel|Bazel]] for making this scalable (source: chapter-17-testing-for-reliability.md):

> Some build systems like Bazel have valuable features that afford more precise control over testing. For example, Bazel creates dependency graphs for software projects. When a change is made to a file, Bazel only rebuilds the part of the software that depends on that file. Such systems provide reproducible builds. Instead of running all tests at every submit, tests only run for changed code. As a result, tests execute cheaper and faster.

Dependency-graph-aware selective testing is what makes continuous build affordable at Google scale. Without it, every commit would trigger every test, and the build queue would never drain.

## Coverage as engineering work

> There are a variety of tools to help you quantify and visualize the level of test coverage you need. Use these tools to shape the focus of your testing: approach the prospect of creating highly tested code as an engineering project rather than a philosophical mental exercise. Instead of repeating the ambiguous refrain "We need more tests," set explicit goals and deadlines. Remember that not all software is created equal. Life-critical or revenue-critical systems demand substantially higher levels of test quality and coverage than a nonproduction script with a short shelf life. (source: chapter-17-testing-for-reliability.md)

Coverage is a project with deliverables: measured baselines, target numbers, deadlines. The chapter's implicit argument against perpetual "we should test more" as an aspiration without an owner.

## Cross-book connections

- [[system-stability-vs-agility]] (Ch 9) — Ch 9 argues that reliable processes increase agility; Ch 17's stability-drives-agility case study is the testing-infrastructure realisation
- [[blaze-bazel]] (Ch 8) — the build tool named in Ch 17 as essential; Ch 8 covers Blaze / Bazel in full
- [[hermetic-builds]] (Ch 8) — the property that makes continuous build reproducible; without hermeticity, "the build is green" means different things on different machines
- [[push-on-green]] (Ch 8) — the logical endpoint: continuous build + continuous test + automated deploy
- [[continuous-integration-delivery-deployment]] (Bellemare) — the broader practice this chapter describes the SRE slice of

## Related pages

- [[testing-for-reliability]]
- [[hermetic-builds]]
- [[blaze-bazel]]
- [[push-on-green]]
- [[system-stability-vs-agility]]
