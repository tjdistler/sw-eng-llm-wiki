# Cluster Turnup Automation

**Summary**: Chapter 7's second case study — the evolution of how Google turns up a new cluster. Starting from SSH-based shell scripts, the story moves through Prodtest (Python unit tests for real services), idempotent fix scripts, a dedicated turnup team (which eroded competence and relevance), and finally a Service-Oriented Architecture where each service exposes an Admin Server RPC contract to the turnup coordinator. The central lesson: *the most functional tools are usually written by those who use them.*

**Sources**: `raw/site-reliability-engineering/chapter-07-the-evolution-of-automation-at-google.md`

**Last updated**: 2026-04-17

---

## The turnup problem

Ten years before Chapter 7 was written, the Cluster Infrastructure SRE team got new hires at roughly the rate it turned up new clusters. Because turning up a service in a new cluster exposed a new hire to a service's internals, turnup doubled as training. The canonical six-step sequence (source: chapter-07-the-evolution-of-automation-at-google.md):

1. Fit out a datacenter building for power and cooling.
2. Install and configure core switches and connections to the backbone.
3. Install a few initial racks of servers.
4. Configure basic services — DNS, installers, lock service, storage, computing.
5. Deploy the remaining racks of machines.
6. Assign user-facing services resources; teams set up their services.

Steps 4 and 6 were "extremely complex." Storage and compute subsystems were in heavy development; new flags and components landed weekly; some services had more than a hundred component subsystems with a web of dependencies. **Any misconfiguration was a customer-impacting outage waiting to happen.**

## Four generations of turnup automation

### 1. Shell-script era

Early automation focused on accelerating cluster delivery through creative use of SSH for package distribution and service initialisation. Effective at first but accumulated as "a cholesterol of technical debt" (source: chapter-07-the-evolution-of-automation-at-google.md). The scripts could not answer the questions that mattered:

- Were all the service's dependencies available and correctly configured?
- Were all configurations and packages consistent with other deployments?
- Could the team confirm every configuration exception was desired?

Clusters routinely took six or more weeks to go from "network-ready" to "serving live traffic," and no one could predict the duration.

### 2. Prodtest (detection)

The team's first structural answer: **Production Test**, which extended the Python unit-test framework to unit-test real services. Tests had dependencies, so a failing test aborted a chain. A per-team Prodtest, given a cluster name, could validate that team's services in that cluster. A graph view let engineers see at a glance which steps were failing and why.

The big win: *project managers could, for the first time, predict when a cluster would go live, and had a complete understanding of why each cluster took six or more weeks*. Whenever one team hit a delay from another team's misconfiguration, a Prodtest bug was filed to catch it next time.

### 3. Idempotent fixes (remediation)

Prodtest found problems but didn't fix them. When senior management gave the team a "five clusters turned up in one week" mandate, filing hundreds of bugs across dozens of teams was not an option (source: chapter-07-the-evolution-of-automation-at-google.md).

The evolution: pair each unit test with a fix. Every fix had to be **idempotent** and could assume its dependencies were met. Idempotence meant teams could run their fix script every 15 minutes without fearing damage. A failed fix after multiple retries halted the loop and notified a human.

This got the team from "network-ready" to "serving 1% of websearch and ads traffic" in a week or two. At the time it looked like the apex of automation technology.

In hindsight the chapter flags the flaws (source: chapter-07-the-evolution-of-automation-at-google.md):

- The test-fix-retest latency produced flaky tests that sometimes worked, sometimes didn't.
- Not every fix was naturally idempotent, so a flaky test followed by a partial fix could leave the system in an inconsistent state.

### 4. The specialisation trap

To reduce latency the team centralised: service-owning teams instructed a single **turnup team** what automation to run, tracked by tickets. With the turnup team in one room, cluster turnups ran faster.

But the incentives were broken (source: chapter-07-the-evolution-of-automation-at-google.md):

- A team whose only job is to speed up the current turnup has no incentive to reduce the technical debt the service team will inherit later.
- A team not running the service has no incentive to build systems that are easy to automate.
- A product manager whose schedule is not affected by low-quality automation prioritises features over simplicity and automation.

The result: the automation became less **relevant** (new real-world steps were missed) and less **competent** (new flags broke it). The chapter names the general principle: *the most functional tools are usually written by those who use them*.

Turnups slid back to high-latency, inaccurate, and incompetent — the worst of all worlds.

### 5. Service-Oriented turnup

The escape came obliquely, via a security mandate. Distributed automation had relied on SSH with root access — a poor fit for privilege-minimisation. The team replaced SSH with an **authenticated, ACL-driven, RPC-based Local Admin Daemon** (Admin Server) per machine, with per-RPC audit logging (source: chapter-07-the-evolution-of-automation-at-google.md).

Admin Servers then scaled up to service teams' workflows:

- **Machine-specific Admin Servers** — install packages, reboot.
- **Cluster-level Admin Servers** — drain or turn up a service.

With Admin Servers as the substrate, the team reframed cluster turnup as a Service-Oriented Architecture problem:

- Service owners create an Admin Server that handles cluster turnup/turndown RPCs.
- The turnup system knows when clusters are ready and sends RPCs to each Admin Server.
- Teams own the contract (the API) but are free to change the underlying implementation.

When a cluster reached "network-ready," the turnup system issued RPCs to each participating Admin Server. The result: "low-latency, competent, and accurate" turnup that has held up as service count, team count, and change rate have doubled year over year.

## The three dimensions of automation quality

Chapter 7 names three dimensions along which automation processes vary (source: chapter-07-the-evolution-of-automation-at-google.md):

- **Competence** — accuracy.
- **Latency** — how quickly all steps execute once initiated.
- **Relevance** — the proportion of the real-world process that is covered.

The specialisation trap above is a trade between them: the turnup team bought **latency** at the cost of **competence** and **relevance**. A winning design maximises all three — and the SOA-with-Admin-Servers model does so because ownership aligns with the team that has the domain expertise (competence + relevance) while the RPC substrate provides the coordination (latency).

## The implicit-safety-signal caution

The chapter includes a named cautionary tale in the middle of this case study (source: chapter-07-the-evolution-of-automation-at-google.md):

> A multi-petabyte Bigtable cluster was configured to not use the first (logging) disk on 12-disk systems, for latency reasons. A year later, some automation assumed that if a machine's first disk wasn't being used, that machine didn't have any storage configured; therefore, it was safe to wipe the machine and set it up from scratch. All of the Bigtable data was wiped, instantly.

The lesson: **automation needs to be careful about relying on implicit "safety" signals**. A convention that was explicit to the humans who set it up ("disk 0 is logging-disabled") became an implicit signal that meant something entirely different to a downstream automation a year later. See [[automation-gone-wrong]] for the chapter's full treatment of this failure mode.

## Cross-book connections

- [[borg]] — Borg itself is the parallel case study where turnup was *designed out* via autonomy rather than iteratively automated.
- [[operator-pattern]] (Burns) — a modern Kubernetes operator is structurally similar to the per-service Admin Server: owned by the service team, exposes declarative control over cluster-local operations.
- [[rpc]] — gRPC is the modern mechanism that would make the Admin Server approach feasible today.
- [[idempotence]] — the property that makes the fix-loop safe to retry.
- [[sre-tenets]] — cluster turnup exercises change management, capacity planning, and provisioning simultaneously.

## Related pages

- [[automation-at-google]]
- [[automation-gone-wrong]]
- [[hierarchy-of-automation-classes]]
- [[autonomous-systems]]
- [[borg]]
- [[idempotence]]
- [[change-management-sre]]
