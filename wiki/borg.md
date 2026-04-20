# Borg

**Summary**: Google's distributed cluster operating system — the software that binpacks jobs (server processes and batch tasks) onto machines, monitors them, restarts failures, and enforces resource quotas. Borg is the direct ancestor of [[container-management-system|Kubernetes]], and structurally similar to Apache Mesos. Chapter 7 also presents Borg as the canonical level-5 [[autonomous-systems|autonomous system]] in Google's [[hierarchy-of-automation-classes|automation hierarchy]] — the mature form of an evolutionary path that started with Python scripts and SSH.

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`, `raw/site-reliability-engineering/chapter-07-the-evolution-of-automation-at-google.md`, `raw/site-reliability-engineering/chapter-24-distributed-periodic-scheduling-with-cron.md`

**Last updated**: 2026-04-17

---

## What Borg does

Borg manages jobs at the cluster level (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

- Runs **jobs**, which are either indefinitely running servers or batch processes like a [[mapreduce]].
- A job consists of one or many (up to thousands) of identical **tasks**, both for reliability and because a single process can't usually handle all cluster traffic.
- On job submission, Borg finds machines, starts the server program, and continuously monitors the tasks. A malfunctioning task is killed and restarted, possibly on a different machine.

## Resource allocation and binpacking

Every job specifies its required resources (e.g., *3 CPU cores, 2 GiB RAM*). Using all jobs' requirements, Borg binpacks the tasks onto machines **optimally, subject to failure-domain constraints**: for example, Borg will not place all of a job's tasks on the same rack because the top-of-rack switch is a single point of failure for that job (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md).

If a task tries to use more resources than requested, Borg kills and restarts it. The quoted rationale: "a slowly crashlooping task is usually preferable to a task that hasn't been restarted at all" (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md).

## Naming and discovery

Because tasks move fluidly between machines, IP address and port number are not stable identifiers. Borg solves this with an extra level of indirection via a **Borg Naming Service**: at job start, each task is given a name like `/bns/<cluster>/<user>/<job name>/<task number>` which resolves to `<IP address>:<port>`. Other processes connect via the symbolic name, not the raw address (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md).

The naming service is the [[service-discovery]] layer for Borg. The mapping is stored in [[chubby]] so it is consistent across the cluster.

## Relationship to Kubernetes and Mesos

Borg is a distributed cluster OS similar to Apache Mesos. Its descendant [[container-management-system|Kubernetes]] — open-sourced by Google in 2014 — carries the same core ideas: declarative job specifications, resource quotas, failure-domain-aware scheduling, fluid task placement, and the [[pod]] as a multi-container deployable unit (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md).

The same chapter's phrasing is useful for positioning Borg in the wiki: Borg is the internal ancestor; Kubernetes is the open-source successor. Both are instances of the general [[container-management-system|CMS]] category Bellemare discusses in the EDM context, and both support [[desired-state-management]] as their operating mode.

## Birth of the warehouse-scale computer (Chapter 7)

Chapter 7 reconstructs Borg's evolution as the canonical level-5 [[autonomous-systems|autonomous system]] story (source: chapter-07-the-evolution-of-automation-at-google.md). Google's clusters were initially deployed like any small shop's: racks of machines with specific purposes and heterogeneous configurations, administered by SSHing into a "master" machine, with "golden" binaries living on those masters and most naming logic implicitly assuming the single colo.

As production grew to multiple clusters, different domain names entered the picture, and a descriptor file grouped machines by loose naming strategy. Combined with parallel SSH, this allowed operations like "reboot all the search machines in one go." Tickets of the form "search is done with machine x1, crawl can have the machine now" were routine.

Automation then evolved through several Chapter-7 stages:

1. **Simple Python scripts** — service management (keeping services running, restart after segfaults), tracking which services run on which machines, SSHing into each machine to parse log messages with regexps.
2. **Machine-state database** — automation mutated into a proper database, and monitoring improved. The union set of automation could now manage most of the machine lifecycle: noticing broken machines, removing services, sending to repair, restoring configuration on return.
3. **Borg** — the conceptual break. Abstractions in (1) and (2) were "relentlessly tied to physical machines." Borg moved away from static host/port/job assignments toward treating a collection of machines as a managed sea of resources, with cluster management reachable via API calls to a central coordinator. This liberated dimensions of efficiency, flexibility, and reliability that the machine-centric model foreclosed.

The chapter's Treynor Sloss framing:

> By taking the approach that this was a software problem, the initial automation bought us enough time to turn cluster management into something *autonomous*, as opposed to *automated*.

The enabling ideas came from classic distributed-system development: data distribution, APIs, hub-and-spoke architectures. Once the framing changed, rescheduling a task between machines became the multi-node equivalent of a process moving between CPUs — an intrinsic system feature, not an automated script. Cluster turnup became "additional schedulable capacity, a bit like adding disk or RAM to a single computer."

The operational payoff cited in Chapter 7: continuous and automatic OS upgrades take "a very small amount of constant effort — effort that does not scale with the total size of production deployments." Slight deviations in machine state are automatically fixed; brokenness and lifecycle management are essentially no-ops for SRE. **Thousands of machines are born, die, and go into repairs daily with no SRE effort.**

The final Chapter-7 twist: a single-node computer isn't expected to keep operating when many components fail, but "the global computer is" — it must be self-repairing once it grows past a certain size, because the number of failures per second at that scale is statistically guaranteed. Level-5 autonomy is not optional for systems at planetary scale.

## Borg as the datacenter scheduler for cron (Chapter 24)

Chapter 24 uses Borg as the concrete backing scheduler for Google's [[distributed-cron|distributed cron service]]. The interaction is instructive for understanding Borg's role in the stack (source: chapter-24-distributed-periodic-scheduling-with-cron.md):

- **Cron replicas themselves run on Borg.** The chapter requires them scheduled into **diverse failure domains** within one datacenter so that a single PDU outage or rack failure cannot take out all cron replicas at once.
- **Cron jobs launch by sending RPCs to Borg.** A single "cron job launch" often decomposes into several Borg RPCs, and partial failure of that RPC sequence is the central correctness problem Chapter 24 solves.
- **Borg's job-naming API is the mechanism.** Because Borg lets callers look up jobs by name (running *and* recently completed), cron can precompute the job name + scheduled launch time and use it as a durable operation ID. See [[cron-partial-failure-resolution]].

Chapter 24's design explicitly depends on a datacenter scheduler providing three features that Borg has: failure-domain-aware placement, job-name-based state lookup, and API-driven launch. Any scheduler with those primitives (Mesos is named by the chapter) could host an equivalent cron service. Any scheduler without them would force cron to either demand stronger idempotence guarantees from job RPCs or skip more launches on failover.

## Cross-book connections

- [[container-management-system]] — Kubernetes and peers, the category Borg belongs to.
- [[pod]] — the Kubernetes multi-container primitive; Borg tasks are the ancestor concept.
- [[desired-state-management]] — Newman's name for the declarative-spec-plus-reconciliation mode Borg pioneered.
- [[operator-pattern]] — Kubernetes-era extension of the Borg model.
- [[capacity-planning]] — Borg's binpacking is the mechanism that makes efficient multi-tenant capacity planning possible at Google.
- [[autonomous-systems]] — the conceptual category Borg canonicalises; the Chapter-7 story is the worked example.
- MySQL-on-Borg (Decider) — the stateful-workload-on-Borg case study; the failover-autonomy layer grafted onto Borg's task-level autonomy.
- [[automation-at-google]] — the chapter's overall argument, of which Borg is the largest case study.

## Related pages

- [[chubby]]
- [[container-management-system]]
- [[pod]]
- [[desired-state-management]]
- [[google-datacenter-topology]]
- [[autonomous-systems]]
- [[hierarchy-of-automation-classes]]
- [[automation-at-google]]
- [[distributed-cron]]
- [[cron-partial-failure-resolution]]
- [[site-reliability-engineering]]
