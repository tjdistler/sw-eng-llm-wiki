# Autonomous Systems

**Summary**: The top of Chapter 7's [[hierarchy-of-automation-classes|automation hierarchy]]: systems that handle their own operational concerns as an intrinsic feature of their design, not as glue logic attached from outside. An autonomous system does not "have automation" — it has no separate failover script, no external turnup tool, no human-triggered rebalancer — because the behaviours those scripts would have performed are properties of the system itself.

**Sources**: `raw/site-reliability-engineering/chapter-07-the-evolution-of-automation-at-google.md`, `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`

**Last updated**: 2026-04-17

---

## Automated vs autonomous

Chapter 7 draws the distinction carefully (source: chapter-07-the-evolution-of-automation-at-google.md):

- **Automated** — a human, a cron job, or an external system triggers a script that performs some action on the managed system. The script lives outside the managed system and knows how to manipulate it.
- **Autonomous** — the managed system notices a condition and acts on it directly. There is no external triggering entity; there is no separate script to maintain.

The quoted phrasing: "*in an ideal world, we wouldn't need externalized automation … it would be even better to have a system that needs no glue logic at all, not just because internalization is more efficient, but because it has been designed to not need glue logic in the first place.*"

Chapter 5 ([[toil-and-engineering-balance]]) introduced Treynor Sloss's "automatic not just automated" phrasing for the same distinction; Chapter 7 develops it into the explicit level-5 tier and traces how Google got there.

## Why autonomy matters

The forces that push toward autonomy over level-4 automation (source: chapter-07-the-evolution-of-automation-at-google.md):

- **Bit rot is cured by construction.** External automation drifts out of sync with the system; an autonomous behaviour is embedded in the system and changes with it.
- **Feedback cycles collapse.** External automation that runs infrequently (failover, cluster turnup) accumulates inconsistencies between runs. An autonomous behaviour exercised continuously has no dormant code path.
- **Scale demands it.** "A single-node computer is not, in general, expected to continue operating when a large number of components fail. The global computer is — it must be self-repairing to operate once it grows past a certain size, due to the essentially statistically guaranteed large number of failures taking place every second."
- **Humans can't react fast enough.** Rescheduling in milliseconds is not a problem that can be solved by automating a script. It has to be a system feature.

The chapter's summary: moving systems up the hierarchy from manually triggered to automatically triggered to autonomous requires capacity for self-introspection, because only the system itself can see its failures quickly enough to respond.

## Worked example: Borg as autonomous system

[[borg|Borg]] is Chapter 7's canonical level-5 story. The stages it moved through (source: chapter-07-the-evolution-of-automation-at-google.md):

1. **Masters and golden binaries on well-known machines** — ops by SSH.
2. **Descriptor files plus parallel SSH** — you can reboot "all the search machines in one go," but machine roles are fixed.
3. **Python scripts** — service management, role tracking, log parsing via SSH into each machine.
4. **A machine-state database with lifecycle automation** — notices broken machines, drains services, sends them to repair, restores configuration on return. Useful but limited: abstractions are tied to physical machines.
5. **Borg itself** — cluster management becomes an entity to which API calls are issued. A collection of machines is a managed sea of resources. Batch and user-facing tasks share machines; OS upgrades roll continuously; slight deviations in machine state are fixed automatically; thousands of machines are born, die, and go into repairs daily with *no SRE effort*.

Treynor Sloss's framing captured in the chapter: "by taking the approach that this was a software problem, the initial automation bought us enough time to turn cluster management into something autonomous, as opposed to automated." The enabling ideas came from classic distributed-system development — data distribution, APIs, hub-and-spoke architectures.

## The CPU analogy

Chapter 7's intuition-building analogy (source: chapter-07-the-evolution-of-automation-at-google.md):

- Rescheduling a task from one machine to another *in Borg* is structurally equivalent to a process moving from one CPU to another on a single machine. The compute resources happen to be at the other end of a network link, but the system treats the cross-machine move as a primitive.
- Cluster turnup, in the same metaphor, is adding compute the way you add a disk or RAM to a workstation — new capacity the scheduler can consume.

Framed this way, the things we would otherwise "automate" (failover, turnup, rebalancing) are not automation at all. They are **intrinsic features** of the system.

## Preconditions for autonomy

The chapter names the preconditions for a system to be a candidate for level 5 (source: chapter-07-the-evolution-of-automation-at-google.md):

- **Decoupled subsystems** — so each can reconcile locally without a global coordinator.
- **Explicit APIs** — so operations are addressable programmatically and can be composed.
- **Minimised side effects** — so retries and reconciliation are safe.
- **Self-introspection** — so the system can observe its own state, detect drift, and act.

These are "standard good practices in software engineering," but the chapter frames them as the preconditions that make autonomy possible rather than as generic virtues. Autonomy is difficult to retrofit onto a system that lacks them.

## The dark side: operator skill atrophy

Chapter 7's closing warning (source: chapter-07-the-evolution-of-automation-at-google.md, citing the Air France 447 literature and Bainbridge/Sarter):

- Highly effective automation progressively relieves operators of direct contact with the system.
- Operators' mental models drift out of sync with system behaviour.
- When automation eventually fails, operators can no longer successfully operate the system.

This failure mode is worst for **non-autonomous** automation — where the automation replaces a manual action that is *presumed* to still be performable. Over time the manual path rots out from under the operators.

Google's response is **not** to retreat to less automation but to push harder toward autonomy *and* aggressively expose internal state so the humans who do need to intervene retain a working model. The regular-practice-drills recommendation from Chapter 33's "Disaster Role Playing" is the organisational complement.

See also the "[[automation-gone-wrong|Automation: Enabling Failure at Scale]]" sidebar (the Diskerase incident) — autonomous systems can fail catastrophically in their own way, and rate-limiting, audit trails, and sanity checks are load-bearing even for systems that work correctly most of the time.

## Autonomous platforms and churn reduction (Chapter 27)

Chapter 27 names **infrastructure churn** as one of the long-horizon pathologies Launch Coordination Engineering could not solve (source: chapter-27-reliable-product-launches-at-scale.md):

> If the underlying infrastructure … is changing due to active development by infrastructure teams, the owners of services running on the infrastructure must invest large amounts of work to simply keep up with the infrastructure changes … service owners must continually modify their configurations and rebuild their executables, consequently "running fast just to stay in the same place."

The prescribed answer sits at the intersection of autonomy and organisational policy:

> The solution to this scenario is to enact some type of churn reduction policy that prohibits infrastructure engineers from releasing backward-incompatible features until they also automate the migration of their clients to the new feature. Creating automated migration tools to accompany new features minimizes the work imposed on service owners to keep up with infrastructure churn.

Concretely: **a platform that evolves autonomously** — with migration tooling shipped alongside every feature — absorbs the churn cost at the platform side rather than pushing it to tenants. Kubernetes CRD conversion webhooks, Borg task-migration tooling, and protocol-buffer schema-migration utilities are realisations of this discipline. Without it, an otherwise autonomous platform becomes the source of continuous tenant toil — a failure mode Chapter 27 names explicitly.

## Cross-book connections

- [[desired-state-management]] (Newman) — the declarative-spec-plus-continuous-reconciliation pattern is the open-source-era shape of autonomy; Kubernetes is Borg's descendant.
- [[operator-pattern]] (Burns) — application-specific autonomy realised as a reconciliation controller inside the orchestrator; Chapter 9 of *Designing Distributed Systems* is the recipe book.
- [[fault-tolerance]] (Kleppmann / Burns) — hardware and software fault tolerance are the building blocks; autonomy is the organisational level above.
- [[safety-and-liveness]] (Kleppmann) — autonomous systems embody safety (never do the wrong thing) *and* liveness (eventually do the right thing) as intrinsic properties.

## Related pages

- [[automation-at-google]]
- [[hierarchy-of-automation-classes]]
- [[borg]]
- [[mysql-on-borg]]
- [[automation-gone-wrong]]
- [[desired-state-management]]
- [[operator-pattern]]
- [[toil-and-engineering-balance]]
- [[mttr-and-mttf]]
- [[reliable-product-launches]]
- [[launch-coordination-engineering]]
