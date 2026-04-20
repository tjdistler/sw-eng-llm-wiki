# Hierarchy of Automation Classes

**Summary**: Chapter 7's five-level taxonomy of how automation evolves, from completely manual operation to fully autonomous systems. Each level removes more of the human and more of the "glue logic" maintained separately from the underlying system; the top level replaces automation entirely with system design that doesn't need it.

**Sources**: `raw/site-reliability-engineering/chapter-07-the-evolution-of-automation-at-google.md`

**Last updated**: 2026-04-17

---

## The five levels

The chapter's evolutionary path, illustrated with database failover (source: chapter-07-the-evolution-of-automation-at-google.md):

1. **No automation.** The database master is failed over manually between locations. A human reads a runbook, runs each command, checks the output. Everything depends on the operator's attention and consistency.
2. **Externally maintained system-specific automation.** An SRE has a failover script in their home directory. The script exists but is tribal: undiscoverable, unmaintained by anyone else, and brittle against changes in the underlying system.
3. **Externally maintained generic automation.** The SRE adds database support to a shared "generic failover" script that everyone uses. The platform effect kicks in — the same tooling covers many services — but the automation still lives beside the system rather than inside it.
4. **Internally maintained system-specific automation.** The database ships with its own failover script. The people who know the system best own the automation; the automation changes when the system does; the extended-feedback-cycle fragility of level-3 automation is cured.
5. **Autonomous systems.** The database notices problems and fails over without human intervention. There is no separate "failover automation" at all; failover is a property of the system.

## Why the levels are not all equivalent

Chapter 7 is explicit that the levels are not merely "more automation is better" (source: chapter-07-the-evolution-of-automation-at-google.md):

- **Bit rot** — automation at levels 2–3 suffers when the underlying system changes and the automation doesn't. "Most turnup automation at Google is problematic because it ends up being maintained separately from the core system." Priorities misalign: product developers resist having to run a test deployment for every change just to satisfy external automation.
- **Infrequent execution** — automation that runs rarely (failover every few months, cluster turnup once per quarter) is *particularly* fragile because the feedback loop on breakage is long. Inconsistencies creep in between runs.
- **The maintainer problem** — "Automation code, like unit test code, dies when the maintaining team isn't obsessive about keeping the code in sync with the codebase it covers." A team whose primary job is running the automation has no incentive to reduce the service owner's future toil; a team not running automation has no incentive to build systems that are easy to automate.

Level 4 — internally maintained system-specific automation — is therefore strictly better than level 3 for most systems, because the incentives line up: the code lives next to the thing it manages, evolves with it, and breaks visibly when the underlying system changes.

## The qualitative jump to level 5

Level 5 is not merely "level 4 plus more testing." It is a different kind of system.

The Borg story in Chapter 7 makes this concrete: the earlier Python scripts at Google *automated* the ops work around racks of machines with specific purposes, but the abstractions were "relentlessly tied to physical machines." [[borg|Borg]] reframed cluster management so that a collection of machines is a managed sea of resources accessible via API calls; **rescheduling became an intrinsic feature rather than something you automate** (source: chapter-07-the-evolution-of-automation-at-google.md).

The chapter's analogy: at level 5, a task moving between machines is the multi-node equivalent of a process moving between CPUs. You don't "automate" that either — it's just how the system works.

See [[autonomous-systems]] for the full treatment of what level 5 looks like and when it's worth the design investment.

## Production-wide changes as a sub-domain

Chapter 7 notes a sub-class of automation that cuts across services rather than belonging to one: production-wide changes like swapping upstream [[chubby]] servers, flipping a flag in the [[bigtable]] client library, or rolling out a library upgrade everywhere. These:

- Are too numerous for manual oversight past a certain volume.
- Are often trivial or succeed with basic relaunch-and-check.
- Nonetheless need to be safely managed and rolled back.

This is a distinct automation surface from service-specific lifecycle management and motivates generic rollout tooling separate from per-service automation.

## Level-4 tooling landscape

Chapter 7 surveys existing tools at roughly level 3–4 (source: chapter-07-the-evolution-of-automation-at-google.md):

- **Puppet, Chef, cfengine** — higher-level abstractions; services and higher-level entities as first-class concepts.
- **Perl (and similar)** — POSIX-level affordances; unlimited scope but you build your own abstractions.

The trade-off named in the chapter is classic: high-level abstractions are easier to reason about but fail systemically when the abstraction leaks. The push-a-binary-to-a-cluster example is the canonical leak — the atomic abstraction hides machine failures, network partitions during the push, control-plane faults that leave binaries staged-but-not-restarted. Most such tools halt and call for human intervention when these cases hit; truly bad automation doesn't even do that.

Google's own tooling spans both levels of abstraction: some is generic rollout machinery with minimal per-service modelling, some is a language for describing service deployment very abstractly. The abstract end yields more reusable platforms; the concrete end is sometimes the only tractable option given the complexity of the production environment.

## Related pages

- [[automation-at-google]]
- [[autonomous-systems]]
- [[borg]]
- [[cluster-turnup-automation]]
- [[desired-state-management]]
